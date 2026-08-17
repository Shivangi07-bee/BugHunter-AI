from pathlib import Path

from .config import (
    IGNORED_DIRECTORIES,
    SUPPORTED_EXTENSIONS
)


class RepositoryLoader:
    """
    Reads a project folder and returns
    all supported source code files.
    """

    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)
        self.root = Path(repository_path)

    def load_repository(self):
        source_files = []

        for file in self.repository_path.rglob("*"):

            # Skip directories
            if file.is_dir():
                continue

            # Ignore unwanted folders
            if any(
                ignored in file.parts
                for ignored in IGNORED_DIRECTORIES
            ):
                continue

            # Only supported programming languages
            if file.suffix in SUPPORTED_EXTENSIONS:
                source_files.append(file)

        return source_files

    def get_root_files(self):
        return [
            file.name
            for file in self.root.iterdir()
            if file.is_file()
        ]