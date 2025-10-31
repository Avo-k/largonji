"""
Louchébem Converter Demo

Demonstrates the hybrid Louchébem converter with various examples.
"""

from largonji import LouchebemConverter


def demo_basic():
    """Basic conversion examples"""
    print("=" * 60)
    print("BASIC LOUCHÉBEM CONVERSION (Hybrid)")
    print("=" * 60)
    
    converter = LouchebemConverter()
    
    examples = [
        "boucher",
        "sac",
        "café",
        "prix",
        "bonjour",
        "merci",
        "fromage",
    ]
    
    for word in examples:
        result = converter.convert_text(word)
        print(f"{word:15} → {result}")
    
    print()


def demo_phrases():
    """Full phrase conversion"""
    print("=" * 60)
    print("PHRASE CONVERSION (Hybrid)")
    print("=" * 60)
    
    converter = LouchebemConverter()
    
    phrases = [
        "Bonjour monsieur le boucher!",
        "Je voudrais un bon morceau de viande.",
        "Le prix est trop cher.",
        "Merci pour le café.",
    ]
    
    for phrase in phrases:
        result = converter.convert_text(phrase)
        print(f"Original: {phrase}")
        print(f"Louchébem: {result}")
        print()


def demo_consonant_clusters():
    """Show consonant cluster handling"""
    print("=" * 60)
    print("CONSONANT CLUSTER HANDLING")
    print("=" * 60)
    
    converter = LouchebemConverter()
    
    examples = [
        ("prix", "pr"),
        ("froid", "fr"),
        ("gras", "gr"),
        ("train", "tr"),
        ("plan", "pl"),
        ("script", "scr"),
    ]
    
    print("French consonant clusters are preserved:")
    for word, cluster in examples:
        result = converter.convert_text(word)
        print(f"  {word:12} ({cluster:3}) → {result}")
    
    print()


def demo_vowel_initial_words():
    """Show vowel-initial word handling (NEW!)"""
    print("=" * 60)
    print("VOWEL-INITIAL WORDS (Attack Consonant)")
    print("=" * 60)
    
    converter = LouchebemConverter(random_seed=42)
    
    print("Based on French rules: find first 'attack consonant' after vowel")
    print()
    
    examples = [
        ("entendre", "en + t + endre"),
        ("attention", "a + tt + ention"),
        ("isolation", "i + s + olation (s→z)"),
        ("orange", "o + r + ange"),
        ("animal", "a + n + imal"),
    ]
    
    for word, explanation in examples:
        result = converter.convert_text(word)
        print(f"  {word:12} → {result:20} [{explanation}]")
    
    print()


def demo_suffix_info():
    """Show suffix selection information"""
    print("=" * 60)
    print("SUFFIX SELECTION BY CONSONANT")
    print("=" * 60)
    
    from largonji import get_suffix_info
    
    consonant_examples = [
        ('b', 'boucher'),
        ('p', 'prix'),
        ('s', 'sac'),
        ('d', 'date'),
        ('t', 'train'),
        ('v', 'ville'),
        ('f', 'fou'),
        ('m', 'merci'),
        ('n', 'non'),
        ('r', 'rue'),
        ('pr', 'prix (cluster)'),
        ('fr', 'froid (cluster)'),
        ('scr', 'script (cluster)'),
    ]
    
    for consonant, example in consonant_examples:
        info = get_suffix_info(consonant)
        print(f"\n{consonant.upper():4} ({example})")
        print(f"  Pattern: {info['pattern_name']}")
        # Get most likely suffix (highest weight)
        suffixes_weights = info['weights']
        most_likely = max(suffixes_weights.items(), key=lambda x: x[1])[0]
        print(f"  Most likely suffix: -{most_likely}")
        print(f"  Top choices: {', '.join(f'-{s}' for s in list(info['available_suffixes'])[:3])}")


def demo_transformation_details():
    """Show detailed transformation breakdown"""
    print("=" * 60)
    print("TRANSFORMATION DETAILS")
    print("=" * 60)
    
    converter = LouchebemConverter(random_seed=42)
    
    words = ['boucher', 'steak', 'poison', 'fromage', 'entendre', 'train']
    
    for word in words:
        info = converter.get_transformation_info(word)
        print(f"\n{word.upper()}")
        print(f"  Transformed: {info['transformed']}")
        print(f"  In dictionary: {info['in_dictionary']}")
        
        if 'algorithm' in info:
            algo = info['algorithm']
            print("  Algorithm breakdown:")
            print(f"    Consonants: {algo['consonant_cluster']}")
            print(f"    Rest: {algo['rest']}")
            print(f"    Adjusted: {algo['adjusted_consonants']}")
            print(f"    Pattern: {algo['consonant_type']}")
            print(f"    Suffix: -{algo['suffix']}")


def demo_preservation_rules():
    """Demonstrate the new word preservation rules"""
    print("=" * 60)
    print("WORD PRESERVATION RULES (NEW!)")
    print("=" * 60)
    print()
    
    converter = LouchebemConverter()
    
    categories = {
        'Ultra-Common Verbs (être, avoir, faire, aller)': [
            'Je suis un boucher.',
            'Il a fait un travail.',
            'Nous allons manger.',
            'Vous avez raison.',
        ],
        'Interjections & Onomatopoeia': [
            'Oh! Quel beau steak!',
            'Aïe! Le couteau!',
            'Boom! Paf! Vlan!',
        ],
        'Numbers & Dates (digits, Roman numerals)': [
            'En 1881, le XVIIIe siècle.',
            'Le 1er janvier 1900.',
            'Article IV, section 2e.',
        ],
        'Proper Nouns (names, places)': [
            'Jean Richepin habitait Paris.',
            'Gaston Esnault et Marie Dupont.',
        ],
        'Acronyms': [
            'M. le président de la SNCF.',
            'Dr. Martin et Mme Leblanc.',
        ],
        'Already Louchébem words': [
            'Le loucherbem parle largonji.',
            'Un lonjourbem au lobo garçon.',
        ],
    }
    
    for category, examples in categories.items():
        print(f"📌 {category}")
        print()
        for example in examples:
            result = converter.convert_text(example)
            print(f"   {example}")
            print(f"   → {result}")
            print()
        print()


def demo_long_text():
    """Test on a longer text about Largonji/Louchébem"""
    print("=" * 60)
    print("LONG TEXT TEST (Wikipedia excerpt)")
    print("=" * 60)
    print()
    
    converter = LouchebemConverter()
    
    # Text from Wikipedia about Largonji/Louchébem
    original_text = """Le pig latin est un argot principalement utilisé en anglais, équivalent au louchébem (largonji) en français : un mélange de verlan (pour le renversement des syllabes) et de javanais (pour l'ajout systématique d'une syllabe)[1]. Une autre dénomination employée par les Britanniques pour pig latin est backslang (à ne pas confondre avec le backslang utilisé par les criminels londoniens du XIXe siècle).

Le pig latin est souvent pratiqué par les enfants pour s'amuser ou pour converser de manière relativement confidentielle pour ne pas être compris des adultes ou des autres enfants[2]. Réciproquement, les adultes l'emploient parfois pour discuter de sujets sensibles qu'ils ne veulent pas dévoiler aux enfants en bas âge. Les touristes anglophones y ont recours parfois pour obscurcir leurs conversations quand ils voyagent dans des pays où l'anglais est couramment parlé comme première langue étrangère."""
    
    print("Original text (first 200 chars):")
    print(f"  {original_text[:200]}...")
    print()
    
    print("Converting entire text...")
    converted_text = converter.convert_text(original_text)
    
    print()
    print("Converted text (first 300 chars):")
    print(f"  {converted_text[:300]}...")
    print()
    
    print("Full comparison (first paragraph):")
    first_para = original_text.split('\n\n')[0]
    converted_para = converter.convert_text(first_para)
    
    print()
    print("ORIGINAL:")
    print(f"  {first_para}")
    print()
    print("LOUCHÉBEM:")
    print(f"  {converted_para}")
    print()
    
    # Word count
    words_original = len(first_para.split())
    words_converted = len(converted_para.split())
    print("Statistics:")
    print(f"  Original words: {words_original}")
    print(f"  Converted words: {words_converted}")
    print(f"  Dictionary hits: {sum(1 for w in first_para.split() if converter._convert_word(w.strip('.,;:!?\"()[]')) != w.strip('.,;:!?\"()[]'))}")
    print()


def demo_interactive():
    """Interactive mode"""
    print("=" * 60)
    print("INTERACTIVE LOUCHÉBEM CONVERTER (Hybrid)")
    print("=" * 60)
    print("Enter French text to convert (or 'quit' to exit)")
    print()
    
    converter = LouchebemConverter()
    
    while True:
        try:
            text = input("French: ")
            if text.lower() in ['quit', 'exit', 'q']:
                break
            
            result = converter.convert_text(text)
            print(f"Louchébem: {result}")
            print()
            
        except KeyboardInterrupt:
            print("\n")
            break
        except EOFError:
            break


def main():
    """Run all demos"""
    print("\n")
    print("█" * 60)
    print("  LOUCHÉBEM CONVERTER - Hybrid Implementation")
    print("  French Butcher's Argot Generator")
    print("█" * 60)
    print("\n")
    
    demo_basic()
    demo_phrases()
    demo_consonant_clusters()
    demo_vowel_initial_words()
    demo_preservation_rules()
    demo_suffix_info()
    demo_transformation_details()
    demo_long_text()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("Use demo_interactive() for interactive mode.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
