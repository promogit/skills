---
name: promo-dev-xlsx
description: "Conventions PROMO.DEV pour les fichiers Excel : exports de données, rapports chiffrés et formulaires à remplir produits au nom de PROMO.DEV (promo.dev, SAS à Aubagne — infrastructure des versements aux clients). Utiliser ce skill dès qu'un tableur est le livrable — export client, extraction, rapport de volumétrie, suivi de versements, réconciliation, grille de saisie, trame à compléter — même si l'utilisateur ne mentionne ni charte ni gabarit. Produit des fichiers sobres et directement exploitables : une table par onglet, en-têtes stylés, volets figés, filtres, valeurs typées, et surtout aucun texte d'explication, aucune note de bas de tableau, aucun onglet « méthodologie ». Use this skill whenever the deliverable for PROMO.DEV is a spreadsheet (.xlsx/.csv) rather than a document."
---

# Tableurs PROMO.DEV

Un tableur PROMO.DEV est un objet de travail, pas un document à lire. Celui qui le reçoit va trier, filtrer, faire un tableau croisé, recopier une colonne dans son propre outil. Tout ce qui n'est pas de la donnée le gêne : une ligne de commentaire casse un tri, une cellule fusionnée casse un filtre, un onglet « Lisez-moi » se perd au premier copier-coller. D'où la règle qui gouverne tout le reste : **le fichier porte le contenu, la conversation porte les explications.**

## Marche à suivre

1. **Établir la donnée.** Rassembler les valeurs, les typer (dates, nombres, textes), décider des colonnes et de leur ordre.
2. **Choisir la forme** selon l'usage : export, rapport ou formulaire (voir plus bas).
3. **Construire le fichier** avec `openpyxl` — lire le SKILL.md du skill `xlsx` pour les pièges généraux (recalcul obligatoire, fonctions qui survivent à la vérification, chargements en deux passes), puis `references/openpyxl-recipes.md` pour la mise en forme de la charte.
4. **Ouvrir le résultat et le regarder** avant de le livrer (procédure de vérification en fin de ce fichier).
5. **Dire à l'utilisateur, dans la conversation, ce qui manque ou ce qui a été supposé.** Jamais dans le fichier.

## Ce qui ne va pas dans un fichier PROMO.DEV

Ces éléments sont fréquents dans les tableurs générés automatiquement et systématiquement retirés ici :

- Onglet « Lisez-moi », « Notice », « Méthodologie », « Définitions », « Sources ».
- Ligne de source, de date d'extraction ou de périmètre sous le tableau. Le nom du fichier et celui des onglets portent ce contexte.
- Commentaires de cellule explicatifs, cellules « N/A — à confirmer », « donnée non disponible », colonne « Commentaire » laissée vide.
- Sous-titre, mention « confidentiel », logo image ou lignes décoratives dans le bandeau — il se limite au mot-symbole et au type de document.
- Cellules fusionnées, y compris dans le bandeau, sous-totaux intercalés au milieu des lignes, lignes de séparation vides entre groupes.
- Réserves méthodologiques et mises en garde sur la fiabilité des chiffres.

Cette dernière interdiction mérite son explication, parce qu'elle va contre un réflexe utile ailleurs : une donnée incertaine ne se signale pas dans la feuille, **elle se signale à l'utilisateur**. Une cellule vide est une cellule vide — elle se filtre, se compte, se remplit. Une cellule qui contient « à confirmer » est du texte dans une colonne de nombres : elle casse les totaux, les tris et les imports. Donc : cellule vide dans le fichier, phrase explicite dans la réponse (« la colonne IBAN est vide pour 14 lignes, l'export source ne la contenait pas »).

## La forme, sobre

Chaque feuille commence par le bandeau bleu nuit, puis la table. C'est la signature visuelle des fichiers PROMO.DEV — la même que l'encadré sombre des documents Word.

```
ligne 1   ████ PROMO.DEV              VERSEMENTS · JUILLET 2026 ████   ← bandeau plein bleu nuit,
          ────────────────────────────────────────────────────────       souligné d'un filet ambre
ligne 2     (vide, respiration)
ligne 3   ▓▓ RÉFÉRENCE   DATE   BÉNÉFICIAIRE   MONTANT ▓▓              ← en-tête bleu nuit, texte blanc
ligne 4   VH-0412       02/07/2026  M. Rousseau    412,00 €
ligne 5   VH-0608       05/07/2026  M. Verdier   1 673,54 €            ← zebra F7F7F7 une ligne sur deux
```

Le **bandeau** : une seule ligne, haute (~34), remplie en bleu nuit `00113D` sur toute la largeur de la table, soulignée d'un filet ambre `D97706` moyen — c'est ce trait qui fait la marque. À gauche, le mot-symbole PROMO.DEV en blanc, Red Hat Display gras. À droite, aligné à droite dans la dernière colonne, le type de document en capitales ambre (« VERSEMENTS · JUILLET 2026 », « FICHE D'OPÉRATION »), petit corps, à la manière des sur-titres des documents Word. Le bandeau court exactement sur la largeur de la table : plus court, il semble posé de travers ; plus long, il déborde dans le vide.

Deux informations, pas trois : l'émetteur et le contenu. Ni date d'extraction, ni mention de confidentialité — le nom du fichier les porte déjà. Sur un classeur à plusieurs onglets, chaque feuille reprend le bandeau avec son propre libellé (`SYNTHÈSE`, `DÉTAIL PAR CLIENT`), pour qu'une feuille imprimée ou copiée seule reste identifiable.

Le bandeau s'écrit en cellules simples, **sans fusion** : le fond bleu est posé cellule par cellule sur toute la largeur, le mot-symbole est en A1 et déborde visuellement sur les cellules vides, le type de document est dans la dernière cellule, aligné à droite. Une cellule fusionnée en haut de feuille empêcherait d'insérer une colonne et se propagerait à tous les copier-coller.

- **En-tête de colonnes** : fond bleu nuit `00113D`, texte blanc gras, ligne un peu plus haute (24), volets figés juste en dessous. Il répond au bandeau et tient la table.
- **Zebra** : une ligne sur deux reçoit un fond `F7F7F7`, à partir de la deuxième ligne de données, sur toute la largeur de la table. C'est ce qui guide l'œil sur une table large sans ajouter un seul trait.
- **Filtre automatique** : posé dès que la table a plusieurs lignes de même nature qu'on voudra trier ou filtrer — un export, un détail par client, une liste de demandes. Inutile sur une synthèse en libellé/valeur ou sur une table de trois lignes : un filtre qui ne sert à rien encombre l'en-tête. La plage du filtre part de la ligne d'en-tête et descend jusqu'à la dernière ligne de données, sans jamais inclure le bandeau.
- **Corps** : Open Sans 10–11, pas de bordures de quadrillage ajoutées, hauteur de ligne par défaut.
- **Alignement** : les nombres, montants et dates à droite ; les textes à gauche ; l'en-tête aligné comme sa colonne.
- **Largeurs** : calibrées sur le contenu réel, jamais laissées par défaut ni fixées au hasard. Quand la table porte un filtre, chaque colonne prend un supplément de largeur : Excel dessine la flèche de filtre **par-dessus** la cellule d'en-tête, et sans cette marge elle mord le titre de la colonne.
- **Ambre `D97706`** : le filet sous le bandeau, le type de document, les cellules à remplir des formulaires et, dans un rapport, le seul chiffre principal. Jamais dans les données elles-mêmes — un fichier où tout est en couleur n'a plus d'accent.
- **Pas d'autre couleur.** Ni vert de réussite, ni rouge d'alerte, sauf demande explicite de l'utilisateur.

## Conventions de données

- **Dates** : vraies dates Excel, format `JJ/MM/AAAA`. Jamais de date écrite en texte, jamais de format américain.
- **Nombres** : vrais nombres. Format `# ##0` avec séparateur de milliers, `# ##0,00 €` pour les montants, `0,0 %` pour les taux **stockés en fraction** (`0,155` s'affiche `15,5 %`).
- **Identifiants** (SIRET, IBAN, références de dossier) : format texte, pour que les zéros de tête survivent et qu'aucun long numéro ne bascule en notation scientifique.
- **Booléens** : `Oui` / `Non` en clair, jamais `TRUE` / `1`.
- **Cellule sans valeur** : vide. Pas de `-`, pas de `N/A`, pas de `0` mis à la place d'une donnée manquante — un zéro faux est pire qu'un vide.
- **Noms d'onglets** : courts et explicites, ils remplacent les titres (`Versements`, `Synthèse`, `Bénéficiaires`). 31 caractères maximum.
- **Nom de fichier** : `promo-dev_<objet>_<AAAA-MM-JJ>.xlsx`. C'est lui qui porte le périmètre et la date d'extraction, puisque la feuille ne les porte pas.

## Les trois formes

### Export de données

Bandeau, puis une table plate, une ligne par enregistrement, prête à être triée et filtrée. Pas de ligne de total : elle se retrouve mélangée aux données au premier tri et fausse toute somme faite par le destinataire. Si un total est attendu, il va dans un onglet `Synthèse` distinct. Valeurs brutes plutôt que formules — un export doit rester lisible hors contexte.

### Rapport chiffré

Onglet `Synthèse` en premier : bandeau, puis les chiffres clés, un par ligne, libellé à gauche et valeur à droite, le chiffre principal en ambre. Pas de filtre sur cette feuille — il n'y a rien à filtrer. Puis les tables de détail dans les onglets suivants. Les agrégats sont calculés **par des formules qui pointent vers les onglets de détail** (`SOMME.SI.ENS`, `INDEX`/`EQUIV`), afin que le fichier se recalcule quand les données changent. Un graphique seulement s'il montre quelque chose qu'un tableau de cinq lignes ne montre pas.

### Formulaire à remplir

Deux dispositions, à choisir selon la nature des champs. **En table** (une ligne par enregistrement) quand on attend plusieurs entrées courtes et homogènes : une liste de demandes, de bénéficiaires, de lignes de facturation. **En fiche verticale** (un champ par ligne, libellé à gauche, zone de saisie à droite) quand on attend une seule entrée avec des champs longs ou hétérogènes : un brief, une fiche d'opération, une demande de paramétrage. Forcer des champs de trois phrases dans les colonnes d'une table donne des cellules illisibles que personne ne remplit correctement.

Dans les deux cas, les cellules à compléter portent un fond ambre très clair `FBF0E1` — seule teinte ajoutée à la palette, et uniquement pour cet usage. Les colonnes calculées ou pré-remplies restent blanches et sont verrouillées, la feuille étant protégée sans mot de passe. Poser une validation de données partout où les valeurs sont contraintes : liste déroulante pour un choix fermé, plage pour une date ou un nombre. Une seule ligne d'exemple est autorisée, en gris italique, avec « Exemple » en première colonne : c'est le moyen le plus court de montrer un format de date ou d'IBAN attendu, et elle se supprime d'un clic. Rien d'autre ne s'écrit dans la feuille.

## Vérification avant livraison

Convertir le fichier et le regarder, plutôt que se fier au script qui vient de l'écrire :

```bash
python /root/.claude/skills/xlsx/scripts/recalc.py fichier.xlsx   # obligatoire dès qu'il y a des formules
python /root/.claude/skills/xlsx/scripts/office/soffice.py --headless --convert-to pdf fichier.xlsx
pdftoppm -jpeg -r 100 fichier.pdf page && ls page-*.jpg   # puis lire les images
```

Contrôler : en-tête figé et filtré, aucune colonne tronquée ni démesurée, dates et montants au bon format (pas de `#####`, pas de `45231` à la place d'une date), aucun texte d'explication résiduel, aucune cellule fusionnée dans les données, et pour un formulaire, que seules les cellules à remplir soient modifiables.

Puis, dans la réponse à l'utilisateur : ce qui manque, ce qui a été supposé, ce qui reste à compléter. C'est là que ça se dit.
