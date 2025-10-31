"""
Louchébem - French Butcher's Argot Converter

A hybrid implementation combining historical dictionary with algorithmic transformation.
"""

from .config import LouchebemConfig
from .converter import LouchebemConverter, convert
from .lexicon import (
    ESTABLISHED_LEXICON, 
    STOPWORDS,
    ULTRA_COMMON_VERBS,
    INTERJECTIONS,
)
from .preservation import PreservationRules
from .suffixes import (
    select_suffix,
    classify_consonant,
    get_suffix_info,
    SUFFIX_MAP,
)

__version__ = "0.1.0"

__all__ = [
    # Core converter
    "LouchebemConverter",
    "convert",
    
    # Configuration
    "LouchebemConfig",
    
    # Preservation
    "PreservationRules",
    
    # Data
    "ESTABLISHED_LEXICON",
    "STOPWORDS",
    "ULTRA_COMMON_VERBS",
    "INTERJECTIONS",
    
    # Suffixes
    "select_suffix",
    "classify_consonant",
    "get_suffix_info",
    "SUFFIX_MAP",
]
