from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent

LOG_TO_IMAGE = [
    (ROOT / "fail.log", ROOT / "fail.png", "FAIL"),
    (ROOT / "patch.log", ROOT / "patch.png", "PATCH"),
    (ROOT / "pass.log", ROOT / "pass.png", "PASS"),
]


def load_font(size):
    candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/lucon.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def line_wrap_for_width(text, font, max_width):
    wrapped_lines = []
    for line in text.splitlines():
        if not line:
            wrapped_lines.append("")
            continue
        probe = ""
        for char in line:
            attempt = probe + char
            bbox = font.getbbox(attempt)
            width = bbox[2] - bbox[0]
            if width > max_width and probe:
                wrapped_lines.append(probe)
                probe = char
            else:
                probe = attempt
        wrapped_lines.append(probe)
    return wrapped_lines


def render_log_to_image(log_path, out_path, stage_title):
    width, height = 1366, 768
    image = Image.new("RGB", (width, height), color=(15, 18, 24))
    draw = ImageDraw.Draw(image)
    title_font = load_font(36)
    body_font = load_font(20)

    draw.rectangle((0, 0, width, 78), fill=(22, 28, 38))
    draw.text((30, 20), f"{stage_title} | pytest workflow", font=title_font, fill=(230, 238, 255))

    raw_log = log_path.read_text(encoding="utf-8")
    wrapped = line_wrap_for_width(raw_log, body_font, max_width=width - 60)

    line_height = 26
    y = 100
    max_lines = (height - y - 20) // line_height
    for line in wrapped[:max_lines]:
        draw.text((30, y), line, font=body_font, fill=(197, 210, 230))
        y += line_height

    image.save(out_path)


def build_gif():
    frames = [Image.open(path) for _, path, _ in LOG_TO_IMAGE]
    durations = [10_000, 10_000, 10_000]
    frames[0].save(
        ROOT / "workflow_30s.gif",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
    )
    for frame in frames:
        frame.close()


def main():
    for log_path, image_path, stage in LOG_TO_IMAGE:
        render_log_to_image(log_path, image_path, stage)
    build_gif()
    print("Generated fail.png, patch.png, pass.png and workflow_30s.gif")


if __name__ == "__main__":
    main()
