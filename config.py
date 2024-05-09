DATABASE_FIELD_MAP = {
    'название': 'title',
    'автор': 'author',
    'жанр': 'genre',
    'год': 'year',
    'чтец': 'narrator',
    'описание': 'description',
    'битрейт': 'bitrate',
    'длительность': 'duration',
    'размер': 'size',
    'путь': 'path',
    'дата добавления': 'date_added'}

DATABASE_AUDIOBOOKS_COLUMNS = [
            'book_id', 'title', 'author', 'genre', 'year', 'narrator',
            'date_added', 'description', 'is_completed', 'is_favorite',
            'bitrate', 'duration', 'size', 'path'
        ]

BOOK_INFO_EDITOR_FIELD_MAP = {
    'название': 'title',
    'автор': 'author',
    'жанр': 'genre',
    'год': 'year',
    'чтец': 'narrator',
    'дата добавления': 'date_added',
    'описание': 'description'
}