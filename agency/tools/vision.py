"""Analisi immagini tramite Claude vision."""
from __future__ import annotations

import base64
from pathlib import Path

import anthropic

MEDIA_TYPES: dict[str, str] = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}

# Modello leggero e veloce per vision
_VISION_MODEL = "claude-haiku-4-5"

_DEFAULT_PROMPT = (
    "Analizza questa immagine per un'agenzia di content marketing travel. "
    "Valuta:\n"
    "1. Qualità tecnica: esposizione, messa a fuoco, composizione\n"
    "2. Potenziale social: appeal per Instagram, TikTok, YouTube\n"
    "3. Mood e palette cromatica dominante\n"
    "4. Elementi di viaggio/destinazione identificabili\n"
    "5. Punti di forza e suggerimenti specifici di editing\n"
    "6. Voto complessivo /10 e se è adatta alla pubblicazione"
)


def analyze_image(path: str, question: str = "", client: anthropic.Anthropic | None = None) -> str:
    """Analizza un'immagine con Claude vision."""
    if client is None:
        return "Errore: client Anthropic non disponibile per vision."

    image_path = Path(path)
    if not image_path.exists():
        return f"Errore: immagine non trovata: {path}"

    media_type = MEDIA_TYPES.get(image_path.suffix.lower(), "image/jpeg")
    image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")

    prompt = question or _DEFAULT_PROMPT

    response = client.messages.create(
        model=_VISION_MODEL,
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return response.content[0].text


def analyze_trip_photos(
    trip_id: str,
    subfolder: str = "01_raw/photo",
    question: str = "",
    client: anthropic.Anthropic | None = None,
) -> str:
    """Analizza tutte le immagini in una cartella del viaggio."""
    if client is None:
        return "Errore: client Anthropic non disponibile per vision."

    folder = Path("content/trips") / trip_id / subfolder
    if not folder.exists():
        return f"Cartella non trovata: {folder}"

    extensions = set(MEDIA_TYPES.keys())
    images = sorted(f for f in folder.iterdir() if f.suffix.lower() in extensions)

    if not images:
        return f"Nessuna immagine trovata in {folder}"

    results = [f"Analisi {len(images)} immagini da {subfolder}/\n{'='*50}"]
    for img in images:
        analysis = analyze_image(str(img), question=question, client=client)
        results.append(f"\n[{img.name}]\n{analysis}")

    return "\n".join(results)
