import subprocess
import sys

# Actualizare și upgrade pentru sistemul de operare (opțional pentru Linux/Termux)
def update_system():
    try:
        print("Updating system packages...")
        subprocess.check_call(["pkg", "update", "-y"])  # Actualizare pachete
        subprocess.check_call(["pkg", "upgrade", "-y"])  # Upgrade pachete
        print("System packages updated successfully.")
    except Exception as e:
        print(f"Error during system update: {e}")

# Instalarea bibliotecilor Python necesare
def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Actualizează sistemul (doar pentru Termux sau Linux)
update_system()

# Instalează pachetele Python necesare
required_packages = ["pydub", "speech_recognition"]
for package in required_packages:
    install_package(package)

# Importurile bibliotecilor Python
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import urllib.request
import os

# === Funcție pentru depanare ===
def debug_prompt(message, default="yes"):
    """
    Afișează un mesaj de depanare și întreabă utilizatorul dacă să continue execuția.
    :param message: Mesajul care descrie ce urmează să fie executat.
    :param default: Valoarea implicită dacă utilizatorul doar apasă Enter ('yes' sau 'no').
    :return: True dacă execuția trebuie să continue, False altfel.
    """
    valid_responses = {"yes": True, "y": True, "no": False, "n": False}
    prompt = f"{message} (yes/[no]): " if default == "no" else f"{message} ([yes]/no): "
    while True:
        user_input = input(prompt).strip().lower()
        if not user_input:  # Implicit
            return valid_responses[default]
        elif user_input in valid_responses:
            return valid_responses[user_input]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")

# === Funcție pentru verificarea existenței fișierului ===
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

# === Funcție pentru verificarea conexiunii la internet ===
def check_internet_connection():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        print("Internet connection available.")
        return True
    except requests.ConnectionError:
        print("No internet connection. Please connect to the internet and try again.")
        return False

def get_file_size(file_path):
    """
    Returnează dimensiunea unui fișier în MB.
    :param file_path: Calea către fișier.
    :return: Dimensiunea fișierului în MB (float).
    """
    try:
        size_in_bytes = os.path.getsize(file_path)
        size_in_mb = size_in_bytes / (1024 * 1024)  # Conversie la MB
        return round(size_in_mb, 2)  # Rotunjire la 2 zecimale
    except Exception as e:
        print(f"Error getting file size: {e}")
        return None

# === Funcție pentru împărțirea segmentelor mari ===
def split_large_chunk(chunk, max_duration=2 * 60 * 1000, overlap=5000):
    """
    Împarte un segment mare în bucăți mai mici, fiecare având o suprapunere.
    Se oprește dacă segmentul curent este mai mic decât overlap.
    """
    segments = []
    start = 0
    while start < len(chunk):
        end = min(start + max_duration, len(chunk))
        segment_duration = end - start
        if segment_duration <= overlap:
            print(f"Skipping segment from {start} ms to {end} ms (too small: {segment_duration} ms).")
            break  # Oprire dacă segmentul este mai mic decât overlap-ul
        segment = chunk[start:end]
        print(f"Creating segment from {start} ms to {end} ms.")
#        if not debug_prompt(f"Ready to process segment {start}-{end} ms. Continue?"):
#            print("Execution stopped at segment creation.")
#            return segments
        segments.append(segment)
        start = end - overlap  # Suprapunerea asigură continuitatea
    return segments

# === Funcție pentru crearea fișierelor WAV și segmentare ===
def wav_creation(mp3_file_path):
    """
    Creează chunk-uri WAV dintr-un fișier MP3, respectând regulile de durată minimă și maximă.
    """
    mp3_file_path = os.path.expanduser(mp3_file_path)
    check_file_exists(mp3_file_path)  # Verifică dacă fișierul există
    base_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    wav_folder = os.path.splitext(mp3_file_path)[0]  # Director pentru chunk-uri WAV
    full_wav_path = f"{os.path.splitext(mp3_file_path)[0]}.wav"  # Fisier WAV complet

    # Conversie MP3 → WAV complet
    if not os.path.exists(full_wav_path):
        print(f"Converting MP3 file '{os.path.basename(mp3_file_path)}' to full WAV...")
#        if not debug_prompt(f"Ready to create the full WAV file from '{os.path.basename(mp3_file_path)}'. Continue?"):
#            print("Execution stopped at full WAV creation.")
#            return
        AudioSegment.from_file(mp3_file_path).export(full_wav_path, format="wav")
        print(f"Full WAV file '{os.path.basename(full_wav_path)}' created.")
    else:
        file_size = get_file_size(full_wav_path)
        size_info = f"{file_size} MB" if file_size else "unknown size"
        print(f"Full WAV file '{os.path.basename(full_wav_path)}' already exists ({size_info}). Skipping creation.")

    # Încărcare fișier WAV complet
    file_size = get_file_size(full_wav_path)
    size_info = f"{file_size} MB" if file_size else "unknown size"
    print(f"Loading full WAV file '{os.path.basename(full_wav_path)}' ({size_info}) into memory...")
#    if not debug_prompt(f"Ready to load the full WAV file '{os.path.basename(full_wav_path)}' ({size_info}) into memory. Continue?"):
#        print("Execution stopped at loading full WAV into memory.")
#        return
    audio = AudioSegment.from_file(full_wav_path)
    print(f"Full WAV file '{os.path.basename(full_wav_path)}' ({size_info}) loaded into memory.")

    # Verifică dacă dosarul pentru chunk-uri există
    if os.path.exists(wav_folder):
        print(f"Folder '{wav_folder}' already exists. Skipping chunk creation.")
        return

    # Segmentare pe baza pauzelor naturale
    print("Splitting audio into chunks based on silence...")
#    if not debug_prompt("Ready to split the audio into chunks based on silence. Continue?"):
#        print("Execution stopped at chunk splitting.")
#        return
    chunks = split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-40
    )
    print(f"{len(chunks)} chunks created in memory.")

    # Crearea chunk-urilor combinate
    print("Combining chunks based on length...")
#    if not debug_prompt("Ready to combine chunks into larger segments. Continue?"):
#        print("Execution stopped at chunk combining.")
#        return
    min_chunk_length = 20 * 1000
    max_chunk_length = 2 * 60 * 1000
    combined_chunks = []
    current_chunk = AudioSegment.silent(duration=0)

    for chunk in chunks:
        if len(current_chunk) + len(chunk) < max_chunk_length:
            current_chunk += chunk
        else:
            combined_chunks.append(current_chunk)
            current_chunk = chunk

    if len(current_chunk) > 0:
        combined_chunks.append(current_chunk)
    print(f"{len(combined_chunks)} combined chunks created in memory.")

    # Împărțirea chunk-urilor mari
    print("Splitting large chunks into smaller segments...")
#    if not debug_prompt("Ready to split large chunks into smaller segments. Continue?"):
#        print("Execution stopped at large chunk splitting.")
#        return
    final_chunks = []
    for chunk in combined_chunks:
        if len(chunk) > max_chunk_length:
            final_chunks.extend(split_large_chunk(chunk, max_duration=max_chunk_length, overlap=5000))
        else:
            final_chunks.append(chunk)
    print(f"{len(final_chunks)} final chunks created in memory.")

    # Crearea directorului pentru WAV chunks
    print(f"Creating directory '{wav_folder}' for WAV chunks...")
    os.makedirs(wav_folder)

    # Export chunk-uri WAV
    print(f"Exporting {len(final_chunks)} chunks to directory '{wav_folder}'...")
    for i, chunk in enumerate(final_chunks, start=1):
        chunk_name = f"{wav_folder}/{i:03}.wav"
        chunk.export(chunk_name, format="wav")
        print(f"Exported: {os.path.basename(chunk_name)}")

# === Funcție pentru transcriere ===
def txt_creation(mp3_file_path):
    """
    Transcrie fișierele WAV dintr-un dosar și salvează textul într-un fișier TXT.
    """
    if not check_internet_connection():
        return

    mp3_file_path = os.path.expanduser(mp3_file_path)
    base_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    wav_folder = os.path.splitext(mp3_file_path)[0]
    txt_file_path = f"{os.path.splitext(mp3_file_path)[0]}.txt"

    recognizer = sr.Recognizer()
    wav_files = sorted(
        [f for f in os.listdir(wav_folder) if f.endswith(".wav")],
        key=lambda x: os.path.getctime(os.path.join(wav_folder, x))
    )

    with open(txt_file_path, "w", encoding="utf-8") as output_file:
        for i, wav_file in enumerate(wav_files, start=1):
            wav_path = os.path.join(wav_folder, wav_file)
            
            # Verifică dacă chunk-ul a fost deja procesat
            if os.path.exists(wav_path) and os.path.getsize(wav_path) == 0:
                print(f"Skipping empty chunk: {wav_file}")
                continue
            
            duration = AudioSegment.from_file(wav_path).duration_seconds
            print(f"Processing {i}/{len(wav_files)} - Duration: {duration:.2f} seconds")
            
            try:
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)
                    text_output = recognizer.recognize_google(audio_data, language="ro-RO")
                    output_file.write(text_output + "\n")
            except Exception as e:
                print(f"Error processing {wav_file}: {e}")
                output_file.write("\n")  # Scrie o linie goală dacă apare o eroare

    print(f"Transcription saved to {txt_file_path}")


# Exemplu de utilizare
mp3_file_path = "~/storage/music/rec/FisierulTau.mp3"
wav_creation(mp3_file_path)  # Creează chunk-urile WAV
txt_creation(mp3_file_path)  # Transcrie chunk-urile WAV
