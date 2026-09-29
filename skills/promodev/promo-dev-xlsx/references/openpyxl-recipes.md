# Recettes openpyxl pour la charte PROMO.DEV

Mise en œuvre concrète des règles du SKILL.md. Lire d'abord le SKILL.md du skill `xlsx` pour les pièges généraux d'openpyxl (recalcul obligatoire, fonctions évaluables, double chargement) — ce fichier ne couvre que ce qui est propre à la charte.

## Palette et styles de base

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BLEU   = "00113D"   # en-têtes, libellés forts
AMBRE  = "D97706"   # chiffre principal, accents — avec parcimonie
GRIS   = "666666"   # ligne d'exemple, texte secondaire
FOND   = "F7F7F7"   # fond d'en-tête
FILET  = "E6E6E6"   # filets
SAISIE = "FBF0E1"   # fond des cellules à remplir (formulaires uniquement)

POLICE = "Open Sans"   # Excel substitue proprement si elle manque

F_CORPS  = Font(name=POLICE, size=10)
F_FORT   = Font(name=POLICE, size=10, bold=True, color=BLEU)
F_CHIFFRE= Font(name=POLICE, size=14, bold=True, color=AMBRE)
F_EXEMPLE= Font(name=POLICE, size=10, italic=True, color=GRIS)

REMPL_SAISIE = PatternFill("solid", fgColor=SAISIE)
```

## Formats de nombres

```python
FMT_DATE    = "DD/MM/YYYY"
FMT_ENTIER  = "#,##0"
FMT_EURO    = '#,##0.00 "€"'
FMT_EURO_R  = '#,##0 "€"'        # montants arrondis
FMT_TAUX    = "0.0%"             # valeur stockée en fraction : 0.155 → 15,5 %
FMT_TEXTE   = "@"                # SIRET, IBAN, références : préserve les zéros de tête
```

Les codes s'écrivent avec le point et la virgule anglo-saxons (`#,##0.00`) : c'est la syntaxe interne du format. Excel les **affiche** ensuite avec les séparateurs de la locale du poste — espace et virgule sur un Excel français. Ne pas essayer d'écrire `# ##0,00` directement, le fichier serait invalide.

Un taux se stocke en fraction. Écrire `0.155` avec `FMT_TAUX` affiche `15,5 %` ; écrire `15.5` afficherait `1550,0 %`.

## Bandeau bleu nuit, en-tête de table, zebra, volets figés, filtre

Le bandeau occupe la ligne 1, la ligne 2 reste vide, la table commence en ligne 3.

```python
F_MARQUE   = Font(name="Red Hat Display", size=12, bold=True, color="FFFFFF")
F_TYPEDOC  = Font(name="Red Hat Display", size=9, bold=True, color=AMBRE)
F_ENTETE   = Font(name=POLICE, size=10, bold=True, color="FFFFFF")   # remplace la version claire
REMPL_BLEU = PatternFill("solid", fgColor=BLEU)
FILET_AMBRE = Side(style="medium", color=AMBRE)

def poser_bandeau(ws, type_doc, n_colonnes):
    """type_doc : en capitales, point médian en séparateur — « VERSEMENTS · JUILLET 2026 »."""
    for i in range(1, n_colonnes + 1):
        c = ws.cell(row=1, column=i)
        c.fill = REMPL_BLEU
        c.border = Border(bottom=FILET_AMBRE)      # le filet ambre qui signe le bandeau
    m = ws.cell(row=1, column=1, value="PROMO.DEV")
    m.font = F_MARQUE
    m.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    t = ws.cell(row=1, column=n_colonnes, value=type_doc.upper())
    t.font = F_TYPEDOC
    t.alignment = Alignment(horizontal="right", vertical="center", indent=1)
    ws.row_dimensions[1].height = 34
    ws.row_dimensions[2].height = 8                # respiration avant la table
    return 3                                       # ligne de l'en-tête de colonnes

def poser_entete(ws, colonnes, ligne=3):
    """colonnes : liste de (titre, largeur, alignement) — alignement 'left' ou 'right'."""
    for i, (titre, largeur, align) in enumerate(colonnes, start=1):
        c = ws.cell(row=ligne, column=i, value=titre)
        c.font, c.fill = F_ENTETE, REMPL_BLEU
        c.alignment = Alignment(horizontal=align, vertical="center")
        ws.column_dimensions[get_column_letter(i)].width = largeur
    ws.row_dimensions[ligne].height = 24
    ws.freeze_panes = ws.cell(row=ligne + 1, column=1)   # → "A4"

REMPL_ZEBRA = PatternFill("solid", fgColor=FOND)

def poser_zebra(ws, premiere=4, derniere=None, n_colonnes=None):
    """Fond F7F7F7 une ligne sur deux, sur toute la largeur de la table."""
    derniere = derniere or ws.max_row
    n_colonnes = n_colonnes or ws.max_column
    for r in range(premiere + 1, derniere + 1, 2):
        for i in range(1, n_colonnes + 1):
            ws.cell(row=r, column=i).fill = REMPL_ZEBRA

# après avoir écrit les données, si le filtre a du sens :
ws.auto_filter.ref = f"A3:{get_column_letter(ws.max_column)}{ws.max_row}"
```

Le mot-symbole n'est pas tronqué : la cellule A1 déborde sur les cellules vides à sa droite tant qu'elles sont vides — c'est le cas dans le bandeau, où seule la dernière cellule porte du texte. Si la table n'a que deux colonnes étroites, élargir plutôt que fusionner.

Le filtre part de la ligne d'en-tête (`A3`) et descend jusqu'à la dernière ligne de données. S'il partait de `A1`, Excel prendrait le mot-symbole pour l'en-tête et trierait le bandeau avec les données. S'il s'arrêtait avant la dernière ligne, le tri ne réordonnerait qu'une partie du tableau. Le poser quand il sert : export, liste, détail par client, grille de saisie en table. Le laisser de côté sur une synthèse libellé/valeur ou une fiche verticale — il n'y a rien à y trier.

**Zebra et tri** : le fond alterné est purement décoratif — après un tri par l'utilisateur, les bandes restent en place (elles sont sur les lignes, pas sur les données), ce qui est le comportement attendu. Le poser en dernier, après l'écriture des données. Sur un formulaire en table, le zebra s'applique aussi, mais les cellules de saisie gardent leur fond `FBF0E1` (le poser avant le zebra et faire sauter ces colonnes dans la boucle, ou poser le zebra d'abord et la saisie ensuite).

Les volets se figent sous la ligne d'en-tête (`A4`), ce qui garde le bandeau **et** les titres de colonnes visibles au défilement.

Ordre de construction : largeurs → `poser_bandeau` → `poser_entete` → données → saisie/validations éventuelles → zebra → filtre.

## Fiche verticale (formulaire à champs longs)

Un champ par ligne : libellé en colonne A, saisie en colonne B, large. Les champs longs prennent plusieurs lignes de hauteur avec retour à la ligne automatique. Le bandeau s'y pose de la même façon, sur les deux colonnes : `poser_bandeau(ws, "Fiche d'opération promotionnelle", 2)` — le type de document arrive à droite dans la colonne B, large, donc lisible. Pas de zebra ni de filtre sur une fiche.

```python
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 82

def champ(ws, ligne, libelle, hauteur=18, multiligne=False):
    a = ws.cell(row=ligne, column=1, value=libelle)
    a.font = F_FORT
    a.alignment = Alignment(horizontal="left", vertical="top")
    b = ws.cell(row=ligne, column=2)
    b.fill = REMPL_SAISIE
    b.border = Border(bottom=Side(style="thin", color=FILET))
    b.alignment = Alignment(horizontal="left", vertical="top", wrap_text=multiligne)
    b.protection = Protection(locked=False)
    ws.row_dimensions[ligne].height = hauteur
    return b
```

Donner une hauteur de 50 à 80 points aux champs qui appellent une réponse rédigée, sinon la personne écrit trois mots là où on attend trois phrases. Le retour à la ligne automatique (`wrap_text`) est indispensable sur ces champs : sans lui, le texte saisi déborde visuellement sur les cellules voisines et paraît perdu.

## Largeurs de colonnes

Calibrer sur le contenu réel plutôt que deviner. Une colonne trop étroite affiche `#####` sur les nombres, une colonne trop large oblige à scroller :

```python
def calibrer(ws, mini=9, maxi=48, filtre=False):
    marge = 6 if filtre else 3
    for col in ws.columns:
        lettre = get_column_letter(col[0].column)
        longueur = max((len(str(c.value)) for c in col if c.value is not None), default=0)
        ws.column_dimensions[lettre].width = min(max(longueur + marge, mini), maxi)
```

À appeler après l'écriture des données. Pour une colonne de dates ou de montants, la largeur du format affiché compte plus que celle de la valeur brute — prévoir large sur ces colonnes (14–16).

**Table filtrée : élargir.** Excel dessine la flèche de filtre par-dessus la cellule d'en-tête, côté droit ; elle occupe l'équivalent de 2 à 3 caractères. Sur une colonne calibrée au plus juste, elle recouvre la fin du titre — et sur une colonne alignée à droite (dates, montants), elle mord aussi les valeurs proches du bord. D'où `filtre=True` ci-dessus (+3 de marge par colonne) dès que `auto_filter` sera posé. La marge ne suffit pas pour les en-têtes **alignés à droite** (dates, montants) : leur titre reste collé au bord droit, exactement sous la flèche, quelle que soit la largeur. Leur ajouter `indent=2` dans l'alignement de la cellule d'en-tête (uniquement l'en-tête — les valeurs, elles, ne portent pas de flèche). Vérifier ce point sur le rendu : un titre dont la dernière lettre disparaît sous la flèche est le défaut le plus fréquent des tables filtrées.

## Écrire les valeurs typées

```python
from datetime import date

c = ws.cell(row=r, column=1, value=date(2026, 7, 24))   # objet date, pas "24/07/2026"
c.number_format = FMT_DATE
c.alignment = Alignment(horizontal="right")

c = ws.cell(row=r, column=5, value=78623.40)            # float, pas "78 623,40 €"
c.number_format = FMT_EURO

c = ws.cell(row=r, column=2, value="0075")              # référence : texte
c.number_format = FMT_TEXTE

# donnée absente : ne rien écrire du tout
```

Une valeur écrite en chaîne de caractères se trie alphabétiquement (`10/01` avant `2/01`) et ne s'additionne pas. C'est l'erreur la plus coûteuse pour le destinataire, et elle est invisible tant qu'il n'a pas essayé de faire une somme.

## Onglet Synthèse d'un rapport

Libellé à gauche, valeur à droite, une ligne par chiffre, le chiffre principal en ambre. Les valeurs pointent vers les onglets de détail :

```python
ws["A1"] = "Passagers couverts"          ; ws["A1"].font = F_CORPS
ws["B1"] = "=NB.SI(Détail!D:D;\"payé\")" ; ws["B1"].font = F_CHIFFRE ; ws["B1"].number_format = FMT_ENTIER
```

Nom d'onglet contenant un espace ou un accent : le quoter dans les formules (`='Détail versements'!D:D`). Rester sur des fonctions d'avant 2007 (`SOMME.SI.ENS`, `INDEX`, `EQUIV`, `SIERREUR`) — voir le SKILL.md du skill `xlsx` sur celles qui ne survivent pas au recalcul.

openpyxl écrit les formules **en anglais** dans le fichier (`SUMIFS`, `COUNTIF`, `INDEX`) ; Excel les affiche traduites selon la langue du poste. Écrire les noms anglais, séparateur virgule.

## Formulaire : saisie, verrouillage, validation

```python
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Protection

# 1. tout verrouiller, puis déverrouiller les seules colonnes de saisie
for ligne in ws.iter_rows(min_row=2, max_row=200):
    for c in ligne:
        c.protection = Protection(locked=True)
for ligne in ws.iter_rows(min_row=2, max_row=200, min_col=3, max_col=5):
    for c in ligne:
        c.protection = Protection(locked=False)
        c.fill = REMPL_SAISIE

# 2. protéger la feuille (sans mot de passe : c'est un garde-fou, pas un verrou)
ws.protection.sheet = True
ws.protection.selectLockedCells = False

# 3. contraindre les valeurs
dv = DataValidation(type="list", formula1='"Virement,Carte,Avoir"', allow_blank=True)
ws.add_data_validation(dv)
dv.add("C2:C200")

dv_date = DataValidation(type="date", operator="between",
                         formula1="DATE(2026,1,1)", formula2="DATE(2026,12,31)", allow_blank=True)
ws.add_data_validation(dv_date)
dv_date.add("D2:D200")
```

Les cellules sont verrouillées par défaut dans Excel, mais le verrouillage ne prend effet qu'une fois `ws.protection.sheet = True` posé — d'où l'ordre ci-dessus. Prévoir la plage de saisie plus longue que le besoin estimé (200 lignes plutôt que le nombre exact) : le destinataire doit pouvoir ajouter des lignes sans buter sur une zone protégée.

Ligne d'exemple, si le format mérite d'être montré :

```python
for i, v in enumerate(["Exemple", "FR7630006000011234567890189", "Virement", date(2026, 9, 1)], start=1):
    c = ws.cell(row=2, column=i, value=v)
    c.font = F_EXEMPLE
```

## Ce qu'il ne faut pas écrire

Aucun de ces gestes n'a sa place dans un fichier PROMO.DEV, même bien intentionné : `ws.merge_cells`, y compris pour centrer le bandeau · un sous-titre, une période ou une mention « confidentiel » sous le titre · une ligne « Source : … » sous le tableau · `ws.cell(...).comment = Comment(...)` pour expliquer une colonne · un onglet `Méthodologie` · une ligne de total au bas d'un export · `"N/A"` ou `"à confirmer"` dans une cellule · des couleurs de statut vert/rouge non demandées.
