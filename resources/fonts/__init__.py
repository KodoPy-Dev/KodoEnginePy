from pathlib import Path


def get_font_file(file_name="", extension="tff"):
    fonts_dir = Path(__file__).parent.resolve()
    font_file = fonts_dir.joinpath(f"{file_name}.{extension}")
    return font_file

