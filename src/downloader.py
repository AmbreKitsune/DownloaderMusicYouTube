import os
from pathlib import Path

import yt_dlp
from rich.console import Console

from ffmpeg import ROOT_PATH

console = Console()


def download_audio(*, url, ffmpeg, output_path=None):
    output_path = Path(output_path) if output_path is not None else ROOT_PATH / "downloads"
    output_path.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "ffmpeg_location": str(ffmpeg),
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": str(output_path / "%(title)s.%(ext)s"),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            console.print(f"[bold green]Download complete: {info['title']}.mp3[/]")
        os.startfile(str(output_path))
    except Exception as error:
        console.print(f"[bold red]Download failed: {error}[/]")
        raise SystemExit(1)
