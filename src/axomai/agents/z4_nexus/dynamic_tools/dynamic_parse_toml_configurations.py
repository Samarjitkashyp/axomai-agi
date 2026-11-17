import toml
from typing import Any, Dict

class ParseTOMLConfigurations:
    """
    A tool class to parse TOML configuration files.
    """

    def __init__(self):
        pass

    def _validate_input(self, file_path: str) -> None:
        """
        Validates the input parameters.

        :param file_path: The path to the TOML file.
        :raises ValueError: If the file_path is not a string or is empty.
        """
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("The file_path must be a non-empty string.")

    def _read_toml_file(self, file_path: str) -> Dict[str, Any]:
        """
        Reads and parses a TOML file.

        :param file_path: The path to the TOML file.
        :return: A dictionary containing the parsed TOML data.
        :raises FileNotFoundError: If the file does not exist.
        :raises toml.TomlDecodeError: If the file is not a valid TOML file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return toml.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} was not found.")
        except toml.TomlDecodeError as e:
            raise toml.TomlDecodeError(f"Error decoding TOML file: {e}")

    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Public method to execute the parsing of a TOML file.

        :param kwargs: Keyword arguments containing 'file_path'.
        :return: A dictionary containing the parsed TOML data.
        :raises ValueError: If the input validation fails.
        :raises FileNotFoundError: If the file does not exist.
        :raises toml.TomlDecodeError: If the file is not a valid TOML file.
        """
        file_path = kwargs.get('file_path')
        self._validate_input(file_path)
        return self._read_toml_file(file_path)