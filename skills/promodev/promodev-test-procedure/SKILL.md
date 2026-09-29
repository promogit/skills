---
name: promodev-test-procedure
description: >-
  Génère le classeur Excel « Procédure de test » adapté à une opération Promo.dev, à partir de son
  lien de test (test.promo.dev/…) et/ou de son idgame. Le skill récupère l'opération dans Houston,
  détecte la mécanique (ODR, jeu instant gagnant, tirage au sort, 100 % gagnant, prime, formulaire/opt-in),
  choisit le bon gabarit et pré-remplit l'onglet 1. Utilise ce skill DÈS QUE l'utilisateur fournit un lien
  test.promo.dev, un idgame / n° d'opération, ou demande de préparer, compléter, générer ou envoyer une
  procédure de test, une checklist de test ou un gabarit de test pour une opération promotionnelle — même
  s'il ne dit pas explicitement « skill » ni ne nomme la mécanique.
---

# Générateur de procédure de test Promo.dev

> **Aucune donnée client dans ce skill.** Les exemples sont fictifs ou génériques : aucun nom de client, d'agence, d'adresse, de DPO, de numéro d'opération ni de formulation propre à un client. Quand une information nécessaire manque dans les documents fournis ou dans Houston (société organisatrice, agence, adresse DPO ou délégation écrite à Promodev, durée de conservation, étude de dépôt, montants, dotations, formulation déjà validée pour ce client…), **poser la question** au chef de projet avant de rédiger. Ne jamais la reprendre d'une autre opération ni l'inventer.

À partir d'un **lien de test** et/ou d'un **idgame**, ce skill produit le classeur Excel de test **adapté à la mécanique** de l'opération, avec l'**onglet 1 pré-rempli** grâce aux données de Houston. L'utilisateur veut, dans l'idéal, ne fournir que le lien + l'idgame.

Le classeur a toujours 5 onglets — *Mode d'emploi · Guide Houston · Checklist · Anomalies · Validation* — avec statut de test **par appareil (Desktop / Tablette / Mobile)**, captures **figées** (ancrage absolu) et habillage navy/orange. Tout est déjà dans le script `scripts/generate.py` ; ton rôle est d'**orchestrer** : trouver l'opération, détecter la mécanique, la faire confirmer, réunir les infos, puis lancer le script.

## Workflow

### 1. Identifier l'opération dans Houston
L'`operationId` est le **dernier segment de l'URL** de test : `https://test.promo.dev/<operationId>`. Si seul l'idgame est fourni, résous-le avec `find_operation(search=<idgame>)`.

Récupère ensuite :
- `operation_info(operationId)` → `client`/`client_nom`, `title`, `idgame`, `date_debut`, `date_fin`, `date_fin_achat`, `type`, statut.
  ⚠️ `client_nom`/`client_prenom` sont les coordonnées du **contact côté CLIENT** (ex. le contact chez la marque/l'annonceur), **pas** le chef de projet Promo.dev. Ne jamais les utiliser pour remplir `"Contact Promo.dev (chef de projet)"`.
- La collection **`lots`** filtrée sur cet `operationId` (`query_collection collection=lots filter={"operationId": "<id>"}`) → pour les jeux : `type` des lots = **IG** (instant gagnant) ou **RANKING** (tirage), et présence éventuelle d'un **lot de consolation**.

### 2. Détecter la mécanique — puis CONFIRMER
Le champ `operations.type` **n'est pas fiable à 100 %** (on a déjà vu une ODR rangée en « JEU SOA »). Utilise-le comme indice, croise avec les lots et, si besoin, avec le parcours réel du site, puis **annonce ta conclusion en une ligne et attends la confirmation (ou correction) de l'utilisateur avant de générer.**

Indices de détection :
- `type = ODR` → **ODR**.
- `type = PRIME` → **PRIME** (cadeau/produit offert après achat ; le formulaire collecte une **adresse de livraison**, pas d'IBAN).
- `type = FORM` / `FORMULAIRE` → **FORMULAIRE** (collecte / opt-in, sans achat ni lot).
- `type = JEU WEB` / `JEU SOA` → un **jeu**. Précise deux axes :
  - **Mécanique de jeu** : lots `type=IG` → instant gagnant ; lots `type=RANKING` → tirage au sort ; présence d'un lot de consolation (petit lot type bon de réduction pour les non-gagnants) → **100 % gagnant**.
  - **Obligation d'achat** : `JEU WEB` ≈ avec achat, `JEU SOA` ≈ sans achat — **à vérifier** (voir §6).

En cas de doute (type incohérent, lots vides, obligation d'achat ambiguë), ouvre le site de test dans le navigateur (§6) : c'est le signal le plus fiable.

### 3. Demander les 3 infos que Houston ne connaît pas
Avant de générer, demande à l'utilisateur (une seule fois) :
- **Testeur(s) côté client**
- **E-mail de test** (une boîte accessible)
- **Date limite de retour des tests**

(S'il ne les a pas sous la main, génère quand même : ces cellules garderont leur exemple à compléter.)

Ne pas demander le **« Contact Promo.dev (chef de projet) »** : c'est la personne qui utilise ce skill. Mettre son nom s'il est connu (profil ou conversation), sinon le lui demander une seule fois ; ne jamais le déduire de Houston.

### 4. Construire le JSON d'infos (onglet 1)
Écris un fichier JSON `{ "<libellé exact de l'onglet 1>": "<valeur>" }`. Les libellés **communs à toutes les mécaniques** (les plus utiles) :

- `"Client / Marque"`, `"Nom de l'opération"`, `"N° opération (idgame)"`, `"URL de test"`
- `"E-mail de test"`, `"Testeur(s) côté client"`, `"Contact Promo.dev (chef de projet)"`, `"Date limite de retour des tests"`, `"Dédoublonnage paramétré"`

Libellés **spécifiques** (n'inclure que ceux de la mécanique visée — voir `references/field-labels.md` pour la liste complète par mécanique) :
- ODR : `"IBAN de test à utiliser"`, `"Type de justificatif attendu"`, `"Montant du remboursement"`, `"Dates de l'offre"`.
- Jeux : `"Dotation / lots"`, et les dates via `"Dates (début / fin)"` (ou `"Dates (début / fin / tirage)"` pour un **tirage au sort**). *(« Type de jeu » et « Obligation d'achat » sont posés automatiquement par le script, ne pas les fournir.)*
- PRIME : `"Nature de la prime"`, `"Justificatif attendu"`, `"Dotation / lots"`, `"Dates (début / fin d'achat / fin)"`.
- FORMULAIRE : `"Objet du formulaire"`, `"Champs collectés"`, `"Dates de l'opération"`.

L'`"IBAN de test à utiliser"` par défaut est **`FR7630001007941234567890185`** (sauf indication contraire). Le `"Contact Promo.dev (chef de projet)"` est **le nom de la personne qui utilise ce skill** (à mettre systématiquement, dans le format qu'elle précise — ex. avec fonction). N'inclure dans le JSON que les clés dont tu as la valeur ; les autres gardent leur exemple.

⚠️ Si l'opération collecte une **carte de paiement dématérialisée** (type « Promocard » ou équivalent), le remboursement est envoyé **par e-mail**, pas par IBAN ni par courrier postal — ne pas supposer un envoi postal même si le formulaire a un champ adresse (souvent utilisé pour l'éligibilité géographique). En cas de doute sur le mode de restitution, vérifie le PDF des **modalités de l'offre** (lien en bas du site de test) avant de renseigner `"IBAN de test à utiliser"` / `"Montant du remboursement"`.

### 5. Générer
```bash
python3 scripts/generate.py --mechanic <CODE> --info <info.json> --out "<Procédure de test ... - NomOp.xlsx>"
```
Codes `--mechanic` : `ODR` · `IG_AOA` · `IG_SOA` · `TAS_AOA` · `TAS_SOA` · `AUTO_AOA` · `AUTO_SOA` · `PRIME` · `FORMULAIRE`
(`IG` = instant gagnant, `TAS` = tirage au sort, `AUTO` = 100 % gagnant ; `AOA` = avec achat, `SOA` = sans achat.)

Nomme le fichier de sortie de façon parlante, ex. `Procédure de test IG avec achat - <Client> <idgame>.xlsx`.

### 6. Présenter
Présente le `.xlsx` à l'utilisateur. Termine en listant, s'il y en a, les cellules de l'onglet 1 restées en exemple (celles qu'il n'a pas fournies) pour qu'il les complète.

## Vérifier la mécanique sur le site (fallback fiable)
Si le type Houston est douteux, ouvre `https://test.promo.dev/<operationId>` avec le navigateur et lis le parcours :
- **Menu « Visuel »** de la barre Houston : `Home / Perdu / <noms de lots>` → jeu **IG** ; `Home / <primes>` → **PRIME** ; `Home / Confirmation` → **ODR** ou **FORMULAIRE**.
- **Formulaire** : présence d'un **IBAN** → ODR ; d'une **adresse de livraison** → PRIME ; d'un **justificatif d'achat** → mécanique avec obligation d'achat ; simple collecte d'e-mail / opt-in sans achat → FORMULAIRE.
- Une **étape de jeu** (résultat gagné/perdu, « je joue ») → jeu.

## Règles déjà intégrées au script (pour information)
- L'onglet 1 est rempli par le chef de projet ; les valeurs fournies s'affichent en **texte foncé**, les champs non fournis restent en **exemple grisé**.
- **Jeux sans obligation d'achat (SOA)** : pas de ligne « Suivi de participation » (ni Guide, ni checklist) — géré automatiquement.
- On dit **« Bon pour mise en ligne »**, jamais « BAT ».
- Captures **figées** en ancrage absolu (mêmes dimensions partout).

## Détails & référence
- `references/field-labels.md` — liste exacte des libellés de l'onglet 1 **par mécanique** (à consulter pour que les clés du JSON correspondent parfaitement).
- `scripts/generate.py` — le générateur (contient toute la logique et les gabarits). `assets/images/` — les captures Houston et pages neutres.

## Exemple
**Entrée utilisateur :** « Prépare la procédure de test pour https://test.promo.dev/0123456789abcdef01234567 (idgame 2026-marque-… / n° 999). Testeur : Marie L., e-mail de test marie+test@marque-exemple.fr, retour le 30/09. »

**Déroulé :**
1. `operationId = 0123456789abcdef01234567` ; `operation_info` → client « Marque Exemple », title « Jeu Rentrée des Classes », dates. Si le client, les dates ou les dotations ne ressortent pas de Houston, poser la question au lieu de les deviner.
2. `lots` → `type=IG` ; formulaire avec justificatif d'achat → **jeu instant gagnant, avec achat**. Annoncer : « Je détecte un JEU IG avec achat, je génère ? »
3. Après confirmation, JSON : `{"Client / Marque":"Marque Exemple","Nom de l'opération":"Jeu Rentrée des Classes","N° opération (idgame)":"999","URL de test":"https://test.promo.dev/0123456789abcdef01234567","Dotation / lots":"…","Dates (début / fin)":"…","E-mail de test":"marie+test@marque-exemple.fr","Testeur(s) côté client":"Marie L.","Contact Promo.dev (chef de projet)":"Prénom Nom","Date limite de retour des tests":"30/09"}`.
4. `python3 scripts/generate.py --mechanic IG_AOA --info info.json --out "Procédure de test IG avec achat - Marque Exemple 999.xlsx"`.
5. Présenter le fichier.
