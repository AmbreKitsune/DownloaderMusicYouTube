import os
import yt_dlp
from rich.console import Console


console = Console()


def download_audio(*, url, ffmpeg, output_path="downloads"):
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'ffmpeg_location': str(ffmpeg),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            console.print(f"[bold green]Download complete: {info['title']}.mp3[/]")
        os.startfile(os.path.abspath(output_path))
    except Exception as error:
        console.print(f"[bold red]Download failed: {error}[/]")
        raise SystemExit(1)
