---
name: "houston-masque-saisie"
description: "Configure ou vérifie le masque de saisie d'une opération Houston — déduplicateurs, consignes, vérifications de fichiers — pour que le robot de saisie tranche l'éligibilité d'un dossier. Dès qu'un operationId, un idgame ou un lien bo.promo.dev accompagne ce besoin."
---

# Masque de saisie d'une opération (Houston + back-office)

Le masque de saisie porte les contrôles qui permettent au **robot de saisie** de décider si une demande de remboursement est valide ou invalide, à partir de l'OCR des justificatifs et des données d'une `/submission`.

Ce sont les **chefs de projet** qui montent les masques. Le MCP Houston n'expose pas le masque : il se lit et s'écrit dans le back-office, onglet Saisie (`https://bo.promo.dev/operation/<operationId>/saisie`), au navigateur. Le MCP sert à l'analyse et aux corrections de formulaire.

## 0. Avant toute chose : demander le cadre

Ne jamais ouvrir le back-office en écriture sans avoir posé ces deux questions, en une fois :

1. **Observer ou configurer ?** Relever le masque existant et le décrire, ou le créer et le corriger.
2. **Sur quelle opération ?** En demander l'`operationId` ou l'idgame.

**Ne jamais écrire sur une opération réelle sans accord explicite et préalable**, même si la demande semble le supposer. Pour s'entraîner ou tester une manipulation, l'opération de test est `6a6aff16f02bb7a04760a343` (« Test personnalisation Pauline »).

En mode configuration : présenter d'abord les blocs, lignes et consignes envisagés, obtenir l'accord, puis saisir.

## 1. Périmètre : éligibilité uniquement (bloquant)

Le robot confirme **l'éligibilité**. Le calcul de la prime n'est pas de sa responsabilité.

Ne créer aucune règle de validation, aucun déduplicateur, aucune consigne et aucune vérification de fichier portant sur : barème, pourcentage, palier de remboursement, plafond de montant, choix du produit remboursé (le moins cher, le plus cher), déduction des remises, arrondi, frais remboursés.

Ne pas reformuler une règle de calcul en contrôle d'éligibilité : si une règle des modalités ne sert qu'à déterminer le montant, l'ignorer sans la remplacer.

**Test à appliquer à chaque règle** : « si cette règle n'est pas respectée, la demande est-elle refusée ? » Oui → contrôle d'éligibilité à créer. Elle ne change que le montant versé → règle de calcul à ignorer.

### Le calcul du remboursement n'est pas dans le masque, et il ne se monte pas tout seul

Hors du masque ne veut pas dire automatique. Sur une ODR, le montant remboursé (`amount_to_refund`) vient des **réglages de l'opération**, ni du formulaire ni du masque :

- les `odr_options` de l'opération portent le mode de calcul — `ODR_SIMPLE_EUR`, `ODR_SIMPLE_PERCENT`, `ODR_EUR_PAR_PRODUIT`, `ODR_PERCENT_PAR_PRODUIT`, `ODR_DOUBLE_EUR_MIN`, ou `ODR_CUSTOM` avec son expression ;
- un barème par produit ou par palier se range dans la **liste de données**, champ `metadata.refund_amount` (en centimes) ;
- un cas qui ne rentre dans aucun mode passe par un hook, donc par le développement.

Tant que ces réglages ne sont pas posés, le montant reste vide ou faux, quel que soit le masque. Le vérifier en même temps que le masque et le signaler dans le livrable (partie 4, corrections hors masque) : ce n'est pas une ligne à créer, c'est un réglage à demander.

## 2. Analyser, dans cet ordre

Ne rien écrire avant d'avoir fait les quatre lectures.

1. **Le formulaire et ses unicités** : `find_operation` puis `operation_info` ; `list_forms(operationId)` ; `get_form` sur le formulaire `CREATE` **et** sur le `UPDATE` (suivi / régularisation). Relever pour chaque champ : `label`, `save_to`, `required`, `unique`, `options`, `dataListId`, `acceptedCountries`, `displayIf`, bornes `min`/`max` des dates.
2. **Les modalités** : le document publié sur l'habillage (`gabarit_kv_habillage` → `documents.modalites`), le fichier joint, ou le lien posé en tête des instructions de saisie. Si le PDF couvre plusieurs offres, ne retenir que celle de l'opération.
3. **Les instructions de saisie** : `get_operation_instructions(operationId)`, bloc `saisie` (le texte affiché en haut de l'onglet). Elles contiennent des règles, des tolérances et des **motifs NC imposés qui priment**. Lire aussi le bloc `interne` : il porte souvent la tolérance réelle.
4. **Le masque existant** : ouvrir l'onglet Saisie et relever ce qui est déjà en place (§3).

### Opération montée par copie : alerter sur les listes de données

La plupart des opérations sont montées en dupliquant la précédente. Tout suit : le formulaire, le masque, les réglages. **Les listes de données, elles, ne suivent pas forcément**, et rien ne proteste. Deux situations distinctes, **et dans les deux cas la question se pose au chef de projet avant d'écrire le contrôle qui s'appuie sur la liste**.

**Cas 1 — le champ vise une liste d'une autre opération.** Comparer chaque `dataListId` des champs du formulaire aux identifiants renvoyés par `list_datalists(operationId)`. Un identifiant absent de ce retour signifie que le champ pointe ailleurs — et l'API ne le refuse pas.

Ce n'est pas forcément une erreur : une même liste est parfois réutilisée volontairement d'une opération à l'autre, quand les produits, les enseignes ou les points de vente sont identiques. Signaler le champ, dire sur quelle liste il pointe et ce qu'elle contient, puis **demander : on conserve cette liste, ou on repointe vers celle de l'opération ?** Ne jamais repointer de sa propre initiative.

Ce qui penche vers l'oubli plutôt que vers la réutilisation voulue, à dire dans l'alerte pour que la réponse soit rapide : le contenu ne correspond pas aux modalités, la liste porte le nom d'un autre client ou d'une autre saison, le champ garde en plus des `options` en dur (une valeur `test`, un produit de l'an passé).

**Cas 2 — la liste est bien celle de l'opération, mais son contenu semble daté.** Comparer la taille et l'échantillon renvoyés par `list_datalists` aux produits, enseignes et points de vente éligibles des modalités.

**Attention à ce que ce retour permet de conclure** : c'est un **échantillon**, pas la liste entière. Un écart ne prouve donc pas que la liste est périmée, et une concordance ne prouve pas qu'elle est complète. Ne jamais annoncer « liste périmée » comme un constat : présenter ce qui a été comparé — nombre de valeurs annoncé par la liste, valeurs vues, produits attendus d'après les modalités — et **demander si c'est la bonne version de la liste**.

Autres traces de duplication à relever au passage : un libellé qui nomme un autre produit ou un autre client, une enseigne absente des modalités, des bornes de date héritées de l'opération précédente.

Dans tous ces cas, **ouvrir le livrable par l'alerte et par la question**, avant le reste : une liste héritée passe inaperçue jusqu'aux premières participations. Le chef de projet met les listes à jour avec le client ; le MCP peut les lire, pas les modifier. Repointer un champ vers une autre liste reste possible avec `update_field`, une fois la réponse obtenue.

### Vérifier que la donnée contrôlée est bien là où le contrôle la cherche

Un déduplicateur lit une **clé précise**. Si le formulaire range la valeur ailleurs, le contrôle ne se déclenche jamais — sans erreur, sans alerte. C'est le piège le plus coûteux de tout le masque.

Le cas le plus fréquent est la **date d'achat**. Elle doit être en `buying_date` (DateInput). Un formulaire qui l'enregistre en `date_input` casse à la fois « Date d'achat valide », « Jours entre achat et date » et « Jours ouvrés entre achat et date », et la rend invisible aux stats, aux exports et à la fiche du support. Le guide métier (`read_houston_guide` section `forms`) l'écrit noir sur blanc : `date_input` est réservé aux dates qui ne sont ni une naissance ni un achat.

Même logique pour les autres clés canoniques : `receipt_number` (numéro de ticket), `enseigne`, `dealer_name` (point de vente), `produit_achete` ou `produit_1` à `produit_10`, `iban`, `email`.

**Corriger le formulaire plutôt que contourner.** Poser un « Date input valide » sur un formulaire mal câblé fait marcher le contrôle, mais fige l'erreur. La correction propre est `update_field(formulaireId, save_to: "date_input", changes: {save_to: "buying_date"})`, puis la ligne du masque repasse sur « Date d'achat valide ». **Les deux doivent bouger ensemble** : corriger l'un sans l'autre rouvre la panne dans l'autre sens.

Sur une opération **qui a déjà des participations**, changer un `save_to` laisse orphelines les valeurs enregistrées sous l'ancienne clé : ne pas le faire de sa propre initiative, le poser comme arbitrage. Vérifier `stats.total_participations` avant.

## 3. Carte de l'onglet Saisie

Les sections apparaissent dans cet ordre. Le bouton **Sauvegarder** est en haut à droite, et **rien n'est persisté tant qu'il n'a pas été cliqué** : on peut déplier, ouvrir une liste, même ajouter une ligne pour l'inspecter puis la supprimer, sans rien modifier.

| Section | Contenu |
|---|---|
| **Instructions de saisie** | Texte libre pour les opérateurs (= bloc `saisie` du MCP) |
| **Opérateurs** | Opérateurs de traitement, blocages |
| **Supervision de la saisie** | « Limite des MISSING (3 max) », « Expiration des MISSING » |
| **Affichage de la fiche** | Mise en page du bloc identité |
| **Saisie de prix multiples** | Configuration des prix produits |
| **Champs de formulaire** | Champs additionnels : Date de poste, **Date d'achat**, Saisir les informations fournisseur, Quantité |
| **Enseigne** / **Point de vente** | Mode de saisie (Non / Liste de données) + datalist associée |
| **Produits** | Jusqu'à 10 slots : Produit N (liste de données) + Prix produit N (TTC) |
| **Consignes de saisie** | « Checkbox de saisie » : Consigne 1…N, « Ajouter une consigne », « Afficher le prix total » |
| **Numéro de saisie & ticket** | Numéro de série, Heure du passage en caisse, Numéro de caisse, Numéro de ticket / facture, Immatriculation |
| **Champs personnalisés** | Nom du champ, condition d'affichage, champ source, devise, liste ou champ libre, position |
| **Module de vérifications** | Les déduplicateurs (§5) |
| **Vérifications de fichiers (OUI / NON)** | Questions par couple Type / Sous-type (§7) |
| **Champs désactivés** | Un identifiant par ligne |
| **Paramètres d'OCR** | « Désactiver la complétion des champs produits en format EAN » |
| **Schema de saisie (JSON)** et **Template de bot de saisie (JSON)** | **Hors périmètre** (§9) |

**Déduplicateurs implicites.** Dans « Numéro de saisie & ticket », **Numéro de série** et **Numéro de ticket / facture** portent chacun une case « Désactiver le déduplicateur » : champ activé et case décochée = déduplication déjà active. C'est souvent ce qui couvre « un achat ne peut être remboursé qu'une fois » : le vérifier avant d'écrire une ligne équivalente.

Activer « Limite des MISSING (3 max) » si les modalités limitent à 3 régularisations, et le champ « Date d'achat » si un contrôle porte sur la date d'achat.

## 4. Règle de choix : où va chaque contrôle

| Le contrôle… | Va dans |
|---|---|
| se résout avec les seules valeurs du formulaire courant (format, obligatoire, cohérence entre deux champs) | une **règle de validation FormKit**, qui se configure dans le **formulaire** → la lister comme correction de formulaire |
| croise des données stockées en base | un **déduplicateur** (module de vérifications) |
| repose sur la lecture d'un document (OCR) ou sur un jugement | une **consigne** (case à cocher) |

En cas de doute entre validation et déduplicateur : si deux participants saisissant exactement les mêmes valeurs peuvent obtenir un résultat différent, c'est un déduplicateur.

**Aucun doublon** (bloquant). Un contrôle n'existe qu'à un seul endroit. Avant d'écrire une consigne ou une question de fichier, vérifier qu'il n'est pas déjà couvert par un déduplicateur, un réglage du masque, une **unicité du formulaire** (`unique: true` sur email, phone, iban…), un déduplicateur implicite, ou une autre consigne. S'il l'est, ne pas l'écrire, **même reformulé ou restreint à un cas particulier**.

## 5. Module de vérifications (déduplicateurs)

**Un bloc** porte : « Description du bloc », « Condition d'affichage du bloc (laisser vide pour toujours afficher) » avec un lien « Aide syntaxe FormKit », la liste « Vérifications », « Ajouter une ligne de vérification » et « Supprimer le bloc ». En bas : « Ajouter un bloc de vérifications ».

**Une ligne** se déplie en cliquant son titre, et porte dans cet ordre :

- **Description \*** — le titre affiché dans la liste ; y mettre la règle et sa période, pas un libellé vague ;
- **Vérification \*** — le type (tableau ci-dessous) ;
- **Champs clés \*** — étiquettes supprimables, champ d'ajout, et des **Presets** (« Foyer » = `Nom` + `address.address` + `address.postcode`). Un champ du formulaire apparaît sous son libellé ; un `save_to` peut être saisi librement (ex. `produit_1`) ;
- **Limite (1 pour unicité) \*** ;
- **Chercher dans opérations** — des ID séparés par virgule. **Attention** : rempli, il ne cherche plus dans l'opération courante, sauf si son propre ID figure dans la liste ;
- **Motif NC** — un seul par ligne, avec des **Presets** cliquables.

Les boutons ↑ ↓ 🗑 à droite de l'en-tête déplacent ou suppriment la ligne.

### Les 12 types, tels qu'ils s'affichent

| Libellé dans la liste | Paramètres |
|---|---|
| Nombre de participations | champs clés, limite (1 = unicité), opérations à inclure |
| Nombre de valeurs distinctes | champ d'agrégation **obligatoire** |
| Somme sur champ | champ d'agrégation **obligatoire** |
| Jours entre achat et date | exige un « Champ (date) » de comparaison : `date` (horodatage de création) pour un délai d'inscription. Limite = nombre de jours. Lit `buying_date` |
| Jours ouvrés entre achat et date | idem, en jours ouvrés |
| Jours entre MISSING et TO_CHECK_AGAIN | limite en jours |
| Date d'achat valide | « Date personnalisée (min) » et « (max) ». Lit `buying_date` |
| Date input valide | idem, sur `date_input` |
| Date de poste valide | idem, sur la date de poste |
| Valeur dans liste blanche | champ, liste de données, regex (défaut `^{value}$`) |
| Valeur dans liste noire | idem |
| Erreur permanente | blocage inconditionnel |

**Bornes vides ≠ contrôle désactivé.** Sur les trois types de date, « Date personnalisée (min) » et « (max) » laissées vides retombent silencieusement sur les dates de l'opération, qui ne sont pas toujours celles des modalités. Les renseigner explicitement avec la période d'achat des modalités.

### Conditions de bloc

Une condition porte sur un **bloc entier**, jamais sur une ligne. Tout contrôle qui ne vaut que dans un cas (achat en magasin, 3ᵉ produit facultatif) va dans un bloc séparé avec sa condition. **Une liste blanche sur un champ vide échoue** : si le champ est facultatif, isoler la ligne dans un bloc conditionné sur sa présence.

La condition se rédige au format FormKit et dépend entièrement des champs de l'opération : il n'y a pas d'écriture passe-partout. **Recopier la forme d'une condition déjà en place sur cette opération**, ou ouvrir le lien « Aide syntaxe FormKit » à côté du champ. Ne jamais la transposer depuis une autre opération : les noms de champs et la forme attendue changent.

### Datalists

Une liste référencée par une ligne de vérification suit la même vérification que celles du formulaire : appliquer le contrôle du §2, alerte et question comprises.

## 6. Consignes (cases à cocher)

Neuf au maximum, texte libre, **sans champ motif NC**.

- Écrire le ou les motifs dans le libellé (« … - sinon NC 037 »), **2 motifs au maximum** par consigne. Si un thème en demande davantage : scinder, ou ne garder que les 2 plus probables. Quand une consigne porte 2 motifs, rattacher chacun à son cas.
- Ne pas remplir les 9 emplacements par principe : une consigne qui ne peut pas conduire à un refus n'a pas sa place.
- **Consigne 1, achat simultané** : dès que les modalités exigent l'achat de plusieurs produits, la première consigne porte la simultanéité. Elle couvre **tous** les produits déclarés et reprend la tolérance exacte des modalités et des instructions de saisie. Y regrouper le nombre minimum de produits éligibles.

  > Achat simultané : tous les produits déclarés (2 ou 3) figurent sur le même ticket de caisse, ou sur plusieurs tickets du même point de vente et du même jour - sinon NC 037. Moins de 2 produits éligibles - sinon NC 082

  Les numéros de cet exemple illustrent la mise en forme. Les motifs de l'opération en cours se trouvent selon le §8.

- Une consigne héritée sans motif (« Présence code-barres ») est à compléter, pas à doubler d'une question de fichier.

## 7. Vérifications de fichiers (OUI / NON)

Chaque entrée porte deux champs et un bouton Supprimer :

- **Type / Sous-type \*** — un **couple unique** choisi dans une seule liste : Preuve d'achat / Facture, / Reçu, / RIB, / Code-barres, / Carte d'identité, / Passeport, / Inconnu, puis RIB / Facture, RIB / Reçu… Un couple ne peut servir qu'une fois.
- **Question (OUI / NON)** — le texte affiché aux opérateurs.

Pas de motif NC : préférer une consigne dès que le contrôle doit conduire à un motif précis, et ne pas poser une question de fichier sur un point déjà couvert par une consigne.

## 8. Trouver le bon motif NC

Un motif se choisit sur **sa description**, pas sur son numéro : c'est ce texte que le participant recevra, et il doit décrire exactement son cas. Un motif cité dans les instructions de saisie est imposé et clôt la question.

Chercher dans la collection `motifsnc`, en partant du thème du contrôle : filtrer sur `group`, parmi `FACTURE`, `MODALITES`, `CODE BARRE`, `IBAN`, `DELAI ET DATE`, `POINT DE VENTE`, `BON DE COMMANDE`, `PNEUMATIQUE`, `AUTRES`, `MOTIFS NC SIMPLIFIÉS`. Un contrôle sur un ticket part de `FACTURE`, un contrôle de période de `DELAI ET DATE`, une limite de participation de `MODALITES`.

Si rien dans le groupe ne colle vraiment, élargir au reste de la collection plutôt que de se rabattre sur un motif approchant : un libellé proche peut viser un tout autre cas. Elle compte environ 210 entrées pour un plafond de 200 par requête, donc `query_collection(motifsnc, sort {_id: 1}, limit 200)` puis `filter {_id: {$gt: "881"}}` pour la fin. Le tri est lexicographique : « 44 » tombe après « 439 », une pagination naïve en oublie.

Le `_id` est le code à écrire (`"037"`), `description` le texte envoyé au participant, `translations` les langues — sur une opération multi-pays, vérifier que le motif existe dans la langue de l'opération et le signaler sinon.

Ne jamais poser un code de mémoire, ni le recopier depuis le masque d'une autre opération ou depuis un exemple de ce skill sans avoir relu sa description. Si aucun motif existant ne convient, le dire dans le livrable au lieu d'en détourner un.

### Choisir le motif selon que le cas est régularisable

Le masque ne porte pas le statut : une ligne de vérification n'a qu'un champ « Motif NC », et la collection `motifsnc` ne marque pas les motifs régularisables, puisqu'elle ne porte que `_id`, `description`, `group` et `translations`. Le statut est posé à la saisie, par l'opérateur ou par la saisie IA, et la formulation du motif est ce qui l'oriente. Avant de choisir un motif, trancher donc la question : le participant peut-il corriger ? Si oui, le motif doit lui dire quoi renvoyer. Sinon, il doit énoncer le refus.

Ce sont les modalités et les instructions de saisie qui disent si la régularisation est offerte, et jusqu'à quelle date. Un même motif finit MISSING sur une opération et INVALID sur une autre, donc ne pas le déduire du texte du motif.

Dès qu'un contrôle du masque est régularisable, vérifier que la chaîne suit : « Limite des MISSING » et « Expiration des MISSING » cohérents avec les modalités, `date_fin_regule` sur l'opération, et un formulaire UPDATE qui ramène le dossier en TO_CHECK_AGAIN (`changeStatusTocheckAgain`, que le MCP ne peut pas modifier). S'il manque un morceau, le signaler dans le livrable, partie 4. Le quatrième passage en MISSING clôt le dossier : un contrôle régularisable posé sur un point que le participant ne peut pas corriger consomme un passage pour rien.

## 9. Ce qui sort du périmètre

- **Les deux blocs JSON** (« Schema de saisie », « Template de bot de saisie ») : ne jamais y écrire. Ils relèvent du développement, pas de la gestion de projet. Si une opération semble pilotée par ce schéma plutôt que par le formulaire simplifié, s'arrêter et le signaler.
- Contrôle déjà assuré par l'unicité d'un champ du formulaire → **effectif**. Vérifier toutefois que le formulaire `UPDATE` ne le contourne pas.
- Contrôle « foyer » existant mais pas exactement identique aux modalités → **ignorer**.
- Mention d'un salarié ou fournisseur de l'organisateur exclu de l'offre → **ignorer** (invérifiable).
- **L'éligibilité des références produits** : quand l'opération a une liste de données de produits porteurs, le contrôle se fait de lui-même au moment où la référence est saisie. Ne pas créer de ligne de vérification, ni de consigne, sur l'appartenance d'un produit à la liste éligible → **ignorer**.
- Toute règle de calcul de la prime → **ignorer** (§1).

## 10. Règle de repli

Tout contrôle d'éligibilité qui ne peut pas être appliqué tel quel doit, dans cet ordre : (1) être porté par une consigne si c'est un contrôle documentaire ou de jugement, sous réserve de la règle « aucun doublon » ; (2) être listé comme correction à faire sur le formulaire ou sur les datalists ; (3) sinon, être signalé comme non appliqué, avec sa raison. Ne jamais l'omettre en silence.

## 11. Saisir dans le back-office

**Avant de commencer.** Vérifier la chaîne des dates : début ≤ fin des achats ≤ fin de l'opération ≤ fin des régularisations ≤ fin des réclamations (`operation_info`, section `operation-dates` du guide). La sauvegarde valide **toute** l'opération et échoue si la chaîne est rompue. Demander l'arbitrage si une date doit changer.

**Les gestes qui marchent.**

- **Champs texte** (description d'une ligne, consignes, question de fichier) : ce sont de vrais `input`, on y écrit directement.
- **Listes déroulantes** (type de vérification, couple Type / Sous-type) : composants maison. Toute tentative de les remplir comme un champ de formulaire échoue avec « Element type "DIV" is not a supported form input ». Cliquer la liste, puis cliquer l'option.
- **Dates** : un calendrier s'ouvre, la frappe ne fonctionne pas. Naviguer de mois en mois avec les flèches, cliquer le jour. Affichage en JJ/MM/AAAA.
- **Changer le type d'une ligne** conserve sa description et son motif NC, et remplace seulement les paramètres. Entre deux types de date, les bornes déjà saisies sont conservées.
- **Échap** ferme une liste sans rien choisir. **Jamais Entrée** : cela soumet le formulaire.
- Un champ obligatoire vide s'affiche en rouge tant qu'il n'est pas rempli.
- Déplier une ligne en cliquant son titre. Tant que « Sauvegarder » n'a pas été cliqué, rien n'est écrit : explorer librement, et supprimer ce qu'on a ajouté pour inspection.

**Après la sauvegarde.** Le bandeau en bas à droite affiche « Modifié par … il y a quelques secondes ». Les écritures passées par le MCP y portent la mention **« via l'assistant (AI) »**, celles faites au navigateur non : c'est ce qui permet de distinguer les deux chemins après coup. Recharger la page et relire chaque ligne, consigne et question de fichier avec son motif.

## 12. Livrable

S'il y a des listes de données à confirmer ou à mettre à jour (§2), **commencer par l'alerte et par la question**, avant tout le reste.

Puis un message structuré en six parties, dans cet ordre :

1. **Les contrôles déjà effectifs** : unicités du formulaire, déduplicateurs implicites, réglages du masque, lignes existantes.
2. **Les blocs et lignes** créés ou corrigés, avec paramètres, condition de bloc éventuelle et motif NC.
3. **Les consignes** (la simultanéité en consigne 1) et **les vérifications de fichiers**.
4. **Les corrections hors masque** : listes de données, `save_to` non canoniques, dates, unicités manquantes ou en trop.
5. **Les contrôles ignorés** (dont les règles de calcul) et **les contrôles non appliqués**, avec leur raison.
6. **Les points à arbitrer**, dont les contrôles pour lesquels aucun motif NC existant ne convient.

Les doutes, hypothèses et questions ouvertes restent dans ce message : ne jamais les écrire dans le masque, et ne jamais remplir une consigne à moitié pour « tenir la place ».
