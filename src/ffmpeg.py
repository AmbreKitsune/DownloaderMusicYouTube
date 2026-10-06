import sys
import shutil
import zipfile
import requests
from pathlib import Path
from rich.console import Console

console = Console()

ROOT_PATH = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else Path(__file__).resolve().parent
)
URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

ffmpeg_folder = ROOT_PATH / "ffmpeg"
ffmpeg_exe = ffmpeg_folder / "ffmpeg.exe"
ffprobe_exe = ffmpeg_folder / "ffprobe.exe"
ffmpeg_zip = ROOT_PATH / "ffmpeg-release-essentials.zip"
temp_folder = ROOT_PATH / "temp"


def check_ffmpeg():
    if not ffmpeg_exe.is_file() or not ffprobe_exe.is_file():
        console.print("[bold yellow]FFmpeg not found. Installing automatically. This may take a few minutes...[/]")
        download_ffmpeg()

    return ffmpeg_exe


def download_ffmpeg():
    try:
        try:
            response = requests.get(URL, timeout=(10, 60), stream=True)
            response.raise_for_status()

            with open(ffmpeg_zip, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except requests.exceptions.RequestException:
            console.print("[bold red]Failed to download FFmpeg. Check your connection and try again.[/]")
            raise SystemExit(1)

        try:
            with zipfile.ZipFile(ffmpeg_zip, mode="r") as zf:
                zf.extractall(temp_folder)

            ffmpeg_folder.mkdir(parents=True, exist_ok=True)
            temp_local = list(temp_folder.iterdir())[0]

            shutil.move(temp_local / "bin" / "ffmpeg.exe", ffmpeg_exe)
            shutil.move(temp_local / "bin" / "ffprobe.exe", ffprobe_exe)
        except (IndexError, zipfile.BadZipFile, OSError):
            console.print("[bold red]FFmpeg installation failed. Please try again.[/]")
            raise SystemExit(1)
    finally:
        try:
            ffmpeg_zip.unlink(missing_ok=True)
        except OSError:
            pass

        shutil.rmtree(temp_folder, ignore_errors=True)
