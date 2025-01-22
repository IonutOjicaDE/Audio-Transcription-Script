"""
AUDIO-TRANSCRIPTION-SCRIPT for Android
https://github.com/IonutOjicaDE/Audio-Transcription-Script
Ionut Ojica 18.01.2025

Automatic transcription of long audio files into text using Python and Google Speech Recognition.

1. Install Termux from PlayStore
2. Grant Storage Permissions executing in Termux: termux-setup-storage
3. Navigate to the folder where the mp3 files are
4. Execute
wget -q -O transcribe.py https://raw.githubusercontent.com/IonutOjicaDE/Audio-Transcription-Script/main/transcribe.py && python transcribe.py
5. Choose the files you want and enjoy!
"""

import subprocess
import sys
import os
import shutil
from datetime import datetime

# Funcție pentru actualizare și upgrade pachete de sistem (doar dacă e nevoie)
def update_system():
    """
    Actualizează și upgradează pachetele de sistem.
    Este apelată doar dacă lipsește o bibliotecă Python.
    """
    try:
        print("Updating system packages...")
        subprocess.check_call(["pkg", "update", "-y"])  # Actualizare pachete
        subprocess.check_call(["pkg", "upgrade", "-y"])  # Upgrade pachete
        print("System packages updated successfully.")
    except Exception as e:
        print(f"Error during system update: {e}")

# Verifică și instalează pachetele necesare
def check_and_install_packages(required_packages):
    """
    Verifică dacă toate pachetele necesare sunt instalate. Dacă lipsește unul,
    se execută update/upgrade și se instalează toate pachetele necesare.
    """
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages detected: {', '.join(missing_packages)}")
        update_system()  # Execută update/upgrade doar dacă lipsesc pachete
        for package in missing_packages:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} installed successfully.")
            except Exception as e:
                print(f"Error installing {package}: {e}")
    else:
        print("All required packages are already installed.")

# Lista pachetelor necesare
required_packages = ["pydub", "speech_recognition"]

# Verifică și instalează pachetele necesare
check_and_install_packages(required_packages)

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
    except:
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

def check_disk_space(required_space):
    """
    Verifică dacă există suficient spațiu pe disc pentru operațiile necesare.
    :param required_space: Spațiul necesar în bytes.
    :return: True dacă există suficient spațiu, altfel False.
    """
    total, used, free = shutil.disk_usage("/")
    if free >= required_space:
        return True
    print(f"Insufficient disk space. Required: {required_space / (1024 ** 2):.2f} MB, Available: {free / (1024 ** 2):.2f} MB.")
    return False

def estimate_wav_size(mp3_file_path):
    """
    Estimează dimensiunea fișierului WAV bazată pe durata fișierului MP3.
    :param mp3_file_path: Calea către fișierul MP3.
    :return: Dimensiunea estimată a fișierului WAV în bytes.
    """
    audio = AudioSegment.from_file(mp3_file_path)
    duration_in_minutes = audio.duration_seconds / 60
    wav_size = duration_in_minutes * 10 * 1024 * 1024  # 10 MB per minute
    return int(wav_size)


def full_wav_creation(mp3_file_path):
    """
    Creează un fișier WAV complet dintr-un fișier MP3 și îl încarcă în memorie.
    """
    mp3_file_path = os.path.expanduser(mp3_file_path)
    base_name = os.path.splitext(os.path.basename(mp3_file_path))[0]
    full_wav_path = f"{os.path.splitext(mp3_file_path)[0]}.wav"

    # Estimare dimensiune WAV și verificare spațiu liber
    wav_size = estimate_wav_size(mp3_file_path)
    required_space = int(wav_size * 1.5)  # 1.5x pentru chunk-uri
    if not check_disk_space(required_space):
        raise RuntimeError("Not enough disk space for WAV export and chunk processing.")

    # Conversie MP3 → WAV complet
    if not os.path.exists(full_wav_path):
        try:
            print(f"Converting MP3 file '{base_name}' to full WAV...")
            AudioSegment.from_file(mp3_file_path).export(full_wav_path, format="wav")
            print(f"Full WAV file '{full_wav_path}' created.")
        except Exception as e:
            print(f"Error exporting full WAV file: {e}")
            raise
    else:
        print(f"Full WAV file '{full_wav_path}' already exists. Skipping creation.")

    # Încărcare fișier WAV complet în memorie
    print(f"Loading full WAV file '{full_wav_path}' into memory...")
    audio = AudioSegment.from_file(full_wav_path)
    print(f"Full WAV file '{full_wav_path}' loaded into memory.")

    return audio, base_name

def chunks_creation_based_silence(audio):
    """
    Creează segmente audio pe baza pauzelor naturale din fișierul WAV complet.
    """
    print("Splitting audio into chunks based on silence...")
    chunks = split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-40
    )
    print(f"{len(chunks)} chunks created based on silence.")
    return chunks

def chunks_creation_based_duration(chunks, max_duration=2 * 60 * 1000, overlap=5000):
    """
    Împarte segmentele mari în bucăți mai mici pe baza duratei maxime.
    """
    print("Splitting large chunks into smaller segments...")
    final_chunks = []
    for chunk in chunks:
        start = 0
        while start < len(chunk):
            end = min(start + max_duration, len(chunk))
            segment = chunk[start:end]
            if len(segment) <= overlap:
                print(f"Skipping segment from {start} ms to {end} ms (too small).")
                break
            final_chunks.append(segment)
            start = end - overlap
    print(f"{len(final_chunks)} final chunks created based on duration.")
    return final_chunks

def chunks_export(chunks, base_name):
    """
    Creează un dosar și exportă segmentele audio în fișiere WAV separate.
    """
    output_dir = base_name
    print(f"Creating directory '{output_dir}' for WAV chunks...")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Exporting {len(chunks)} chunks to directory '{output_dir}'...")
    for i, chunk in enumerate(chunks, start=1):
        chunk_name = f"{output_dir}/{i:03}.wav"
        try:
            chunk.export(chunk_name, format="wav")
            print(f"Exported: {chunk_name}")
        except Exception as e:
            print(f"Error exporting chunk '{chunk_name}': {e}")
            raise


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

# === Funcția pentru listarea și analiza fișierelor ===
def analyze_files():
    """
    Analizează toate fișierele și dosarele din directorul curent, verificând starea lor:
    - Fișiere MP3
    - Fișiere WAV complete
    - Dosare de chunk-uri
    - Fișiere TXT (subtitrări)
    Returnează o listă cu informațiile găsite și afișează în format de listă pentru ecrane înguste.
    """
    current_dir = os.getcwd()  # Calea curentă
    print(f"Current directory: {current_dir}\n")

    files_data = []  # Listă pentru stocarea informațiilor despre fișiere

    for file in os.listdir(current_dir):
        if file.endswith(".mp3"):  # Găsește toate fișierele MP3
            base_name = os.path.splitext(file)[0]
            full_wav = f"{base_name}.wav"
            chunk_dir = base_name
            subtitle = f"{base_name}.txt"

            files_data.append({
                "mp3": file,
                "full_wav": os.path.exists(full_wav),
                "chunk_dir": os.path.exists(chunk_dir),
                "subtitle": os.path.exists(subtitle)
            })

    # Afișare în format de listă
    print("List of MP3 files and their status:\n")
    for idx, file_data in enumerate(files_data, start=1):
        wav_status = "1" if file_data["full_wav"] else "0"
        chunk_status = "1" if file_data["chunk_dir"] else "0"
        subtitle_status = "1" if file_data["subtitle"] else "0"
        print(f"{idx}. {file_data['mp3']} (WAV: {wav_status} Chunks: {chunk_status} SUB: {subtitle_status})")

    return files_data

# === Funcția pentru procesarea fișierelor selectate ===
def process_files(files_data):
    """
    Permite utilizatorului să selecteze fișierele MP3 pentru procesare și execută acțiunile.
    """
    choices = input("Enter your choice (e.g., '1', '1,2', '*', or press Enter to process unprocessed files): ").strip()

    # Dacă utilizatorul doar apasă Enter
    if not choices:
        print("Processing unprocessed files...")
        # Obține o listă de fișiere neprocesate (fără subtitrare)
        unprocessed_files = [data for data in files_data if not data["subtitle"]]
        files_to_process = unprocessed_files
    elif choices in ["*", "all", "toate"]:
        print("Processing all files...")
        files_to_process = files_data
    else:
        # Interpretăm opțiunile utilizatorului
        try:
            selected_indices = [int(x.strip()) - 1 for x in choices.replace(",", " ").split()]
            files_to_process = [files_data[i] for i in selected_indices if 0 <= i < len(files_data)]
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas or spaces.")
            return

    # Procesarea fiecărui fișier selectat
    for file_data in files_to_process:
        mp3_file = file_data["mp3"]
        base_name = os.path.splitext(mp3_file)[0]
        full_wav = f"{base_name}.wav"
        chunk_dir = base_name
        subtitle = f"{base_name}.txt"

        # Dacă opțiunea este "all", mutăm fișierele existente în backup
        if choices in ["*", "all", "toate"]:
            backup_dir = "bak"
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("_%y%m%d_%H%M%S")

            if os.path.exists(full_wav):
                shutil.move(full_wav, os.path.join(backup_dir, f"{base_name}{timestamp}.wav"))
                print(f"Moved '{full_wav}' to backup.")
            if os.path.exists(chunk_dir):
                shutil.move(chunk_dir, os.path.join(backup_dir, f"{base_name}{timestamp}"))
                print(f"Moved '{chunk_dir}' to backup.")
            if os.path.exists(subtitle):
                shutil.move(subtitle, os.path.join(backup_dir, f"{base_name}{timestamp}.txt"))
                print(f"Moved '{subtitle}' to backup.")

        # Creare fișiere WAV și chunk-uri
        print(f"Processing '{mp3_file}'...")
        audio, base_name = full_wav_creation(mp3_file)  # Creează și încarcă fișierul WAV complet
        silence_chunks = chunks_creation_based_silence(audio)  # Creează segmente pe baza pauzelor naturale
        final_chunks = chunks_creation_based_duration(silence_chunks)  # Creează segmente pe baza duratei maxime
        chunks_export(final_chunks, base_name)  # Exportă segmentele audio
        txt_creation(mp3_file)

    print("Processing complete!")

# === Main script ===
if __name__ == "__main__":
    # Analizează fișierele din directorul curent
    files_data = analyze_files()

    # Procesează fișierele selectate
    process_files(files_data)
