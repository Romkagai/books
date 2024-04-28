from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1
import os


def extract_metadata(file_path):
    metadata = {
        "Title": "Без названия",
        "Author": "Неизвестен",
        "Genre": "Неизвестен",
        "Year": 0,
        "Narrator": "Неизвестен",
        "Description": "Без описания",
        "Bitrate": 0,
        "Duration": 0,
        "Size": 0,
        "Path": file_path
    }

    try:
        audio = MP3(file_path, ID3=ID3)
        if audio:
            metadata["Title"] = audio.get("TIT2", ["Без названия"]).text[0]
            metadata["Author"] = audio.get("TPE1", ["Неизвестен"]).text[0]
            metadata["Genre"] = audio.get("TCON", ["Неизвестен"])[0]
            metadata["Year"] = int(str(audio.get("TDRC", [0])[0]))
            metadata["Narrator"] = audio.get("TPE2", ["Неизвестен"])[0]
            metadata["Description"] = audio.get("TIT3", ["Без описания"])[0]
            metadata["Bitrate"] = audio.info.bitrate
            metadata["Duration"] = int(audio.info.length)
            metadata["Size"] = os.path.getsize(file_path)
    except Exception as e:
        print(f"Ошибка при обработке аудиофайла: {e}")

    return metadata


def extract_cover_from_file(file_path):
    tags = ID3(file_path)
    cover_data = None
    for tag in tags.getall("APIC"):
        if tag.mime == "image/jpeg":
            cover_data = tag.data
            break
    return cover_data
