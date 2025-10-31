# 🔪 Largonji

[![PyPI version](https://badge.fury.io/py/largonji.svg)](https://badge.fury.io/py/largonji)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> _« Larlépem-vous louchébem? »_ — Hybrid French ↔ Louchébem converter

**[🇫🇷 Version française / French version →](README.md)**

A modern Python converter to transform French into **louchébem**, the historical slang of Parisian butchers.

**[Louchébem](https://fr.wikipedia.org/wiki/Largonji#Définition)** is the main variant of **[largonji](https://fr.wikipedia.org/wiki/Largonji)** ([English Wikipedia](https://en.wikipedia.org/wiki/Louchébem)), a family of linguistic deformation techniques used in French slang (including also javanais and other variants).

This package implements **louchébem** with a **hybrid approach**: dictionary of authentic historical terms + algorithmic transformation for unknown words.

---

## 📖 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [What is Louchébem?](#-what-is-louchébem)
- [The Naive Approach](#-the-naive-approach)
- [Our Implementation Choices](#-our-implementation-choices)
- [Advanced Configuration](#-advanced-configuration)
- [Sources & Acknowledgments](#-sources--acknowledgments)
- [License](#-license)

---

## 🚀 Installation

```bash
# With uv (recommended)
uv add largonji

# With pip
pip install largonji
```

---

## 💻 Quick Start

```python
from largonji import LouchebemConverter

# Create a converter
converter = LouchebemConverter()

# Convert a word
print(converter.convert_text("boucher"))
# → loucherbem

# Convert a sentence
print(converter.convert_text("Bonjour monsieur le boucher"))
# → Lonjourbem lonsieurmic le loucherbem

# With custom configuration
from largonji import LouchebemConfig

config = LouchebemConfig(
    preserve_stopwords=False,  # Also transform function words
    preserve_proper_nouns=False,  # Transform proper nouns
)
converter = LouchebemConverter(config=config)
```

---

## 🥩 What is Louchébem?

**[Louchébem](https://en.wikipedia.org/wiki/Louchébem)** is the main variant of **[largonji](https://fr.wikipedia.org/wiki/Largonji)**, a family of linguistic deformation techniques developed in French slang. Louchébem was created and popularized by Parisian butchers in the 19th century.

The word "**louchébem**" itself comes from transforming "**boucher**" (butcher) according to the process's rules.

### 📜 A Bit of History

Largonji appeared in the slang of Parisian working classes from the late 18th or early 19th century. The earliest recorded words include:
- **lomben** (← bon, "good") in an 1821 slang glossary
- **La Lorcefé** (← La Force, a Parisian prison) in Vidocq's Memoirs (1828-1829)
- **loucherbem** (← boucher, "butcher") attested around 1876

Louchébem is still used in the 21st century in the professional butcher community, particularly in Parisian markets and slaughterhouses.

### 🎯 The Basic Principle

The louchébem process follows a simple rule:

1. **Replace** the first consonant (or consonant cluster) with "**l**"
2. **Move** that consonant to the end of the word
3. **Add** a suffix (often related to the moved consonant)

**Examples:**
- **b**oucher → **l**oucher**b**em
- **j**argon → **l**argon**j**i
- **p**rix → **l**i**pr**em

---

## 🔧 The Naive Approach

A basic louchébem implementation might look like this:

```python
def louchebem_naive(word):
    """Simplified version (only works for basic cases)"""
    if not word:
        return word
    
    # Extract first consonant
    first_consonant = word[0]
    rest = word[1:]
    
    # Build transformed word
    return 'l' + rest + first_consonant + 'em'

# Examples
print(louchebem_naive("boucher"))  # → loucherbem ✓
print(louchebem_naive("prix"))     # → lixprem ✗ (should be liprem)
print(louchebem_naive("entendre")) # → lntendree ✗ (should be enlendreté)
```

### ⚠️ Limitations of the Naive Approach

This method doesn't handle:
- **Consonant clusters** (pr, tr, fr, etc.)
- **Vowel-initial words**
- **Silent consonants** at word end (discret → discrè)
- **French phonetics** (qu, gu, s/z, etc.)
- **Varied suffixes** based on consonant type
- **Historical words** with established spelling

Our hybrid implementation solves all these problems! 🎉

---

## ✨ Our Implementation Choices

This section details the technical decisions that make this converter high-quality.

### 1. 📚 Hybrid Approach: Dictionary + Algorithm

**Problem:** Some louchébem words have established historical spelling that may differ from algorithmic transformation.

**Solution:** 
- **Dictionary** of ~100 authentic historical words (sources: Lorédan Larchey 1858, Gaston Esnault 1965, louchebem.fr)
- **Algorithmic transformation** for unlisted words
- Dictionary takes priority when word exists

```python
# Example: "argot" is in the dictionary
converter.convert_text("argot")  # → largomuche (historical form)

# "robot" doesn't exist in the dictionary
converter.convert_text("robot")  # → lobotrem (algorithmic transformation)
```

---

### 2. 🎵 Multi-Consonant Clusters

**Problem:** How to handle "prix", "train", "fromage" that start with 2+ consonants?

**Solution:** Extract the **complete cluster** of consonants before the first vowel and move it as a block.

```python
"prix"    → "p" + "r" + "ix" → l + ix + pr + em → "liprem"
"train"   → "t" + "r" + "ain" → l + ain + tr + oc → "laintroc"
"fromage" → "f" + "r" + "omage" → l + omage + fr + é → "lomagefré"
```

**Technical detail:** Clusters are **always preserved in full**, even if the suffix already contains one of the letters (e.g., "pl" stays "pl", not just "p").

---

### 3. 🔤 Vowel-Initial Words

**Problem:** How to transform "entendre", "attention", "orange" that start with a vowel?

**Solution:** Find the **attack consonant** (first consonant cluster **after** the initial vowel sound).

```python
"entendre"  → "en" (nasal vowel) + "t" (attack) + "endre"
            → en + l + endre + t + é
            → "enlendreté"

"attention" → "a" + "tt" → "t" (simplified) + "ention"
            → a + l + ention + t + em
            → "alentiontem"

"orange"    → "o" + "r" + "ange"
            → o + l + ange + r + em
            → "olangrem"
```

**Tip:** The code handles nasal vowels ("an", "en", "in", "on", "un") as vowel sounds.

---

### 4. 🎯 Weighted Suffixes by Consonant Type

**Problem:** Not all suffixes are equally probable. Historically, certain suffixes match better with certain consonants.

**Solution:** **Weighted random** suffix selection organized by consonant, based on historical usage.

```python
# Example suffixes for different consonants
D → dé (35%), dem (25%), doc (5%), dique (5%), ...
P → pem (30%), puche (25%), poc (15%), pique (5%), ...
F → fès (35%), foc (20%), fem (15%), fique (10%), ...
```

Each suffix **already contains its consonant** to ensure phonetic harmony.

---

### 5. 🔇 Silent Consonants and Phonetic Adjustments

**Problem:** Written French ≠ spoken French. How to handle silent consonants?

**Solution:** Detection and removal of silent consonants with vowel adjustments.

```python
"discret"  → discrè + t (silent removed, e→è to preserve sound)
           → l + iscrè + d + em
           → "liscrèdem"

"employée" → employé (ée→é, extra 'e' is silent)
           → e + l + oyé + pl + oc
           → "emloyéploc"

"parler"   → parlé (er→é, identical sound)
           → l + arlé + p + em
           → "larlépem"
```

**Applied rules:**
- `-et` → `-è` (discret → discrè)
- `-ent` → `-en` (moment → momen, 't' is silent)
- `-er` → `-é` (infinitive verbs)
- `-ée` → `-é` (extra 'e' is redundant)

---

### 6. 🎲 Doubled Consonant Simplification

**Problem:** What to do with "attention" (two 't's)? What if we create duplicates (pl + lé = pllé)?

**Solution:** 
- **Before moving:** Simplify doubled consonants (tt→t, nn→n, mm→m)
- **After construction:** Simplify any accidentally created duplicates

```python
"attention" → "a" + "tt" → "a" + "t" (simplified) + "ention"
            → alentiontem

"employée"  → "em" + "pl" + "oyé" 
            → em + l + oyé + pl + lé
            → emloyépllé → emloyéplé (pll→pl simplified)
```

---

### 7. 🛡️ Selective Word Preservation

**Problem:** Transforming all words makes text unreadable. Which words to preserve?

**Solution:** System of individually toggleable preservation rules:

| Category | Examples | Reason |
|----------|----------|--------|
| **Function words** | le, la, de, un, et, à | Grammatical structure |
| **Ultra-common verbs** | être, avoir, faire, aller | Readability |
| **Interjections** | oh, ah, hein, ben | Oral expression |
| **Numbers & dates** | 123, XIV, 31/12/2023 | Precise information |
| **Proper nouns** | Paris, Marie | Identification |
| **Acronyms** | SNCF, UNESCO | Abbreviations |
| **Already louchébem** | loucherbem, louf | Avoid double transformation |

```python
# Disable certain preservations
config = LouchebemConfig(
    preserve_stopwords=True,        # Keep "le", "la", etc.
    preserve_proper_nouns=False,    # Transform "Paris" too!
    preserve_numbers=True,          # Keep "123"
)
converter = LouchebemConverter(config=config)
```

---

### 8. 📝 Apostrophe Handling (Elisions)

**Problem:** How to handle "l'argot", "d'autre", "j'aime"?

**Solution:** Specific rules based on prefix:

```python
# Special case: l' + word → merge
"l'argot"   → "largot" → "largomuche" (then check dictionary)
"l'origine" → "lorigine" → "loriginlé"

# Other apostrophes: preserve prefix
"d'autre" → "d'" + "autre" transformed → "d'autrelé"
"j'aime"  → "j'" + "aime" transformed → "j'aimelé"
```

**Logic:** Merging with 'l' makes sense since the word will start with 'l' anyway!

---

### 9. 🔤 Handling "qu" Cluster

**Problem:** "qu" is a digraph representing the [k] sound. How to handle it?

**Solution:** Treat "qu" as an **indivisible unit** (don't remove the 'u').

```python
"équivalent" → "é" + "qu" + "ivalen" (ent→en, 't' silent)
             → é + l + uivalen + qu + em
             → "éluivalenquem"  # "qu" stays together!
```

**Phonetics:** "k" and "qu" are treated as variants of the same sound, but the 'u' stays with the 'q'.

---

### 10. 💅 Case Preservation

**Problem:** How to preserve capitalization?

**Solution:** Detection and application of original case pattern.

```python
"Bonjour"  → "Lonjourbem"  (Title case)
"BOUCHER"  → "BOUCHER"     (All caps = proper noun, preserved)
"bonjour"  → "lonjourbem"  (lowercase)
```

---

## ⚙️ Advanced Configuration

The converter offers many configuration options:

```python
from largonji import LouchebemConfig, LouchebemConverter

# Maximum configuration (default behavior)
config = LouchebemConfig.maximal()

# Minimal configuration (transforms almost everything)
config = LouchebemConfig.minimal()

# Configuration for reproducible tests
config = LouchebemConfig.for_testing(seed=42)

# Custom configuration
config = LouchebemConfig(
    # Preservation
    preserve_stopwords=True,
    preserve_ultra_common_verbs=True,
    preserve_interjections=True,
    preserve_numbers=True,
    preserve_proper_nouns=True,
    preserve_acronyms=True,
    preserve_already_louchebem=True,
    
    # Features
    enable_apostrophe_merging=True,
    enable_l_initial_transform=True,
    enable_silent_consonants=True,
    enable_doubled_consonant_simplification=True,
    enable_infinitive_verbs=True,
    
    # Behavior
    preserve_case=True,
    preserve_punctuation=True,
    random_seed=None,  # For random suffixes
)

converter = LouchebemConverter(config=config)
```

---

## 📚 Sources & Acknowledgments

This project is based on rigorous historical and linguistic sources:

### Primary Sources

- **[Wikipedia - Largonji](https://fr.wikipedia.org/wiki/Largonji)** (French): Detailed article on the history and processes of largonji
- **[louchebem.fr](https://louchebem.fr/)**: The reference site for louchébem, with translator and examples
- **Lorédan Larchey** (1858, 1878): _Dictionnaire historique d'argot_ — First recordings of louchébem
- **Gaston Esnault** (1965): _Dictionnaire historique des argots français_ — Major academic reference

### Additional Sources

- **Albert Dauzat** (1946): _Les argots_ — Analysis of the louchébem process
- **Le Canard Enchaîné**: Article "Voyage dans les microlangues" — Contemporary state of louchébem
- **Sylvain Macouin**: "À propos du Ladukteurtrès Largonjem" — Analysis of automatic transformation challenges
- **Jacques Haddad**: Documentation on historical louchébem

### Technical Inspiration

Thanks to the developers of [louchebem.fr](https://louchebem.fr/) for their work in preserving this slang and their online translator which served as a reference.

---

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- ➕ Add words to the historical dictionary

---

<div align="center">

**Made with ❤️ to preserve the largonji of the louchébems**

_« Dans le gigot, tout est bon ! »_ (In the leg, everything is good!)

</div>

