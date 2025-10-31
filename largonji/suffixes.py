"""
Suffix selection system organized by consonant sound types.

Based on traditional louchébem usage patterns where suffixes follow
phonetic rules related to the final consonant sound.

Key insight: Most suffixes ALREADY contain their consonant!
- For 'f': suffixes are 'fok', 'fès', 'fé' (already start with 'f')
- For 'd': suffixes are 'dé', 'dem', 'di' (already start with 'd')
- Neutral suffixes like 'em', 'oc' don't contain a specific consonant

This design eliminates consonant doubling at the source.
"""

import random


# ============================================================================
# SUFFIX DEFINITIONS
# Each suffix dict contains:
# - suffix string as key
# - weight (relative frequency) as value
# ============================================================================

# D consonant: suffixes already contain 'd'
D_SUFFIXES = {
    'dé': 0.35,      # d + é
    'dem': 0.25,     # d + em
    'doc': 0.15,     # d + oc
    'di': 0.10,      # d + i
    'doque': 0.05,   # d + oque
    'dèque': 0.05,   # d + èque
    'dique': 0.05,   # d + ique
}

# S consonant: suffixes already contain 's'
S_SUFFIXES = {
    'sé': 0.30,      # s + é
    'sès': 0.20,     # s + ès
    'sic': 0.15,     # s + ic
    'se': 0.10,      # s + e
    'soc': 0.10,     # s + oc
    'sèque': 0.05,   # s + èque
    'sique': 0.05,   # s + ique
    'suche': 0.05,   # s + uche
}

# T consonant: suffixes already contain 't'
T_SUFFIXES = {
    'té': 0.30,      # t + é
    'tem': 0.25,     # t + em
    'tès': 0.15,     # t + ès
    'ti': 0.10,      # t + i
    'toc': 0.10,     # t + oc
    'tèque': 0.05,   # t + èque
    'tique': 0.05,   # t + ique
}

# V consonant: suffixes already contain 'v'
V_SUFFIXES = {
    'vé': 0.30,      # v + é
    'vem': 0.25,     # v + em
    'vès': 0.15,     # v + ès
    'vi': 0.10,      # v + i
    'voc': 0.10,     # v + oc
    'vèque': 0.05,   # v + èque
    'vique': 0.05,   # v + ique
}

# P consonant: suffixes already contain 'p'
P_SUFFIXES = {
    'puche': 0.30,   # p + uche
    'pem': 0.25,     # p + em
    'pé': 0.15,      # p + é
    'pic': 0.10,     # p + ic
    'poc': 0.10,     # p + oc
    'pèque': 0.05,   # p + èque
    'pique': 0.05,   # p + ique
}

# F consonant: suffixes already contain 'f'
F_SUFFIXES = {
    'fok': 0.25,     # f + ok
    'fès': 0.20,     # f + ès
    'fé': 0.15,      # f + é
    'fi': 0.10,      # f + i
    'foc': 0.10,     # f + oc
    'fèque': 0.05,   # f + èque
    'fique': 0.05,   # f + ique
    'fuche': 0.05,   # f + uche
    'fem': 0.05,     # f + em
}

# M consonant: suffixes already contain 'm'
M_SUFFIXES = {
    'muche': 0.35,   # m + uche
    'mé': 0.20,      # m + é
    'mem': 0.15,     # m + em
    'mi': 0.10,      # m + i
    'moc': 0.10,     # m + oc
    'mèque': 0.05,   # m + èque
    'mique': 0.05,   # m + ique
}

# N consonant: suffixes already contain 'n'
N_SUFFIXES = {
    'nem': 0.30,     # n + em
    'né': 0.25,      # n + é
    'noc': 0.15,     # n + oc
    'ni': 0.10,      # n + i
    'nuche': 0.10,   # n + uche
    'nèque': 0.05,   # n + èque
    'nique': 0.05,   # n + ique
}

# B consonant: suffixes already contain 'b'
B_SUFFIXES = {
    'bé': 0.30,      # b + é
    'boc': 0.20,     # b + oc
    'bem': 0.15,     # b + em
    'bès': 0.10,     # b + ès
    'bi': 0.10,      # b + i
    'bèque': 0.05,   # b + èque
    'bique': 0.05,   # b + ique
    'buche': 0.05,   # b + uche
}

# K consonant: suffixes already contain 'k'
K_SUFFIXES = {
    'ké': 0.30,      # k + é
    'kès': 0.20,     # k + ès
    'koc': 0.15,     # k + oc
    'kem': 0.10,     # k + em
    'ki': 0.10,      # k + i
    'kèque': 0.05,   # k + èque
    'kique': 0.05,   # k + ique
    'kuche': 0.05,   # k + uche
}

# C consonant: suffixes already contain 'c' (as 'qu' for phonetics)
C_SUFFIXES = {
    'qué': 0.30,     # c → qu (for phonetics)
    'quem': 0.20,    # c → qu + em
    'quoc': 0.15,    # c → qu + oc
    'quès': 0.10,    # c → qu + ès
    'qui': 0.10,     # c → qu + i
    'quèque': 0.05,  # c → qu + èque
    'quique': 0.05,  # c → qu + ique
    'quuche': 0.05,  # c → qu + uche
}

# QU consonant: suffixes already contain 'qu'
QU_SUFFIXES = {
    'qué': 0.30,     # qu + é (qu already contains u!)
    'quem': 0.20,    # qu + em
    'quoc': 0.15,    # qu + oc
    'quès': 0.10,    # qu + ès
    'qui': 0.10,     # qu + i
    'quèque': 0.05,  # qu + èque
    'quique': 0.05,  # qu + ique
    'quuche': 0.05,  # qu + uche
}

# G consonant: suffixes already contain 'g' (as 'gu' for phonetics)
G_SUFFIXES = {
    'gué': 0.30,     # g → gu (for phonetics)
    'guem': 0.20,    # g → gu + em
    'guoc': 0.15,    # g → gu + oc
    'guès': 0.10,    # g → gu + ès
    'gui': 0.10,     # g → gu + i
    'guèque': 0.05,  # g → gu + èque
    'guique': 0.05,  # g → gu + ique
    'guuche': 0.05,  # g → gu + uche
}

# R consonant: suffixes already contain 'r'
R_SUFFIXES = {
    'ré': 0.30,      # r + é
    'roc': 0.20,     # r + oc
    'rem': 0.15,     # r + em
    'ric': 0.10,     # r + ic
    'ri': 0.10,      # r + i
    'rèque': 0.05,   # r + èque
    'rique': 0.05,   # r + ique
    'ruche': 0.05,   # r + uche
}

# L consonant: suffixes already contain 'l'
L_SUFFIXES = {
    'lem': 0.30,     # l + em
    'loc': 0.20,     # l + oc
    'lé': 0.15,      # l + é
    'lic': 0.10,     # l + ic
    'li': 0.10,      # l + i
    'lèque': 0.05,   # l + èque
    'lique': 0.05,   # l + ique
    'luche': 0.05,   # l + uche
}

# Z consonant: suffixes already contain 'z'
Z_SUFFIXES = {
    'zé': 0.30,      # z + é
    'zès': 0.20,     # z + ès
    'zem': 0.15,     # z + em
    'zi': 0.10,      # z + i
    'zoc': 0.10,     # z + oc
    'zèque': 0.05,   # z + èque
    'zique': 0.05,   # z + ique
    'zuche': 0.05,   # z + uche
}

# J consonant: suffixes already contain 'j'
J_SUFFIXES = {
    'ji': 0.30,      # j + i
    'jé': 0.20,      # j + é
    'jem': 0.15,     # j + em
    'joc': 0.10,     # j + oc
    'jès': 0.10,     # j + ès
    'jèque': 0.05,   # j + èque
    'jique': 0.05,   # j + ique
    'juche': 0.05,   # j + uche
}

# CH consonant: suffixes already contain 'ch'
CH_SUFFIXES = {
    'ché': 0.25,     # ch + é
    'chem': 0.20,    # ch + em
    'choc': 0.15,    # ch + oc
    'che': 0.10,     # ch + e
    'chès': 0.10,    # ch + ès
    'chèque': 0.05,  # ch + èque
    'chique': 0.05,  # ch + ique
    'chuche': 0.05,  # ch + uche
    'chi': 0.05,     # ch + i
}

# DEFAULT: neutral suffixes for other consonants or clusters
DEFAULT_SUFFIXES = {
    'em': 0.30,
    'ème': 0.15,
    'é': 0.15,
    'ès': 0.10,
    'oc': 0.10,
    'ic': 0.10,
    'uche': 0.10,
}

# ============================================================================
# SUFFIX METADATA
# Defines which suffixes already contain their consonant
# ============================================================================

# Neutral suffixes that DON'T contain a specific consonant
# These need the consonant prepended: word + consonant + suffix
NEUTRAL_SUFFIXES = {
    'em', 'ème', 'é', 'ès', 'oc', 'ic', 'uche', 'oque', 
    'e', 'i', 'ok', 'o', 'a', 'u'
}

def suffix_contains_consonant(suffix: str) -> bool:
    """
    Check if a suffix already contains its consonant.
    
    Args:
        suffix: The suffix string (e.g., 'fok', 'em', 'dé')
        
    Returns:
        False if suffix is neutral (needs consonant prepended)
        True if suffix already contains the consonant
    """
    return suffix not in NEUTRAL_SUFFIXES


# ============================================================================
# SUFFIX MAPPING
# Maps consonants/clusters to their specific suffix patterns
# ============================================================================

SUFFIX_MAP = {
    'd': D_SUFFIXES,
    's': S_SUFFIXES,
    't': T_SUFFIXES,
    'v': V_SUFFIXES,
    'p': P_SUFFIXES,
    'f': F_SUFFIXES,
    'm': M_SUFFIXES,
    'n': N_SUFFIXES,
    'b': B_SUFFIXES,
    
    # Split K/C/QU into separate variants
    'k': K_SUFFIXES,
    'c': C_SUFFIXES,     # NEW: separate C suffixes
    'qu': QU_SUFFIXES,   # NEW: separate QU suffixes
    'q': QU_SUFFIXES,
    
    'g': G_SUFFIXES,
    'r': R_SUFFIXES,
    'l': L_SUFFIXES,
    'z': Z_SUFFIXES,
    'j': J_SUFFIXES,
    'ch': CH_SUFFIXES,
    
    # Common consonant clusters keep the last consonant's pattern
    'pr': R_SUFFIXES,
    'br': R_SUFFIXES,
    'tr': R_SUFFIXES,
    'dr': R_SUFFIXES,
    'cr': R_SUFFIXES,
    'gr': R_SUFFIXES,
    'fr': R_SUFFIXES,
    'vr': R_SUFFIXES,
    
    'pl': L_SUFFIXES,
    'bl': L_SUFFIXES,
    'cl': L_SUFFIXES,
    'gl': L_SUFFIXES,
    'fl': L_SUFFIXES,
    
    'sp': P_SUFFIXES,
    'st': T_SUFFIXES,
    'sc': C_SUFFIXES,    # CHANGED: use C_SUFFIXES
    'scr': R_SUFFIXES,
    'str': R_SUFFIXES,
    'spr': R_SUFFIXES,
    'spl': L_SUFFIXES,
}


def get_suffix_pattern(consonant_cluster: str) -> dict:
    """
    Get the appropriate suffix pattern for a consonant cluster.
    
    Args:
        consonant_cluster: The consonant(s) to find suffixes for
        
    Returns:
        Dictionary of suffix -> weight mappings
    """
    # Normalize to lowercase
    cluster_lower = consonant_cluster.lower()
    
    # Look up the cluster in SUFFIX_MAP
    if cluster_lower in SUFFIX_MAP:
        return SUFFIX_MAP[cluster_lower]
    
    # If cluster ends with a known consonant, use that pattern
    last_char = cluster_lower[-1]
    if last_char in SUFFIX_MAP:
        return SUFFIX_MAP[last_char]
    
    # Default to DEFAULT_SUFFIXES
    return DEFAULT_SUFFIXES


def classify_consonant(consonant_cluster: str) -> str:
    """
    Get a descriptive name for the consonant pattern.
    
    Args:
        consonant_cluster: The consonant(s) to classify
        
    Returns:
        Pattern name (e.g., 'pattern_f', 'pattern_d')
    """
    cluster_lower = consonant_cluster.lower()
    
    # Check if we have a direct mapping
    if cluster_lower in SUFFIX_MAP:
        # Get the pattern name from the suffix dict
        suffix_dict = SUFFIX_MAP[cluster_lower]
        
        # Map each suffix dict to a pattern name
        pattern_names = {
            id(D_SUFFIXES): 'pattern_d',
            id(S_SUFFIXES): 'pattern_s',
            id(T_SUFFIXES): 'pattern_t',
            id(V_SUFFIXES): 'pattern_v',
            id(P_SUFFIXES): 'pattern_p',
            id(F_SUFFIXES): 'pattern_f',
            id(M_SUFFIXES): 'pattern_m',
            id(N_SUFFIXES): 'pattern_n',
            id(B_SUFFIXES): 'pattern_b',
            id(K_SUFFIXES): 'pattern_k',
            id(C_SUFFIXES): 'pattern_c',
            id(QU_SUFFIXES): 'pattern_qu',
            id(G_SUFFIXES): 'pattern_g',
            id(R_SUFFIXES): 'pattern_r',
            id(L_SUFFIXES): 'pattern_l',
            id(Z_SUFFIXES): 'pattern_z',
            id(J_SUFFIXES): 'pattern_j',
            id(CH_SUFFIXES): 'pattern_ch',
            id(DEFAULT_SUFFIXES): 'pattern_default',
        }
        
        return pattern_names.get(id(suffix_dict), 'pattern_unknown')
    
    return 'pattern_default'


def select_suffix(consonant_cluster: str, seed: int | None = None) -> tuple[str, bool]:
    """
    Select a suffix based on the consonant cluster using weighted random choice.
    
    Follows traditional louchébem patterns where suffixes are chosen based on
    the final consonant sound for phonetic harmony.
    
    Args:
        consonant_cluster: The consonant(s) moved to the end of the word
        seed: Optional random seed for deterministic output (useful for testing)
        
    Returns:
        Tuple of (suffix_string, needs_consonant_prepended)
        - suffix_string: The suffix to add (e.g., 'fok', 'em', 'dé')
        - needs_consonant_prepended: True if consonant should be added before suffix
    """
    # Get the appropriate suffix pattern
    suffix_weights = get_suffix_pattern(consonant_cluster)
    
    # Set seed if provided (for testing/reproducibility)
    if seed is not None:
        random.seed(seed)
    
    # Weighted random choice
    suffixes = list(suffix_weights.keys())
    weights = list(suffix_weights.values())
    
    selected_suffix = random.choices(suffixes, weights=weights, k=1)[0]
    
    # Check if this suffix needs the consonant prepended
    needs_consonant = not suffix_contains_consonant(selected_suffix)
    
    return (selected_suffix, needs_consonant)


def get_all_suffixes() -> list[str]:
    """
    Get a list of all possible suffixes across all patterns.
    
    Returns:
        Sorted list of unique suffix strings
    """
    all_suffixes = set()
    
    # Collect from all suffix dictionaries
    for suffix_dict in [D_SUFFIXES, S_SUFFIXES, T_SUFFIXES, V_SUFFIXES, 
                        P_SUFFIXES, F_SUFFIXES, M_SUFFIXES, N_SUFFIXES,
                        B_SUFFIXES, K_SUFFIXES, C_SUFFIXES, QU_SUFFIXES,
                        G_SUFFIXES, R_SUFFIXES, L_SUFFIXES, Z_SUFFIXES,
                        J_SUFFIXES, CH_SUFFIXES, DEFAULT_SUFFIXES]:
        all_suffixes.update(suffix_dict.keys())
    
    return sorted(all_suffixes)


def get_suffix_info(consonant_cluster: str) -> dict:
    """
    Get detailed information about suffix selection for a consonant cluster.
    
    Useful for debugging and understanding the suffix system.
    
    Args:
        consonant_cluster: The consonant(s) to analyze
        
    Returns:
        Dictionary with suffix information
    """
    pattern = get_suffix_pattern(consonant_cluster)
    pattern_name = classify_consonant(consonant_cluster)
    
    return {
        'consonant_cluster': consonant_cluster,
        'pattern_name': pattern_name,
        'available_suffixes': list(pattern.keys()),
        'weights': pattern,
        'total_weight': sum(pattern.values()),
    }
