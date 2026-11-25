# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow==11.3.0"]
# ///
"""Redraw the recorded decimal case study. Does not run OCR."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/decimal"
INK, MUTED, DONOR = "#171717", "#666666", "#ce5100"


def frame(original: Image.Image, donor: Image.Image, rows: list[int], field: str) -> Image.Image:
    """Draw source zooms, a schematic feature bank, and a recorded field."""
    image = Image.new("RGB", (960, 600), "white")
    draw = ImageDraw.Draw(image)

    def text(x: int, y: int, value: str, size: int = 20, color: str = INK) -> None:
        draw.text((x, y), value, fill=color, font=ImageFont.load_default(size=size))

    text(36, 24, "One-at-a-time checks miss the joint change.", 32)
    text(36, 70, "GLM-OCR / recorded experiment / no tokens deleted", 18, MUTED)
    for source, x, label in ((original, 36, "Input zoom (unchanged)"), (donor, 504, "Donor zoom (8 pixels erased)")):
        text(x, 112, label, 19)
        zoom = source.crop((98, 0, 150, 24)).resize((312, 144), Image.Resampling.NEAREST)
        image.paste(zoom, (x + 42, 146))
    selected = " + ".join(map(str, rows)) if rows else "none"
    text(36, 312, f"Swap donor features: {selected}", 25)
    text(36, 350, "Final visual features (schematic; zero-based indices)", 16, MUTED)
    for index in range(38):
        x = 43 + index * 23
        draw.rectangle((x, 382, x + 18, 405), fill=DONOR if index in rows else "#d7d7d7")
        if index in (0, 4, 5, 37):
            text(x, 409, str(index), 14, MUTED)
    text(670, 409, "all 38 features remain", 16, MUTED)
    text(36, 465, "OCR:", 22)
    text(130, 437, field, 66, DONOR if rows == [4, 5] else INK)
    text(36, 534, "One crop; two complete greedy outputs per state. Field shown above.", 17, MUTED)
    text(36, 565, "Modified visualization of DocLayNet data / CDLA-Permissive-1.0", 14, MUTED)
    return image


def main() -> None:
    """Verify source bindings and render four recorded states with a shared palette."""
    evidence = json.loads((DATA / "results.json").read_text())
    for name, digest in evidence["source"]["files_sha256"].items():
        assert hashlib.sha256((DATA / name).read_bytes()).hexdigest() == digest, name
    original, donor = (Image.open(DATA / name).convert("RGB") for name in ("original.png", "dot-erased.png"))
    frames = []
    for condition in evidence["method"]["condition_order"]:
        records = [r for r in evidence["records"] if r["condition"] == condition]
        assert len(records) == 2 and records[0]["generated_ids"] == records[1]["generated_ids"]
        assert all(not r["hit_token_limit"] and r["generated_ids"][-1] == r["eos_id"] for r in records)
        record = records[0]
        field = record["text"].split("We calculate ", 1)[1].split(" VaR", 1)[0]
        frames.append(frame(original, donor, record["donor_rows"], field))
    sheet = Image.new("RGB", (960, 600 * len(frames)))
    for index, image in enumerate(frames):
        sheet.paste(image, (0, index * 600))
    palette = sheet.quantize(colors=128)
    frames = [image.quantize(palette=palette, dither=Image.Dither.NONE) for image in frames]
    output = ROOT / "assets/decimal.gif"
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=[1800, 1800, 1800, 2600],
        loop=0,
        disposal=2,
        optimize=False,
        comment=(
            "Modified visualization of DocLayNet 1.0; source crop and an eight-pixel decimal erasure. "
            "Recorded feature swaps, not token deletion. Data license: CDLA-Permissive-1.0 "
            "(https://cdla.dev/permissive-1-0/). See decimal/results.json for provenance and outputs."
        ).encode("ascii"),
    )
    print(f"{output.relative_to(ROOT)}: {len(frames)} frames, {output.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
