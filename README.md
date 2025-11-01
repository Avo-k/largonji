# 🔪🥩 largonji

[![PyPI version](https://badge.fury.io/py/largonji.svg)](https://badge.fury.io/py/largonji)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/)

> _« Larlépem-vous louchébem? »_ — Convertisseur hybride français ↔ louchébem

**[🇬🇧 English version / Version anglaise →](README_EN.md)**

Un convertisseur Python moderne pour transformer du français en **louchébem**, l'argot historique des bouchers parisiens. 

Le **[louchébem](https://fr.wikipedia.org/wiki/Largonji#Définition)** est la variante principale du **[largonji](https://fr.wikipedia.org/wiki/Largonji)**, une famille de procédés de déformation linguistique utilisés en argot français (incluant aussi le verlan, le javanais...).

Ce package implémente le **louchébem** avec une approche **hybride** : dictionnaire de termes historiques authentiques + transformation algorithmique pour les mots inconnus.

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

# Créer un convertisseur et transformer du texte
converter = LouchebemConverter()
print(converter.convert_text("Bonjour le boucher"))
# → Lonjourbem le loucherbem
```

---

## 📖 Table des matières

- [Qu'est-ce que le louchébem ?](#quest-ce-que-le-louchébem-)
- [La méthode naïve](#la-méthode-naïve)
- [Nos choix d'implémentation](#nos-choix-dimplémentation)
- [Configuration avancée](#configuration-avancée)
- [Sources et remerciements](#sources-et-remerciements)
- [Licence](#licence)

---

## 🥩 Qu'est-ce que le louchébem ?

Le **[louchébem](https://fr.wikipedia.org/wiki/Largonji)** est la principale variante du **[largonji](https://fr.wikipedia.org/wiki/Largonji)**, une famille de procédés de déformation linguistique développés en argot français. Le louchébem a été créé et popularisé par les bouchers parisiens au XIXe siècle. 

Le mot « **louchébem** » lui-même vient de la transformation de « **boucher** » selon les règles du procédé.

### 📜 Un peu d'histoire

Le largonji apparaît dans l'argot des classes populaires parisiennes dès la fin du XVIIIe ou début du XIXe siècle. Les premiers mots recensés incluent :
- **lomben** (← bon) dans un glossaire argotique de 1821
- **La Lorcefé** (← La Force, une prison parisienne) dans les Mémoires de Vidocq (1828-1829)
- **loucherbem** (← boucher) attesté vers 1876

Certains mots issus du louchébem sont entrés dans le langage français courant :
- **loufoque** (← fou) : bizarre, farfelu
- **larfeuille** (← portefeuille, billets) : l'argent
- **à loilpé** (← à poil) : nu

### 🎯 Le principe de base

Le procédé du louchébem suit une règle simple :

1. **Remplacer** la première consonne (ou groupe de consonnes) par « **l** »
2. **Déplacer** cette consonne à la fin du mot
3. **Ajouter** un suffixe (souvent en rapport avec la consonne déplacée)

**Exemples :**
- **b**oucher → **l**oucher**b**em
- **j**argon → **l**argon**j**i
- **p**rix → **l**i**pr**em (groupe "pr" déplacé ensemble)

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

## ✨ Choix d'implémentation

Le louchébem n'a jamais été un langage standardisé : tous les bouchers ne parlaient pas exactement le même argot. Les suffixes en particulier variaient d'une personne à l'autre, et le langage évoluait volontairement pour rester moins évident aux non-initiés (aspect non-déterministe). Certains cas ne sont pas vraiment clairs dans les sources historiques, notamment le traitement des mots commençant par une voyelle.

Cette implémentation repose donc sur des **choix assumés** : elle se base sur les sources disponibles et sur ce qui sonne le mieux à l'oreille. Cette section détaille ces décisions techniques.

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

### 2. 🛡️ Conservation sélective des mots

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

### 3. 🔤 Mots commençant par une voyelle

**Problème :** Comment transformer "entendre", "attention", "orange" qui commencent par une voyelle ?

**Solution :** Chercher la **consonne d'attaque** (premier groupe de consonnes **après** le son voyelle initial). C'est un **choix d'implémentation** — les sources historiques ne sont pas claires sur ce cas. Cette approche sonne mieux à l'oreille et permet de garder des mots ne commençant pas tous par "l" dans un texte, ce qui est plus agréable à lire.

```python
"entendre"  → "en" (voyelle nasale) + "t" (attaque) + "endre"
            → en + l + endre + t + és
            → "enlendretès"

"attention" → "a" + "t" (simplifié de "tt") + "ention"
            → a + l + ention + t + és
            → "alentiontès"

"orange"    → "o" + "r" + "ange"
            → o + l + ange + r + em
            → "olangerem"
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

### 5. 🎵 Groupes de consonnes multiples

**Problème :** Comment traiter "prix", "train", "fromage" qui commencent par 2+ consonnes ?

**Solution :** Extraire le **groupe complet** de consonnes avant la première voyelle et le déplacer en bloc.

```python
"prix"    → "p" + "r" + "ix" → l + ix + pr + em → "liprem"
"train"   → "t" + "r" + "ain" → l + ain + tr + em → "laintrem"
"fromage" → "f" + "r" + "omage" → l + omaj + fr + é → "lomajfré"
```

**Détail technique :** Les clusters sont **toujours conservés intégralement**, même si le suffixe contient déjà l'une des lettres (ex : "pl" reste "pl", pas seulement "p").

---

### 6. 🔇 Consonnes muettes et ajustements phonétiques

**Problème :** Le français écrit ≠ français oral. Comment gérer les consonnes muettes ?

**Solution :** Détection et suppression des consonnes muettes avec ajustement des voyelles.

```python
"discret"  → discrè + t (muet retiré, e→è pour préserver le son)
           → l + iscrè + d + oc
           → "liscrèdoc"

"employée" → employé (ée→é, le 'e' supplémentaire est muet)
           → e + l + oyé + pl + é
           → "emloyéplé"

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

### 7. 🎲 Simplification des consonnes doublées

**Problème :** Que faire avec "attention" (deux 't') ? Et si on crée des doublons (pl + lé = pllé) ?

**Solution :** 
- **Avant déplacement :** Simplifier les consonnes doublées (tt→t, nn→n, mm→m)
- **Après construction :** Simplifier tout doublon créé accidentellement

```python
"attention" → "a" + "tt" → "a" + "t" (simplifié) + "ention"
            → alentiontès

"employée"  → "em" + "pl" + "oyé" 
            → em + l + oyé + pl + é
            → emloyéplé
```

---

### 8. 📝 Gestion des apostrophes (élisions)

**Problème :** Comment traiter "l'argot", "d'autre", "j'aime" ?

**Solution :** Règles spécifiques selon le préfixe :

```python
# Cas spécial : l' + mot → fusion
"l'argot"   → "largot" → "largomuche" (puis cherche dans dictionnaire)
"l'origine" → "lorigine" → "loriginelé"

# Autres apostrophes : préserver le préfixe
"d'autre" → "d'" + "autre" transformé → "d'auletrem"
"j'aime"  → "j'" + "aime" transformé → "j'ailemem"
```

**Logique :** Fusionner avec 'l' fait sens car le mot va commencer par 'l' de toute façon !

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
    # Préservation des mots
    preserve_stopwords=True,              # Garder "le", "la", "de", "un", etc. (mots-outils)
    preserve_ultra_common_verbs=True,     # Garder "être", "avoir", "faire", "aller" (lisibilité)
    preserve_interjections=True,          # Garder "oh", "ah", "hein", "ben" (expressions orales)
    preserve_numbers=True,                # Garder les nombres et dates (123, XIV, 31/12/2023)
    preserve_proper_nouns=True,           # Garder les noms propres détectés (Paris, Marie)
    preserve_acronyms=True,               # Garder les acronymes (SNCF, UNESCO)
    preserve_already_louchebem=True,      # Ne pas retransformer les mots déjà en louchébem
    
    # Fonctionnalités de transformation
    enable_apostrophe_merging=True,       # Fusionner "l'argot" en "largot" avant transformation
    enable_l_initial_transform=True,      # Transformer les mots commençant par "l" (sinon préservés)
    enable_silent_consonants=True,        # Retirer consonnes muettes (discret → discrè)
    enable_doubled_consonant_simplification=True,  # Simplifier "tt" → "t", "ll" → "l", etc.
    enable_infinitive_verbs=True,         # Transformer "-er" en "-é" pour les verbes infinitifs
    
    # Comportement général
    preserve_case=True,                   # Conserver majuscules/minuscules du texte original
    preserve_punctuation=True,            # Garder la ponctuation intacte
    random_seed=None,                     # Graine aléatoire pour suffixes (None = aléatoire, int = reproductible)
)

converter = LouchebemConverter(config=config)
```

---

## 📚 Sources et remerciements

Ce projet s'appuie sur des sources historiques et linguistiques :

- **[Wikipédia - Largonji](https://fr.wikipedia.org/wiki/Largonji)** : Article détaillé sur l'histoire et les procédés du largonji
- **[louchebem.fr](https://louchebem.fr/)** : Site de référence pour le louchébem. Nous nous en sommes inspirés, mais notre implémentation diffère sur plusieurs aspects.
- **Sylvain Macouin** : « À propos du Ladukteurtrès Largonjem » — Analyse des difficultés de transformation automatique
- **Jacques Haddad** : Documentation sur le louchébem historique

---

## 📄 Licence

WTFPL - voir le fichier [LICENSE](LICENSE) pour plus de détails.

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

_« Dans le cochon, tout est bon ! »_

</div>

