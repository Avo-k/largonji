"""
Word preservation rules for Louchébem converter.

Determines which words should NOT be transformed, including:
- Stopwords (articles, prepositions, etc.)
- Ultra-common verbs (être, avoir, faire, aller)
- Interjections and onomatopoeia
- Numbers and dates
- Acronyms
- Proper nouns
- Words already in Louchébem
"""

import re
from .config import LouchebemConfig
from .lexicon import (
    STOPWORDS,
    ULTRA_COMMON_VERBS,
    INTERJECTIONS,
)


class PreservationRules:
    """
    Determines which words should be preserved (not transformed).
    
    Uses a LouchebemConfig to control which preservation rules are active.
    """
    
    def __init__(self, config: LouchebemConfig):
        """
        Initialize preservation rules with configuration.
        
        Args:
            config: Configuration controlling which rules are active
        """
        self.config = config
    
    def should_preserve(self, word: str, is_sentence_start: bool = False) -> bool:
        """
        Master check: should this word be preserved?
        
        Checks all active preservation rules based on configuration.
        
        Args:
            word: The word to check
            is_sentence_start: Whether this word starts a sentence
            
        Returns:
            True if word should be preserved, False if it should be transformed
        """
        # Always check stopwords (if enabled in config)
        if self.config.preserve_stopwords and self.is_stopword(word):
            return True
        
        # Check each category based on config
        if self.config.preserve_ultra_common_verbs and self.is_ultra_common_verb(word):
            return True
        
        if self.config.preserve_interjections and self.is_interjection(word):
            return True
        
        if self.config.preserve_numbers and self.is_number_or_date(word):
            return True
        
        if self.config.preserve_acronyms and self.is_acronym(word):
            return True
        
        if self.config.preserve_proper_nouns and self.is_proper_noun(word, is_sentence_start):
            return True
        
        if self.config.preserve_already_louchebem and self.is_already_louchebem(word):
            return True
        
        return False
    
    @staticmethod
    def is_stopword(word: str) -> bool:
        """
        Check if a word is a stopword (article, preposition, pronoun, etc.).
        
        Args:
            word: The word to check
            
        Returns:
            True if word is a stopword
        """
        return word.lower().strip("'\"") in STOPWORDS
    
    @staticmethod
    def is_ultra_common_verb(word: str) -> bool:
        """
        Check if a word is an ultra-common verb form (être, avoir, faire, aller).
        
        These verbs are so frequent that transforming them hurts comprehension.
        
        Args:
            word: The word to check
            
        Returns:
            True if word is an ultra-common verb form
        """
        return word.lower().strip("'\"") in ULTRA_COMMON_VERBS
    
    @staticmethod
    def is_interjection(word: str) -> bool:
        """
        Check if a word is an interjection or onomatopoeia.
        
        These express emotion/sound and should stay natural.
        
        Args:
            word: The word to check
            
        Returns:
            True if word is an interjection
        """
        return word.lower().strip("'\"!?,;:.") in INTERJECTIONS
    
    @staticmethod
    def is_number_or_date(word: str) -> bool:
        """
        Check if a word is a digit, Roman numeral, or date-related number.
        
        Examples: 1881, XVIIIe, XIXe, 19e, 1er, etc.
        
        Args:
            word: The word to check
            
        Returns:
            True if word is a number or date
        """
        word_clean = word.strip("'\".,;:!?")
        
        # Pure digits (including with punctuation like 1,000 or 1.5)
        if re.match(r'^\d+([.,]\d+)*$', word_clean):
            return True
        
        # Roman numerals (possibly with 'e' or 'er' suffix for ordinals)
        # Matches: XVIII, XVIIIe, XIXe, Ier, IIe, etc.
        if re.match(r'^[IVXLCDM]+e?r?$', word_clean, re.IGNORECASE):
            return True
        
        # Ordinal numbers: 1er, 2e, 3ème, 19e, etc.
        if re.match(r'^\d+(er|e|ème)$', word_clean, re.IGNORECASE):
            return True
        
        return False
    
    @staticmethod
    def is_acronym(word: str) -> bool:
        """
        Check if a word is an acronym.
        
        Examples: SNCF, M., Mme, Dr., etc.
        
        Args:
            word: The word to check
            
        Returns:
            True if word is an acronym
        """
        word_clean = word.strip("'\".,;:!?")
        
        # All uppercase (2+ letters): SNCF, NATO, FBI
        if len(word_clean) >= 2 and word_clean.isupper():
            return True
        
        # Abbreviations with dots: M., Mme., Dr., etc.
        if '.' in word and len(word_clean.replace('.', '')) <= 4:
            return True
        
        return False
    
    @staticmethod
    def is_proper_noun(word: str, is_sentence_start: bool = False) -> bool:
        """
        Check if a word is likely a proper noun (name, place, etc.).
        
        Args:
            word: The word to check
            is_sentence_start: Whether this word starts a sentence
            
        Returns:
            True if the word is capitalized and NOT at sentence start
        """
        # Don't flag sentence-initial words as proper nouns
        if is_sentence_start:
            return False
        
        # Check if first letter is uppercase
        word_clean = word.strip("'\".,;:!?")
        if not word_clean:
            return False
        
        return word_clean[0].isupper()
    
    @staticmethod
    def is_already_louchebem(word: str) -> bool:
        """
        Check if a word looks like it's already in Louchébem form.
        
        Louchébem pattern: starts with 'l', ends with typical suffixes.
        Examples: loucherbem, largonji, laféquès, lombem, etc.
        
        Args:
            word: The word to check
            
        Returns:
            True if word looks like Louchébem
        """
        word_lower = word.lower().strip("'\".,;:!?")
        
        # Must start with 'l' (but not la/le/les/l')
        if not word_lower.startswith('l') or len(word_lower) < 4:
            return False
        
        # Skip obvious articles
        if word_lower in {'le', 'la', 'les', 'leur', 'leurs'}:
            return False
        
        # Check for common Louchébem suffixes
        louchebem_suffixes = [
            'em', 'ème', 'é', 'ès', 'esse', 'ok', 'oc', 'oque', 'ic', 'ique',
            'uche', 'muche', 'puche', 'dem', 'dé', 'tem', 'té', 'vé', 'vem',
            'sé', 'bé', 'boc', 'fé', 'ji', 'gué', 'ré', 'rré', 'cou', 'mé',
        ]
        
        for suffix in louchebem_suffixes:
            if word_lower.endswith(suffix):
                return True
        
        return False


# Backwards compatibility: standalone functions that use default config
_default_rules = None


def _get_default_rules() -> PreservationRules:
    """Get or create default preservation rules instance."""
    global _default_rules
    if _default_rules is None:
        from .config import LouchebemConfig
        _default_rules = PreservationRules(LouchebemConfig())
    return _default_rules


def should_preserve_word(word: str, is_sentence_start: bool = False) -> bool:
    """
    Backwards compatibility: check if word should be preserved using default config.
    
    Args:
        word: The word to check
        is_sentence_start: Whether this word starts a sentence
        
    Returns:
        True if word should be preserved
    """
    return _get_default_rules().should_preserve(word, is_sentence_start)


def is_stopword(word: str) -> bool:
    """Backwards compatibility: check if word is a stopword."""
    return PreservationRules.is_stopword(word)


def is_ultra_common_verb(word: str) -> bool:
    """Backwards compatibility: check if word is ultra-common verb."""
    return PreservationRules.is_ultra_common_verb(word)


def is_interjection(word: str) -> bool:
    """Backwards compatibility: check if word is interjection."""
    return PreservationRules.is_interjection(word)


def is_number_or_date(word: str) -> bool:
    """Backwards compatibility: check if word is number/date."""
    return PreservationRules.is_number_or_date(word)


def is_acronym(word: str) -> bool:
    """Backwards compatibility: check if word is acronym."""
    return PreservationRules.is_acronym(word)


def is_proper_noun(word: str, is_sentence_start: bool = False) -> bool:
    """Backwards compatibility: check if word is proper noun."""
    return PreservationRules.is_proper_noun(word, is_sentence_start)


def is_already_louchebem(word: str) -> bool:
    """Backwards compatibility: check if word is already Louchébem."""
    return PreservationRules.is_already_louchebem(word)

