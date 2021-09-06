

from typing import List, Dict, Tuple, Union
from typing_extensions import Literal

SOURCE_TYPE = Union[str, List[str]]
OUTPUT_TYPE = Union[str, None, Literal[False]]
OPTION_TYPE = Dict[str, Union[str, List[str], Tuple[str]]]
CSS_TYPE = Union[str, List[str]]
