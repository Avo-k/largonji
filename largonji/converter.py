"""
Louchébem Converter - Hybrid Implementation

Combines hardcoded dictionary for attested words with algorithmic
transformation for creative/unknown words.

Based on traditional louchébem rules where:
- The first "attack consonant" (or consonant cluster) is moved to the end
- Replaced by 'L' at the beginning  
- A suffix is added based on the final consonant sound
"""

import re

from .config import LouchebemConfig
from .lexicon import ESTABLISHED_LEXICON, get_louchebem_word
from .preservation import PreservationRules
from .suffixes import select_suffix, classify_consonant


class LouchebemConverter:
    """
    Convert French text to Louchébem using a hybrid approach.
    
    The converter:
    1. Preserves stopwords (articles, prepositions, etc.)
    2. Uses dictionary lookup for known words
    3. Applies algorithmic transformation for unknown words
    4. Selects suffixes based on consonant sound types
    5. Handles vowel-initial words by finding the first attack consonant
    """
    
    # Simple vowels for detection (including accented)
    VOWELS = 'aeiouyàâäéèêëïîôùûü'
    
    # Nasal vowels and complex vowel patterns (treated as complete vowel sounds)
    # These are checked first before simple vowels
    NASAL_VOWELS = ['an', 'en', 'in', 'on', 'un', 'ain', 'ein', 'oin', 
                    'am', 'em', 'im', 'om', 'um', 'aim', 'eim',
                    'eau', 'au', 'eu', 'œu', 'ou', 'oi', 'ai', 'ei', 'ui']
    
    # Consonant cluster pattern (all consonants before first vowel)
    # Note: 'qu' is treated as a consonant cluster (u is part of the consonant)
    CONSONANT_PATTERN = re.compile(r'^(qu|[bcdfghjklmnpqrstvwxz]+)(.+)$', re.IGNORECASE)
    
    # Pattern to find attack consonant in vowel-initial words
    # Matches: vowel_sound + consonant_cluster + rest
    # Note: 'qu' is treated as a consonant cluster (u is part of the consonant)
    VOWEL_INITIAL_PATTERN = re.compile(
        r'^([aeiouyàâäéèêëïîôùûü]+(?:n|m)?|an|en|in|on|un|ain|ein|oin|am|em|im|om|um|eau|au|eu|œu|ou|oi|ai|ei|ui)'
        r'(qu|[bcdfghjklmnpqrstvwxz]+)'  # 'qu' is matched first as a unit
        r'(.+)$', 
        re.IGNORECASE
    )
    
    # Silent consonants at the end of French words
    # These are typically not pronounced and should be removed
    SILENT_ENDINGS = {
        't': ['et', 'ot', 'ut', 'at', 'it', 'ent'],  # discret, trot, debut, chat, petit, équivalent
        's': ['s', 'es', 'as', 'is', 'os', 'us'],  # temps, tres, pas, pris, gros, plus
        'x': ['ux', 'eux', 'oux', 'oix', 'aix'],  # deux, heureux, doux, voix, paix
        'd': ['d', 'ed', 'id', 'nd', 'rd'],  # pied, grand, sourd
        'p': ['p', 'up', 'op'],  # coup, trop, beaucoup
        'c': ['c'],  # blanc, franc
        'g': ['g', 'ng'],  # sang, long
    }
    
    def __init__(
        self,
        config: LouchebemConfig | None = None,
        # Backwards compatibility: individual parameters
        preserve_stopwords: bool | None = None,
        preserve_case: bool | None = None,
        preserve_punctuation: bool | None = None,
        random_seed: int | None = None,
    ):
        """
        Initialize the Louchébem converter (hybrid mode).
        
        Args:
            config: Configuration object (preferred). If None, uses defaults or kwargs
            preserve_stopwords: [DEPRECATED] Use config instead
            preserve_case: [DEPRECATED] Use config instead
            preserve_punctuation: [DEPRECATED] Use config instead
            random_seed: [DEPRECATED] Use config instead
        """
        # Use provided config or create from kwargs (backwards compatibility)
        if config is None:
            config = LouchebemConfig(
                preserve_stopwords=preserve_stopwords if preserve_stopwords is not None else True,
                preserve_case=preserve_case if preserve_case is not None else True,
                preserve_punctuation=preserve_punctuation if preserve_punctuation is not None else True,
                random_seed=random_seed,
            )
        
        self.config = config
        self.preservation_rules = PreservationRules(config)
        
        # Expose commonly accessed config values as properties for convenience
        self.preserve_stopwords = config.preserve_stopwords
        self.preserve_case = config.preserve_case
        self.preserve_punctuation = config.preserve_punctuation
        self.random_seed = config.random_seed
        
    def convert_text(self, text: str) -> str:
        """
        Convert a French text to Louchébem.
        
        Args:
            text: Input French text
            
        Returns:
            Louchébem-transformed text
        """
        if not text:
            return text
        
        # Split on word boundaries while preserving punctuation
        tokens = self._tokenize(text)
        
        # Track sentence starts for proper noun detection
        is_sentence_start = True
        sentence_end_punctuation = {'.', '!', '?', ':', ';'}
        
        # Convert each token
        converted = []
        for token in tokens:
            if token.get('type') == 'word':
                word = token['value']
                transformed = self._convert_word(word, is_sentence_start=is_sentence_start)
                converted.append(transformed)
                is_sentence_start = False  # Next word is not sentence start
            else:
                # Preserve punctuation and whitespace
                punct = token['value']
                converted.append(punct)
                # Check if this punctuation ends a sentence
                if any(p in punct for p in sentence_end_punctuation):
                    is_sentence_start = True
        
        return ''.join(converted)
    
    def _tokenize(self, text: str) -> list[dict]:
        """
        Split text into words and non-words (punctuation, spaces).
        
        Returns:
            List of tokens with 'type' and 'value'
        """
        # Pattern: word characters (including French accents) vs non-word
        pattern = re.compile(r"([a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ'']+|[^a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ'']+)")
        
        tokens = []
        for match in pattern.finditer(text):
            token = match.group(1)
            # Check if it's a word or punctuation/space
            if re.match(r"[a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇ'']+", token):
                tokens.append({'type': 'word', 'value': token})
            else:
                tokens.append({'type': 'other', 'value': token})
        
        return tokens
    
    def _convert_word(self, word: str, is_sentence_start: bool = False) -> str:
        """
        Convert a single word to Louchébem (hybrid approach).
        
        Handles French élisions (apostrophes):
        - l' + word: merge and transform (l'argot → largot → largonji)
        - Other apostrophes (d', j', s', etc.): preserve + transform word
        
        Args:
            word: A single French word
            is_sentence_start: Whether this word starts a sentence (for proper noun detection)
            
        Returns:
            The Louchébem transformation
        """
        # Handle empty or very short words
        if not word or len(word) < 2:
            return word
        
        # Handle apostrophes (French élisions)
        if "'" in word:
            before_apos, after_apos = word.split("'", 1)
            
            # Special case: l' + word → merge them (l'argot → largot → largonji)
            # This makes phonetic sense since the word will start with 'l' anyway
            if before_apos.lower() == 'l':
                # First check if the word after apostrophe is in dictionary (e.g., argot → largomuche)
                lexicon_word = get_louchebem_word(after_apos)
                if lexicon_word:
                    # Use the dictionary form (l'argot → largomuche)
                    if self.preserve_case:
                        return self._apply_case_pattern(lexicon_word, word)
                    return lexicon_word
                
                # Not in dictionary, merge l' with the word and transform as one
                merged_word = 'l' + after_apos
                return self._convert_word(merged_word, is_sentence_start)
            
            # For other apostrophes (d', j', s', t', m', n', qu', c'):
            # Preserve the prefix and transform the word after
            elif before_apos.lower() in ['d', 'j', 's', 't', 'm', 'n', 'qu', 'c']:
                # Check if the word after apostrophe should be preserved
                if self.preserve_stopwords and self.preservation_rules.should_preserve(after_apos, is_sentence_start):
                    # Both parts are stopwords, keep as-is
                    return word
                else:
                    # Transform the word, keep the prefix
                    transformed_after = self._convert_word(after_apos, is_sentence_start)
                    # Preserve original case of the prefix
                    return before_apos + "'" + transformed_after
        
        # Remove apostrophes from the word (handle contractions)
        clean_word = word.strip("'")
        
        # Check if word should be preserved (using comprehensive preservation rules)
        if self.preserve_stopwords and self.preservation_rules.should_preserve(clean_word, is_sentence_start):
            return word
        
        # Check dictionary first (hybrid approach)
        lexicon_word = get_louchebem_word(clean_word)
        if lexicon_word:
            # Preserve original case pattern
            if self.preserve_case:
                return self._apply_case_pattern(lexicon_word, word)
            return lexicon_word
        
        # Remove silent ending consonants before transformation
        clean_word = self._remove_silent_consonants(clean_word)
        
        # Handle infinitive verbs (-er → -é)
        clean_word = self._handle_infinitive_verbs(clean_word)
        
        # Apply algorithmic transformation for unknown words
        return self._apply_transformation(clean_word, word)
    
    def _remove_silent_consonants(self, word: str) -> str:
        """
        Remove silent consonants at the end of French words.
        
        Examples:
        - discret → discrè (remove t, add accent to preserve é sound)
        - petit → peti (remove t)
        - temps → temp (remove s)
        - deux → deu (remove x)
        - employée → employé (remove extra e from -ée ending)
        
        Args:
            word: The word to process
            
        Returns:
            Word with silent consonants removed and accents adjusted
        """
        if len(word) < 3:
            return word
        
        word_lower = word.lower()
        
        # Special case: words ending in -ée should become -é
        # (The extra 'e' is silent/redundant)
        if word_lower.endswith('ée'):
            return word[:-2] + 'é'
        
        # Check each type of silent ending
        for consonant, patterns in self.SILENT_ENDINGS.items():
            for pattern in patterns:
                if word_lower.endswith(pattern):
                    # Remove the silent consonant(s)
                    cleaned = word[:-len(pattern)] + pattern[:-len(consonant)]
                    
                    # Special case: if word ends in "et" (like discret), 
                    # change final "e" to "è" to preserve pronunciation
                    if pattern == 'et' and len(cleaned) >= 2 and cleaned[-1] == 'e':
                        cleaned = cleaned[:-1] + 'è'
                    
                    # Similar for "es", "ed", etc. ending in e
                    elif pattern in ['es', 'ed'] and len(cleaned) >= 2 and cleaned[-1] == 'e':
                        cleaned = cleaned[:-1] + 'è'
                    
                    return cleaned
        
        return word
    
    def _handle_infinitive_verbs(self, word: str) -> str:
        """
        Handle French infinitive verbs ending in -er.
        
        Change -er to -é (phonetic equivalent, easier to combine with consonants).
        
        Examples:
        - parler → parlé
        - manger → mangé
        - couper → coupé
        
        Args:
            word: The word to process
            
        Returns:
            Word with -er changed to -é if applicable
        """
        if len(word) < 3:
            return word
        
        word_lower = word.lower()
        
        # Check if word ends in -er (infinitive verb)
        if word_lower.endswith('er'):
            # Don't change if it's a short word or might not be a verb
            # (like "mer", "ver", "fer")
            if len(word) <= 3:
                return word
            
            # Change -er to -é
            return word[:-2] + 'é'
        
        return word
    
    def _apply_transformation(self, clean_word: str, original_word: str) -> str:
        """
        Apply the Louchébem transformation algorithm.
        
        Based on the rule: find the first "attack consonant" (consonne d'attaque)
        and replace it with 'l', moving the original consonant(s) to the end.
        
        For vowel-initial words like "entendre":
        - "en" is treated as a vowel sound
        - "t" is the attack consonant
        - Result: "en" + "l" + "endre" + "t" + suffix = "enlendreté"
        
        Args:
            clean_word: Word without punctuation
            original_word: Original word with original case
            
        Returns:
            Transformed word
        """
        # Check if word starts with a vowel
        if clean_word[0].lower() in self.VOWELS:
            # Try to find the attack consonant after the vowel sound
            match = self.VOWEL_INITIAL_PATTERN.match(clean_word)
            if match:
                vowel_sound, consonants, rest = match.groups()
                
                # Make sure there's content after the consonants
                if not rest:
                    return original_word
                
                # Simplify doubled consonants (attention: tt → t)
                consonants = self._simplify_doubled_consonants(consonants)
                
                # Apply phonetic adjustments
                adjusted_consonants = self._phonetic_adjust_vowel_initial(
                    consonants, vowel_sound, rest
                )
                
                # Select suffix (returns suffix and whether consonant is needed)
                suffix, needs_consonant = select_suffix(adjusted_consonants, seed=self.random_seed)
                
                # Build word: check if suffix already contains the consonant
                # Example: "entendre" → "en" + "l" + "endre" + "té" (té already has t)
                # Special case: multi-character clusters (like "pl") must be kept in full
                if needs_consonant or len(adjusted_consonants) > 1:
                    # Neutral suffix OR multi-char cluster - needs full cluster prepended
                    louchebem_word = vowel_sound + 'l' + rest + adjusted_consonants + suffix
                else:
                    # Single consonant suffix like 'té' already contains 't'
                    louchebem_word = vowel_sound + 'l' + rest + suffix
                
                # Simplify any doubled consonants (e.g., 'pll' → 'pl')
                louchebem_word = self._simplify_doubled_consonants_in_word(louchebem_word)
                
                # Preserve case
                if self.preserve_case:
                    return self._apply_case_pattern(louchebem_word, original_word)
                
                return louchebem_word
            else:
                # No attack consonant found, return as-is
                return original_word
        
        # Standard consonant-initial word
        # Extract consonant cluster before first vowel
        match = self.CONSONANT_PATTERN.match(clean_word)
        if not match:
            return original_word
        
        consonants, rest = match.groups()
        
        # Make sure there's a vowel in the rest
        if not any(c.lower() in self.VOWELS for c in rest):
            return original_word
        
        # Simplify doubled consonants (attention: tt → t)
        consonants = self._simplify_doubled_consonants(consonants)
        
        # Apply phonetic adjustments to moved consonants
        adjusted_consonants = self._phonetic_adjust(consonants, rest)
        
        # Select appropriate suffix (returns suffix and whether consonant is needed)
        suffix, needs_consonant = select_suffix(adjusted_consonants, seed=self.random_seed)
        
        # Build word: check if suffix already contains the consonant
        # Special case: multi-character clusters (like "pr", "pl") must be kept in full
        if needs_consonant or len(adjusted_consonants) > 1:
            # Neutral suffix OR multi-char cluster - needs full cluster prepended
            louchebem_word = 'l' + rest + adjusted_consonants + suffix
        else:
            # Single consonant suffix like 'fès' already contains 'f'
            louchebem_word = 'l' + rest + suffix
        
        # Simplify any doubled consonants (e.g., 'pll' → 'pl')
        louchebem_word = self._simplify_doubled_consonants_in_word(louchebem_word)
        
        # Preserve case pattern from original
        if self.preserve_case:
            return self._apply_case_pattern(louchebem_word, original_word)
        
        return louchebem_word
    
    def _simplify_doubled_consonants(self, consonants: str) -> str:
        """
        Simplify doubled consonants to single consonant.
        
        When the attack consonant is doubled (like tt, nn, mm, etc.),
        keep only one when moving it to the end.
        
        Examples:
        - tt → t (attention → alention + t)
        - nn → n
        - mm → m
        
        Args:
            consonants: The consonant cluster
            
        Returns:
            Simplified consonant cluster
        """
        if not consonants:
            return consonants
        
        # Check if it's a doubled consonant (same consonant repeated)
        if len(consonants) >= 2:
            # Check if all characters are the same
            if all(c.lower() == consonants[0].lower() for c in consonants):
                # Return just one of the consonant
                return consonants[0]
        
        return consonants
    
    def _simplify_doubled_consonants_in_word(self, word: str) -> str:
        """
        Simplify any doubled consonants that appear in the final word.
        
        This can happen when a moved consonant meets a suffix starting with
        the same consonant (e.g., 'f' + 'fès' = 'ffès' → 'fès').
        
        Examples:
        - linffès → linfès (f + fès → fès)
        - lotmmé → lotmé (m + mé → mé)
        - lièclessès → lièclesès (s + sès → sès)
        
        Args:
            word: The constructed Louchébem word
            
        Returns:
            Word with doubled consonants simplified
        """
        if len(word) < 2:
            return word
        
        # First handle 'qu' doubling (ququ → qu)
        # This needs to be done before single consonant doubling
        result = word
        result = result.replace('ququ', 'qu')
        result = result.replace('QUQU', 'QU')
        result = result.replace('QuQu', 'Qu')
        result = result.replace('Ququ', 'Qu')
        result = result.replace('quQu', 'qu')
        
        # Replace any doubled single consonants with single consonant
        # We need to check each possible consonant
        for consonant in 'bcdfghjklmnpqrstvwxz':
            # Replace doubled (case-insensitive)
            doubled_lower = consonant * 2
            doubled_upper = consonant.upper() * 2
            doubled_mixed1 = consonant + consonant.upper()
            doubled_mixed2 = consonant.upper() + consonant
            
            # Replace all variations
            result = result.replace(doubled_lower, consonant)
            result = result.replace(doubled_upper, consonant.upper())
            result = result.replace(doubled_mixed1, consonant)
            result = result.replace(doubled_mixed2, consonant.upper())
        
        return result
    
    def _phonetic_adjust(self, consonants: str, rest: str) -> str:
        """
        Adjust consonants for phonetic consistency (standard consonant-initial words).
        
        French orthographic rules for maintaining pronunciation:
        - c → qu before a, o, u (to preserve [k] sound)
        - c → ss before e, i (to preserve [s] sound) 
        - g → gu before e, i (to preserve [g] sound)
        - g → gh before a, o, u (rare, to preserve [g])
        
        Args:
            consonants: The consonant cluster being moved
            rest: The remaining part of the word
            
        Returns:
            Adjusted consonant cluster
        """
        if not rest:
            return consonants
        
        # Get the first character of rest (what comes after moved consonants)
        first_vowel = rest[0].lower()
        consonants_lower = consonants.lower()
        consonants_upper = consonants.isupper()
        
        # Handle single 'c'
        if consonants_lower == 'c':
            if first_vowel in 'aouàôù':
                # c → qu to maintain [k] sound
                result = 'qu'
            else:
                # Keep 'c' before e, i (becomes [s])
                result = 'c'
            return result.upper() if consonants_upper else result
        
        # Handle single 'g'
        if consonants_lower == 'g':
            if first_vowel in 'eéèêëiïî':
                # g → gu to maintain [g] sound
                result = 'gu'
            else:
                result = 'g'
            return result.upper() if consonants_upper else result
        
        # For clusters ending in c or g, apply similar rules
        if consonants_lower.endswith('c'):
            if first_vowel in 'aouàôù':
                consonants = consonants[:-1] + 'qu'
        
        if consonants_lower.endswith('g'):
            if first_vowel in 'eéèêëiïî':
                consonants = consonants[:-1] + 'gu'
        
        return consonants
    
    def _phonetic_adjust_vowel_initial(self, consonants: str, vowel_before: str, rest: str) -> str:
        """
        Adjust consonants for vowel-initial words.
        
        Special rules from the French text:
        - s between vowels represents [z] sound, write as 'z'
          Example: "isolation" → "ilolationz..." (not "ilolations...")
        - s representing [s] sound, write as single 's'
        - All variants of [k] sound (qu, ch, c) → 'k'
        
        Args:
            consonants: The attack consonant cluster
            vowel_before: The vowel sound before the consonant
            rest: The remaining part after the consonant
            
        Returns:
            Adjusted consonant cluster
        """
        consonants_lower = consonants.lower()
        consonants_upper = consonants.isupper()
        
        # Handle 's' between vowels (pronounced [z])
        if consonants_lower == 's':
            # Check if we're between vowels (vowel before, vowel after)
            if rest and rest[0].lower() in self.VOWELS:
                # s between vowels → z (for [z] sound)
                result = 'z'
                return result.upper() if consonants_upper else result
        
        # Handle 'ss' → 's' (always [s] sound, not [z])
        if consonants_lower == 'ss':
            result = 's'
            return result.upper() if consonants_upper else result
        
        # Handle 'c' and 'ch' variants for [k] sound → 'k'
        # Note: 'qu' is kept as-is (don't drop the 'u')
        if consonants_lower in ['c', 'ch']:
            # According to rules: [k] variants → 'k'
            result = 'k'
            return result.upper() if consonants_upper else result
        
        # Keep 'qu' as-is (don't convert to 'k', preserve the 'u')
        if consonants_lower == 'qu':
            return consonants
        
        # Handle double consonants (tt, nn, etc.) - simplify to single
        if len(consonants_lower) == 2 and consonants_lower[0] == consonants_lower[1]:
            result = consonants_lower[0]
            return result.upper() if consonants_upper else result
        
        # Default: return as-is
        return consonants
    
    def _apply_case_pattern(self, transformed: str, original: str) -> str:
        """
        Apply the case pattern from original word to transformed word.
        
        Handles:
        - All lowercase
        - All uppercase  
        - Title case (first letter capitalized)
        - Mixed case (tries to preserve pattern)
        
        Args:
            transformed: The transformed word
            original: Original word with desired case pattern
            
        Returns:
            Transformed word with case pattern applied
        """
        if not transformed or not original:
            return transformed
        
        # All uppercase
        if original.isupper():
            return transformed.upper()
        
        # All lowercase
        if original.islower():
            return transformed.lower()
        
        # Title case (first letter capital)
        if original[0].isupper() and (len(original) == 1 or original[1:].islower()):
            return transformed.capitalize()
        
        # Mixed case - do best effort
        # Apply pattern character by character where possible
        result = list(transformed.lower())
        for i, char in enumerate(original):
            if i < len(result):
                if char.isupper():
                    result[i] = result[i].upper()
        
        return ''.join(result)
    
    def get_transformation_info(self, word: str, is_sentence_start: bool = False) -> dict:
        """
        Get detailed information about how a word would be transformed.
        Useful for debugging and learning.
        
        Args:
            word: The word to analyze
            is_sentence_start: Whether this word starts a sentence
        
        Returns:
            Dictionary with transformation steps and metadata
        """
        info = {
            'original': word,
            'transformed': self._convert_word(word, is_sentence_start=is_sentence_start),
            'should_preserve': self.preservation_rules.should_preserve(word, is_sentence_start),
            'in_dictionary': word.lower() in ESTABLISHED_LEXICON,
        }
        
        # If not in dictionary and not preserved, show algorithmic breakdown
        if not info['in_dictionary'] and not info['should_preserve']:
            clean_word = word.strip("'")
            match = self.CONSONANT_PATTERN.match(clean_word)
            if match:
                consonants, rest = match.groups()
                adjusted = self._phonetic_adjust(consonants, rest)
                info['algorithm'] = {
                    'consonant_cluster': consonants,
                    'rest': rest,
                    'adjusted_consonants': adjusted,
                    'consonant_type': classify_consonant(adjusted),
                    'suffix': select_suffix(adjusted, seed=self.random_seed)[0],  # Get just the suffix string
                }
        
        return info


# Convenience function for quick conversions
def convert(text: str) -> str:
    """
    Quick conversion function (hybrid mode).
    
    Uses dictionary lookup for known words, algorithmic transformation for unknown words.
    
    Args:
        text: French text to convert
        
    Returns:
        Louchébem text
    """
    converter = LouchebemConverter()
    return converter.convert_text(text)

