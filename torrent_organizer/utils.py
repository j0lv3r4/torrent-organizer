import PTN
from itertools import chain
from pathlib import Path, PurePath
from typing import Union, List
from torrent_organizer.config import Config
from torrent_organizer.models import MediaFile
from torrent_organizer.exceptions import InIgnoreList


config = Config()


def has_ignored_words(item: str) -> bool:
    ignore_list = Config().ignore_list

    for ignore_word in ignore_list:
        if ignore_word in item.lower():
            return True

    return False


def get_media(
    source: Union[str, PurePath], extensions: Union[list, tuple]
) -> List[MediaFile.dict]:
    path = Path(source).absolute()
    print("path", path)
    list_of_files = []
    for extension in extensions:
        pattern = f"*.{extension}"

        # Get only the file names
        files = [
            MediaFile(name=file.name, path=str(file)).dict()
            for file in list(path.rglob(pattern))
            if not has_ignored_words(str(file))
        ]

        # Skip empty lists
        if files:
            list_of_files.append(files)

    # Flatten the list
    return list(chain.from_iterable(list_of_files))


def format_name(file_name: str, with_extension=True) -> str:
    formatted_name = PTN.parse(file_name)
    title = formatted_name.get("title")
    year = formatted_name.get("year")
    extension = str.lower(formatted_name.get("container"))
    media_name = f"{title} ({year})"
    return f"{media_name}.{extension}" if with_extension else media_name
