from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from requests import get
from bs4 import BeautifulSoup
import os


def format_bitrate(bitrate):
    return f"{bitrate / 1000:.2f} kbps"


def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    return f"{hours}h {minutes}m {seconds}s"


def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / 1024 ** 2:.2f} MB"
    else:
        return f"{size / 1024 ** 3:.2f} GB"


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
            metadata.update({
                "title": audio.get("TIT2", ["Без названия"]).text[0],
                "author": audio.get("TPE1", ["Неизвестен"]).text[0],
                "genre": audio.get("TCON", ["Неизвестен"])[0],
                "year": int(str(audio.get("TDRC", [0])[0])),
                "narrator": audio.get("TPE2", ["Неизвестен"])[0],
                "description": audio.get("TIT3", ["Без описания"])[0],
                "bitrate": audio.info.bitrate,
                "duration": int(audio.info.length),
                "size": os.path.getsize(file_path)
            })
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
            if f.lower().endswith(('.mp3', '.aac', '.wav', '.ogg')) and os.path.isfile(os.path.join(directory_path, f))]


def find_books(book_title):
    """
    Ищет книги по названию на сайте uknig.com.

    :param book_title: Название книги.
    :return: Список словарей с информацией о книгах.
    """
    url = f"https://uknig.com/?q={'+'.join(book_title.split())}"
    response = get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for div_data in html_soup.find_all('div', class_='media-body'):
        title_tag = div_data.find('a', class_='book-title')
        author_tag = div_data.find('div', class_='book-author')
        reader_tag = div_data.find('div', class_='book-reader')

        authors = []
        if author_tag:
            author_links = author_tag.find_all('a')
            authors = [author.text.strip() for author in author_links]

        readers = []
        if reader_tag:
            reader_links = reader_tag.find_all('a')
            readers = [reader.text.strip() for reader in reader_links]

        book = {
            'Название': title_tag.text.strip() if title_tag else 'Без названия',
            'Автор': ', '.join(authors) if authors else 'Неизвестен',
            'Чтец': ', '.join(readers) if readers else 'Неизвестен',
            'URL': title_tag['href'] if title_tag else 'Без URL'
        }
        books.append(book)

    return books


def find_book_info(book_title):
    """
    Ищет детальную информацию о книгах по названию на сайте uknig.com.

    :param book_title: Название книги.
    :return: Список словарей с детальной информацией о книгах.
    """
    url = f"https://uknig.com/?q={'+'.join(book_title.split())}"
    response = get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for div_data in html_soup.find_all('div', class_='media-body'):
        book_title_tag = div_data.find('a', class_='book-title')
        if book_title_tag:
            book_url = book_title_tag['href']
            book_details = parse_book_details(book_url)
            if book_details:
                books.append(book_details)

    return books if books else None


def parse_book_details(url):
    """
    Извлекает детальную информацию о книге по URL.

    :param url: URL страницы книги.
    :return: Словарь с детальной информацией о книге.
    """
    response = get(url)
    html_soup = BeautifulSoup(response.text, "html.parser")

    authors = []
    author_tag = html_soup.find('div', class_='book-series')
    if author_tag:
        author_links = author_tag.find_all('a')
        authors = [author.text.strip() for author in author_links]

    readers = []
    reader_tags = html_soup.find_all('a', href=lambda x: x and 'readers' in x)
    readers = [reader.text.strip() for reader in reader_tags] if reader_tags else []

    book_details = {
        'Название': get_tag_text(html_soup, 'h1', {'itemprop': 'name'}, 'Без названия'),
        'Автор': ', '.join(authors) if authors else 'Без автора',
        'Год': get_year(html_soup),
        'Жанр': get_genres(html_soup),
        'Чтец': ', '.join(readers) if readers else 'Без чтеца',
        'Описание': get_tag_text(html_soup, 'div', {'class': 'description'}, 'Без описания', strip=True)
    }

    return book_details


def get_tag_text(soup, tag_name, attrs=None, default='', strip=False):
    """
    Извлекает текст из HTML тега.

    :param soup: Объект BeautifulSoup.
    :param tag_name: Название тега.
    :param attrs: Атрибуты тега для поиска.
    :param default: Значение по умолчанию, если тег не найден.
    :param strip: Удалять ли пробелы вокруг текста.
    :return: Текст тега или значение по умолчанию.
    """
    tag = soup.find(tag_name, attrs=attrs)
    text = tag.text.strip() if strip and tag else tag.text if tag else default
    return text


def get_year(soup):
    """
    Извлекает год из HTML.

    :param soup: Объект BeautifulSoup.
    :return: Год или 'Без года'.
    """
    year_tag = soup.find('a', href=lambda x: x and 'years' in x)
    return int(year_tag.text) if year_tag else 'Без года'


def get_genres(soup):
    """
    Извлекает жанры из HTML.

    :param soup: Объект BeautifulSoup.
    :return: Строка с жанрами или 'Без жанра'.
    """
    genre_tags = soup.find_all('a', href=lambda x: x and 'genres' in x)
    genres = [tag.text for tag in genre_tags if 'Жанры' not in tag.text]
    return ', '.join(genres) if genres else 'Без жанра'
