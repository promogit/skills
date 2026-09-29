# Recettes docx-js pour la charte PROMO.DEV

Comment traduire le gabarit doc-page (HTML) en un `.docx` fidèle, avec la bibliothèque `docx` (npm, préinstallée). Lire d'abord le SKILL.md du skill `docx` pour les pièges généraux (largeurs de tables en DXA, listes via `numbering`, jamais de `\n`, etc.) — ce fichier ne couvre que ce qui est propre à la charte.

## Conversions

Le gabarit est en px. Règles : `pt = px × 0.75` · taille docx-js = pt × 2 (demi-points) · `twips = px × 15` · bordures docx en huitièmes de point (`1 px → size: 6`).

Deux polices : **Red Hat Display** pour les titres (h1/h2/h3), les eyebrows, les chiffres clés et le mot-symbole ; **Open Sans** (police par défaut du document) pour le corps, les tables, les légendes et le pied de page. Tout run de titre/eyebrow/chiffre doit porter explicitement `font: "Red Hat Display"` — la police par défaut ne s'applique qu'au reste.

| Élément | Gabarit | docx-js (run) | Interligne (paragraphe) |
|---|---|---|---|
| Titre du document (h1) | 34 px, bold, bleu nuit | `font: "Red Hat Display", size: 51, bold: true, color: "00113D"` | `spacing: { line: 600, lineRule: "atLeast", after: 280 }` |
| Chapô | 18 px, léger, noir 70 % | `size: 27, color: "4D4D4D"` (pas de gras, Open Sans) | `spacing: { line: 440, lineRule: "atLeast", after: 420 }` |
| Titre de section (h2) | 21 px, bold, bleu nuit | `font: "Red Hat Display", size: 32, bold: true, color: "00113D"` | `spacing: { line: 380, lineRule: "atLeast", before: 360, after: 180 }`, `keepNext: true` |
| Sous-titre (h3) | 17 px, semibold, bleu nuit | `font: "Red Hat Display", size: 26, bold: true, color: "00113D"` | `spacing: { line: 320, lineRule: "atLeast", before: 280, after: 150 }`, `keepNext: true` |
| Corps | 14,5 px, interligne 1,7, noir 80 % | `size: 22, color: "333333"` (Open Sans) | `spacing: { line: 408, after: 180 }` (défaut du document) |
| Sur-titre (eyebrow) | 9–10 px, caps, interlettré, ambre | `font: "Red Hat Display", size: 15, bold: true, allCaps: true, characterSpacing: 30, color: "D97706"` | `spacing: { line: 240, lineRule: "atLeast" }` |
| Chiffre clé | 40 px, bold, ambre | `font: "Red Hat Display", size: 60, bold: true, color: "D97706"` | `spacing: { line: 640, lineRule: "atLeast", after: 100 }` |
| Pied de page | 8,5 px, noir 60 % | `size: 13, color: "666666"` (Open Sans) | `spacing: { line: 240, lineRule: "atLeast" }` |
| Mot-symbole PROMO.DEV | 15 px, bold | `font: "Red Hat Display", size: 23, bold: true, color: "00113D"` | `spacing: { line: 240, lineRule: "atLeast" }` |
| Cellule de table | 13 px | `size: 20` (Open Sans) | `spacing: { line: 280, lineRule: "atLeast", before: 60, after: 60 }` |

**L'interligne des titres se déclare toujours, et toujours avec `lineRule: "atLeast"`.** Deux pièges se combinent ici, et ils ont produit les deux défauts les plus visibles du gabarit :

1. Le style par défaut du document porte `line: 408` en mode `auto`, c'est-à-dire 1,7 fois la hauteur naturelle de ligne. Parfait pour du corps en 11 pt ; sur un titre de 25 pt, un titre qui passe sur deux lignes se retrouve avec un trou béant au milieu. Tout paragraphe de titre doit donc redéclarer son propre interligne.
2. Si on écrit `spacing: { line: 276 }` sans `lineRule`, Word comprend « 1,15 fois » mais LibreOffice comprend « 276 twips exactement » — soit 13,8 pt pour un titre de 25 pt, et les deux lignes se chevauchent. Les valeurs du tableau sont des hauteurs absolues en twips (twips = points × 20) avec `lineRule: "atLeast"` : les deux moteurs les lisent pareil, et une ligne plus haute que prévu s'ajuste au lieu d'être tronquée.

Le corps de texte garde le `line: 408` par défaut du document : c'est le rendu validé, ne pas y toucher.

**Titres solidaires de leur texte** : mettre `keepNext: true` sur tout paragraphe de titre, et `cantSplit: true` sur les lignes de table. Sans cela un titre de section reste régulièrement seul en bas de page et un encadré se coupe en deux — c'est arrivé sur chaque document de test avant qu'on l'ajoute.

**Polices sur la machine de rendu** : pour que la vérification visuelle soit fidèle, installer Red Hat Display et Open Sans si `fc-list | grep -iE "red hat display|open sans"` ne renvoie rien :

```bash
mkdir -p ~/.fonts && cd ~/.fonts
curl -sSL -o "RedHatDisplay[wght].ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/redhatdisplay/RedHatDisplay%5Bwght%5D.ttf"
curl -sSL -o "RedHatDisplay-Italic[wght].ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/redhatdisplay/RedHatDisplay-Italic%5Bwght%5D.ttf"
curl -sSL -o "OpenSans[wdth,wght].ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/opensans/OpenSans%5Bwdth%2Cwght%5D.ttf"
curl -sSL -o "OpenSans-Italic[wdth,wght].ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/opensans/OpenSans-Italic%5Bwdth%2Cwght%5D.ttf"
fc-cache -f
```

Le `.docx` déclare les noms de polices sans les embarquer : sur le poste du lecteur, Word utilisera ses polices installées (c'est le cas chez PROMO.DEV).

## Couleurs (opacités converties sur fond blanc)

Bleu nuit `00113D` · ambre `D97706` · ambre 50 % `ECBB82` · noir 80 % `333333` · 75 % `404040` · 70 % `4D4D4D` · 60 % `666666` · 50 % `808080` · 45 % `8C8C8C` · 40 % `999999` · filet 10 % `E6E6E6` · filet 20 % `CCCCCC` · fond gris `F7F7F7` · blanc 60 % sur bleu nuit `99A0B1`. Rien d'autre.

## Squelette du document

Page A4, marges 0,85 in = **1224 twips**. Largeur utile ≈ **9458 twips** (les `columnWidths` de chaque table doivent sommer à cette valeur). Police par défaut Open Sans (si elle n'est pas installée sur la machine de rendu, Word/LibreOffice substituera — c'est acceptable, ne pas chercher à l'embarquer).

```js
const doc = new Document({
  styles: { default: { document: { run: { font: "Open Sans", size: 22, color: "333333" },
    paragraph: { spacing: { line: 408, after: 180 } } } } },
  numbering: { config: [ /* puces et listes numérotées — jamais de caractères littéraux */ ] },
  sections: [{
    properties: { page: { margin: { top: 1224, bottom: 1224, left: 1224, right: 1224 } } },
    headers: { default: new Header({ children: [enTete] }) },
    footers: { default: new Footer({ children: piedDePage }) },
    children: [ /* contenu */ ],
  }],
});
```

### En-tête (jamais modifié)

Un seul paragraphe : mot-symbole à gauche, sur-titre (eyebrow) du document à droite via tabulation droite, filet sous le paragraphe.

```js
const enTete = new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E6E6E6", space: 4 } },
  spacing: { after: 240 },
  children: [
    new TextRun({ text: "PROMO.DEV", font: "Red Hat Display", bold: true, size: 23, color: "00113D" }),
    new TextRun({ text: "\t" }),
    new TextRun({ text: EYEBROW, font: "Red Hat Display", bold: true, allCaps: true, size: 15, characterSpacing: 30, color: "D97706" }),
  ],
});
```

L'eyebrow décrit le type de document : « Proposition commerciale », « Mémo interne », « Lettre », « Rapport »… en capitales, séparateur point médian si besoin (ex. « PROPOSITION · VOYAGES HORIZON »).

### Pied de page (jamais modifié)

Deux paragraphes avec tab droite, filet au-dessus du premier :

```js
const piedDePage = [
  new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: "E6E6E6", space: 4 } },
    spacing: { line: 240, after: 0 },
    children: [
      new TextRun({ text: "SAS PROMO.DEV", bold: true, size: 13, color: "333333" }),
      new TextRun({ text: "\tSIREN 890 559 883 — SIRET 890 559 883 00024", size: 13, color: "666666" }),
    ],
  }),
  new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
    spacing: { line: 240, after: 0 },
    children: [
      new TextRun({ text: "276 avenue du Douard, 13400 Aubagne, France — https://promo.dev", size: 13, color: "666666" }),
      new TextRun({ text: "\tTVA FR28890559883 — NAF 7311Z", size: 13, color: "666666" }),
    ],
  }),
];
```

## Recettes par bloc

Les tables de mise en page (blocs A, C, D, F, H) sont des tables docx **sans bordures** sauf celles indiquées (`borders` avec `style: BorderStyle.NONE` partout ailleurs), `columnWidths` sommant à 9458.

- **Bloc A — destinataire** : table 2 colonnes (4729/4729) sans bordures. Gauche : adresse du destinataire en `808080`. Droite, alignée à droite : « Aubagne, le [date] » en `4D4D4D`, puis Objet et Réf. en `808080`.
- **Bloc B — titre de section** : un titre h2 numéroté (« 1. Un pipeline unique, de la demande au versement. »), puis le corps. Rien au-dessus du titre — pas de sur-titre ambre, pas de filet, pas de mention de rubrique. Le numéro est saisi dans le texte du titre, pas via une liste automatique : les titres restent ainsi manipulables un par un et le numéro adopte la couleur et la police du titre. Titres en minuscules de phrase, terminés par un point.
- **Bloc C — chiffres clés** : table 3 colonnes sans bordures. Par cellule : le chiffre (`size: 60, bold, "D97706"`) puis la légende (`size: 19, color: "4D4D4D"`) qui précise ce que mesure le chiffre, pour quel client, sur quelle période.
- **Bloc D — encadré sombre** (une seule fois par document) : table 1×1, `shading: { type: ShadingType.CLEAR, fill: "00113D" }`, marges de cellule ~300 twips. Eyebrow ambre, affirmation en blanc `size: 27` non gras, source en `99A0B1` `size: 18`.
- **Bloc E — avant / après** : vraie table de données, uniquement des bordures horizontales (`E6E6E6`, `CCCCCC` sous l'en-tête). En-têtes en style eyebrow : « Indicateur » et « Avec PROMO.DEV » en ambre, « Avant » en `999999`. Colonne « Avant » en `8C8C8C`, colonne « Avec PROMO.DEV » en gras `00113D`.
- **Bloc F — étapes numérotées** : table 3 colonnes, bordure haute `E6E6E6` et filets verticaux intérieurs `E6E6E6`. Par cellule : « 01 » (`ECBB82`, bold, `characterSpacing: 30`, Red Hat Display), nom de l'étape en gras `00113D`, une phrase en `4D4D4D`. Étapes canoniques : Collecter · Décider · Agir.
- **Bloc G — citation** : paragraphe avec `border.left { size: 12, color: "D97706" }`, `indent: { left: 300 }`, italique `00113D` `size: 26` ; attribution en dessous `size: 18, color: "666666"`.
- **Bloc H — prochaines étapes** : table 1×1 bordée `E6E6E6`, titre « Prochaines étapes. » en gras `00113D`, puis liste numérotée (config `numbering`, format « [Action] — [responsable], [échéance]. »).
- **Bloc I — signature** : formule de politesse française complète, puis nom en gras `00113D`, fonction « [Fonction] — PROMO.DEV » et coordonnées en `666666` `size: 19`.
- **Encadré clair (note ou avertissement)** : table 1×1, fond `F7F7F7`, bordure gauche ambre `size: 18`, autres bordures `E6E6E6`. Eyebrow ambre puis texte corps.

## Vérification

Après génération, rendre et regarder chaque page (commandes dans le SKILL.md du skill `docx` : `soffice.py --convert-to pdf` puis `pdftoppm`). Vérifier en particulier : en-tête et pied présents sur toutes les pages, mentions légales exactes, aucune couleur hors palette, chiffres clés lisibles, tables non débordantes, pas de bloc D en double.
