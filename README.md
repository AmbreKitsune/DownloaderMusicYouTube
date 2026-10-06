EN / [RU](README.ru.md)

<h1 align="center">🎵 DOWNLOADER MUSIC YOUTUBE 🎵</h1>

<p align="center">A lightweight command-line tool for downloading audio from YouTube and YouTube Music as MP3.</p>

---

# Table of Contents 📃

- [Description 😼](#description-)
- [Features 🛠️](#features-️)
- [How It Works ⚙️](#how-it-works-️)
- [Tech Stack 📂](#tech-stack-)
- [Quick Start 👾](#quick-start-)
- [CLI Usage 💻](#cli-usage-)
- [Files and Paths 📁](#files-and-paths-)
- [Errors and Troubleshooting ❌](#errors-and-troubleshooting-)
- [Q&A ❓](#qa-)
- [Limitations 📢](#limitations-)
- [Links 🙀](#links-)

---

# Description 😼

**DownloaderMusicYouTube** is a small Python command-line application that downloads audio from a YouTube or YouTube Music URL and converts it to **MP3**. It is intended for people who prefer a straightforward console workflow instead of installing a separate graphical downloader.

The project started as a simple script that prompted for a URL. It has since been updated with **Typer** for command-line options, **Rich** for console messages, and automatic preparation of a **local FFmpeg** installation. The audio download itself is handled by **yt-dlp**.

**Version v0.2.0** includes a standalone **`music.exe`** and a **Windows installer**. The installer adds the program directory to your user `PATH`, so you can download music from any newly opened terminal without installing Python. Once a download finishes, the program automatically opens its `downloads/` folder.

---

# Features 🛠️

- Download audio from supported **YouTube** and **YouTube Music** URLs.
- Convert downloaded audio to **MP3** using FFmpeg.
- Request **192 kbps** MP3 encoding (this does not improve low-quality source audio).
- Start a download with the `--download <URL>` CLI option.
- Show command help with `--help`.
- Download and extract the required FFmpeg binaries automatically when missing.
- Reuse the local FFmpeg installation on subsequent runs.
- Keep FFmpeg separate from the system installation and system `PATH`.
- Show status and error messages in English, with a nonzero exit code for handled download errors.
- Install the Windows CLI with a setup wizard that adds `music.exe` to the user's `PATH`.
- Run the standalone executable without installing Python.
- Save MP3 files beside the executable and open the output folder after a successful download.

**Current scope:** download a URL to MP3. Playlist handling, batch downloading, and other formats are not documented as supported features yet.

---

# How It Works ⚙️

1. The CLI reads the URL passed to `--download`.
2. The application checks for `ffmpeg.exe` and `ffprobe.exe` in `ffmpeg/` **beside the application**.
3. If either file is missing, it downloads the FFmpeg Essentials archive from **Gyan.dev**, extracts the two binaries, and cleans up temporary files.
4. **yt-dlp** downloads the available audio, and the local **FFmpeg** converts it into MP3.
5. The finished MP3 is saved in `downloads/` **beside `music.exe`**, and Windows File Explorer opens that directory.

When running from source, the application files are `src/*.py`, so the generated `ffmpeg/` and `downloads/` directories are created **inside `src/`**. The download location does not depend on the directory from which you open the terminal.

FFmpeg is only downloaded on the first run (or when a binary is missing); it is not installed system-wide. A connection to YouTube is still required for downloads.

---

# Tech Stack 📂

| Component | Purpose |
| --- | --- |
| **Python 3.12+** | Runtime when launching from source |
| **Typer** | CLI options and help |
| **Rich** | Console messages |
| **yt-dlp** | Audio extraction and download |
| **FFmpeg / ffprobe** | Audio conversion and media probing |
| **Requests** | Downloading the FFmpeg archive |
| **pathlib / zipfile / shutil** | Paths, extraction, and temporary-file cleanup |
| **PyInstaller** | Building the standalone Windows executable |
| **Inno Setup** | Packaging the Windows installer |

**Platform:** Windows is the current target. The FFmpeg bootstrap downloads Windows `.exe` binaries; other operating systems are not supported by the current bootstrap.

---

# Quick Start 👾

## Requirements

- **Windows 10/11**.
- Internet access for YouTube and for downloading FFmpeg on first use.
- Free disk space for the temporary FFmpeg archive, extracted binaries, and downloaded music.
- **Python 3.12+ is required only when running from source.** It is **not required** for the released installer or standalone `music.exe`.

## Recommended: Windows Installer 📦

1. Open the [latest release](https://github.com/AmbreKitsune/DownloaderMusicYouTube/releases/latest).
2. Download **`DownloaderMusicYouTube-Setup.exe`** and run it.
3. Select an installation directory (the default is `%LOCALAPPDATA%\Programs\DownloaderMusicYouTube`). Administrator privileges are not required for the standard per-user installation.
4. After installation, **open a new terminal** so the updated user `PATH` is recognized.
5. Download an audio track:

   ```powershell
   music.exe --download "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

The setup installs `music.exe`; on first launch, the application installs its own FFmpeg binaries if needed. Finished MP3 files are stored in the installed application's `downloads/` folder, which opens automatically after a successful download.

## Alternative: Standalone EXE 💻

1. Download **`music.exe`** from the [latest release](https://github.com/AmbreKitsune/DownloaderMusicYouTube/releases/latest).
2. Place it in a **writable folder** of your choice (for example, `D:\MusicDownloader`).
3. Open a terminal in that folder and run:

   ```powershell
   .\music.exe --download "https://music.youtube.com/watch?v=VIDEO_ID"
   ```

This version needs no Python. It does **not** automatically add itself to `PATH`; invoke it by path or use the installer for global access. The portable executable creates `ffmpeg/` and `downloads/` beside itself.

## Alternative: Run from Source 🐍

1. Clone the project:

   ```powershell
   git clone https://github.com/AmbreKitsune/DownloaderMusicYouTube.git
   cd DownloaderMusicYouTube
   ```

2. Create a virtual environment and install the repository's dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Run the CLI from the repository root:

   ```powershell
   .\.venv\Scripts\python.exe src/main.py --download "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

Generated FFmpeg files and downloaded MP3s are stored in `src/ffmpeg/` and `src/downloads/` in source mode.

## First Run

- If FFmpeg is missing, the application downloads and extracts the necessary Windows binaries automatically.
- The first launch may take a few minutes; subsequent launches reuse the existing files.
- The program opens the downloads folder after successful conversion.

---

# CLI Usage 💻

**Show help (installed version):**

```powershell
music.exe --help
```

**Download from YouTube:**

```powershell
music.exe --download "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download from YouTube Music:**

```powershell
music.exe --download "https://music.youtube.com/watch?v=VIDEO_ID&si=SHARE_TOKEN"
```

**Run from source (repository root):**

```powershell
python src/main.py --download "https://www.youtube.com/watch?v=VIDEO_ID"
```

Always **quote the complete URL**, particularly when it includes `&` or other shell-special characters. The YouTube Music `si` sharing parameter does not need manual removal when the entire URL is quoted.

Without arguments, the program suggests `--help`. Passing `--download` without a URL produces Typer's standard argument error. To use `music.exe` from any directory, install it with **Setup** and open a new terminal afterward; the standalone EXE does not register itself in `PATH`.

---

# Files and Paths 📁

## Installed / Standalone App

| Location (relative to `music.exe`) | Purpose |
| --- | --- |
| `music.exe` | Standalone Windows CLI executable |
| `ffmpeg/ffmpeg.exe` | Locally installed audio converter |
| `ffmpeg/ffprobe.exe` | Locally installed media probe |
| `downloads/` | Downloaded MP3 files; automatically opened after success |
| `ffmpeg-release-essentials.zip` | Temporary archive, removed after installation attempts |
| `temp/` | Temporary extraction folder, removed after installation attempts |

The installer places these files in a directory that you choose (by default `%LOCALAPPDATA%\Programs\DownloaderMusicYouTube`). They are **not saved under the terminal's current working directory**. Choose a writable directory for a standalone `music.exe`.

## Source Repository

| Path | Purpose |
| --- | --- |
| `src/main.py` | CLI entry point and argument handling |
| `src/downloader.py` | yt-dlp configuration, MP3 output, and folder opening |
| `src/ffmpeg.py` | Local FFmpeg preparation and temporary-file cleanup |
| `src/ffmpeg/` | Generated FFmpeg binaries when running Python directly |
| `src/downloads/` | Generated MP3 files when running Python directly |
| `assets/icon.ico` | Application icon |
| `requirements.txt` | Python dependencies |

`.gitignore` excludes runtime downloads, locally installed FFmpeg, temporary files, virtual environments, and build artifacts. It does not retroactively untrack files already committed to Git.

---

# Errors and Troubleshooting ❌

**`'music.exe' is not recognized`**  
Use **`DownloaderMusicYouTube-Setup.exe`** to install the program, and then open a **new terminal**. If you downloaded the standalone EXE, use its full path or `./music.exe` (PowerShell: `.\music.exe`) from its folder.

**`No module named 'typer'`, `'rich'`, `'requests'`, or `'yt_dlp'`**  
This concerns **source mode only**. Install dependencies using `python -m pip install -r requirements.txt` in the environment you use to run `src/main.py`.

**`FFmpeg not found. Installing automatically...`**  
Expected on first use. Wait for the archive to download and extract.

**`Failed to download FFmpeg`**  
Check your network connection and the FFmpeg source at [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/), then retry.

**`FFmpeg installation failed`**  
Check free disk space and whether the application folder is writable. If installation was interrupted, inspect or remove incomplete `ffmpeg/` files before retrying.

**`Download failed: ...`**  
The link might be unavailable, restricted, or unsupported, or YouTube may have changed its media delivery. Check the link. If running from source, updating `yt-dlp` may help.

**`No supported JavaScript runtime` warning**  
Some `yt-dlp` versions can show this warning. Downloads may still work, but available audio formats may be limited. It does not mean FFmpeg installation failed.

**`Option '--download' requires an argument`**  
Pass a URL, for example: `music.exe --download "https://www.youtube.com/watch?v=VIDEO_ID"`.

**The MP3 is not where expected**  
Check `downloads/` beside **`music.exe`** (installed or portable) or `src/downloads/` (Python source mode). The folder should also open after a successful download.

---

# Q&A ❓

**Q: Is Python required?**  
**A:** No, not for the released installer or `music.exe`. Python is only required to run the source code.

**Q: Can I run `music.exe` from any directory?**  
**A:** Yes, after installing with Setup and starting a new terminal. The installer registers the installation directory in the user `PATH`.

**Q: Does FFmpeg get installed system-wide?**  
**A:** No. The application keeps `ffmpeg.exe` and `ffprobe.exe` beside itself inside `ffmpeg/`.

**Q: Where is my music?**  
**A:** In `downloads/` beside `music.exe`. When running source code, it is in `src/downloads/`.

**Q: Does the application open the output folder automatically?**  
**A:** Yes, after a successful download and MP3 conversion on Windows.

**Q: Does it support YouTube Music URLs?**  
**A:** Direct track links have been tested. Quote the whole URL when it contains `&`.

**Q: Is the result lossless audio?**  
**A:** No. It converts the available source audio into MP3 using the requested 192 kbps encoding quality; conversion cannot restore information missing from the original source.

**Q: Is there a graphical interface?**  
**A:** No. The program is designed as a Windows console application.

**Q: What happens when I uninstall?**  
**A:** The installer is designed to remove the application and its `PATH` entry while preserving the `downloads/` directory. Back up important music before manually deleting the installation folder.

---

# Limitations 📢

- The current implementation and installer are **Windows-specific**.
- FFmpeg installation requires access to a third-party download source on first use.
- Changes to YouTube or YouTube Music may affect extraction and download availability.
- Region restrictions, authentication requirements, and other platform limitations may prevent some downloads.
- Playlist support, batch processing, and non-MP3 output have not been validated for this release.
- MP3 filenames are derived from media titles; duplicate or unusual titles can require special handling.
- The program needs write access beside `music.exe` to store FFmpeg and music. Avoid protected directories when using the standalone version.
- A `yt-dlp` warning about a missing JavaScript runtime can affect available formats even when a download completes.
- Download only material you are authorized to save, in accordance with applicable platform terms and copyright rules.

---

# Links 🙀

- **Repository:** [DownloaderMusicYouTube](https://github.com/AmbreKitsune/DownloaderMusicYouTube)
- **Latest release (installer + EXE):** [GitHub Releases](https://github.com/AmbreKitsune/DownloaderMusicYouTube/releases/latest)
- **FFmpeg:** [ffmpeg.org](https://ffmpeg.org/)
- **FFmpeg Windows builds:** [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- **yt-dlp:** [GitHub](https://github.com/yt-dlp/yt-dlp)
- **Website:** [ambrekitsune.dev](https://ambrekitsune.dev/)
- **Telegram:** [@NightAmbreKitsune](https://t.me/NightAmbreKitsune)
- **Discord:** [Join server](https://discord.gg/U59cgYUNwv)

License information is available in the repository's `LICENSE` file. FFmpeg and other third-party dependencies retain their own licenses.
