from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from requests import get
from bs4 import BeautifulSoup
import re
import os


def extract_metadata(file_path):
    """
    Извлекает метаданные из аудиофайла.

    :param file_path: Путь к аудиофайлу.
    :return: Словарь с метаданными.
    """
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
        print(f"Ошибка при обработке аудиофайла '{file_path}': {e}")

    return metadata


def extract_cover_from_file(file_path):
    """
    Извлекает обложку из аудиофайла.

    :param file_path: Путь к аудиофайлу.
    :return: Данные обложки в виде байтов или None.
    """
    cover_data = None
    try:
        tags = ID3(file_path)
        for tag in tags.getall("APIC"):
            if tag.mime == "image/jpeg":
                cover_data = tag.data
                break
    except Exception as e:
        print(f"Ошибка при извлечении обложки из файла '{file_path}': {e}")
    return cover_data


def get_audio_files(directory_path):
    """
    Получает список аудиофайлов в директории.

    :param directory_path: Путь к директории.
    :return: Список путей к аудиофайлам.
    """
    return [os.path.join(directory_path, f) for f in os.listdir(directory_path)
            if f.endswith(('.mp3', '.aac', '.wav', '.ogg')) and os.path.isfile(os.path.join(directory_path, f))]


def find_book_info(book_title):
    url = 'https://uknig.com/?q='
    l = book_title.split()
    req = '+'.join(l)
    url = url + req
    print(url)

    # запрос
    response = get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    div_data = html_soup.find('div', class_='media-body')

    if div_data:
        book_title_tag = div_data.find('a', class_='book-title')
        if book_title_tag:
            book_url = book_title_tag['href']
            return parse_book_details(book_url)
    else:
        return None


def parse_book_details(file_path):
    response = get(file_path)
    html_soup = BeautifulSoup(response.text, "html.parser")

    book_details = {}

    # Название книги
    title_tag = html_soup.find('h1', itemprop='name')
    title = title_tag.text if title_tag else None

    # Автор книги
    author_tag = html_soup.find('div', class_='book-series').find('a')
    author = author_tag.text if author_tag else None

    # Год публикации
    year_tag = html_soup.find('a', href=lambda x: x and 'years' in x)
    year = int(year_tag.text) if year_tag else None

    # Жанр
    genre_tags = html_soup.find_all('a', href=lambda x: x and 'genres' in x)
    genres = [tag.text for tag in genre_tags if 'Жанры' not in tag.text]
    genre = ', '.join(genres) if genres else None

    # Чтец
    reader_tag = html_soup.find('a', href=lambda x: x and 'readers' in x)
    reader = reader_tag.text if reader_tag else None

    # Описание книги
    description_tag = html_soup.find('div', class_='description')
    description = description_tag.text.strip() if description_tag else None

    # Формирование словаря book_details только из обнаруженных параметров
    if title:
        book_details['Название'] = title

    if author:
        book_details['Автор'] = author

    if year:
        book_details['Год'] = year

    if genre:
        book_details['Жанр'] = genre

    if reader:
        book_details['Чтец'] = reader

    if description:
        book_details['Описание'] = description

    return book_details
