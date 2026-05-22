"""Analisi video tramite estrazione frame chiave + Claude vision."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import anthropic

from .vision import analyze_image

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".mts", ".3gp"}
_VISION_MODEL = "claude-haiku-4-5"


def _ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def _get_video_metadata(video_path: Path) -> dict:
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_streams", "-show_format",
                str(video_path),
            ],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return {}


def _extract_frames(video_path: Path, num_frames: int, output_dir: Path) -> list[Path]:
    """Estrae frame chiave con scene detection, fallback a spaziatura uniforme."""
    pattern = str(output_dir / "frame_%03d.jpg")

    # Tentativo 1: scene detection — sceglie i frame più visivamente interessanti
    subprocess.run(
        [
            "ffmpeg", "-i", str(video_path),
            "-vf", "select=gt(scene\\,0.25),scale=1280:-1",
            "-frames:v", str(num_frames),
            "-vsync", "0", "-q:v", "3",
            pattern, "-y",
        ],
        capture_output=True, timeout=90,
    )
    frames = sorted(output_dir.glob("frame_*.jpg"))

    # Tentativo 2: un frame ogni 3 secondi (fallback se scene detection produce pochi frame)
    if len(frames) < max(1, num_frames // 2):
        for f in frames:
            f.unlink()
        subprocess.run(
            [
                "ffmpeg", "-i", str(video_path),
                "-vf", "fps=1/3,scale=1280:-1",
                "-frames:v", str(num_frames),
                "-q:v", "3",
                pattern, "-y",
            ],
            capture_output=True, timeout=90,
        )
        frames = sorted(output_dir.glob("frame_*.jpg"))

    return frames


def analyze_video(
    path: str,
    question: str = "",
    num_frames: int = 6,
    client: anthropic.Anthropic | None = None,
) -> str:
    """
    Analizza un video estraendo frame chiave con ffmpeg e analizzandoli con Claude vision.

    Produce: metadati tecnici, analisi frame-by-frame, sintesi con
    raccomandazioni di montaggio, piattaforme consigliate e voto /10.
    """
    if client is None:
        return "Errore: client Anthropic non disponibile."
    if not _ffmpeg_available():
        return "Errore: ffmpeg non installato. Installa con: apt install ffmpeg"

    video_path = Path(path)
    if not video_path.exists():
        return f"Errore: video non trovato: {path}"
    if video_path.suffix.lower() not in VIDEO_EXTENSIONS:
        return f"Formato non supportato: {video_path.suffix}. Supportati: {', '.join(VIDEO_EXTENSIONS)}"

    # Metadati
    meta = _get_video_metadata(video_path)
    video_stream = next(
        (s for s in meta.get("streams", []) if s.get("codec_type") == "video"), {}
    )
    fmt = meta.get("format", {})
    audio_stream = next(
        (s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), {}
    )

    duration_s = float(fmt.get("duration", 0))
    width = video_stream.get("width", "?")
    height = video_stream.get("height", "?")
    fps_raw = video_stream.get("r_frame_rate", "?")
    codec = video_stream.get("codec_name", "?")
    size_mb = int(fmt.get("size", 0)) / (1024 * 1024)
    audio_codec = audio_stream.get("codec_name", "nessuno")

    # Aspect ratio → piattaforma probabile
    if width != "?" and height != "?":
        ratio = width / height if height else 0
        orientation = "verticale 9:16 (TikTok/Reels)" if ratio < 0.7 else \
                      "orizzontale 16:9 (YouTube)" if ratio > 1.4 else \
                      "quadrato 1:1 (Instagram feed)"
    else:
        orientation = "?"

    metadata_str = (
        f"File: {video_path.name}\n"
        f"  Risoluzione: {width}×{height} ({orientation})\n"
        f"  Durata: {duration_s:.1f}s  |  FPS: {fps_raw}  |  "
        f"Codec video: {codec}  |  Audio: {audio_codec}\n"
        f"  Dimensione: {size_mb:.1f} MB"
    )

    # Estrazione frame
    with tempfile.TemporaryDirectory() as tmp_dir:
        frames = _extract_frames(video_path, num_frames, Path(tmp_dir))

        if not frames:
            return f"{metadata_str}\n\nErrore: impossibile estrarre frame dal video."

        # Analisi frame-by-frame
        frame_analyses: list[str] = []
        for i, frame in enumerate(frames, 1):
            timestamp_s = (i / len(frames)) * duration_s if duration_s else 0
            frame_prompt = question or (
                f"Frame {i}/{len(frames)} di un video di viaggio (circa {timestamp_s:.0f}s). "
                "Descrivi brevemente in italiano: "
                "soggetto e scena, qualità tecnica (esposizione, messa a fuoco, stabilità), "
                "composizione, colori dominanti, potenziale come clip per social."
            )
            analysis = analyze_image(str(frame), question=frame_prompt, client=client)
            frame_analyses.append(f"[Frame {i} @ ~{timestamp_s:.0f}s]\n{analysis}")

        # Sintesi finale basata su tutti i frame
        frames_summary = "\n\n".join(frame_analyses)
        synthesis_prompt = (
            "Sei un senior video editor di un'agenzia travel. "
            "Hai analizzato i seguenti frame di un video di viaggio:\n\n"
            f"{frames_summary}\n\n"
            "Fornisci una sintesi professionale in italiano con:\n"
            "1. Valutazione qualità complessiva del girato\n"
            "2. Piattaforme ideali (TikTok, Reels, YouTube Short, YouTube long-form) e perché\n"
            "3. Suggerimenti di montaggio: ritmo, punti di taglio, struttura narrativa\n"
            "4. Color grading consigliato\n"
            "5. Idea per l'hook nei primi 3 secondi\n"
            "6. Musica/audio consigliato (genere/mood)\n"
            "7. Voto /10 e se è adatto alla pubblicazione così com'è"
        )
        synthesis = client.messages.create(
            model=_VISION_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": synthesis_prompt}],
        ).content[0].text

    sep = "=" * 55
    return (
        f"{metadata_str}\n"
        f"Frame analizzati: {len(frames)}\n"
        f"{sep}\n\n"
        f"ANALISI FRAME\n{sep}\n"
        + "\n\n".join(frame_analyses)
        + f"\n\n{sep}\n"
        f"SINTESI E RACCOMANDAZIONI DI MONTAGGIO\n{sep}\n"
        + synthesis
    )


def analyze_trip_videos(
    trip_id: str,
    subfolder: str = "01_raw/video",
    question: str = "",
    num_frames: int = 4,
    client: anthropic.Anthropic | None = None,
) -> str:
    """Analizza tutti i video in una cartella del viaggio."""
    if client is None:
        return "Errore: client Anthropic non disponibile."

    folder = Path("content/trips") / trip_id / subfolder
    if not folder.exists():
        return f"Cartella non trovata: {folder}"

    videos = sorted(f for f in folder.iterdir() if f.suffix.lower() in VIDEO_EXTENSIONS)
    if not videos:
        return f"Nessun video trovato in {folder}"

    results = [f"Analisi {len(videos)} video da {subfolder}/\n{'='*55}"]
    for vid in videos:
        analysis = analyze_video(
            str(vid), question=question, num_frames=num_frames, client=client
        )
        results.append(f"\n[{vid.name}]\n{analysis}")

    return "\n".join(results)
