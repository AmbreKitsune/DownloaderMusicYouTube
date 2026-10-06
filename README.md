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

The current version runs from Python. A standalone `music.exe`, a Windows installer, a global `music` command, and automatic opening of the output folder are **planned, not implemented**.

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

**Current scope:** download a URL to MP3. Playlist handling, batch downloading, and other formats are not documented as supported features yet.

---

# How It Works ⚙️

1. The CLI reads the URL passed to `--download`.
2. The program checks for `ffmpeg.exe` and `ffprobe.exe` in the project's `ffmpeg/` folder.
3. If either file is missing, the program downloads the FFmpeg Essentials ZIP from **Gyan.dev**, extracts the two binaries, and removes its temporary files.
4. `yt-dlp` retrieves the audio stream and hands it to the local FFmpeg installation for MP3 conversion.
5. The final MP3 is saved in `downloads/`, relative to the **directory where the command was launched**.

The initial FFmpeg download requires an internet connection and can take a few minutes. FFmpeg is not installed system-wide.

---

# Tech Stack 📂

| Component | Purpose |
| --- | --- |
| **Python 3.12+** | Application runtime |
| **Typer** | CLI options and help |
| **Rich** | Console messages |
| **yt-dlp** | Audio extraction and download |
| **FFmpeg / ffprobe** | Audio conversion and media probing |
| **Requests** | Downloading the FFmpeg archive |
| **pathlib / zipfile / shutil** | Paths, extraction, and temporary-file cleanup |

**Platform:** Windows is the current target. The FFmpeg bootstrap downloads Windows `.exe` binaries; other operating systems are not supported by the current bootstrap.

---

# Quick Start 👾

## Requirements

- Windows 10/11.
- **Python 3.12 or newer** available from the terminal.
- An internet connection for YouTube access and first-time FFmpeg installation.
- Git (optional, for cloning the repository).
- Enough free disk space for the temporary FFmpeg archive, extracted files, and downloaded audio.

You **do not** need to install FFmpeg manually or add it to `PATH`.

## Installation

1. Download the project or clone it:

   ```powershell
   git clone https://github.com/AmbreKitsune/DownloaderMusicYouTube.git
   cd DownloaderMusicYouTube
   ```

2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Install the Python dependencies:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install yt-dlp typer rich requests
   ```

   **Note:** the repository's older `requirements.txt` only lists `yt_dlp`. Update it to include `typer`, `rich`, and `requests` before relying on `pip install -r requirements.txt`.

4. Start a download:

   ```powershell
   .\.venv\Scripts\python.exe main.py --download "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

5. Find the result in `downloads/` in the directory where you ran the command.

## First Run

- If FFmpeg is missing, the application downloads a Windows Essentials archive and prepares `ffmpeg.exe` and `ffprobe.exe`.
- The first run may take longer than later runs.
- On the next run, existing binaries are reused.

---

# CLI Usage 💻

**Show help:**

```powershell
python main.py --help
```

**Download from YouTube:**

```powershell
python main.py --download "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download from YouTube Music:**

```powershell
python main.py --download "https://music.youtube.com/watch?v=VIDEO_ID&si=SHARE_TOKEN"
```

Keep URLs **inside quotation marks**, especially when they contain `&` or other characters with a special meaning in the shell. The `si` parameter is a share-link parameter; it does not need to be removed if the URL is quoted correctly.

Running `python main.py` without an option prints a hint to use `--help`. Using `--download` without a value produces Typer's argument error.

The command above is **not global**: run it from the project directory for now. `music.exe --download <URL>` is the planned installed experience.

---

# Files and Paths 📁

| Path | Purpose |
| --- | --- |
| `main.py` | CLI entry point and argument handling |
| `downloader.py` | yt-dlp options and audio downloading |
| `ffmpeg.py` | FFmpeg detection, download, extraction, and cleanup |
| `ffmpeg/ffmpeg.exe` | Locally installed converter (generated) |
| `ffmpeg/ffprobe.exe` | Locally installed probing tool (generated) |
| `ffmpeg-release-essentials.zip` | Temporary FFmpeg archive (removed after normal setup) |
| `temp/` | Temporary extraction directory (removed after normal setup) |
| `downloads/` | Downloaded MP3 files (generated in the working directory) |
| `assets/icon.ico` | Application icon for future packaging |

**Important:** `ffmpeg/` is located next to `ffmpeg.py`, but `downloads/` uses a **relative path**. If you launch the script from a different working directory, the MP3 will be written to that directory's `downloads/` folder. A fixed user-level music directory is planned for a later release.

The `.gitignore` excludes generated FFmpeg files, temporary files, build output, virtual environments, and downloaded music. It does not retroactively untrack binaries already committed to Git.

---

# Errors and Troubleshooting ❌

**`No module named 'typer'`, `'rich'`, `'requests'`, or `'yt_dlp'`**  
Install all four packages into the Python environment used to launch the script. If you created `.venv`, use its Python executable.

**`FFmpeg not found. Installing automatically...`**  
This is normal on first run. Wait for the archive to download and extract.

**`Failed to download FFmpeg`**  
Check the internet connection and availability of the FFmpeg source, then retry. The download depends on [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/).

**`FFmpeg installation failed`**  
Check available disk space and write permissions. If necessary, close the program and inspect temporary `ffmpeg/` or `temp/` files before retrying.

**`Download failed: ...`**  
The link may be unavailable, restricted, or unsupported, or YouTube may have changed how it serves media. Check the URL and update `yt-dlp` if necessary.

**`No supported JavaScript runtime` warning**  
This warning may appear in some versions of `yt-dlp`. A download may still succeed, but available formats can be limited. It is not the same as an FFmpeg installation failure.

**`Option '--download' requires an argument`**  
Add a URL after `--download`. Example: `python main.py --download "https://www.youtube.com/watch?v=VIDEO_ID"`.

**The MP3 is not where expected**  
Check `downloads/` relative to the terminal's current working directory, not necessarily next to `main.py`.

---

# Q&A ❓

**Q: Does the application install FFmpeg globally?**  
**A:** No. It downloads local copies of `ffmpeg.exe` and `ffprobe.exe` under the project directory.

**Q: Is Python required?**  
**A:** Yes, for the current source-code version. A standalone executable and installer are planned.

**Q: Can I run `music.exe` from any folder?**  
**A:** Not yet. A setup process and a command available through `PATH` are planned.

**Q: Does it support YouTube Music links?**  
**A:** Direct track URLs have been used successfully. Keep the whole link quoted when it contains `&`.

**Q: Does the tool provide original lossless audio?**  
**A:** No. It converts the available source stream to MP3, requesting 192 kbps output. Converting cannot restore detail missing from the original stream.

**Q: Does the application open the music folder automatically?**  
**A:** Not in the current version. Open `downloads/` manually.

**Q: Does it have a graphical user interface?**  
**A:** No. This project is designed for the terminal.

---

# Limitations 📢

- The current FFmpeg downloader is **Windows-specific**.
- FFmpeg setup depends on the availability of a third-party download source.
- YouTube or YouTube Music changes can break extraction even when the program itself has not changed.
- Some videos may be inaccessible because of region, age, login, or other service restrictions.
- Playlist, batch, and non-MP3 output workflows have not been validated as part of this release.
- The filename is based on the media title; identical or problematic titles may require additional handling.
- The tool does not currently provide a global command, dedicated installer, fixed download location, or automatic folder opening.
- Download only content you are authorized to save, and follow the applicable platform terms and copyright rules.

---

# Links 🙀

- **Repository:** [DownloaderMusicYouTube](https://github.com/AmbreKitsune/DownloaderMusicYouTube)
- **FFmpeg:** [ffmpeg.org](https://ffmpeg.org/)
- **FFmpeg Windows builds:** [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- **yt-dlp:** [GitHub](https://github.com/yt-dlp/yt-dlp)
- **Website:** [ambrekitsune.dev](https://ambrekitsune.dev/)
- **Telegram:** [@NightAmbreKitsune](https://t.me/NightAmbreKitsune)
- **Discord:** [Join server](https://discord.gg/U59cgYUNwv)

License information is available in the repository's `LICENSE` file. FFmpeg and other third-party dependencies retain their own licenses.
