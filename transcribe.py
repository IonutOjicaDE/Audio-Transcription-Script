import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import requests


def check_internet_connection():
    """
    Verifică dacă există conexiune la internet.
    """
    try:
        requests.get("https://www.google.com", timeout=5)
        print("Internet connection available.")
        return True
    except requests.ConnectionError:
        print("No internet connection. Please connect to the internet and try again.")
        return False


def split_large_chunk(chunk, max_duration=2 * 60 * 1000, overlap=5000):
    """
    Împarte un chunk mare în bucăți mai mici cu o durată maximă specificată.
    :param chunk: Chunk-ul AudioSegment de procesat.
    :param max_duration: Durata maximă în milisecunde.
    :param overlap: Suprapunerea între bucăți în milisecunde.
    :return: Listă de bucăți AudioSegment.
    """
    segments = []
    start = 0
    while start < len(chunk):
        end = min(start + max_duration, len(chunk))
        segments.append(chunk[start:end])
        start = end - overlap  # Suprapunere între bucăți
    return segments


def wav_creation(mp3_file_path):
    """
    Creează chunk-uri WAV dintr-un fișier MP3, respectând regulile de durată minimă și maximă.
    """
    mp3_file_path = os.path.expanduser(mp3_file_path)
    base_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    wav_folder = os.path.splitext(mp3_file_path)[0]  # Director pentru chunk-uri WAV
    full_wav_path = f"{os.path.splitext(mp3_file_path)[0]}.wav"  # Fisier WAV complet

    # Verifică dacă fișierul complet WAV există
    if not os.path.exists(full_wav_path):
        print("Converting MP3 to full WAV...")
        AudioSegment.from_file(mp3_file_path).export(full_wav_path, format="wav")
    else:
        print(f"Full WAV file '{os.path.basename(full_wav_path)}' already exists. Skipping creation.")

    # Verifică dacă dosarul pentru chunk-uri există
    if os.path.exists(wav_folder):
        print(f"Folder '{wav_folder}' already exists. Skipping chunk creation.")
        return

    # Creează dosarul pentru chunk-uri WAV
    os.makedirs(wav_folder)

    # Încărcare fișier WAV complet
    audio = AudioSegment.from_file(full_wav_path)

    # Segmentarea pe baza pauzelor naturale
    chunks = split_on_silence(
        audio,
        min_silence_len=500,  # Pauze de cel puțin 0.5 secunde
        silence_thresh=-40    # Prag de tăcere la -40 dB
    )

    # Reguli de combinare: minim 20 secunde, maxim 2 minute
    min_chunk_length = 20 * 1000  # 20 secunde în milisecunde
    max_chunk_length = 2 * 60 * 1000  # 2 minute în milisecunde
    combined_chunks = []
    current_chunk = AudioSegment.silent(duration=0)

    for chunk in chunks:
        if len(current_chunk) + len(chunk) < max_chunk_length:
            current_chunk += chunk
        else:
            combined_chunks.append(current_chunk)
            current_chunk = chunk

    # Adaugă ultima bucată, dacă există
    if len(current_chunk) > 0:
        combined_chunks.append(current_chunk)

    # Asigurare că fiecare chunk are minim 20 secunde
    final_chunks = []
    current_chunk = AudioSegment.silent(duration=0)
    for chunk in combined_chunks:
        if len(current_chunk) + len(chunk) < min_chunk_length:
            current_chunk += chunk
        else:
            final_chunks.append(current_chunk)
            current_chunk = chunk

    if len(current_chunk) > 0:
        final_chunks.append(current_chunk)

    # Împarte chunk-urile mai mari de 2 minute
    final_processed_chunks = []
    for chunk in final_chunks:
        if len(chunk) > max_chunk_length:
            final_processed_chunks.extend(split_large_chunk(chunk, max_duration=max_chunk_length, overlap=5000))
        else:
            final_processed_chunks.append(chunk)

    # Exportă fișierele WAV și afișează doar numele fișierului
    for i, chunk in enumerate(final_processed_chunks, start=1):
        chunk_name = f"{wav_folder}/{i:03}.wav"
        chunk.export(chunk_name, format="wav")
        print(f"Exported: {os.path.basename(chunk_name)}")


def txt_creation(mp3_file_path):
    """
    Transcrie fișierele WAV dintr-un dosar și salvează textul într-un fișier TXT.
    """
    if not check_internet_connection():
        return

    mp3_file_path = os.path.expanduser(mp3_file_path)
    base_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    wav_folder = os.path.splitext(mp3_file_path)[0]  # Directorul pentru chunk-uri WAV
    txt_file_path = f"{os.path.splitext(mp3_file_path)[0]}.txt"  # Fisierul TXT final

    recognizer = sr.Recognizer()

    # Găsește toate fișierele WAV din dosar
    wav_files = sorted(
        [f for f in os.listdir(wav_folder) if f.endswith(".wav")],
        key=lambda x: os.path.getctime(os.path.join(wav_folder, x))
    )

    with open(txt_file_path, "w", encoding="utf-8") as output_file:
        for i, wav_file in enumerate(wav_files, start=1):
            wav_path = os.path.join(wav_folder, wav_file)
            duration = AudioSegment.from_file(wav_path).duration_seconds

            print(f"Processing {i}/{len(wav_files)} - Duration: {duration:.2f} seconds")
            try:
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)
                    text_output = recognizer.recognize_google(audio_data, language="ro-RO")
                    output_file.write(text_output + "\n")  # Scrie textul cu linie nouă între segmente
            except Exception as e:
                print(f"Error processing {wav_file}: {e}")
                output_file.write("\n")  # Scrie o linie goală dacă apare o eroare

    print(f"Transcription saved to {txt_file_path}")


# Exemplu de utilizare
mp3_file_path = "~/storage/music/rec/FisierulTau.mp3"
wav_creation(mp3_file_path)  # Creează chunk-urile WAV
txt_creation(mp3_file_path)  # Transcrie chunk-urile WAV
