# File Organizer 📁

A modern, lightweight, cross-platform desktop application built with Python and CustomTkinter to automatically organize files in your target directory (e.g., `Downloads`) into structured category folders.

![Platform Support](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20(Fedora%2FUbuntu)-blue)
![Python Version](https://img.shields.io/badge/Python-3.11-green)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ Key Features

- **Automated Directory Monitoring:** Real-time folder watching using `watchdog` to sort new files instantly as they arrive.
- **Manual "Organize Now" Mode:** One-click directory cleanup for existing messy folders.
- **Zero-Dependency Architecture:** Single standalone binary executable for both Windows and Linux without requiring extra system library installations.
- **Auto Start-Menu Integration (Linux):** Automatically registers a desktop launcher in GNOME / Fedora Applications Menu on its first run.
- **Granular Organization Rules:** Enable or disable specific file categories (Videos, Images, Audio, Documents, Archives, Software Executables).
- **Clean Modern Interface:** Minimalist light-theme desktop user experience powered by `CustomTkinter`.

---

## 🚀 How to Download & Run

### 🐧 For Linux Users (Fedora / GNOME / Ubuntu)

No terminal commands or extra package extractions needed! Follow these plug-and-play steps:

1. Go to the **[Releases](https://github.com/umair5464/file-organizer/releases)** page and download `FileOrganizer-Linux`.
2. Right-click the downloaded `FileOrganizer-Linux` file in your **Files** app and select **Properties**.
3. Switch to the **Permissions** tab and toggle ON **"Allow executing file as program"** (or run `chmod +x FileOrganizer-Linux` in terminal).
4. Double-click `FileOrganizer-Linux` to launch!

> 💡 **Start Menu Integration:** On your very first run, the app automatically registers itself with your Fedora system. You can afterwards press the **Super Key** (Windows Key) and search for **"File Organizer"** to launch it directly from your App Launcher!

---

### 🪟 For Windows Users

1. Go to the **[Releases](https://github.com/umair5464/file-organizer/releases)** page and download `FileOrganizer-Windows.exe`.
2. Double-click `FileOrganizer-Windows.exe` to run the application directly.

> 🛡️ **Windows SmartScreen Notice:**  
> Since this project is open-source and not signed with a paid corporate certificate, Windows Defender SmartScreen might show a warning dialog (*"Windows protected your PC"*).  
> **To bypass this:** Click on **More info** $\rightarrow$ Click **Run anyway**.

---

## 📂 Supported File Categories

| Category | Description | Sample Extensions |
| :--- | :--- | :--- |
| **Videos & Clips** | Movies, screen recordings, media files | `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm` |
| **Images & Photos** | Vector graphics, photos, web formats | `.jpg`, `.png`, `.gif`, `.webp`, `.heic`, `.svg` |
| **Audio & Music** | Music tracks, voice recordings | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg` |
| **Documents & Text** | Spreadsheets, PDFs, office docs | `.pdf`, `.docx`, `.xlsx`, `.txt`, `.csv` |
| **Archives** | Compressed files, tarballs | `.zip`, `.tar.gz`, `.7z`, `.rar` |
| **Apps & Executables** | Installers, AppImages, system binaries | `.exe`, `.msi`, `.appimage`, `.deb`, `.rpm` |

---

## 🛠️ Building from Source

If you want to run or build the project manually using Python:

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/umair5464/file-organizer.git](https://github.com/umair5464/file-organizer.git)
   cd file-organizer
Install Dependencies:

Bash
pip install -r requirements.txt
Run Application:

Bash
python app.py
Build Local Executable via PyInstaller:

Bash
# Linux Standalone Binary
pyinstaller --noconfirm --onefile --windowed --add-data "$(python3 -c 'import customtkinter; print(customtkinter.__path__[0])'):customtkinter/" --name "FileOrganizer-Linux" app.py

# Windows Standalone .exe
pyinstaller --noconfirm --onefile --windowed --add-data "$(python -c 'import customtkinter, os; print(os.path.dirname(customtkinter.__file__))');customtkinter/" --name "FileOrganizer-Windows.exe" app.py
📜 License
Distributed under the MIT License. See LICENSE for more information.
