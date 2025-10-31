"""
Louchébem Lexicon - Data-only module for dictionaries and word lists.

This module contains:
- ESTABLISHED_LEXICON: Historically documented Louchébem transformations
  from sources including Lorédan Larchey (1858), Gaston Esnault (1965),
  and modern usage (louchebem.fr, various argot dictionaries)
- STOPWORDS: French words that should not be transformed
- ULTRA_COMMON_VERBS: All conjugated forms of être, avoir, faire, aller
- INTERJECTIONS: Common interjections and onomatopoeia

Note: Preservation logic has been moved to preservation.py
"""

# Core established Louchébem vocabulary
ESTABLISHED_LEXICON = {
    # The word that gave its name to the argot
    'boucher': 'loucherbem',
    'bouchère': 'loucherbème',
    
    # Common argot-related words
    'argot': 'largomuche',
    'jargon': 'largonji',
    'parler': 'larlépem',
    
    # Common words
    'fou': 'louf',
    'douce': 'loucedé',
    'bon': 'lombem',
    'bien': 'lienbem',
    'mieux': 'lieuxmé',
    
    # Greetings and social
    'bonjour': 'lonjourbem',
    'bonsoir': 'lonsoirbem',
    'merci': 'lercimuche',
    'pardon': 'lardonpem',
    'salut': 'lalusse',
    
    # Butcher-specific vocabulary
    'patron': 'latronpem',
    'gigot': 'ligogem',
    'morceau': 'lorsomic',
    'porc': 'lorpic',
    'viande': 'liandève',
    'boeuf': 'leufboc',
    'veau': 'lovo',
    'mouton': 'loutonmem',
    'côte': 'lotquem',
    'filet': 'lileffé',
    'steak': 'leak-stesse',
    
    # Food and drink
    'café': 'laféquès',
    'pain': 'linpem',
    'vin': 'linvem',
    'bière': 'lièrbem',
    'fromage': 'lomajfré',
    'saucisse': 'laucissesé',
    
    # People
    'client': 'linclès',
    'femme': 'lamfé',
    'dame': 'lamdé',
    'homme': 'lomme',
    'fille': 'lifé',
    'type': 'lypte',
    'mec': 'lecmès',
    'môme': 'lomé',
    'garçon': 'larçongon',
    'monsieur': 'lonsieurmic',
    
    # Body parts (historical butcher usage)
    'cul': 'luquesse',
    'tête': 'letquesse',
    'main': 'linmé',
    'pied': 'liépé',
    'dos': 'lodesse',
    
    # Numbers (important for prices)
    'dix': 'lixdesse',
    'cent': 'lentsé',
    'franc': 'lanfrè',
    
    # Actions/verbs
    'manger': 'langémé',
    'boire': 'loirbe',
    'vendre': 'lendrevé',
    'couper': 'loupécou',
    'payer': 'layépé',
    'donner': 'lonnédé',
    'faire': 'lairfé',
    'gaffer': 'lafgué',
    'gaffé': 'lafgué',
    'passer': 'lassépem',
    
    # Objects
    'sac': 'lacsé',
    'prix': 'liprem',
    'jour': 'jourlem',
    'temps': 'lempsté',
    'travail': 'lavailtrè',
    'maison': 'laisonmé',
    'rue': 'lurée',
    'porte': 'lortpé',
    
    # Adjectives
    'beau': 'lobo',
    'grand': 'landgré',
    'petit': 'letipé',
    'sale': 'lalsé',
    'propre': 'loprepré',
    
    # Expressions
    'tout': 'loutqué',
    'rien': 'liemrié',
    'mal': 'lalmé',
    'vite': 'litvé',
    'trop': 'loptré',
    'pas': 'laspé',
    'oui': 'louivème',
    'moi': 'loimique',
    'truc': 'luctrème',
    'coin': 'loinqué',
    'noir': 'loirnoque',
    'rouge': 'lougeroque',
    'coup': 'louqué',
    
    # From sources - additional attested words
    'poil': 'loilpé',  # "à poil" → "à loilpé"
    'force': 'lorcefé',  # La Force (prison)
    'feuille': 'larfeuille',
    'portefeuille': 'larfeuille',
    'feuillard': 'larfeuille',
    'prince': 'linspré',
    'pousse': 'lousse',  # gendarmerie
    'garcon': 'larsonquès',
    'combien': 'lombienquès',
    'comprend': 'lomprenquès',
    'gitan': 'litjoc',
    'maquereau': 'lacromuche',
    'paquet': 'lacsonpem',
    'pacson': 'lacsonpem',
    'pardessus': 'lardeuss',
    'pourboire': 'lourboirpem',
    'putain': 'lutinpem',
    'toqué': 'locdu',
    'chouette': 'louettechem',
    
    # Numbers (from sources)
    'deux': 'leude',
    'quatre': 'latqué',
    'cinq': 'lincsé',
    'vingt': 'linve',
    'quarante': 'laranque',
    
    # Additional quality/description words
    'cher': 'lerchem',  # also: lerchoque (variant)
    'gras': 'lagrem',  # also: lagrèm
    'rassis': 'lassirok',
    'con': 'lonqué',
    'poire': 'loirpem',  # (un ahuri)
}

# Ultra-common verbs that should be preserved for readability
# These verbs are so frequent that transforming them hurts comprehension
ULTRA_COMMON_VERBS = {
    # être (to be) - all forms
    'être', 'suis', 'es', 'est', 'sommes', 'êtes', 'sont',
    'étais', 'était', 'étions', 'étiez', 'étaient',
    'fus', 'fut', 'fûmes', 'fûtes', 'furent',
    'serai', 'seras', 'sera', 'serons', 'serez', 'seront',
    'serais', 'serait', 'serions', 'seriez', 'seraient',
    'sois', 'soit', 'soyons', 'soyez', 'soient',
    'fusse', 'fusses', 'fût', 'fussions', 'fussiez', 'fussent',
    'été', 'étant',
    
    # avoir (to have) - all forms
    'avoir', 'ai', 'as', 'a', 'avons', 'avez', 'ont',
    'avais', 'avait', 'avions', 'aviez', 'avaient',
    'eus', 'eut', 'eûmes', 'eûtes', 'eurent',
    'aurai', 'auras', 'aura', 'aurons', 'aurez', 'auront',
    'aurais', 'aurait', 'aurions', 'auriez', 'auraient',
    'aie', 'aies', 'ait', 'ayons', 'ayez', 'aient',
    'eusse', 'eusses', 'eût', 'eussions', 'eussiez', 'eussent',
    'eu', 'ayant',
    
    # faire (to do/make) - most common forms
    'faire', 'fais', 'fait', 'faisons', 'faites', 'font',
    'faisais', 'faisait', 'faisions', 'faisiez', 'faisaient',
    'ferai', 'feras', 'fera', 'ferons', 'ferez', 'feront',
    'ferais', 'ferait', 'ferions', 'feriez', 'feraient',
    'fasse', 'fasses', 'fassions', 'fassiez', 'fassent',
    'faisant',
    
    # aller (to go) - most common forms
    'aller', 'vais', 'vas', 'va', 'allons', 'allez', 'vont',
    'allais', 'allait', 'allions', 'alliez', 'allaient',
    'irai', 'iras', 'ira', 'irons', 'irez', 'iront',
    'irais', 'irait', 'irions', 'iriez', 'iraient',
    'aille', 'ailles', 'aillent',
    'allé', 'allée', 'allés', 'allées', 'allant',
}

# Interjections and onomatopoeia that should be preserved
# These express emotion/sound and should stay natural
INTERJECTIONS = {
    # Basic interjections
    'ah', 'oh', 'eh', 'hé', 'hein', 'euh', 'ouh',
    'aïe', 'ouille', 'aïe', 'ouf', 'oof',
    'bof', 'bah', 'pfff', 'pff', 'pfft', 'pffft',
    'chut', 'psst', 'hop', 'allez', 'hop-là',
    'hola', 'holà', 'oups', 'oops', 'ouah', 'waouh', 'waou',
    'zut', 'mince', 'flûte', 'fichtre',
    
    # Onomatopoeia
    'crac', 'boum', 'paf', 'bing', 'bang', 'vlan',
    'plouf', 'splash', 'clic', 'clac', 'toc',
    'tic', 'tac', 'dong', 'dring', 'pouet',
    'miam', 'glouglou', 'snif', 'atchoum',
    
    # Exclamations
    'hélas', 'tant pis', 'tant mieux',
}

# French stopwords that should NOT be transformed
# (articles, prepositions, pronouns, etc.)
STOPWORDS = {
    # Articles
    'le', 'la', 'les', "l'",
    'un', 'une', 'des',
    'du', 'de', 'd\'', 'de la',
    
    # Prepositions
    'à', 'au', 'aux', 'en', 'dans', 'sur', 'sous',
    'pour', 'par', 'avec', 'sans', 'chez',
    'vers', 'pendant', 'depuis', 'avant', 'après',
    'entre', 'devant', 'derrière',
    
    # Conjunctions
    'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car',
    'que', 'qui', 'quoi', 'dont', 'où',
    'si', 'comme', 'quand', 'lorsque', 'puisque',
    'alors', 'cependant', 'néanmoins', 'toutefois',
    
    # Pronouns
    'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles',
    'me', 'te', 'se', 'lui', 'leur',
    'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses',
    'notre', 'votre', 'leur', 'nos', 'vos', 'leurs',
    'ce', 'cet', 'cette', 'ces',
    'toi', 'moi',
    'celui', 'celle', 'ceux', 'celles',
    'ça', 'ceci', 'cela',
    
    # Common adverbs and connectors (REVIEW THESE!)
    'ainsi', 'aussi', 'alors', 'encore', 'enfin', 'puis',
    'ensuite', 'déjà', 'jamais', 'toujours', 'souvent',
    'peut-être', 'sans doute', 'bien sûr',
    'très', 'trop', 'assez', 'plus', 'moins', 'aussi',
    'autant', 'beaucoup', 'peu',
    'ici', 'là', 'où', 'ailleurs', 'partout',
    'maintenant', 'aujourd\'hui', 'hier', 'demain',
    
    # Common short verbs and auxiliaries (consider removing some!)
    'y', 'en',
    'ne', 'pas', 'plus', 'non', 'oui',
    
    # Interrogatives
    'comment', 'pourquoi', 'combien', 'quand',
    
    # Common existentials
    'voici', 'voilà', 'il y a',
    
    # Contractions
    "j'", "t'", "s'", "c'", "d'", "l'", "m'", "n'",
    "qu'", "jusqu'", "lorsqu'", "puisqu'",
}

# Simple lookup function
def get_louchebem_word(word: str) -> str | None:
    """
    Look up a word in the established lexicon.
    
    Args:
        word: The word to look up
        
    Returns:
        The Louchébem transformation if found, None otherwise
    """
    return ESTABLISHED_LEXICON.get(word.lower())

