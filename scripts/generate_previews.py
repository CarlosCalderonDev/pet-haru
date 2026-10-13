#!/usr/bin/env python3
"""Generate frames, GIF previews, and QA sheets using only Pillow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from pet_config import ROOT, STATES, sprite_settings

FRAMES_ROOT = ROOT / "assets" / "frames"
PREVIEWS = ROOT / "previews"
BG_A = (246, 246, 246, 255)
BG_B = (224, 224, 224, 255)


def save_optimized_sheet(image: Image.Image, path: Path) -> None:
    indexed = image.convert("RGB").quantize(
        colors=256,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    indexed.save(path, optimize=True)


def checkerboard(size: tuple[int, int], step: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, BG_A)
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], step):
        for x in range(0, size[0], step):
            if (x // step + y // step) % 2:
                draw.rectangle((x, y, x + step - 1, y + step - 1), fill=BG_B)
    return image


def extract_frames(atlas: Image.Image, cell_w: int, cell_h: int, counts: list[int]) -> dict[str, list[Image.Image]]:
    result: dict[str, list[Image.Image]] = {}
    for row, (state, count) in enumerate(zip(STATES, counts)):
        output = FRAMES_ROOT / state
        output.mkdir(parents=True, exist_ok=True)
        frames = []
        for col in range(count):
            box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
            frame = atlas.crop(box)
            frame.save(output / f"{col:02d}.png", optimize=True)
            frames.append(frame)
        result[state] = frames
    return result


def save_gifs(frames_by_state: dict[str, list[Image.Image]]) -> None:
    output = PREVIEWS / "animations"
    output.mkdir(parents=True, exist_ok=True)
    durations = {"idle": 180, "failed": 170, "waiting": 190, "review": 180}
    for state, frames in frames_by_state.items():
        if state.startswith("look-"):
            continue
        canvas_frames = []
        for frame in frames:
            canvas = checkerboard(frame.size)
            canvas.alpha_composite(frame)
            canvas_frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE))
        canvas_frames[0].save(
            output / f"{state}.gif",
            save_all=True,
            append_images=canvas_frames[1:],
            duration=durations.get(state, 110),
            loop=0,
            disposal=2,
            optimize=True,
        )


def save_contact_sheet(atlas: Image.Image, cell_w: int, cell_h: int, counts: list[int]) -> None:
    columns = atlas.width // cell_w
    header = 28
    sheet = Image.new("RGBA", (atlas.width, len(STATES) * (cell_h + header)), (20, 20, 24, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for row, (state, count) in enumerate(zip(STATES, counts)):
        top = row * (cell_h + header)
        draw.text((8, top + 8), f"row {row}: {state}", fill="white", font=font)
        draw.text((atlas.width - 70, top + 8), f"{count} frames", fill="white", font=font)
        for col in range(columns):
            panel = checkerboard((cell_w, cell_h))
            source_box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
            panel.alpha_composite(atlas.crop(source_box))
            sheet.alpha_composite(panel, (col * cell_w, top + header))
            color = (45, 190, 110, 255) if col < count else (220, 70, 70, 255)
            draw.rectangle((col * cell_w, top + header, (col + 1) * cell_w - 1, top + header + cell_h - 1), outline=color, width=2)
            draw.text((col * cell_w + 5, top + header + 5), str(col), fill=(20, 20, 20), font=font)
    save_optimized_sheet(sheet, PREVIEWS / "contact-sheet.png")


def save_direction_sheet(frames_by_state: dict[str, list[Image.Image]]) -> None:
    frames = frames_by_state["look-a"] + frames_by_state["look-b"]
    labels = [f"{index * 22.5:05.1f}°" for index in range(16)]
    cell_w, cell_h = frames[0].size
    label_h = 24
    sheet = Image.new("RGBA", (8 * cell_w, 2 * (cell_h + label_h)), (245, 245, 247, 255))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, (frame, label) in enumerate(zip(frames, labels)):
        x = (index % 8) * cell_w
        y = (index // 8) * (cell_h + label_h)
        panel = checkerboard((cell_w, cell_h))
        panel.alpha_composite(frame)
        sheet.alpha_composite(panel, (x, y + label_h))
        draw.text((x + 5, y + 7), label, fill=(30, 30, 35), font=font)
    save_optimized_sheet(sheet, PREVIEWS / "look-directions.png")


def main() -> None:
    atlas_path, _, _, cell_w, cell_h, counts = sprite_settings()
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
        frames = extract_frames(atlas, cell_w, cell_h, counts)
        save_gifs(frames)
        save_contact_sheet(atlas, cell_w, cell_h, counts)
        save_direction_sheet(frames)
    print(f"Generated frames and previews in {PREVIEWS}")


if __name__ == "__main__":
    main()
