# Libellés exacts de l'onglet 1 par mécanique

Les clés du JSON `--info` doivent correspondre **exactement** à ces libellés (accents et espaces compris) pour pré-remplir la bonne cellule. Les clés inconnues sont ignorées ; les champs non fournis gardent leur exemple grisé.

Libellés **communs** à toutes les mécaniques :
`Client / Marque` · `Nom de l'opération` · `N° opération (idgame)` · `URL de test` · `E-mail de test` · `Dédoublonnage paramétré` · `Testeur(s) côté client` · `Contact Promo.dev (chef de projet)` · `Date limite de retour des tests`

## ODR (`--mechanic ODR`)
- `IBAN de test à utiliser`  (défaut : `FR7630001007941234567890185`)
- `Type de justificatif attendu`
- `Montant du remboursement`
- `Dates de l'offre`

## Jeux (`IG_AOA`, `IG_SOA`, `TAS_AOA`, `TAS_SOA`, `AUTO_AOA`, `AUTO_SOA`)
- `Dotation / lots`
- Dates : `Dates (début / fin)` — **sauf tirage au sort** (`TAS_*`) qui utilise `Dates (début / fin / tirage)`
- **Ne pas fournir** `Type de jeu` ni `Obligation d'achat` : le script les renseigne automatiquement selon le code mécanique.
- `AOA` (avec achat) ajoute la ligne `Justificatif attendu` ; tu peux la fournir.

## PRIME (`--mechanic PRIME`)
- `Nature de la prime`
- `Justificatif attendu`
- `Preuve produit demandée ?`  (ex. « n° de série / IMEI » ou « non »)
- `Dates (début / fin d'achat / fin)`
- (`Adresse de livraison requise` est posée automatiquement.)

## FORMULAIRE (`--mechanic FORMULAIRE`)
- `Objet du formulaire`
- `Champs collectés`
- `Pièce jointe demandée ?`
- `Double opt-in (confirmation e-mail) ?`
- `Dates de l'opération`
