import json
from pathlib import Path

WALLPAPER_DIR = Path("wallpaper")
CATALOG_FILE = Path("catalog.json")

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}

CATEGORY_NAMES = {
    "literature": "Literatura",
    "fantasy": "Fantasy",
    "sci-fi": "Sci-Fi",
    "dark-fantasy": "Fantasia Sombria",
    "dark-academia": "Dark Academia",
    "nature": "Natureza",
    "japanese": "Japonês",
    "minimal": "Minimalista",
}

WALLPAPER_NAMES = {
    "reading-room": "Sala de Leitura",
    "jornada": "Jornada",
    "distant-worlds": "Mundos Distantes",
    "fallen-kingdom": "Reino Caído",
    "silent-cloister": "Claustro Silencioso",
    "scholars-garden": "Jardim dos Eruditos",
}


def pretty_name(slug):
    return slug.replace("-", " ").replace("_", " ").title()


def load_current_version():
    if not CATALOG_FILE.exists():
        return 1

    try:
        with CATALOG_FILE.open("r", encoding="utf-8") as f:
            current = json.load(f)
        return int(current.get("version", 0)) + 1
    except Exception:
        return 1


def build_catalog():
    categories = []

    if not WALLPAPER_DIR.exists():
        raise SystemExit("Pasta wallpaper/ não encontrada.")

    for category_dir in sorted(WALLPAPER_DIR.iterdir()):
        if not category_dir.is_dir():
            continue

        wallpapers = []

        for image in sorted(category_dir.iterdir()):
            if not image.is_file():
                continue

            if image.suffix.lower() not in SUPPORTED:
                continue

            wallpaper_id = image.stem

            wallpapers.append({
                "id": wallpaper_id,
                "name": WALLPAPER_NAMES.get(
                    wallpaper_id,
                    pretty_name(wallpaper_id)
                ),
                "file": image.as_posix(),
                "format": image.suffix.lower().lstrip("."),
                "orientation": "portrait"
            })

        if wallpapers:
            category_id = category_dir.name

            categories.append({
                "id": category_id,
                "name": CATEGORY_NAMES.get(
                    category_id,
                    pretty_name(category_id)
                ),
                "wallpapers": wallpapers
            })

    return {
        "version": load_current_version(),
        "name": "Kobo Wallpapers",
        "categories": categories
    }


catalog = build_catalog()

with CATALOG_FILE.open("w", encoding="utf-8") as f:
    json.dump(
        catalog,
        f,
        ensure_ascii=False,
        indent=2
    )
    f.write("\n")

print(
    f"catalog.json atualizado: "
    f"{len(catalog['categories'])} categorias"
)
