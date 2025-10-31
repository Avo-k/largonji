"""
Configuration for Louchébem converter.

Provides a dataclass-based configuration system with feature flags
and preservation options.
"""

from dataclasses import dataclass


@dataclass
class LouchebemConfig:
    """
    Configuration for Louchébem converter behavior.
    
    This allows fine-grained control over transformation features
    and word preservation rules.
    """
    
    # ===== Basic Options =====
    preserve_stopwords: bool = True
    """Preserve structural words (articles, prepositions, etc.)"""
    
    preserve_case: bool = True
    """Maintain original capitalization patterns"""
    
    preserve_punctuation: bool = True
    """Keep punctuation and spacing intact"""
    
    random_seed: int | None = None
    """Random seed for reproducible suffix selection (None = random)"""
    
    # ===== Feature Flags =====
    enable_apostrophe_merging: bool = True
    """Merge l' with word (l'origine → lorigine → transformed)"""
    
    enable_silent_consonants: bool = True
    """Remove silent consonants before transformation (discret → discrè)"""
    
    enable_doubled_simplification: bool = True
    """Simplify doubled consonants (ff → f, mm → m)"""
    
    enable_infinitive_verbs: bool = True
    """Transform -er to -é for infinitive verbs (parler → parlé → parlépem)"""
    
    # ===== Preservation Categories =====
    # These control which word categories should NOT be transformed
    
    preserve_ultra_common_verbs: bool = True
    """Preserve être, avoir, faire, aller (all conjugations)"""
    
    preserve_interjections: bool = True
    """Preserve interjections and onomatopoeia (ah, oh, aïe, paf, etc.)"""
    
    preserve_numbers: bool = True
    """Preserve numbers and dates (1881, XVIIIe, 1er, etc.)"""
    
    preserve_proper_nouns: bool = True
    """Preserve proper nouns (capitalized mid-sentence)"""
    
    preserve_acronyms: bool = True
    """Preserve acronyms (SNCF, M., Dr., etc.)"""
    
    preserve_already_louchebem: bool = True
    """Preserve words that look like Louchébem (avoid double-transformation)"""
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure seed is None or a valid integer
        if self.random_seed is not None and not isinstance(self.random_seed, int):
            raise ValueError(f"random_seed must be None or int, got {type(self.random_seed)}")
    
    @classmethod
    def minimal(cls) -> 'LouchebemConfig':
        """
        Create a minimal config that preserves only essential stopwords.
        
        Returns:
            LouchebemConfig with most preservation features disabled
        """
        return cls(
            preserve_stopwords=True,
            preserve_case=True,
            preserve_punctuation=True,
            preserve_ultra_common_verbs=False,
            preserve_interjections=False,
            preserve_numbers=False,
            preserve_proper_nouns=False,
            preserve_acronyms=False,
            preserve_already_louchebem=False,
        )
    
    @classmethod
    def maximal(cls) -> 'LouchebemConfig':
        """
        Create a maximal config that preserves as much as possible.
        
        Returns:
            LouchebemConfig with all preservation features enabled
        """
        return cls()  # Default is already maximal
    
    @classmethod
    def for_testing(cls, seed: int = 42) -> 'LouchebemConfig':
        """
        Create a config suitable for testing (with fixed seed).
        
        Args:
            seed: Random seed for reproducible results
            
        Returns:
            LouchebemConfig with deterministic behavior
        """
        return cls(random_seed=seed)

