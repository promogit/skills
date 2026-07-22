---
name: no-slop-fr
description: >
  Écrire et réviser du contenu qui sonne humain, pas généré.
  Utiliser ce skill pour tout contenu rédigé ou relu : articles de blog,
  newsletters, posts LinkedIn, scripts, emails, pages de vente.
  Déclencher automatiquement dès qu'un contenu est produit ou corrigé,
  même si l'utilisateur ne le demande pas explicitement.
---

# No-Slop FR

Garantir que chaque contenu produit sonne comme son auteur, pas comme une IA.
Appliquer ces règles pendant la rédaction, pas seulement en relecture.

## Compatibilité avec `write-technical-docs`

Pour une documentation technique en français, combiner ce skill avec
[`write-technical-docs`](../write-technical-docs/SKILL.md).

- Conserver ici les règles de précision, de suppression du jargon creux et de
  suppression du méta-commentaire.
- Donner la priorité aux conventions techniques pour les listes de procédures,
  d’options ou de champs, même lorsqu’elles contiennent trois éléments ou plus.
- Conserver les structures répétées lorsqu’elles rendent des étapes ou des
  entrées de référence plus faciles à comparer.
- Accepter un système, un composant ou un document comme sujet grammatical
  lorsqu’il exécute ou porte réellement l’action décrite.
- Conserver les fragments utiles dans les titres, libellés d’interface, cellules
  de tableau, états et descriptions de paramètres.
- Conserver le passif lorsqu’il met au premier plan un état ou un résultat et
  que l’acteur est inconnu, inutile ou déjà établi.
- Ne jamais sacrifier le sens technique, le code, les identifiants, les liens,
  les libellés littéraux ou la force d’un mot-clé normatif pour satisfaire une
  préférence de style.


---

## Règles fondamentales

### 1. Voix active, acteur nommé
Chaque phrase a un sujet humain qui fait quelque chose.
Pas de passif masqué. Pas d'objets inanimés qui "émergent", "évoluent"
ou "récompensent".

- ❌ "La décision a émergé du processus."
- ✅ "L'équipe a décidé."

### 2. Zéro contraste binaire formulaique
Les constructions "pas X, c'est Y" créent un faux suspense mécanique.
Énoncer Y directement.

- ❌ "Ce n'est pas un problème de motivation. C'est un problème de système."
- ✅ "Le problème, c'est le système."

### 3. Zéro liste négative
Lister ce que quelque chose n'est pas avant de dire ce que c'est.

- ❌ "Pas un consultant. Pas un formateur. Un stratège."
- ✅ "Un stratège qui construit des systèmes."

### 4. Zéro méta-commentaire
Le texte ne doit pas annoncer sa propre structure.

- ❌ "Dans cette section, on va voir pourquoi…"
- ✅ Expliquer directement.

### 5. Précision concrète
Pas de déclaratifs vagues. Nommer la chose précise.

- ❌ "Les implications sont significatives."
- ✅ "Tu perds 30 % de tes abonnés dans les 48h si ton email de bienvenue est générique."

### 6. Rythme varié
Pas de tiret cadratin (—). Pas de fragmentation staccato systématique.
Pas chaque paragraphe qui se termine par une formule percutante.
Mélanger les longueurs. Deux éléments dans une liste valent mieux que trois.

### 7. Faire confiance au lecteur
Pas d'adoucissements, de justifications ou de prise en main excessive.
Énoncer les faits. Laisser le lecteur tirer ses conclusions.

---

## Liste noire universelle

Ces formulations déclenchent une réécriture automatique.
# Liste noire — formules IA universelles

Formulations à réécrire automatiquement, quelle que soit l'intention de l'auteur.

---

## Hyperboles vides

Ces mots prétendent à l'importance sans la démontrer.

| Éviter | Faire à la place |
|---|---|
| "révolutionnaire" | Décrire ce qui change concrètement |
| "disruptif" | Idem |
| "game-changer" | Idem |
| "incontournable" | Justifier ou reformuler |
| "ça change tout" | Nommer ce qui change |
| "rien ne sera plus comme avant" | Interdit |
| "innovant" sans preuve | Montrer l'innovation concrète |
| "sans précédent" | Préciser en quoi |

---

## Adverbes superflus

Supprimer ou remplacer par un exemple concret.

- "fondamentalement"
- "intrinsèquement"
- "véritablement"
- "résolument"
- "particulièrement" (collé à un adjectif évaluatif)
- "stratégiquement" (collé à un adjectif)
- "profondément" (sauf usage physique littéral)
- "crucialement"
- "naturellement" (en ouverture de phrase)
- "évidemment" (condescendant)
- "clairement" (si c'était clair, inutile de le préciser)
- "simplement" (minimise souvent ce qui ne l'est pas)
- "littéralement"

---

## Jargon creux

| Éviter | Utiliser à la place |
|---|---|
| "paradigme" | "façon de faire", "modèle", "logique" |
| "synergie" | Décrire ce qui se passe concrètement |
| "levier puissant" | "outil efficace", "mécanisme qui fonctionne" |
| "approche holistique" | "sur tous les fronts", décrire ce qu'elle couvre |
| "insights actionnables" | "idées concrètes à appliquer" |
| "recommandations pertinentes" | "conseils qui collent à ta situation" |
| "la mise en œuvre de cette approche" | "faire ça" |
| "l'optimisation de vos processus" | "améliorer comment tu travailles" |
| "expérience sur-mesure" | "quelque chose qui correspond vraiment" |
| "naviguer dans" (des défis) | "gérer", "traiter" |
| "deep dive" | "analyse", "examen approfondi" |

---

## Ouvertures IA typiques

Supprimer et commencer par le fait concret.

- "Dans le paysage actuel de [secteur]…"
- "À l'ère de l'intelligence artificielle…"
- "Dans un monde où…"
- "Dans un contexte où…"
- "Force est de constater que…"
- "Il convient de noter que…"
- "À l'heure où…"
- "Face aux enjeux de…"

---

## Béquilles d'emphase

N'ajoutent aucun sens. Supprimer.

- "Point final." / "C'est tout."
- "Laissez ça infuser."
- "Ne vous y trompez pas."
- "Je le dis clairement."
- "Soyons honnêtes."
- "Permettez-moi d'être direct."
- "Je vais être franc."

---

## Déclaratifs vagues

Phrases qui annoncent l'importance sans nommer la chose précise.
Remplacer par la chose concrète.

- "Les implications sont significatives."
- "Les enjeux sont élevés."
- "Les conséquences sont réelles."
- "Les raisons sont structurelles."
- "C'est le problème fondamental."

---

## Méta-commentaire sur le texte

Le texte ne doit pas annoncer sa propre structure.

- "Dans cette section, on va voir…"
- "Laisse-moi t'expliquer…"
- "La suite de cet article explique…"
- "Comme on le verra plus loin…"
- "Je veux explorer…"
- "Je vais te montrer comment…"

---

# Structures à éviter

Les tics de structure que les LLMs reproduisent en boucle.
Ils trahissent l'IA même quand le vocabulaire est correct.
Structure à réécrire automatiquement.

---

## Contrastes binaires formulaiques

Tout ce qui ressemble à "pas X, c'est Y" crée un faux suspense mécanique.

| Formule | Correction |
|---|---|
| "Ce n'est pas X. C'est Y." | Énoncer Y directement |
| "Le problème n'est pas X. C'est Y." | "Le problème, c'est Y." |
| "Pas parce que X. Parce que Y." | Phrase causale naturelle avec "parce que" |
| "Ça ressemble à X. C'est en réalité Y." | "C'est Y." |
| "Pas seulement X, mais aussi Y." | Reformuler sans la béquille additive |
| "La question n'est pas X. C'est Y." | Énoncer Y |

**Règle :** énoncer ce qui est vrai, sans passer par la négation de ce qui est faux.

---

## Listes négatives

Lister ce que quelque chose n'est *pas* avant de dire ce que c'est.

| Formule | Correction |
|---|---|
| "Pas un X. Pas un Y. Un Z." | "Un Z qui…" |
| "Ce n'était pas X. Ce n'était pas Y. C'était Z." | "C'était Z." |

---

## Fausse agentivité

Donner à des objets inanimés des verbes d'action humains.
Les LLMs adorent ça parce que ça évite de nommer un acteur concret.

| Formule | Correction |
|---|---|
| "la décision émerge" | Quelqu'un décide |
| "le marché récompense" | Les clients paient pour ça |
| "la culture évolue" | Les gens changent de comportement |
| "la donnée nous dit" | Quelqu'un lit les chiffres et conclut que… |
| "la conversation se déplace vers" | Quelqu'un oriente la conversation |
| "les résultats parlent d'eux-mêmes" | Nommer les résultats précis |

**Règle :** nommer le sujet humain. Si personne de précis, utiliser "tu".

---

## Voix passive masquée

Cache l'acteur et vide le texte de son énergie.

| Formule | Correction |
|---|---|
| "X a été créé" | Nommer qui l'a créé |
| "Il est généralement admis que" | Nommer qui l'admet |
| "Des erreurs ont été commises" | Nommer qui les a faites |
| "La décision a été prise" | Nommer qui a décidé |

---

## Narrateur en survol

Écrire depuis les hauteurs au lieu de mettre le lecteur dans la scène.

| Formule | Correction |
|---|---|
| "Les gens ont tendance à…" | "Tu as tendance à…" + exemple concret |
| "Personne n'a conçu ça exprès." | "Tu n'as pas décidé un matin de…" |
| "C'est ainsi que ça fonctionne." | Montrer comment ça fonctionne sur un cas précis |

---

## Fragmentation staccato

Phrases-chocs empilées pour simuler la profondeur.

| Formule | Correction |
|---|---|
| "[Mot]. C'est tout. C'est ça l'essentiel." | Une phrase complète |
| "X. Et Y. Et Z." en rafale | Fusionner ou choisir le plus fort |
| Trois phrases de 3 mots à la suite | Varier les longueurs |

---

## Méta-commentaire

Le texte ne doit pas annoncer sa propre structure.

| Formule | Correction |
|---|---|
| "Laisse-moi t'expliquer…" | Expliquer directement |
| "Dans cette section, on va voir…" | Supprimer |
| "La suite de cet article explique…" | Supprimer, aller au fait |
| "Je vais être direct…" | Être direct, sans le dire |

---

## Patterns de rythme

| Pattern | Correction |
|---|---|
| Listes de trois éléments systématiques | Deux éléments ou un seul |
| Chaque paragraphe se termine "en punch" | Varier les fins |
| Tiret cadratin (—) | Virgule ou reformulation, jamais de tiret cadratin |
| Questions suivies immédiatement d'une réponse | Laisser respirer ou couper |
| Même longueur de phrase sur 4+ phrases de suite | Varier |

---

## Amorces à éviter

| Amorce | Correction |
|---|---|
| "Ce qui rend ça [adjectif], c'est…" | Nommer la contrainte précise |
| "Ce que la plupart des gens ne savent pas…" | Énoncer l'information directement |
| Paragraphe commençant par "Donc," | Commencer par le contenu |
| Phrase commençant par "Écoute," | Supprimer |

# Checklist avant livraison

- [ ] Un adverbe en -ment collé à un adjectif ? → supprimer
- [ ] Une construction "pas X, c'est Y" ? → énoncer Y directement
- [ ] Un objet inanimé qui "émerge" ou "récompense" ? → nommer l'acteur
- [ ] Une phrase en voix passive qui masque une information utile ? → nommer l'acteur
- [ ] Une liste de trois éléments ? → en garder deux ou reformuler en prose
- [ ] Un tiret cadratin (—) ? → virgule ou reformulation
- [ ] Un déclaratif vague ? → nommer la chose précise
- [ ] Du méta-commentaire sur le texte ? → supprimer
- [ ] Une fin de paragraphe qui sonne comme une citation LinkedIn ? → varier
- [ ] Est-ce qu'une vraie personne dirait ça à voix haute ? → si non, reformuler

---

## Scoring rapide

| Dimension | Question | /10 |
|---|---|---|
| Directness | Le texte énonce ou annonce ? | |
| Rythme | Varié ou métronomique ? | |
| Confiance | Respecte l'intelligence du lecteur ? | |
| Authenticité | Sonne humain ? | |
| Densité | Quelque chose à couper ? | |

En dessous de 35/50 : réécrire.
