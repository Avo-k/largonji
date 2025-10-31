# 🔪 Largonji

[![PyPI version](https://badge.fury.io/py/largonji.svg)](https://badge.fury.io/py/largonji)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> _« Larlépem-vous louchébem? »_ — Convertisseur hybride français ↔ louchébem

**[🇬🇧 English version / Version anglaise →](README_EN.md)**

Un convertisseur Python moderne pour transformer du français en **louchébem**, l'argot historique des bouchers parisiens. 

Le **[louchébem](https://fr.wikipedia.org/wiki/Largonji#Définition)** est la variante principale du **[largonji](https://fr.wikipedia.org/wiki/Largonji)**, une famille de procédés de déformation linguistique utilisés en argot français (incluant aussi le javanais et d'autres variantes).

Ce package implémente le **louchébem** avec une approche **hybride** : dictionnaire de termes historiques authentiques + transformation algorithmique pour les mots inconnus.

---

## 📖 Table des matières

- [Installation](#-installation)
- [Utilisation rapide](#-utilisation-rapide)
- [Qu'est-ce que le louchébem ?](#-quest-ce-que-le-louchébem-)
- [La méthode naïve](#-la-méthode-naïve)
- [Nos choix d'implémentation](#-nos-choix-dimplémentation)
- [Configuration avancée](#-configuration-avancée)
- [Sources et remerciements](#-sources-et-remerciements)
- [Licence](#-licence)

---

## 🚀 Installation

```bash
# Avec uv (recommandé)
uv add largonji

# Avec pip
pip install largonji
```

---

## 💻 Utilisation rapide

```python
from largonji import LouchebemConverter

# Créer un convertisseur
converter = LouchebemConverter()

# Convertir un mot
print(converter.convert_text("boucher"))
# → loucherbem

# Convertir une phrase
print(converter.convert_text("Bonjour monsieur le boucher"))
# → Lonjourbem lonsieurmic le loucherbem

# Avec configuration personnalisée
from largonji import LouchebemConfig

config = LouchebemConfig(
    preserve_stopwords=False,  # Transformer aussi les mots-outils
    preserve_proper_nouns=False,  # Transformer les noms propres
)
converter = LouchebemConverter(config=config)
```

---

## 🥩 Qu'est-ce que le louchébem ?

Le **[louchébem](https://fr.wikipedia.org/wiki/Largonji)** est la principale variante du **[largonji](https://fr.wikipedia.org/wiki/Largonji)**, une famille de procédés de déformation linguistique développés en argot français. Le louchébem a été créé et popularisé par les bouchers parisiens au XIXe siècle. 

Le mot « **louchébem** » lui-même vient de la transformation de « **boucher** » selon les règles du procédé.

### 📜 Un peu d'histoire

Le largonji apparaît dans l'argot des classes populaires parisiennes dès la fin du XVIIIe ou début du XIXe siècle. Les premiers mots recensés incluent :
- **lomben** (← bon) dans un glossaire argotique de 1821
- **La Lorcefé** (← La Force, une prison parisienne) dans les Mémoires de Vidocq (1828-1829)
- **loucherbem** (← boucher) attesté vers 1876

Le louchébem reste encore utilisé au XXIe siècle dans le milieu professionnel des bouchers, notamment dans les marchés et abattoirs parisiens.

### 🎯 Le principe de base

Le procédé du louchébem suit une règle simple :

1. **Remplacer** la première consonne (ou groupe de consonnes) par « **l** »
2. **Déplacer** cette consonne à la fin du mot
3. **Ajouter** un suffixe (souvent en rapport avec la consonne déplacée)

**Exemples :**
- **b**oucher → **l**oucher**b**em
- **j**argon → **l**argon**j**i
- **p**rix → **l**i**pr**em

---

## 🔧 La méthode naïve

Une implémentation basique du louchébem pourrait ressembler à ceci :

```python
def louchebem_naif(mot):
    """Version simplifiée (ne fonctionne que pour les cas basiques)"""
    if not mot:
        return mot
    
    # Extraire la première consonne
    premiere_consonne = mot[0]
    reste = mot[1:]
    
    # Construire le mot transformé
    return 'l' + reste + premiere_consonne + 'em'

# Exemples
print(louchebem_naif("boucher"))  # → loucherbem ✓
print(louchebem_naif("prix"))     # → lixprem ✗ (devrait être liprem)
print(louchebem_naif("entendre")) # → lntendree ✗ (devrait être enlendreté)
```

### ⚠️ Limites de l'approche naïve

Cette méthode ne gère pas :
- Les **groupes de consonnes** (pr, tr, fr, etc.)
- Les **mots commençant par une voyelle** 
- Les **consonnes muettes** en fin de mot (discret → discrè)
- La **phonétique française** (qu, gu, s/z, etc.)
- Les **suffixes variés** selon la consonne
- Les **mots historiques** avec orthographe établie

Notre implémentation hybride résout tous ces problèmes ! 🎉

---

## ✨ Nos choix d'implémentation

Cette section détaille les décisions techniques qui font la qualité de ce convertisseur.

### 1. 📚 Approche hybride : Dictionnaire + Algorithme

**Problème :** Certains mots de louchébem ont une orthographe historique établie qui peut différer de la transformation algorithmique.

**Solution :** 
- **Dictionnaire** de ~100 mots historiques authentiques (sources : Lorédan Larchey 1858, Gaston Esnault 1965, louchebem.fr)
- **Transformation algorithmique** pour les mots non répertoriés
- Priorité au dictionnaire quand le mot existe

```python
# Exemple : "argot" est dans le dictionnaire
converter.convert_text("argot")  # → largomuche (forme historique)

# "robot" n'existe pas dans le dictionnaire
converter.convert_text("robot")  # → lobotrem (transformation algorithmique)
```

---

### 2. 🎵 Groupes de consonnes multiples

**Problème :** Comment traiter "prix", "train", "fromage" qui commencent par 2+ consonnes ?

**Solution :** Extraire le **groupe complet** de consonnes avant la première voyelle et le déplacer en bloc.

```python
"prix"    → "p" + "r" + "ix" → l + ix + pr + em → "liprem"
"train"   → "t" + "r" + "ain" → l + ain + tr + oc → "laintroc"
"fromage" → "f" + "r" + "omage" → l + omage + fr + é → "lomagefré"
```

**Détail technique :** Les clusters sont **toujours conservés intégralement**, même si le suffixe contient déjà l'une des lettres (ex : "pl" reste "pl", pas seulement "p").

---

### 3. 🔤 Mots commençant par une voyelle

**Problème :** Comment transformer "entendre", "attention", "orange" qui commencent par une voyelle ?

**Solution :** Chercher la **consonne d'attaque** (premier groupe de consonnes **après** le son voyelle initial).

```python
"entendre"  → "en" (voyelle nasale) + "t" (attaque) + "endre"
            → en + l + endre + t + é
            → "enlendreté"

"attention" → "a" + "tt" → "t" (simplifié) + "ention"
            → a + l + ention + t + em
            → "alentiontem"

"orange"    → "o" + "r" + "ange"
            → o + l + ange + r + em
            → "olangrem"
```

**Astuce :** Le code gère les voyelles nasales ("an", "en", "in", "on", "un") comme des sons voyelle.

---

### 4. 🎯 Suffixes pondérés par type de consonne

**Problème :** Tous les suffixes ne sont pas équiprobables. Historiquement, certains suffixes correspondent mieux à certaines consonnes.

**Solution :** Sélection **aléatoire pondérée** de suffixes organisés par consonnes, basée sur l'usage historique.

```python
# Exemples de suffixes pour différentes consonnes
D → dé (35%), dem (25%), doc (5%), dique (5%), ...
P → pem (30%), puche (25%), poc (15%), pique (5%), ...
F → fès (35%), foc (20%), fem (15%), fique (10%), ...
```

Chaque suffixe **contient déjà sa consonne** pour garantir l'harmonie phonétique.

---

### 5. 🔇 Consonnes muettes et ajustements phonétiques

**Problème :** Le français écrit ≠ français oral. Comment gérer les consonnes muettes ?

**Solution :** Détection et suppression des consonnes muettes avec ajustement des voyelles.

```python
"discret"  → discrè + t (muet retiré, e→è pour préserver le son)
           → l + iscrè + d + em
           → "liscrèdem"

"employée" → employé (ée→é, le 'e' supplémentaire est muet)
           → e + l + oyé + pl + oc
           → "emloyéploc"

"parler"   → parlé (er→é, son identique)
           → l + arlé + p + em
           → "larlépem"
```

**Règles appliquées :**
- `-et` → `-è` (discret → discrè)
- `-ent` → `-en` (moment → momen, le 't' est muet)
- `-er` → `-é` (verbes infinitifs)
- `-ée` → `-é` (le 'e' supplémentaire est redondant)

---

### 6. 🎲 Simplification des consonnes doublées

**Problème :** Que faire avec "attention" (deux 't') ? Et si on crée des doublons (pl + lé = pllé) ?

**Solution :** 
- **Avant déplacement :** Simplifier les consonnes doublées (tt→t, nn→n, mm→m)
- **Après construction :** Simplifier tout doublon créé accidentellement

```python
"attention" → "a" + "tt" → "a" + "t" (simplifié) + "ention"
            → alentiontem

"employée"  → "em" + "pl" + "oyé" 
            → em + l + oyé + pl + lé
            → emloyépllé → emloyéplé (pll→pl simplifié)
```

---

### 7. 🛡️ Conservation sélective des mots

**Problème :** Transformer tous les mots rend le texte illisible. Quels mots préserver ?

**Solution :** Système de règles de préservation désactivables individuellement :

| Catégorie | Exemples | Raison |
|-----------|----------|--------|
| **Mots-outils** | le, la, de, un, et, à | Structure grammaticale |
| **Verbes ultra-courants** | être, avoir, faire, aller | Lisibilité |
| **Interjections** | oh, ah, hein, ben | Expression orale |
| **Nombres & dates** | 123, XIV, 31/12/2023 | Information précise |
| **Noms propres** | Paris, Marie | Identification |
| **Acronymes** | SNCF, UNESCO | Sigles |
| **Déjà en louchébem** | loucherbem, louf | Éviter double transformation |

```python
# Désactiver certaines préservations
config = LouchebemConfig(
    preserve_stopwords=True,        # Garder "le", "la", etc.
    preserve_proper_nouns=False,    # Transformer "Paris" aussi !
    preserve_numbers=True,          # Garder "123"
)
converter = LouchebemConverter(config=config)
```

---

### 8. 📝 Gestion des apostrophes (élisions)

**Problème :** Comment traiter "l'argot", "d'autre", "j'aime" ?

**Solution :** Règles spécifiques selon le préfixe :

```python
# Cas spécial : l' + mot → fusion
"l'argot"   → "largot" → "largomuche" (puis cherche dans dictionnaire)
"l'origine" → "lorigine" → "loriginlé"

# Autres apostrophes : préserver le préfixe
"d'autre" → "d'" + "autre" transformé → "d'autrelé"
"j'aime"  → "j'" + "aime" transformé → "j'aimelé"
```

**Logique :** Fusionner avec 'l' fait sens car le mot va commencer par 'l' de toute façon !

---

### 9. 🔤 Gestion du cluster "qu"

**Problème :** Le "qu" est un digramme représentant le son [k]. Comment le traiter ?

**Solution :** Traiter "qu" comme une **unité indivisible** (ne pas retirer le 'u').

```python
"équivalent" → "é" + "qu" + "ivalen" (ent→en, 't' muet)
             → é + l + uivalen + qu + em
             → "éluivalenquem"  # "qu" reste ensemble !
```

**Phonétique :** "k" et "qu" sont traités comme des variantes du même son, mais le 'u' reste avec le 'q'.

---

### 10. 💅 Préservation de la casse

**Problème :** Comment conserver les majuscules ?

**Solution :** Détection et application du pattern de casse original.

```python
"Bonjour"  → "Lonjourbem"  (Titre)
"BOUCHER"  → "BOUCHER"     (Tout en majuscules = nom propre, préservé)
"bonjour"  → "lonjourbem"  (minuscules)
```

---

## ⚙️ Configuration avancée

Le convertisseur offre de nombreuses options de configuration :

```python
from largonji import LouchebemConfig, LouchebemConverter

# Configuration maximale (comportement par défaut)
config = LouchebemConfig.maximal()

# Configuration minimale (transforme presque tout)
config = LouchebemConfig.minimal()

# Configuration pour tests reproductibles
config = LouchebemConfig.for_testing(seed=42)

# Configuration personnalisée
config = LouchebemConfig(
    # Préservation
    preserve_stopwords=True,
    preserve_ultra_common_verbs=True,
    preserve_interjections=True,
    preserve_numbers=True,
    preserve_proper_nouns=True,
    preserve_acronyms=True,
    preserve_already_louchebem=True,
    
    # Fonctionnalités
    enable_apostrophe_merging=True,
    enable_l_initial_transform=True,
    enable_silent_consonants=True,
    enable_doubled_consonant_simplification=True,
    enable_infinitive_verbs=True,
    
    # Comportement
    preserve_case=True,
    preserve_punctuation=True,
    random_seed=None,  # Pour des suffixes aléatoires
)

converter = LouchebemConverter(config=config)
```

---

## 📚 Sources et remerciements

Ce projet s'appuie sur des sources historiques et linguistiques rigoureuses :

### Sources principales

- **[Wikipédia - Largonji](https://fr.wikipedia.org/wiki/Largonji)** : Article détaillé sur l'histoire et les procédés du largonji
- **[louchebem.fr](https://louchebem.fr/)** : Le site de référence pour le louchébem, avec traducteur et exemples
- **Lorédan Larchey** (1858, 1878) : _Dictionnaire historique d'argot_ — Premiers recensements du loucherbem
- **Gaston Esnault** (1965) : _Dictionnaire historique des argots français_ — Référence académique majeure

### Sources complémentaires

- **Albert Dauzat** (1946) : _Les argots_ — Analyse du procédé du loucherbem
- **Le Canard Enchaîné** : Article « Voyage dans les microlangues » — État contemporain du louchébem
- **Sylvain Macouin** : « À propos du Ladukteurtrès Largonjem » — Analyse des difficultés de transformation automatique
- **Jacques Haddad** : Documentation sur le loucherbem historique

### Inspiration technique

Merci aux développeurs de [louchebem.fr](https://louchebem.fr/) pour leur travail de préservation de cet argot et leur traducteur en ligne qui a servi de référence.

---

## 📄 Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 📝 Améliorer la documentation
- ➕ Ajouter des mots au dictionnaire historique

---

<div align="center">

**Fait avec ❤️ pour préserver le largonji des louchébems**

_« Dans le gigot, tout est bon ! »_

</div>

