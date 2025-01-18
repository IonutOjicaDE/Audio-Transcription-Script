# **Script de Transcriere Audio**  
_Transcriere automată a fișierelor audio lungi în text utilizând Python și Google Speech Recognition._

[English Version - click here](#audio-transcription-script-english-version)

---

## **Prezentare Generală**
Acest script Python vă permite să transcrieți gratuit fișiere audio lungi (peste o oră) în text. Scriptul împarte automat fișierele audio în segmente mai mici, de 2 minute (cu o suprapunere de 5 secunde între segmente), pentru a facilita procesarea eficientă folosind Google Speech Recognition.

---

## **Funcționalități**
- **Procesare audio:** Transformă MP3 în WAV, segmentează fișierul și transcrie textul folosind Google Speech Recognition.
- **Conversia automată MP3 → WAV** (doar dacă fișierul WAV nu există deja).
- **Analiză și afișare:** Identifică fișierele `.mp3` și starea lor (WAV, chunk-uri, TXT) într-un format ușor de citit.
- **Selecție flexibilă:** Permite alegerea fișierelor pentru procesare prin:
  - Procesare automată a fișierelor neprocesate.
  - Procesare specifică pe baza numerelor sau a tuturor fișierelor.
- **Backup automat:** Protejează fișierele existente prin mutarea lor în backup cu timestamp.
- **Segmentare audio:** Împarte fișierele WAV pe baza pauzelor naturale sau a unei durate maxime de 2 minute.
- **Gestionarea fișierelor zgomotoase:** Dacă nu pot fi detectate pauze, segmentele mari sunt împărțite în bucăți mai mici.
- **Transcriere automată:** Fiecare segment este procesat și textul este salvat direct într-un fișier `.txt`.
- **Feedback în timp real:** Afișează progresul procesării (numărul segmentelor transcrise, durata fiecărui segment).

---

## **Cum să folosești scriptul?**

### **1. Instalează Termux și un manager de fișiere**
- **Termux:** Descarcă aplicația din Google Play Store (sau altă sursă de încredere) pentru a rula scripturi Python pe Android.
- **Total Commander:** Opțional: descarcă această aplicație pentru a organiza și edita fișierele de pe telefon.

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

### **3. Instalează Python**
Scriptul are nevoie de Python, care poate fi instalat executând comenzile următoare în Termux:
```bash
pkg update && pkg upgrade
pkg install python
```

Instalarea bibliotecilor necesare de script se face automat la execuția scriptului, deci poți sări complet peste acest pas.
```bash
pkg update && pkg upgrade
pip install SpeechRecognition pydub ffmpeg
```

Aceste comenzi instalează componentele esențiale:
- **Python:** Limbajul de programare pentru rularea scripturilor.
- **SpeechRecognition:** Bibliotecă utilizată pentru transcrierea audio în text.
- **pydub:** Manipularea fișierelor audio (conversie și segmentare).
- **FFmpeg:** Instrument pentru manipularea formatelor audio/video.

---

### **4. Pregătește fișierele audio**
- Copiază fișierele audio pe care dorești să le transcrii în dosarul dorit. Eu le-am salvat în dosarul nou `rec` din dosarul `music`:
   ```bash
   ~/storage/music/rec/
   ```

---

### **6. Rulează scriptul**
1. Deschide Termux și navighează în directorul cu fișierele mp3:
   ```bash
   cd ~/storage/music/rec
   ```
2. Rulează scriptul:
   ```bash
   wget -q -O transcribe.py https://raw.githubusercontent.com/IonutOjicaDE/Audio-Transcription-Script/main/transcribe.py && python transcribe.py
   ```

---

## **Cum funcționează scriptul?**

1. **Conectivitate la internet:** 
   - Verifică dacă există o conexiune activă la internet înainte de a începe transcrierea pentru a asigura funcționarea Google Speech Recognition.

2. **Analiza fișierelor din directorul curent:** 
   - Identifică fișierele `.mp3` din directorul curent.
   - Verifică pentru fiecare fișier dacă există:
     - Fișierul WAV complet (convertit din MP3).
     - Dosarul care conține chunk-urile audio.
     - Fișierul TXT care conține subtitrarea.
   - Afișează informațiile despre fișiere într-o listă numerotată, în format compact, indicând starea fiecărui fișier:
     - Exemplu:
       ```
       1. audio1.mp3 (WAV: 1 Chunks: 1 SUB: 0)
       2. audio2.mp3 (WAV: 0 Chunks: 0 SUB: 1)
       ```

3. **Selectarea fișierelor pentru procesare:**
   - Permite utilizatorului să aleagă ce fișiere MP3 să proceseze:
     - **`Enter`:** Procesează doar fișierele care nu au fișierul TXT creat.
     - **`*`, `all`, `toate`:** Procesează toate fișierele MP3, indiferent de starea lor:
       - Fișierele WAV, chunk-urile și subtitrările existente sunt mutate în backup, într-un dosar `bak`, cu timestamp adăugat la nume.
     - **Numere individuale sau liste numerice:** Permite procesarea fișierelor selectate (ex. `1`, `1,3`, `2 4`).

4. **Mutarea fișierelor existente în backup:**
   - Înainte de a procesa un fișier selectat (în cazul opțiunii `*` sau `all`):
     - Fișierul WAV complet este mutat într-un dosar `bak` și redenumit cu un timestamp (ex. `audio1_230101_120000.wav`).
     - La fel se procedează cu dosarul de chunk-uri și cu fișierul TXT.

5. **Conversie audio:**
   - Dacă fișierul WAV complet nu există, scriptul convertește fișierul MP3 în format WAV.

6. **Segmentare:** 
   - Împarte fișierul WAV în bucăți mai mici:
     - Detectează pauzele naturale din audio.
     - Dacă pauzele nu pot fi identificate (zgomot de fond), segmentează în bucăți de maxim 2 minute cu suprapunere de 5 secunde.

7. **Transcriere:** 
   - Procesează fiecare segment audio folosind Google Speech Recognition.
   - Salvează textul transcris într-un fișier `.txt`.

---

## **Întrebări Frecvente**

#### **De ce folosim `pydub` și `FFmpeg`?**
- **Pydub:** Pentru a manipula fișierele audio, inclusiv conversia din MP3 în WAV și segmentarea acestora.
- **FFmpeg:** Pentru a permite pydub să efectueze conversii audio între diferite formate, cum ar fi MP3 → WAV.

#### **Cum gestionează scriptul fișierele cu zgomot de fundal?**
- Dacă scriptul detectează un segment lung fără pauze naturale (de exemplu, din cauza zgomotului de fundal), acesta împarte automat fișierul audio în bucăți mai mici, de maxim 2 minute, cu o suprapunere de 5 secunde între segmente, pentru a nu pierde informații.

#### **Ce se întâmplă dacă nu am internet?**
- Scriptul verifică conexiunea la internet înainte de a începe transcrierea.
- Dacă nu există conexiune, scriptul afișează un mesaj de eroare și se oprește pentru a preveni erorile legate de transcriere.

#### **Cum sunt afișate fișierele MP3 analizate?**
- Scriptul afișează o listă numerotată a fișierelor MP3 găsite în directorul curent, împreună cu informații despre starea acestora:
  - **WAV:** Există sau nu fișierul WAV complet.
  - **Chunks:** Există sau nu dosarul cu chunk-uri audio.
  - **SUB:** Există sau nu fișierul TXT (subtitrare).
- Exemplu de afișare:
  ```
  1. audio1.mp3 (WAV: 1 Chunks: 1 SUB: 0)
  2. audio2.mp3 (WAV: 0 Chunks: 0 SUB: 1)
  ```

#### **Cum pot selecta fișierele pentru procesare?**
- Scriptul oferă mai multe opțiuni pentru a selecta fișierele de procesat:
  - **`Enter`:** Procesează doar fișierele MP3 care nu au subtitrarea creată.
  - **`*`, `all`, `toate`:** Procesează toate fișierele MP3 din listă, indiferent de starea lor, mutând fișierele existente (WAV, chunk-uri, TXT) într-un dosar `bak` pentru backup.
  - **Numere individuale sau liste numerice:** Permite procesarea fișierelor selectate, introducând numerele lor din listă (ex. `1`, `1,3`, `2 4`).

#### **Ce se întâmplă cu fișierele existente înainte de procesare?**
- În cazul opțiunilor `*`, `all` sau `toate`, scriptul mută fișierele existente în backup:
  - Fișierul WAV complet este mutat într-un dosar `bak`, cu un timestamp adăugat la nume (ex. `audio1_230101_120000.wav`).
  - Dosarul chunk-urilor și fișierul TXT sunt tratate similar.

#### **Cum asigură scriptul că nu suprascrie fișierele existente?**
- Scriptul verifică existența fișierelor WAV, chunk-urilor și subtitrărilor înainte de a începe procesarea.
- Dacă fișierele există și utilizatorul selectează opțiunea de a procesa tot (`all`), acestea sunt mutate într-un dosar `bak` cu timestamp, prevenind suprascrierea.

#### **Cum mă asigur că toate dependențele sunt instalate?**
- Scriptul verifică automat dacă toate pachetele necesare (ex. `pydub`, `speechrecognition`) sunt instalate.
- Dacă lipsesc, scriptul le instalează automat și actualizează sistemul de operare, dacă este necesar.

#### **Ce fac dacă întâmpin erori în timpul rulării?**
- Verifică dacă ai o conexiune stabilă la internet.
- Asigură-te că fișierele audio sunt într-un format suportat (`.mp3`).
- Dacă problema persistă, verifică logurile afișate de script pentru a identifica pasul unde apare eroarea.

#### **Cum gestionează scriptul backup-urile?**
- Toate fișierele existente (WAV complet, chunk-uri și TXT) sunt mutate într-un dosar `bak` înainte de procesare, cu timestamp adăugat la numele lor. Acest lucru asigură că nu pierzi datele generate anterior.

#### **Ce se întâmplă dacă directorul curent nu conține fișiere MP3?**
- Scriptul va afișa un mesaj informând că nu există fișiere MP3 de procesat și se va opri.

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
This Python script enables you to transcribe long audio files (over an hour) to text for free. The script automatically splits audio files into smaller 2-minute segments (with a 5-second overlap between segments) to ensure efficient processing using Google Speech Recognition.

---

## **Features**
- **Audio processing:** Converts MP3 to WAV, segments the audio, and transcribes text using Google Speech Recognition.
- **Automatic MP3 → WAV conversion** (only if the WAV file doesn't already exist).
- **Analysis and display:** Identifies `.mp3` files and their status (WAV, chunks, TXT) in an easy-to-read format.
- **Flexible selection:** Allows you to choose files for processing via:
  - Automatic processing of unprocessed files.
  - Specific processing based on numbers or all files in the directory.
- **Automatic backup:** Protects existing files by moving them to a backup folder with a timestamp.
- **Audio segmentation:** Splits WAV files based on natural pauses or a maximum duration of 2 minutes.
- **Handling noisy files:** If no pauses are detected, large segments are divided into smaller chunks.
- **Automatic transcription:** Each audio segment is processed, and the text is saved directly into a `.txt` file.
- **Real-time feedback:** Displays processing progress, including the number of transcribed segments and the duration of each.

---

## **How to Use the Script**

### **1. Install Termux and a File Manager**
- **Termux:** Download the app from Google Play Store (or a trusted source) to run Python scripts on Android.
- **Total Commander:** Optional: Download this app to organize and edit files on your phone.

---

### **2. Grant Permissions to Termux**
1. Open Termux and run the following command:
   ```bash
   termux-setup-storage
   ```
2. Provide the necessary permissions. After this step, Termux will be able to access files on your phone under the path:
   ```bash
   ~/storage/
   ```
3. Ensure Termux is allowed to run in the background without being interrupted by Android.

---

### **3. Install Python**
The script requires Python, which can be installed by running the following commands in Termux:
```bash
pkg update && pkg upgrade
pkg install python
```

Installation of the required libraries will be handled automatically when running the script, so you can skip manual installation. For reference:
```bash
pkg update && pkg upgrade
pip install SpeechRecognition pydub ffmpeg
```

These commands install essential components:
- **Python:** The programming language used to run the script.
- **SpeechRecognition:** A library used for audio-to-text transcription.
- **pydub:** For audio manipulation (conversion and segmentation).
- **FFmpeg:** A tool for handling audio/video formats.

---

### **4. Prepare Audio Files**
- Copy the audio files you want to transcribe into the desired folder. For example, save them in a new `rec` folder under `music`:
   ```bash
   ~/storage/music/rec/
   ```

---

### **5. Run the Script**
1. Open Termux and navigate to the directory containing your MP3 files:
   ```bash
   cd ~/storage/music/rec
   ```
2. Run the script:
   ```bash
   wget -q -O transcribe.py https://raw.githubusercontent.com/IonutOjicaDE/Audio-Transcription-Script/main/transcribe.py && python transcribe.py
   ```

---

## **How the Script Works**

1. **Internet Connectivity:** 
   - Checks for an active internet connection before starting transcription to ensure Google Speech Recognition works properly.

2. **File Analysis:** 
   - Identifies `.mp3` files in the current directory.
   - Checks for the presence of:
     - The full WAV file (converted from MP3).
     - The folder containing audio chunks.
     - The `.txt` file containing the transcription.
   - Displays file information in a numbered list with their status in a compact format:
     - Example:
       ```
       1. audio1.mp3 (WAV: 1 Chunks: 1 SUB: 0)
       2. audio2.mp3 (WAV: 0 Chunks: 0 SUB: 1)
       ```

3. **File Selection for Processing:**
   - Allows the user to choose which MP3 files to process:
     - **`Enter`:** Processes only files without a `.txt` transcription.
     - **`*`, `all`, `toate`:** Processes all MP3 files, regardless of status:
       - Existing WAV files, chunks, and transcriptions are moved to a backup folder with a timestamp.
     - **Individual numbers or numeric lists:** Processes selected files based on their list numbers (e.g., `1`, `1,3`, `2 4`).

4. **Backup Existing Files:**
   - Before processing a selected file (for options `*` or `all`):
     - The full WAV file is moved to a `bak` folder and renamed with a timestamp (e.g., `audio1_230101_120000.wav`).
     - The chunk folder and `.txt` transcription are similarly handled.

5. **Audio Conversion:**
   - Converts the MP3 file to WAV if the full WAV file doesn't already exist.

6. **Segmentation:** 
   - Splits the WAV file into smaller chunks:
     - Detects natural pauses in the audio.
     - If no pauses are detected (due to background noise), segments are created with a maximum duration of 2 minutes and a 5-second overlap.

7. **Transcription:** 
   - Processes each audio segment using Google Speech Recognition.
   - Saves the transcribed text directly into a `.txt` file.

---

## **Frequently Asked Questions**

#### **Why do we use `pydub` and `FFmpeg`?**
- **Pydub:** For audio file manipulation, including MP3 to WAV conversion and segmentation.
- **FFmpeg:** Enables `pydub` to handle audio format conversions like MP3 → WAV.

#### **How does the script handle noisy files?**
- If the script detects long segments without natural pauses (e.g., due to background noise), it automatically divides the audio into smaller chunks (up to 2 minutes each) with a 5-second overlap to avoid losing information.

#### **What happens if I don't have an internet connection?**
- The script checks for an internet connection before starting transcription.
- If no connection is available, the script displays an error message and stops to prevent transcription errors.

#### **How are MP3 files displayed for processing?**
- The script displays a numbered list of MP3 files found in the current directory, along with their statuses:
  - **WAV:** Indicates if the full WAV file exists.
  - **Chunks:** Indicates if the chunk folder exists.
  - **SUB:** Indicates if the `.txt` transcription exists.
- Example:
  ```
  1. audio1.mp3 (WAV: 1 Chunks: 1 SUB: 0)
  2. audio2.mp3 (WAV: 0 Chunks: 0 SUB: 1)
  ```

#### **How can I select files for processing?**
- The script provides several options:
  - **`Enter`:** Processes only untranscribed MP3 files.
  - **`*`, `all`, `toate`:** Processes all MP3 files in the list, backing up existing files.
  - **Individual numbers or numeric lists:** Allows processing selected files based on their list numbers (e.g., `1`, `1,3`, `2 4`).

#### **How does the script prevent overwriting existing files?**
- The script checks for existing WAV, chunk, and transcription files before starting processing.
- If such files exist and the user selects `all`, they are moved to a backup folder with a timestamp.

#### **How does the script manage backups?**
- All existing files (WAV, chunks, TXT) are moved to a `bak` folder before processing, with a timestamp added to their names. This ensures no data is overwritten.

#### **What if there are no MP3 files in the directory?**
- The script will display a message indicating no MP3 files were found and will stop execution.

---

### **Contribute to the Project!**
If you have suggestions for improvements or encounter any issues, you're welcome to contribute to the project! Feel free to leave a comment or submit a pull request.

---

### **Support My Work**
🍓☕ If this script has been useful to you, do not hesitate to offer me a strawberry milk 😃

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/ionutojica)

---

### **License**
This project is open-source and free to use. Contributions are welcome!
