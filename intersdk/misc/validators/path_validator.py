from pathlib import Path


class PathValidator:
    def __init__(self, path: Path, must_exist: bool, extension: str) -> None:
        self.path = path
        self.must_exist = must_exist
        self.extension = extension

    def validate_path(self) -> None:
        if not isinstance(self.path, Path):
            raise TypeError("path deve ser uma instância de Path")

    def validate_exists(self) -> None:
        if self.must_exist and not self.path.exists():
            raise ValueError("o path não existe")
        if not self.must_exist and self.path.exists():
            raise ValueError("o path já existe")

    def validate_extension(self) -> None:
        if self.path.suffix != self.extension:
            raise ValueError(f"o arquivo deve ter a extensão {self.extension}")

    def validate_is_file(self) -> None:
        if self.must_exist and not self.path.is_file():
            raise ValueError("o path não é um arquivo")

    def validate(self) -> None:
        self.validate_path()
        self.validate_exists()
        self.validate_extension()
        self.validate_is_file()
