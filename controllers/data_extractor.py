from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1
import os


def extract_metadata(file_path):
    metadata = {
        "title": "Без названия",
        "author": "Неизвестен",
        "genre": "Неизвестен",
        "year": 0,
        "narrator": "Неизвестен",
        "description": "Без описания",
        "bitrate": 0,
        "duration": 0,
        "size": 0,
        "path": file_path
    }

    try:
        audio = MP3(file_path, ID3=ID3)
        if audio:
            metadata["title"] = audio.get("TIT2", ["Без названия"]).text[0]
            metadata["author"] = audio.get("TPE1", ["Неизвестен"]).text[0]
            metadata["genre"] = audio.get("TCON", ["Неизвестен"])[0]
            metadata["year"] = int(str(audio.get("TDRC", [0])[0]))
            metadata["narrator"] = audio.get("TPE2", ["Неизвестен"])[0]
            metadata["description"] = audio.get("TIT3", ["Без описания"])[0]
            metadata["bitrate"] = audio.info.bitrate
            metadata["duration"] = int(audio.info.length)
            metadata["size"] = os.path.getsize(file_path)
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
