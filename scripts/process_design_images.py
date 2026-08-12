from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "images" / "content" / "sub" / "design"


def polish(image: Image.Image) -> Image.Image:
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.035)
    return image.filter(ImageFilter.UnsharpMask(radius=1.4, percent=125, threshold=3))


def stack(parts: list[Image.Image], gap: int) -> Image.Image:
    canvas = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts) + gap * (len(parts) - 1)), "white")
    y = 0
    for part in parts:
        canvas.paste(part, ((canvas.width - part.width) // 2, y))
        y += part.height + gap
    return canvas


def save(image: Image.Image, name: str) -> None:
    image.save(DESIGN / name, quality=94, subsampling=0, optimize=True)


card = Image.open(DESIGN / "card_news.jpg").convert("RGB")
card_rows = [card.crop(box) for box in [(28, 108, 790, 298), (28, 497, 790, 687), (28, 883, 790, 1074), (28, 1270, 790, 1461), (28, 1652, 790, 1843)]]
save(polish(stack(card_rows, 26)), "card_news-clean.jpg")
for month, row in zip(("06", "05", "04", "03", "02"), card_rows):
    save(polish(row), f"card-news-{month}.jpg")

banner = Image.open(DESIGN / "banner&popup.jpg").convert("RGB")
save(polish(stack([banner.crop((33, 112, 784, 512)), banner.crop((33, 719, 784, 1459))], 30)), "banner-popup-clean.jpg")

proposal = Image.open(DESIGN / "proposal_cover.jpg").convert("RGB")
save(polish(proposal.crop((28, 102, 790, 338))), "proposal-cover-clean.jpg")
