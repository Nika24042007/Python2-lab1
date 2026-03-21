from typing import Any
from src.Sources.file_source import File_Source
from src.Sources.api_source import Api_source
from src.Sources.generator_source import Generator_source

TYPE_SOURCE: dict[str, Any] = {"file" : File_Source,
                               "generator":Generator_source,
                               "api": Api_source}