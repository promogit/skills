---
name: houston-datalist
description: "Crée le fichier Excel d'import d'une datalist Houston (produits porteurs/EAN, enseignes, PDV, paliers de remboursement) à partir d'un Excel client, d'un PDF ou d'un copier-coller."
---

# Datalist Houston : fichier d'import .xlsx

> **Aucune donnée client dans ce skill.** Les exemples sont fictifs ou génériques : aucun nom de client, d'agence, d'adresse, de DPO, de numéro d'opération ni de formulation propre à un client. Quand une information nécessaire manque dans les documents fournis ou dans Houston (société organisatrice, agence, adresse DPO ou délégation écrite à Promodev, durée de conservation, étude de dépôt, montants, dotations, formulation déjà validée pour ce client…), **poser la question** au chef de projet avant de rédiger. Ne jamais la reprendre d'une autre opération ni l'inventer.

Utiliser ce skill dès que le chef de projet demande de préparer, créer, convertir ou nettoyer une datalist pour une opération Houston : liste de produits porteurs / codes EAN, liste d'enseignes, liste de points de vente (PDV), liste avec paliers de remboursement. Déclencher aussi sur « fichier codes EAN Houston », « liste produits pour le formulaire », « import datalist ».

## Format d'import (impératif)

- Fichier **.xlsx**, **un seul onglet** nommé `Feuil1` (Houston lit le premier onglet : ne jamais laisser d'onglet de travail devant).
- Ligne 1 = en-têtes, en minuscules, dans cet ordre : `label` | `value` | colonnes metadata éventuelles.
- Données dès la ligne 2, sans ligne vide, sans titre, sans total, sans note.
- Toutes les cellules au **format texte** (EAN compris : sinon Excel perd les zéros de tête ou affiche en notation scientifique).
- Chaque colonne après `value` devient une clé `metadata` dans Houston, avec l'en-tête comme nom de clé (les espaces deviennent `_` : « montant remboursé » → `montant_remboursé`). Nommer ces en-têtes directement en snake_case sans espace.
- Nom du fichier : `<n° opé> - <Type> Houston.xlsx` (ex. `999 - Codes EAN Houston.xlsx`, `999 - PDV Houston.xlsx`).

## Les modèles de liste

### 1. Produits porteurs / codes EAN (champ `EAN` du formulaire)
- `label` = **EAN seul** (13 chiffres le plus souvent), c'est ce que le participant saisit.
- `value` = hiérarchie produit séparée par ` > ` (espace, chevron, espace), **EAN toujours en dernier**.
- La hiérarchie suit les colonnes disponibles dans le fichier client, du plus général au plus précis. Exemples (fictifs) :
  - marque > famille > référence > EAN : `MARQUE > ASPIRATEUR > REF-200 > 3000000000017`
  - réf. interne > désignation > EAN : `REF123ABC > Coque smartphone transparente > 3000000000024`
  - arborescence longue : `MARQUE > COULEURS INTERIEURS > GAMME > Mat Velouté > 2 L > Teinte > 3000000000031`
- Variante courte (petites listes) : `label` = `value` = `EAN - Désignation` (`3000000000048 - Caméra compacte`). À utiliser seulement si le chef de projet le demande ou si l'opération de référence le fait.

### 2. Enseignes
- `label` = `value` = nom de l'enseigne, orthographe et accents officiels (`Brico Dépôt`, `Mr Bricolage`, `La Fnac`).

### 3. Points de vente (PDV)
- `label` = `value` = `CODE,NOM DU MAGASIN,Adresse,CP VILLE` (virgules sans espace entre les blocs).
- Données de suivi en metadata si le client les fournit : ex. `RT`, `RR`, `DV` (responsables terrain / régional / directeur des ventes). S'il y a des colonnes de suivi dans le fichier et qu'on ne sait pas s'il faut les garder, poser la question.

### 4. ODR à paliers de remboursement
- Liste produits (modèle 1) + colonne metadata **`amount_to_refund`**.
- Montant **en centimes, entier, sans symbole ni séparateur** : 15 € → `1500`, 75 € → `7500`, 29,90 € → `2990`.
- Toujours reconvertir les euros du fichier client en centimes et le signaler dans le récap.
- `amount_to_refund` est la clé standard. Si l'opération de référence utilise une autre clé (ex. `montant_remboursé`), demander laquelle garder avant de livrer.

## Déroulé

1. **Identifier l'opération** si un n° / idgame est donné : `find_operation`, puis `list_datalists` pour voir les listes existantes (titres, format de value déjà utilisé, metadata). S'aligner sur ce qui existe déjà pour ce client (même hiérarchie, même clé metadata).
2. **Lire la source** :
   - Excel client : repérer les colonnes (marque, catégorie, modèle, désignation, contenance, teinte, EAN, montant…) ; ignorer lignes de titre, totaux, lignes vides, onglets annexes.
   - PDF / règlement : extraire le tableau des produits éligibles (skill pdf si besoin).
   - Copier-coller : parser ligne à ligne.
3. **Choisir le modèle** (produits / enseignes / PDV / paliers). Si la hiérarchie de `value` n'est pas évidente, proposer l'ordre des niveaux en une ligne avant de générer.
4. **Nettoyer** : espaces multiples et insécables, espaces en début/fin, EAN stockés en nombre ou en notation scientifique (`3.03152E+12` → reprendre depuis la source), apostrophes typographiques incohérentes. Garder la casse et les accents d'origine des désignations.
5. **Contrôler** :
   - pas de `label` vide ni en doublon (un EAN présent deux fois = alerte, garder la première occurrence et le signaler) ;
   - EAN : 8, 12, 13 ou 14 chiffres et clé de contrôle valide (alerter sans supprimer) ;
   - l'EAN en fin de `value` est identique au `label` ;
   - montants : numériques, en centimes, cohérents avec les paliers annoncés.
6. **Générer** le .xlsx avec le script ci-dessous, dans `/mnt/user-data/outputs/`, puis l'envoyer en téléchargement.
7. **Récap court** : nombre de lignes, modèle utilisé, exemple de 2 lignes, alertes (doublons, EAN invalides, conversions en centimes), paliers détectés avec le nombre de produits par palier.

## Script de génération

```python
import re, unicodedata
from openpyxl import Workbook

EAN_RE = re.compile(r"^\d{8}$|^\d{12,14}$")

def ean_ok(code):
    code = str(code)
    if not EAN_RE.match(code):
        return False
    digits = [int(c) for c in code]
    check = digits.pop()
    s = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(digits)))
    return (10 - s % 10) % 10 == check

def clean(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", str(s)).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()

def build_datalist(rows, out_path, metadata_keys=()):
    """rows : liste de dicts {"label", "value", <clés metadata>}"""
    warnings, seen, out = [], set(), []
    for i, r in enumerate(rows, 1):
        label, value = clean(r.get("label")), clean(r.get("value"))
        if not label or not value:
            warnings.append(f"ligne {i} : label ou value vide -> ignorée"); continue
        if label in seen:
            warnings.append(f"ligne {i} : doublon de label '{label}' -> ignoré"); continue
        seen.add(label)
        m = re.search(r"(\d{8,14})\s*$", value) or re.match(r"^(\d{8,14})$", label)
        if m and not ean_ok(m.group(1)):
            warnings.append(f"ligne {i} : EAN '{m.group(1)}' clé de contrôle invalide (conservé, à vérifier)")
        out.append([label, value] + [clean(r.get(k)) for k in metadata_keys])
    wb = Workbook(); ws = wb.active; ws.title = "Feuil1"
    ws.append(["label", "value", *metadata_keys])
    for row in out:
        ws.append(row)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.number_format = "@"
    for col, w in zip("ABCDEFGH", [20, 70] + [18] * 6):
        ws.column_dimensions[col].width = w
    wb.save(out_path)
    return len(out), warnings
```

Lire les EAN de la source en texte (`pd.read_excel(..., dtype=str)`) ; si un EAN arrive en float (`3031520289986.0`), le convertir via `str(int(x))`.

## À ne pas faire

- Pas d'en-tête stylé, de volet figé, de filtre, de couleur ni d'onglet explicatif : le fichier est un import technique brut.
- Ne pas inventer de niveau de hiérarchie absent de la source.
- Ne pas mettre de montant en euros décimaux dans `amount_to_refund`.
- Ne pas créer ni modifier la datalist dans Houston (import manuel par le chef de projet dans le backoffice).