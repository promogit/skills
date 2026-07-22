# Règles complémentaires pour le français

Appliquer ces règles au français de France après les règles générales. Traiter chaque identifiant en majuscules comme une interface stable entre le skill, le checker, les tests et les comptes rendus.

Respecter le glossaire et les conventions du projet avant toute préférence générale. Ne pas utiliser ce fichier comme méthode de traduction depuis l’anglais.

## Flexion

### `FR_FLEXION` — Adapter le terme à sa fonction grammaticale

- Chercher les termes par lemme sans perdre leur forme dans la phrase.
- Accorder le genre et le nombre des noms, déterminants et adjectifs.
- Conjuguer le verbe selon le sujet, le temps et le mode retenus.
- Adapter toute suggestion à la phrase complète au lieu de remplacer une chaîne mécaniquement.
- Conserver la graphie officielle des produits, interfaces et identifiants.

## Consignes

### `FR_INSTRUCTION_MOOD` — Choisir l’impératif ou l’infinitif et s’y tenir

- Choisir un mode pour une procédure ou un ensemble de procédures parallèles.
- Employer l’impératif pour s’adresser directement au lecteur : « Sélectionnez le certificat. »
- Employer l’infinitif pour un style de consigne impersonnel : « Sélectionner le certificat. »
- Ne pas mélanger les deux modes entre des étapes équivalentes.
- Conserver les fragments nominaux dans les libellés, titres courts et cellules de tableau.

## Nominalisations

### `FR_NOMINALIZATION` — Préférer un verbe quand il rend l’action plus nette

- Remplacer une chaîne de noms par un verbe lorsque l’acteur ou l’action devient plus clair.
- Conserver une nominalisation qui désigne un concept métier, un état, un événement ou un terme défini.
- Ne pas transformer une obligation, une condition ou un résultat en simple commentaire de style.
- Vérifier `MEANING_PRESERVE` avant toute reformulation.

## Pronoms et reprises

### `FR_PRONOUN_REFERENCE` — Lever les antécédents ambigus

- Examiner « il », « elle », « ils », « elles », « ce », « ceci », « cela », « ça », « le », « la », « lui » et les relatifs lorsque plusieurs référents sont possibles.
- Répéter le nom précis ou employer un terme défini quand la reprise peut désigner plusieurs éléments.
- Garder le pronom lorsque son antécédent est adjacent et sans ambiguïté.
- Signaler les cas ambigus avec `REFERENCE_VAGUE` dans la sortie commune du checker.

## Anglicismes

### `FR_ANGLICISM` — Préférer le terme français précis sans imposer un purisme mécanique

- Employer le terme français établi quand il exprime exactement le même concept.
- Conserver un anglicisme validé par le glossaire ou dominant dans le domaine lorsque sa traduction créerait une ambiguïté.
- Conserver les noms de produit, éléments d’API, commandes, identifiants et libellés officiels.
- Expliquer une recommandation lorsque plusieurs traductions françaises correspondent à des concepts différents.
- Utiliser `TERM_DISCOURAGED` ou `TERM_INCONSISTENT` seulement lorsque le contexte justifie le signalement.

## Voix passive

### `FR_PASSIVE` — Employer le passif lorsqu’il sert le point de vue technique

- Garder le passif pour décrire un état résultant, mettre l’objet traité au premier plan ou omettre un acteur réellement inconnu ou inutile.
- Nommer l’acteur lorsque la responsabilité, la cause ou l’ordre des opérations doit être compris.
- Accepter un système ou un composant comme sujet grammatical lorsqu’il exécute réellement l’action décrite.
- Signaler avec `PASSIVE_AMBIGUOUS` uniquement les formulations qui masquent une information utile.

## Typographie

### `FR_TYPOGRAPHY` — Appliquer une typographie française compatible avec le support

- Utiliser les guillemets français « … » pour la prose lorsque le format les prend en charge.
- Placer une espace insécable, de préférence fine, avant `;`, `?` et `!`, et une espace insécable avant `:` selon la convention éditoriale retenue.
- Employer l’apostrophe typographique `’` dans la prose si le dépôt accepte Unicode ; suivre la convention existante dans le cas contraire.
- Séparer le nombre de son unité par une espace insécable quand le format le permet.
- Employer la virgule décimale dans la prose française, sauf pour une valeur littérale, un protocole, du code ou un format qui exige le point.
- Respecter les conventions du projet pour les majuscules, les titres, les dates et les espaces insécables.
- Ne modifier aucun caractère dans le code, les commandes, les URL, les identifiants, les chemins ou les libellés littéraux.

## Contrôle final en français

- Vérifier les accords après chaque changement terminologique.
- Vérifier la cohérence du mode dans chaque procédure.
- Vérifier les antécédents des pronoms et la portée des négations.
- Vérifier que la simplification ne change ni le sens technique ni la force normative.
- Appliquer `no-slop-fr` pour supprimer le jargon creux et le méta-commentaire.
- Donner la priorité aux conventions techniques pour les listes utiles, les structures répétées, les sujets non humains exacts, les fragments d’interface et le passif utile.
