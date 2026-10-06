import typer
from typing import Annotated
from rich.console import Console

from downloader import download_audio
from ffmpeg import check_ffmpeg


console = Console()
app = typer.Typer()


@app.command()
def main(
    download: Annotated[
        str | None,
        typer.Option(
            "--download",
            metavar="<URL>",
            help="Download audio from YouTube or YouTube Music as MP3."
        )
    ] = None):
    
    if download is None:
        console.print("[bold red]Run with --help to see available options.[/]")
        raise typer.Exit()

    ffmpeg = check_ffmpeg()
    
    console.print(f"[bold green]URL accepted. Starting download...[/]")
    download_audio(url=download, ffmpeg=ffmpeg)

if __name__ == "__main__":
    app()
