"""
Test suite for Louchébem converter

Tests the converter against examples from the plan and validates
the hybrid approach.
"""

from largonji import LouchebemConverter, convert
from largonji.lexicon import ESTABLISHED_LEXICON
from largonji.suffixes import classify_consonant, get_suffix_info


def test_dictionary_words():
    """Test that known words from the dictionary are correctly returned"""
    print("=" * 60)
    print("TEST: Dictionary Words")
    print("=" * 60)
    
    converter = LouchebemConverter()
    
    # Test cases from the plan (section 3.1)
    test_cases = {
        'boucher': 'loucherbem',
        'argot': 'largomuche',
        'jargon': 'largonji',
        'fou': 'louf',
        'bonjour': 'lonjourbem',
        'merci': 'lercimuche',
        'café': 'laféquès',
        'sac': 'lacsé',
        'prix': 'liprem',
        'bon': 'lombem',
    }
    
    passed = 0
    failed = 0
    
    for french, expected in test_cases.items():
        result = converter.convert_text(french)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {french:15} → {result:20} (expected: {expected})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    if failed > 0:
        print(f"Failed: {failed}/{len(test_cases)}")
    print()
    
    return failed == 0


def test_consonant_clusters():
    """Test consonant cluster handling (section 2.1 of plan)"""
    print("=" * 60)
    print("TEST: Consonant Clusters")
    print("=" * 60)
    
    converter = LouchebemConverter(random_seed=42)
    
    # Examples from plan section 2.1
    test_cases = [
        ('prix', 'liprem'),  # pr cluster
        ('gras', 'lagrem'),  # gr cluster (from dictionary)
    ]
    
    passed = 0
    failed = 0
    
    for french, expected in test_cases:
        result = converter.convert_text(french)
        # For consonant cluster tests, we check structure not exact suffix
        # because suffixes are randomized
        if french in ESTABLISHED_LEXICON:
            matches = result == expected
        else:
            # Check that consonant cluster is preserved
            matches = 'pr' in result or 'gr' in result
        
        status = "✓" if matches else "✗"
        
        if matches:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {french:15} → {result:20}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    print()
    
    return failed == 0


def test_stopwords():
    """Test that stopwords are preserved (section 3.2 of plan)"""
    print("=" * 60)
    print("TEST: Stopword Preservation")
    print("=" * 60)
    
    converter = LouchebemConverter(preserve_stopwords=True)
    
    stopwords = ['le', 'la', 'les', 'de', 'un', 'une', 'et', 'à', 'du']
    
    passed = 0
    failed = 0
    
    for word in stopwords:
        result = converter.convert_text(word)
        matches = result == word
        status = "✓" if matches else "✗"
        
        if matches:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {word:15} → {result:20} (should be unchanged)")
    
    print(f"\nPassed: {passed}/{len(stopwords)}")
    print()
    
    return failed == 0


def test_vowel_initial_words():
    """Test that vowel-initial words are transformed using attack consonant"""
    print("=" * 60)
    print("TEST: Vowel-Initial Words (attack consonant)")
    print("=" * 60)
    
    converter = LouchebemConverter(random_seed=42)
    
    # Vowel-initial words should find attack consonant and transform
    test_cases = [
        ('entendre', 'enlendre'),  # en + t + endre → enlendre + t + suffix
        ('attention', 'alention'),  # a + tt (→t) + ention → alention + t + suffix
        ('orange', 'olange'),  # o + r + ange → olange + r + suffix
    ]
    
    passed = 0
    failed = 0
    
    for word, stem in test_cases:
        result = converter.convert_text(word)
        # Should be transformed (contains the stem)
        matches = stem in result
        
        status = "✓" if matches else "✗"
        
        if matches:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {word:15} → {result:20}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    print()
    
    return failed == 0


def test_l_initial_words():
    """Test L-initial words are transformed (L moves to end)"""
    print("=" * 60)
    print("TEST: L-Initial Words (transform)")
    print("=" * 60)
    
    converter = LouchebemConverter(random_seed=42)
    
    # L-initial words should be transformed: l + rest → l + rest + l + suffix
    # Note: doubled 'll' is simplified to 'l' by the doubled consonant fix
    test_cases = [
        ('large', 'largel'),  # l + arge + l + suffix → largel...
        ('long', 'lonl'),     # l + ong + l + suffix → longl... → lonl... (ll simplified)
        ('livre', 'livrel'),  # l + ivre + l + suffix → livrel...
    ]
    
    passed = 0
    failed = 0
    
    for word, expected_stem in test_cases:
        result = converter.convert_text(word)
        # Should be transformed (contains the stem)
        matches = expected_stem in result
        status = "✓" if matches else "✗"
        
        if matches:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {word:15} → {result:20}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    print()
    
    return failed == 0


def test_phrases():
    """Test full phrase conversion from plan (section 8)"""
    print("=" * 60)
    print("TEST: Full Phrases")
    print("=" * 60)
    
    converter = LouchebemConverter()
    
    # Test phrase from plan section 8
    phrase = "Bonjour monsieur le boucher"
    result = converter.convert_text(phrase)
    
    print(f"Input:  {phrase}")
    print(f"Output: {result}")
    
    # Check that key words are transformed
    checks = {
        'Bonjour → Lonjourbem': 'Lonjourbem' in result,
        'boucher → loucherbem': 'loucherbem' in result,
        'Stopword "le" preserved': ' le ' in result,
    }
    
    print("\nVerifications:")
    passed = 0
    for check, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"{symbol} {check}")
        if status:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(checks)}")
    print()
    
    return passed == len(checks)


def test_case_preservation():
    """Test that case patterns are preserved"""
    print("=" * 60)
    print("TEST: Case Preservation")
    print("=" * 60)
    
    converter = LouchebemConverter(preserve_case=True)
    
    test_cases = [
        ('boucher', 'lowercase'),
        ('Boucher', 'titlecase'),
        ('BOUCHER', 'uppercase'),
    ]
    
    passed = 0
    
    for word, case_type in test_cases:
        result = converter.convert_text(word)
        
        if case_type == 'lowercase':
            correct = result.islower()
        elif case_type == 'titlecase':
            correct = result[0].isupper() and result[1:].islower()
        elif case_type == 'uppercase':
            correct = result.isupper()
        else:
            correct = False
        
        status = "✓" if correct else "✗"
        if correct:
            passed += 1
        
        print(f"{status} {word:15} → {result:20} ({case_type})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    print()
    
    return passed == len(test_cases)


def test_suffix_organization():
    """Test that suffixes are organized by consonant type"""
    print("=" * 60)
    print("TEST: Suffix Organization by Consonant Type")
    print("=" * 60)
    
    # Test classification (updated to match current pattern names)
    consonant_patterns = {
        'b': 'pattern_b',
        'p': 'pattern_p',
        't': 'pattern_t',
        'd': 'pattern_d',
        'f': 'pattern_f',
        's': 'pattern_s',
        'm': 'pattern_m',
        'n': 'pattern_n',
        'r': 'pattern_r',
        'l': 'pattern_l',
    }
    
    passed = 0
    failed = 0
    
    for consonant, expected_pattern in consonant_patterns.items():
        result_pattern = classify_consonant(consonant)
        matches = result_pattern == expected_pattern
        status = "✓" if matches else "✗"
        
        if matches:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} '{consonant}' → {result_pattern:15} (expected: {expected_pattern})")
    
    print(f"\nPassed: {passed}/{len(consonant_patterns)}")
    print()
    
    return failed == 0


def test_conversion_modes():
    """Test hybrid conversion mode (dictionary + algorithmic)"""
    print("=" * 60)
    print("TEST: Hybrid Conversion Mode")
    print("=" * 60)
    
    # Use words both IN and NOT IN dictionary for testing
    text = "boucher robot"  # "boucher" in dict, "robot" not in dict
    
    # Hybrid mode: dictionary words preserved, unknown words transformed
    converter = LouchebemConverter(random_seed=42)
    result = converter.convert_text(text)
    print(f"Input:  {text}")
    print(f"Output: {result}")
    print()
    
    # Check that "boucher" → "loucherbem" (from dictionary)
    dict_ok = 'loucherbem' in result
    print(f"{'✓' if dict_ok else '✗'} Dictionary word 'boucher' → 'loucherbem': {dict_ok}")
    
    # Check that "robot" is transformed algorithmically (not left as-is)
    algo_ok = 'robot' not in result and 'lobo' in result
    print(f"{'✓' if algo_ok else '✗'} Unknown word 'robot' transformed: {algo_ok}")
    
    print()
    
    return dict_ok and algo_ok


def run_all_tests():
    """Run all test suites"""
    print("\n")
    print("█" * 60)
    print("  LOUCHÉBEM CONVERTER TEST SUITE")
    print("█" * 60)
    print("\n")
    
    tests = [
        ("Dictionary Words", test_dictionary_words),
        ("Consonant Clusters", test_consonant_clusters),
        ("Stopword Preservation", test_stopwords),
        ("Vowel-Initial Words", test_vowel_initial_words),
        ("L-Initial Words", test_l_initial_words),
        ("Full Phrases", test_phrases),
        ("Case Preservation", test_case_preservation),
        ("Suffix Organization", test_suffix_organization),
        ("Conversion Modes", test_conversion_modes),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"✗ {name} failed with error: {e}\n")
            results.append((name, False))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {total_passed}/{total_tests} test suites passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! The hybrid converter is working correctly.")
    else:
        print(f"\n⚠️  {total_tests - total_passed} test suite(s) need attention.")
    
    print()


if __name__ == "__main__":
    run_all_tests()

