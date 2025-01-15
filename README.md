# **Script de Transcriere Audio**  
_Transcriere automată a fișierelor audio lungi în text utilizând Python și Google Speech Recognition._

[English Version - click here](#audio-transcription-script-english-version)

---

## **Prezentare Generală**
Acest script Python vă permite să transcrieți gratuit fișiere audio lungi (peste o oră) în text. Scriptul împarte automat fișierele audio în segmente mai mici, de 2 minute (cu o suprapunere de 5 secunde între segmente), pentru a facilita procesarea eficientă folosind Google Speech Recognition.

---

## **Funcționalități**
- **Conversia automată MP3 → WAV** (doar dacă fișierul WAV nu există deja).
- **Segmentare audio:** Împarte fișierele WAV pe baza pauzelor naturale sau a unei durate maxime de 2 minute.
- **Gestionarea fișierelor zgomotoase:** Dacă nu pot fi detectate pauze, segmentele mari sunt împărțite în bucăți mai mici.
- **Transcriere automată:** Fiecare segment este procesat și textul este salvat direct într-un fișier `.txt`.
- **Feedback în timp real:** Afișează progresul procesării (numărul segmentelor transcrise, durata fiecărui segment).

---

## **Cum să folosești scriptul?**

### **1. Instalează Termux și un manager de fișiere**
- **Termux:** Descarcă aplicația din Google Play Store (sau altă sursă de încredere) pentru a rula scripturi Python pe Android.
- **Total Commander:** Descarcă această aplicație pentru a organiza și edita fișierele de pe telefon.

---

### **2. Acordă permisiuni pentru Termux**
1. Deschide Termux și rulează comanda:
   ```bash
   termux-setup-storage
   ```
2. Oferă permisiunile necesare. După acest pas, Termux va putea accesa fișierele din telefon la calea:
   ```bash
   ~/storage/
   ```
3. Asigură-te că permiți Termux să ruleze în fundal fără a fi întrerupt de Android.

---

### **3. Instalează Python și bibliotecile necesare**
Instalarea bibliotecilor necesare se face de script automat, deci poți sări complet peste acest pas.
```bash
pkg update && pkg upgrade
pkg install python
pip install SpeechRecognition pydub
pkg install ffmpeg
```

Aceste comenzi instalează componentele esențiale:
- **Python:** Limbajul de programare pentru rularea scripturilor.
- **SpeechRecognition:** Bibliotecă utilizată pentru transcrierea audio în text.
- **pydub:** Manipularea fișierelor audio (conversie și segmentare).
- **FFmpeg:** Instrument pentru manipularea formatelor audio/video.

---

### **4. Pregătește fișierele audio**
- Copiază fișierele audio pe care dorești să le transcrii în dosarul:
   ```bash
   ~/storage/music/rec/
   ```

---

### **5. Creează scriptul Python**
1. Creează un fișier nou în directorul menționat mai sus, cu numele `transcribe.py`.
2. Copiază conținutul scriptului (din acest repository) în fișier.
3. Editează următoarea linie din script pentru a introduce numele fișierului MP3:
   ```python
   mp3_file_path = "~/storage/music/rec/FișierulTău.mp3"
   ```

---

### **6. Rulează scriptul**
1. Deschide Termux și navighează în directorul cu scriptul:
   ```bash
   cd ~/storage/music/rec
   ```
2. Rulează scriptul:
   ```bash
   python transcribe.py
   ```

---

## **Cum funcționează scriptul?**

1. **Conectivitate la internet:** Verifică dacă există o conexiune activă la internet înainte de a începe transcrierea.
2. **Conversie audio:** Transformă fișierul MP3 într-un fișier WAV, dacă nu există deja.
3. **Segmentare:** Împarte fișierul WAV în bucăți mai mici:
   - Detectează pauzele naturale din audio.
   - În cazul zgomotului de fond, segmentează în bucăți de maxim 2 minute.
4. **Transcriere:** Procesează fiecare segment și salvează rezultatul într-un fișier `.txt`.

---

## **Întrebări Frecvente**

#### **De ce folosim pydub și FFmpeg?**
- **Pydub:** Pentru a manipula fișierele audio (conversie și segmentare).
- **FFmpeg:** Pentru conversia formatelor audio, necesar pentru ca pydub să funcționeze corect.

#### **Ce se întâmplă dacă fișierul audio are zgomot de fundal?**
- Scriptul identifică segmentele lungi fără pauze și le împarte automat în bucăți mai mici, cu suprapunere.

#### **Ce fac dacă nu am internet?**
- Scriptul se oprește automat și afișează un mesaj dacă nu există conexiune la internet.

---

## **Contribuie la proiect!**
Dacă ai sugestii pentru îmbunătățiri sau ai întâmpinat probleme, te invit să contribui la proiect! Lasă un comentariu sau trimite un pull request.

---

### **Susține-mi munca**
🍓☕ Dacă acest script îți este de ajutor, nu ezita să-mi oferi un lapte cu zmeură 😃

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/ionutojica)

---

# **Audio Transcription Script (English Version)**  
_Automatic transcription of long audio files into text using Python and Google Speech Recognition._

---

## **Overview**  
This Python script allows you to transcribe long audio files (over an hour) into text for free. The script splits large audio files into smaller 2-minute chunks (with a 5-second overlap) for efficient processing. It uses libraries like `pydub` and `SpeechRecognition` for audio manipulation and transcription.  

---

## **Features**  
- Automatically converts MP3 files to WAV format (if not already in WAV).
- Splits audio files based on silence or predefined duration (max. 2 minutes).
- Handles noisy audio by splitting large segments without silence detection.
- Saves transcriptions immediately to a `.txt` file for each audio input.
- Displays real-time progress for the transcription process.
- Avoids redundant processing by skipping existing files or folders.

---

## **Setup Instructions**  

### **1. Install Termux and File Manager (Android)**
- Download **Termux** from Google Play Store or another trusted source to run Python scripts.
- Download **Total Commander** to manage files and folders on your device.

---

### **2. Grant Termux Storage Permissions**
1. Open Termux and run:
   ```bash
   termux-setup-storage
   ```
2. Grant access to storage when prompted. This allows Termux to access files in internal storage (`~/storage/`).
3. Allow the background execution of Termux.

---

### **3. Install Required Libraries**
This step is optional, as the installation of the required libraries is taken by the script.
```bash
pkg update && pkg upgrade
pkg install python
pip install SpeechRecognition pydub
pkg install ffmpeg
```

These libraries provide essential functionality:
- **`python`:** The programming language to execute the script.
- **`SpeechRecognition`:** For converting audio into text using Google Speech Recognition.
- **`pydub`:** For audio conversion and segmentation.
- **`ffmpeg`:** Required for audio format handling (MP3 to WAV).

---

### **4. Prepare Your Audio Files**
- Copy your MP3 audio files to `~/storage/music/rec` or a similar directory.  
- The script will access these files and create necessary output in the same location.

---

### **5. Save and Edit the Script**
- Create a Python script named `transcribe.py` in the same directory as your audio files.
- Copy the full script (provided in this repository) into the file.
- Update the `mp3_file_path` variable inside the script with the path to your audio file:
   ```python
   mp3_file_path = "~/storage/music/rec/YourAudioFile.mp3"
   ```

---

### **6. Run the Script**
1. Navigate to the folder containing `transcribe.py`:
   ```bash
   cd ~/storage/music/rec
   ```
2. Execute the script:
   ```bash
   python transcribe.py
   ```

---

## **How It Works**
1. **Checks internet connectivity:** Ensures Google Speech Recognition can process the files.
2. **Converts MP3 to WAV:** Prepares the audio file for processing.
3. **Splits the audio into chunks:**
   - Detects natural silences for segmentation.
   - Handles noisy audio by splitting large chunks into 2-minute segments with overlaps.
4. **Processes and transcribes each chunk:** Saves the transcription directly to a text file in real-time.

---

## **Customization Options**
- **Max chunk duration:** Change the `max_duration` parameter in `split_large_chunk`.
- **Silence detection thresholds:** Adjust `min_silence_len` and `silence_thresh` in `wav_creation`.
- **Output format:** Modify the script to save results in JSON or CSV if needed.

---

## **Questions for You**
- Would you use this script for your transcription needs?
- Are there any additional features you'd like to see (e.g., multi-language support, custom formatting)?
- Would you like to see this script on GitHub for easier access?

---

### **Support My Work**
🍓☕ If this script has been useful to you, do not hesitate to offer me a strawberry milk 😃

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/ionutojica)

---

### **License**
This project is open-source and free to use. Contributions are welcome!
