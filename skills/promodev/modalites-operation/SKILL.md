---
name: modalites-operation
description: "Rédige et vérifie en Word les modalités des opérations Promodev (ODR, Promocard, offres à primes, annexes produits/enseignes/PDV depuis Excel) pour validation client V1/V2, avec contrôle des règles Promodev et de Houston."
---

# Modalités d'opération (Word, validation client)

> **Aucune donnée client dans ce skill.** Les exemples sont fictifs ou génériques : aucun nom de client, d'agence, d'adresse, de DPO, de numéro d'opération ni de formulation propre à un client. Quand une information nécessaire manque dans les documents fournis ou dans Houston (société organisatrice, agence, adresse DPO ou délégation écrite à Promodev, durée de conservation, étude de dépôt, montants, dotations, formulation déjà validée pour ce client…), **poser la question** au chef de projet avant de rédiger. Ne jamais la reprendre d'une autre opération ni l'inventer.

Les modalités sont le document contractuel entre la **marque organisatrice** et les consommateurs. Promodev les rédige pour le client, qui les valide, souvent après plusieurs allers-retours. Trois conséquences :

- Le document est écrit **au nom de la Société Organisatrice** (la marque), pas de Promodev. Ne pas appliquer la charte promo-dev-docs : pas d'en-tête ni de logo Promodev. Promodev n'apparaît que comme prestataire de l'opération : adresse de traitement des dossiers, et sous-traitant pour les données personnelles (règle R1).
- Chaque version doit montrer au client **ce qui a changé** et pourquoi, sinon il relit tout à chaque fois et les allers-retours se multiplient.
- Une incohérence (date, montant, nom d'opération, adresse) se retrouve sur le site, dans les e-mails et dans le paramétrage Houston. Le contrôle final compte autant que la rédaction.

Écrire en français, avec les conventions des modèles : dates JJ/MM/AAAA, montants « 20 € » ou « 20€ » (garder la forme du client), guillemets « », « Société Organisatrice » et « Participant » avec majuscule.

## 0. Règles Promodev obligatoires

Ces règles s'appliquent à **tout** document de modalités : ceux que Promodev rédige, ceux que le client rédige lui-même et ceux qui reviennent du client après relecture. Un document validé (« DEF ») n'en est pas dispensé. Les modèles historiques ne les respectent pas toujours : ne jamais recopier une clause d'un ancien document sans la vérifier.

Un manquement est **bloquant** (sauf les points sur l'adresse DPO, qui sont de simples alertes : voir R1) : le signaler en tête du message, proposer la correction en suivi des modifications avec un commentaire qui explique la règle, et ne pas présenter le document comme prêt à valider tant qu'il n'est pas corrigé ou que le chef de projet n'a pas décidé autrement.

### R1. Client responsable de traitement, Promodev sous-traitant, DPO du client

La clause données personnelles doit dire clairement :
- que la **Société Organisatrice** (raison sociale) est le **responsable de traitement** ;
- que les données sont traitées pour son compte par des **sous-traitants ou prestataires** : soit PROMO.DEV nommément (SAS, 276 avenue du Douard, 13400 Aubagne), soit une mention générale du type « ses sous-traitants et prestataires ». Les deux formulations sont acceptées ; « sous-traitant » et « prestataire » aussi ;
- une **adresse pour exercer les droits** : l'adresse DPO de la Société Organisatrice, par e-mail ou par courrier. Une adresse postale du service en charge des données (ex. « {SOCIÉTÉ} - Service Marketing - … ») suffit.

**Renvoi vers la politique de confidentialité.** Si les modalités se contentent de renvoyer vers la politique de confidentialité (ex. « Les conditions et modalités de ce traitement […] sont précisées dans la Politique de confidentialité accessible sur le site … »), c'est conforme, **à condition** que cette politique contienne bien les trois informations : responsable de traitement (la Société Organisatrice), sous-traitants ou prestataires (PROMO.DEV nommé ou mention générale), adresse pour exercer les droits (celle du client, e-mail ou courrier, ou `dpo@promo.dev` seulement en cas de délégation écrite confirmée). Dans ce cas :
1. Récupérer la politique : fichier ou texte fourni par le chef de projet, sinon la page du site de l'offre. Les sites d'opération s'affichent souvent en JavaScript, donc WebFetch ne voit qu'une page vide : utiliser le navigateur (Claude in Chrome ou navigateur intégré) avec `get_page_text`, ou demander le texte au chef de projet.
2. Vérifier les trois informations dans la politique elle-même, en citant les passages trouvés.
3. Vérifier que le renvoi est utilisable : le lien (lien hypertexte du Word, à lire dans `word/_rels/document.xml.rels`) ou l'adresse indiquée mène bien à la politique, pas seulement à la page d'accueil du site. Sinon, le signaler, sans que ce soit bloquant.
4. Résultat : **conforme** si les trois informations y sont ; **non conforme** s'il manque un rôle (préciser lequel, et proposer soit de corriger la politique, avec le skill dédié aux politiques de confidentialité s'il est installé, soit d'ajouter les rôles directement dans les modalités) ; simple alerte s'il ne manque que l'adresse DPO ; **à vérifier** si la politique n'a pas pu être lue. Dans ce dernier cas, ne jamais conclure que c'est conforme : demander le texte au chef de projet.

**Adresse DPO.** La règle générale : le client est responsable de traitement, donc c'est **l'adresse du client** (e-mail DPO ou adresse postale du service en charge des données) qui figure dans les modalités. C'est ce qu'on attend pour tous les clients.

Exception : un client sans DPO qui a demandé **par écrit** à Promodev de prendre en charge cette partie. Dans ce cas seulement, c'est `dpo@promo.dev` qui doit apparaître, et le client reste responsable de traitement dans la clause. Cette délégation ne se présume pas : si le client n'a pas de DPO connu, poser la question au chef de projet avant de rédiger.

Les points sur l'adresse DPO ne bloquent **pas** les modalités, quel que soit le client : les signaler comme simple point d'attention dans le message. Cas possibles :
- `dpo@promo.dev` sans délégation écrite confirmée : le signaler et demander au chef de projet si ce client a délégué cette partie par écrit ;
- aucune adresse pour exercer les droits, ni e-mail ni postale (ni dans les modalités ni dans la politique citée) : le signaler ;
- une adresse du client à la place de `dpo@promo.dev` alors qu'une délégation écrite est confirmée : le signaler.

Sont non conformes et à corriger (bloquant) :
- aucun rôle indiqué, ni dans les modalités ni dans une politique de confidentialité citée (le client doit être nommé responsable de traitement ; les sous-traitants ou prestataires peuvent rester génériques), par exemple « Les données collectées ne sont réservées qu'à l'usage des destinataires suivants : PROMODEV et la Société Organisatrice » ; le rôle de responsable de traitement du client doit être écrit, même en cas de délégation à Promodev ;
- Promodev présenté comme responsable de traitement, responsable conjoint, ou « la société que vous consultez actuellement » ;
- la politique de confidentialité de Promodev citée à la place de celle de la Société Organisatrice.

Clause type : §5.

### R2. Ne jamais demander d'entourer les informations sur les justificatifs

Les modalités ne doivent jamais demander au participant d'**entourer**, surligner, encadrer ou marquer la date d'achat, la référence ou le libellé du produit, le prix, le montant ou l'enseigne sur la preuve d'achat, ni sur aucun autre justificatif.

- Rechercher dans le texte : `entour`, `surlign`, `encadr`, `cercl`, `stabilo`, `marqu`, `souligne` (dans une consigne donnée au participant).
- Remplacer par une formulation qui dit ce qui doit **figurer** sur le justificatif, par exemple : « une photo ou un scan lisible du ticket de caisse ou de la facture d'achat, sur lequel doivent figurer la date d'achat, le libellé et/ou la référence du produit éligible et son prix ».
- Si le client demande d'ajouter une consigne pour entourer les informations, ne pas l'appliquer : le signaler au chef de projet.

## 1. Identifier la situation

| Situation | Déroulé |
|---|---|
| Nouvelle opération, rien d'existant | §2 brief → §3 choix de la base → §4 et §5 contenu (parcours utilisateur construit depuis le formulaire CREATE Houston : §4.4 ; annexes depuis l'Excel client : §4.5) → §7 génération → §9 contrôles → V1 |
| Nouvelle opération d'un client qui a déjà eu des modalités (même marque, reconduction, saison suivante) | Partir de ses anciennes modalités (§3), les adapter en **suivi des modifications** → V1 |
| Le client renvoie un Word annoté | §8 retour client → V(n+1) |
| Le client envoie **ses propres modalités** (rédigées par lui ou son agence) | §0 règles Promodev puis §9 contrôles. Corrections en suivi des modifications (auteur `Promodev`) et commentaires dans son fichier, plus un récapitulatif des écarts (§8 point 6) |
| Relecture ou correction d'un document existant | §0 puis §9 contrôles, puis corrections en suivi des modifications et commentaires |
| Le client envoie un Excel de produits, d'enseignes ou de points de vente | §4.5 annexes, puis contrôles §9 |
| Offre à primes (cadeau, dotation, carte énergie ou carburant) | Même déroulé que l'ODR, avec le contenu propre aux primes du §6 (mécanique, clauses, contrôles) |

## 2. Rassembler le brief

Récupérer d'abord ce qui existe déjà, pour ne demander que ce qui manque :

1. **Houston** : si un idgame, un nom d'opération ou un lien test.promo.dev est fourni, utiliser `find_operation` puis `operation_info`. Lire `read_houston_guide` section `operation-dates` avant de reprendre les dates, car les 5 dates d'une opération n'ont pas le même sens. Les datalists (`list_datalists`) donnent souvent les produits/EAN et les montants.
2. **Documents joints** : brief client, e-mail, Excel de produits, anciennes modalités.
3. Puis **poser les questions restantes en une seule fois** (AskUserQuestion ou liste courte), en proposant les valeurs par défaut ci-dessous.

| Information | Remarque / valeur par défaut Promodev |
|---|---|
| Société Organisatrice : raison sociale, forme, capital, RCS + ville, siège | Obligatoire. Reprendre à l'identique des anciennes modalités du client s'il y en a |
| Nom commercial de l'opération (entre « ») | Doit être identique partout (titre, articles, adresse postale, contact) |
| N° Promodev | Format `Promodev N°<année><idgame>`, ex. N°2026999 |
| Mécanique et montants | Identifier la mécanique dans le catalogue §4.1 (et la formule Houston si l'opération existe) : montant, %, paliers, plafonds, nb de produits, mode de versement |
| Dates d'achat (début / fin inclus) | Heures si le client les précise (00h01 / 23h59) |
| Date limite de participation | En ligne : fin d'achat + 10 à 15 j en général. Autre formule : « dans un délai de N jours suivant l'achat » |
| Date limite de régularisation | Après la date limite de participation |
| Date limite de réclamation / contact | Environ fin d'offre + 1 à 3 mois |
| Territoire | France métropolitaine (Corse incluse), + DROM COM ou DOM si demandé |
| Lieux d'achat | Enseignes listées, « magasins participants », sites web ; exclusion des marketplaces |
| Produits éligibles, enseignes, points de vente | En annexe s'il y en a plus d'une dizaine, construite depuis l'Excel client (§4.5) |
| Limites | Les trois familles du §4.3 : géographique et type de participants, participation, remboursement. Elles varient selon le brief client |
| Parcours utilisateur | Formulaire CREATE Houston (§4.4) : étapes, champs obligatoires, justificatifs, cases à cocher, e-mails |
| Justificatifs | Preuve d'achat (informations qui doivent y figurer, **jamais à entourer** : R2), code-barres (photo ou découpé), IBAN/RIB (sauf Promocard et primes), attestation de majorité… |
| Participation par courrier | Oui/non. Adresse : `<Nom opération> – Promodev N°… – BP 82110 – 13847 Vitrolles Cedex` |
| Site de l'offre, e-mail de contact | URL exacte ; formulaire « Contact » du site |
| Données personnelles | Raison sociale et adresse du responsable de traitement (la Société Organisatrice), adresse DPO du client (`dpo@promo.dev` seulement en cas de délégation écrite confirmée : R1), durée de conservation, base légale (exécution du contrat ou consentement : c'est au client de trancher), opt-ins newsletter, lien vers la politique de confidentialité |
| Mode de remboursement | Virement (IBAN), paiement express 72 h, Promocard, carte carburant ou bon d'achat (§4.1 E) |
| Prime (offres à primes, §6) | Nature exacte, valeur TTC indicative, prime au choix ou non, stock ou quota, mode et délai d'envoi, conditions d'utilisation (cartes) |
| Délai de remboursement | 6 à 8 semaines par défaut ; « 4 à 6 semaines » ou « 1 à 8 semaines » selon les clients |
| Régularisations | 3 au maximum par dossier ; délai éventuel de 14 jours par demande |
| Contrôle des originaux | Envoi sous 8 jours calendaires ; frais postaux remboursés (1,51 € lettre verte 20 g en 2026 : faire confirmer le tarif chaque nouvelle année) |
| Style de document | §3 |

S'il manque une information, ne pas l'inventer : laisser un repère **surligné en jaune** `[À COMPLÉTER : …]` dans le Word et le lister dans le message d'envoi.

## 3. Choisir la base et le style

**Règle de priorité.** Si des modalités précédentes du **même client** existent, les reprendre comme base : le client y reconnaît sa structure, ses clauses validées par son juridique et sa mise en page. Dupliquer le fichier, puis modifier le XML directement (voir §8 pour la méthode). Ne pas reconstruire un document neuf, qui perdrait la mise en forme.

Sans modèle client, choisir parmi les 4 styles observés chez Promodev. Proposer le style « articles » par défaut. Pour une ODR simple destinée à un encart court, proposer « compact ».

| Style | Aspect | Quand | Exemple d'origine |
|---|---|---|---|
| `articles` | Titre « MODALITÉS » (ou « Règlement de l'opération n°… ») centré gras 14 pt, nom de l'opération en bleu (4472C4), « Article N - Titre » gras souligné, étapes numérotées avec puces, annexe en tableau. Century Gothic 10, marges étroites (1,3 / 1,5 cm), n° de page | Règlement complet et structuré, grands comptes, beaucoup de produits | ODR multi-produits, satisfait ou remboursé ; Promocard (numérotation « 1. Société organisatrice ») |
| `sections` | Bloc titre centré gras 14 pt sur 3-4 lignes (MODALITÉS DE L'OPÉRATION / « Nom » / saison / dates), intertitres gras soulignés terminés par « : », sans numéros | Règlement complet non numéroté, avec participation web et/ou courrier | ODR saisonnière d'une grande marque |
| `conditions` | « CONDITIONS GÉNÉRALES DE L'OFFRE … » 16 pt, rubriques en MAJUSCULES grasses, tableau Enseignes / Dates de validité / Dates de participation, étapes « 1 - INSCRIVEZ-VOUS », « 2 – TÉLÉCHARGEZ » | Offre courte, orientée consommateur, souvent un seul réseau | ODR accessoires réservée à un réseau |
| `compact` | Titre « Modalités – Offre de remboursement … », accroche entre « », dates, produits listés avec montant, étapes « 1 – … » en texte continu justifié | ODR simple, peu de produits, modalités affichées sur le site de la marque | ODR de fin d'année affichée sur le site de la marque |

Dans les styles sans numéros (`sections`, `conditions`, `compact`), ne jamais écrire « (article 1) ». Renvoyer vers la rubrique par son nom.

## 4. Contenu d'une ODR

### 4.1 Catalogue des mécaniques ODR (relevé Houston, septembre 2026)

Relevé fait sur les ~600 opérations de type ODR de Houston (et les PRIME proches). Dans Houston, le calcul du remboursement est dans `odr_options` : `ODR_SIMPLE_EUR`, `ODR_SIMPLE_PERCENT`, `ODR_EUR_PAR_PRODUIT`, `ODR_PERCENT_PAR_PRODUIT`, `ODR_DOUBLE_EUR_MIN`, ou `ODR_CUSTOM` avec une formule (`code_expr`). Pour une opération existante, lire cette formule avec `operation_info` : elle dit exactement ce que les modalités doivent décrire, et un écart entre la formule et le texte est à signaler (§9).

Pour chaque mécanique : ce que les modalités doivent préciser, et une formulation type. Toujours donner un **exemple chiffré** dès que le calcul n'est pas un montant fixe.

**A. Comment le montant est calculé**

1. **Montant fixe** (`ODR_SIMPLE_EUR`) : même montant quel que soit le produit éligible. « Pour l'achat d'un produit éligible, recevez 25 € remboursés. » Préciser si le montant est multiplié par la quantité (« 25 € par produit acheté, dans la limite de N produits ») ou non.
2. **Montant selon le produit** (`ODR_EUR_PAR_PRODUIT`, ou formule avec liste de produits) : grille en annexe EAN / désignation / montant, ou blocs « 5 € remboursés pour l'achat d'un : … ». Presque toujours **plafonné au prix payé** : « dans la limite du prix d'achat TTC figurant sur la preuve d'achat ».
3. **Pourcentage du prix** (`ODR_SIMPLE_PERCENT`, `ODR_PERCENT_PAR_PRODUIT`) : « X % du prix TTC payé, déduction faite des remises immédiates », avec plafond éventuel par produit ou par dossier. Variantes :
   - 100 % remboursé (satisfait ou remboursé, produit offert) ;
   - **TVA remboursée** : montant = prix TTC − prix TTC / 1,2, soit 16,67 % du prix TTC et non 20 %. Écrire « remboursement du montant de la TVA (20 %) incluse dans le prix TTC, dans la limite de 18 € » et donner un exemple (ex. « TVA offerte ») ;
   - pourcentage d'un panier plafonné (ex. 20 % dans la limite de 50 €).
4. **Palier selon le prix du produit** : « 30 € pour un produit de moins de 400 € TTC, 50 € de 400 à 599,99 €… ». Bornes exactes, sans trou ni chevauchement (« moins de », « à partir de »).
5. **Palier selon le montant total d'achat** : « 30 € remboursés dès 99 € d'achat, 50 € dès 149 € » (ex. 8/20/50 € selon trois seuils, ou 40 € dès 100 €). Préciser si le seuil s'apprécie TTC, sur une seule preuve d'achat, produits éligibles seulement.
6. **Palier selon la quantité achetée** : « 20 € pour 1 produit, 50 € pour 2, 100 € pour 3 ». Préciser le maximum de produits pris en compte.
7. **Par tranche d'achat** : « 30 € par tranche de 200 € TTC d'achat ». Préciser l'arrondi (tranche entière uniquement) et le plafond.
8. **Montant par produit × quantité** : somme des montants de chaque ligne (ex. unités plafonnées à 10 par dossier, 50 € par produit dans la limite de 400 €). Préciser le plafond d'unités et de montant par dossier.
9. **Pneumatiques par lot de 2** : montant selon le diamètre de jante, versé par paire (2 pneus = 1 montant, 4 pneus = 2 montants), rien en dessous de 2 pneus. Tableau diamètre / montant en annexe, et préciser si au-delà de 4 pneus on continue par paire ou si c'est plafonné à 2 montants (les deux existent).

**B. Achats combinés**

10. **Le moins cher des N produits remboursé à 100 %** : « 3 produits achetés simultanément = le moins cher des trois remboursé » + exemple (ex. « 3 achetés, le 3e remboursé »). Variante déjà rencontrée (formule Houston) : 3 produits = le moins cher à 100 %, **2 produits = le moins cher à 50 %** ; si le calcul Houston prévoit ce palier, les modalités doivent le dire.
11. **Le 3e produit le moins cher parmi les 3 plus chers** (prix distincts) : expliquer la règle avec un exemple à 4 ou 5 produits, sinon incompréhensible pour le consommateur.
12. **2e produit à -50 %** (`ODR_DOUBLE_EUR_MIN`) : « 50 % du prix TTC du moins cher des 2 produits, dans la limite de X € » ; plafond parfois **selon la contenance** du produit le moins cher (ex. 25 € / 53 € pour 5 L / 71 € pour 10 L). Préciser panachage et exclusions (testeurs).
13. **Le moins cher de 2 produits, plafonné, sous seuil de panier** : « pour l'achat simultané de 2 produits pour au moins 59 € TTC, le moins cher remboursé dans la limite de 30 € ».
14. **Produit porteur + accessoire ou produit associé** : remboursement conditionné à l'achat du couple, plafonné au prix total des deux (ex. téléphone + objet connecté, robot + accessoire, option « Kit »). Lister les deux catégories éligibles et dire si l'accessoire doit être sur la même preuve d'achat.
15. **Offre croisée entre marques** : montant selon les combinaisons achetées (ex. 40 € ou 90 € selon les produits achetés dans chaque marque). Un tableau des combinaisons évite les ambiguïtés, et les deux sociétés doivent apparaître clairement (qui organise, qui rembourse).

**C. Montant qui dépend d'une autre donnée**

16. **Bonus sous condition** : montant de base, majoré si une condition est remplie (ex. précommande / lancement : montant supérieur si l'IMEI ou une information complémentaire est fourni). Écrire les deux montants et la condition exacte.
17. **Selon l'enseigne ou l'opérateur** : montant différent par enseigne (ex. ODR sur une assurance : montant par enseigne, plafonné à un multiple du prix de l'assurance). Tableau enseigne / montant.
18. **Selon une option ou une formule choisie** : ex. formule premium 60 €, sinon 30 €. Lister les options.
19. **Montant fourni par un partenaire** (ex. montant transmis par API) : les modalités renvoient à la grille du partenaire ; demander cette grille pour l'annexe.

**D. Conditions particulières d'accès**

20. **Satisfait ou remboursé** : sans retour produit (ex. « Testez votre produit 100 jours ») ou **avec retour produit** (ex. « Convaincu ou remboursé »). Avec retour : motif d'insatisfaction au formulaire, délai de demande après l'achat (« dans un délai de 60 jours calendaires suivant l'achat »), article « Conditions de retour du Produit » (produit complet, accessoires et emballage d'origine, sans casse ; traces d'usage raisonnables admises), circuit e-mail de conformité → confirmation de l'adresse → étiquette prépayée → envoi sous 5 jours calendaires → contrôle → virement, produit non conforme (reste à disposition jusqu'au JJ/MM/AAAA, réexpédition à la charge du participant), perte ou casse pendant le transport.
21. **ODR avec tirage au sort ou instant gagnant** : seuls les participants désignés gagnants sont remboursés (ex. « Tentez de vous faire rembourser »). Ce n'est plus une simple ODR : le document doit être un **règlement de jeu** (nombre de gagnants, modalités du tirage ou de l'instant gagnant, dotation = remboursement), et le vocabulaire « gagnant », « lot », « dotation » y est normal. Demander au chef de projet le modèle de règlement de jeu à utiliser.
22. **Précommande, lancement, prolongation** (ex. lancement d'un smartphone, « offre de prolongation ») : dates de précommande et date de livraison ou d'activation à distinguer de la date d'achat ; dire laquelle fait foi.
23. **Offre réservée à une enseigne ou à un opérateur** (opérateur télécom, enseigne d'électroménager, centre auto…) : nommer l'enseigne partout, et dire si ses sites en ligne et ses franchisés sont inclus.
24. **Professionnels (B2B)** : remises arrières, challenge revendeurs, poids lourd, grands comptes. Participants personnes morales (raison sociale, SIRET, facture au nom de la société), montants HT ou TTC à préciser, et pas de clause « personne physique majeure ».
25. **Remboursement de frais hors achat de produit** (ex. taxi, hôtel, transport TER) : justificatif = facture de la prestation, plafond par trajet ou par nuit, période de la prestation.
26. **Multi-pays** : une version des modalités par pays et par langue, avec la devise, l'organisateur local le cas échéant, et une grille produits par pays.
27. **Participation papier** (ex. « ODR papier ») : adresse postale, éléments à joindre, date limite cachet de la poste faisant foi, et pas de régularisation en ligne sauf si prévue.

**E. Mode de versement**

28. **Virement bancaire** (IBAN, cas général). Variante **paiement express 72 h** (titre du type « Offre de remboursement 72h … – Virement bancaire ») : reprendre cette formulation validée, qui distingue bien les deux délais :
    > Le traitement de votre participation sera effectué sous 72h ouvrées à compter de la réception de votre dossier et vous recevrez un email vous permettant de suivre son avancement. Le remboursement sera effectué sous 48 à 72h après validation de la participation (délai variable selon les banques). Toute autre forme de remboursement est exclue de l'offre.
    
    Ne jamais écrire « remboursé sous 72h » tout court : le délai total peut aller jusqu'à 72 h ouvrées de traitement puis 48 à 72 h de virement. Ne pas promettre ce délai sur une opération qui n'a pas l'option paiement 72 h dans Houston.
29. **Promocard** (carte de paiement dématérialisée) : remboursement sur une carte de paiement dématérialisée (réseau Visa, utilisable comme une carte bancaire) envoyée à l'adresse e-mail du participant. Variantes : Promocard grand public, challenge Promocard, Promocard enseigne. Dans le modèle validé : tableau Famille produits / Références / Montant total / Dont montant dédié à l'enseigne d'achat ; part fléchée éventuelle (« Sur ce montant disponible, 20 € seront utilisables uniquement dans l'enseigne dans laquelle le participant a réalisé l'achat », détail par enseigne ou groupe) ; envoi dans un délai maximum de N semaines après validation ; durée de validité (« utilisable pendant 1 an à compter de la date de fin d'opération ») ; montant crédité plafonné au prix payé, hors frais de livraison et accessoires ; pas d'IBAN ni de RIB dans les justificatifs, et pas de « virement » dans le texte. Ne pas ajouter de règle sur le solde non utilisé ni sur le fonctionnement interne de la carte, et ne pas en demander au client : cela relève de la gestion interne de Promodev. Si le participant **choisit** entre virement et Promocard, décrire les deux options et leurs montants.
30. **Carte carburant / carte énergie, bon d'achat** (ex. « Carte Énergie », carte carburant, « bon d'achat ») : nature exacte de la dotation, valeur, mode d'envoi, validité, enseigne où l'utiliser. Quand la carte est la dotation de l'offre (pas un remboursement en argent), c'est une offre à primes : suivre le §6.

**F. Limites transverses** (à combiner avec toutes les mécaniques)

- **Quota** : « Opération limitée aux 10 000 premières participations » en sous-titre, puis « Une fois ce quota atteint, le formulaire de participation est automatiquement fermé. Les participations déjà enregistrées continueront à être instruites conformément aux présentes modalités. » Avec **compteur** : « Le compteur de participations est actualisé en temps réel et accessible sur {site}. », et participation uniquement en ligne.
- **Budget / enveloppe** : « dans la limite de N remboursements » ou « dans la limite du budget alloué à l'opération », à écrire si le client plafonne le budget.
- **Plusieurs produits sur une même facture** : « Offre limitée à une demande par facture et au remboursement de 2 produits maximum par facture […] Le participant bénéficiera d'un virement unique regroupant les remboursements des produits achetés. »
- **Plafond par dossier et par foyer**, et **plafond au prix payé** : les écrire explicitement dès que la formule Houston contient un `min(…, prix)` ou un `max`.

Si une opération ne rentre dans aucune de ces cases, la décrire à partir de la formule Houston, en langage simple et avec deux exemples chiffrés, puis la faire relire au chef de projet.

### 4.1 bis Vocabulaire

Dans une ODR, « prime » désigne le remboursement (une prime peut être financière, digitale ou physique) : « la prime sera calculée sur… » est acceptable et ne doit pas être signalé.

### 4.2 Plan type (style `articles`) : adapter les titres aux autres styles

1. **Organisation de l'offre** : « La société {FORME} {RAISON SOCIALE} (ci-après dénommée « Société Organisatrice »), société enregistrée au R.C.S. {VILLE} sous le numéro {RCS}, dont le siège social est situé {ADRESSE}, organise du {JJ mois AAAA} au {JJ mois AAAA} inclus une offre de remboursement avec obligation d'achat intitulée « {NOM} » (ci-après dénommée « l'offre »). »
2. **Modalités de participation** : étapes numérotées, reprises du parcours utilisateur (§4.4). Par exemple : 1. Acheter (produit, période, territoire, lieux). 2. Se connecter sur {site} avant le {date} et renseigner : coordonnées complètes (civilité, nom, prénom, e-mail, adresse postale, n° mobile), informations d'achat (date, enseigne), code-barres. 3. Télécharger : preuve d'achat sur laquelle doivent figurer l'enseigne, la date, le prix, la référence du produit et le n° de la preuve (sans demander de les entourer : R2), photo du code-barres à 13 chiffres, RIB avec IBAN commençant par « FR » correspondant aux coordonnées déclarées. 4. Accepter le règlement et le traitement des données en cochant les cases. Puis : « Un e-mail de confirmation d'inscription est envoyé sous 24h. Le suivi de la participation est accessible via l'onglet « Suivi » du site ou le lien dans l'e-mail. »
3. **Modalités de remboursement** : participation conforme (virement sous N semaines), participation non conforme (e-mail de régularisation, 3 régularisations maximum, délai de 14 jours, date butoir absolue).
4. **Conditions de participation** : quota, lieux (vendu et expédié par l'enseigne, marketplaces exclues), type de participants (§4.3), personne physique majeure pour les particuliers, non cumulable, 1 remboursement par foyer, preuve d'achat utilisable une seule fois, produit neuf (ni occasion, ni reconditionné, ni exposition), bénéficiaire = acheteur et nom du RIB identique, demandes incomplètes, falsifiées ou raturées nulles, frais de connexion non remboursés, vérifications possibles (identité, domicile), exclusion du personnel et des prestataires si le client le souhaite.
5. *(Satisfait ou remboursé uniquement)* **Conditions de retour du Produit**
6. **Acceptation du règlement et accès au règlement** : acceptation entière et sans réserve ; fraude = exclusion définitive et poursuites possibles ; règlement disponible sur {site} rubrique « Modalités ».
7. **Annulation / Modification de l'offre** : force majeure, circonstances exceptionnelles.
8. **Contestation et réclamation** : formulaire Contact du site, date limite.
9. **Protection des données personnelles** : §5.
10. **Propriété intellectuelle** (facultatif)
- **Annexe 1 : Produits éligibles exclusivement** : tableau en page séparée (§4.5). **Annexe 2 : Enseignes / points de vente participants** si besoin.

Le style `sections` ajoute en général : participants et exclusions, clause de loyauté et fraude, contrôle des originaux avec frais postaux, visuels non contractuels, risques d'internet, participation par voie postale détaillée, disponibilité des modalités (copie gratuite sur demande, frais remboursés), remboursement des frais, litiges (clause de nullité partielle, réclamation sous 1 mois après la clôture), moyens de communication (PLV, sites et tracts distributeurs), acceptation et droit français.

Le style `conditions` / `compact` suit l'ordre : offre → enseignes/produits/calendrier → modalités de participation (inscription, téléchargement, e-mail de suivi, régularisation) → contrôle des originaux → participation par courrier → validité (achat simultané, stocks, 1 par personne ou foyer, non cumulable, majeur, territoire) → remboursement et délais → contact → données personnelles → mentions légales de la société.

### 4.3 Les trois limites à définir et à vérifier

Chaque opération a trois familles de limites. Elles varient selon le brief client : les reprendre du brief, les écrire sans ambiguïté, et les comparer au paramétrage Houston (§9).

**1. Limite géographique et type de participants**
- Territoire de résidence et territoire d'achat (France métropolitaine, Corse incluse ou non, DROM COM, Monaco…), lieux d'achat (enseignes, points de vente, sites, marketplaces exclues).
- Type de participants :
  - « personnes physiques » = offre réservée aux **particuliers** (majeurs) ;
  - « personnes morales » = offre réservée aux **entreprises** (raison sociale, SIRET, facture au nom de la société) ;
  - les deux sont possibles **si les deux sont écrits explicitement** (« ouverte aux particuliers, personnes physiques majeures, et aux professionnels, personnes morales »).
  
  Les critères de limitation doivent correspondre au type : « par raison sociale » ou « par SIRET » n'a de sens que si les professionnels sont acceptés ; « par foyer » vise les particuliers. Signaler toute contradiction (ex. offre « réservée aux personnes physiques » mais limitée « par raison sociale »).

**2. Limite de participation**
- Nombre de participations par foyer, par personne, par raison sociale, par e-mail, par IBAN, par numéro de facture, par immatriculation, par code… et nombre de produits par participation.
- Quota global (« N premières participations ») et période de participation (date limite ou « N jours suivant l'achat »).

**3. Limite de remboursement**
- Montant maximum par produit, par dossier, par foyer ; plafond au prix payé ; nombre maximum d'unités prises en compte (ex. 3 pneus = calcul sur 2, 5 pneus et plus = calcul sur 4) ; budget ou nombre maximum de remboursements.

### 4.4 Parcours utilisateur (basé sur le formulaire CREATE de Houston)

Le parcours décrit dans les modalités (« 1. Achetez… 2. Connectez-vous… 3. Renseignez… 4. Téléchargez… 5. Validez ») doit correspondre à ce que le participant voit réellement sur le site. La source de vérité technique est le **formulaire CREATE** de l'opération dans Houston.

**Récupérer le parcours dans Houston**
1. `list_forms(operationId)` : repérer le formulaire `type: CREATE` (formulaire principal ; `UPDATE` = régularisation ; `paper: true` = version papier).
2. `get_form(formulaireId)` : lire les étapes (`form[].name`) et, pour chaque champ, `label`, `save_to`, `required`, `displayIf` (champ conditionnel), `options` (listes de choix), `min`/`max` des dates, `accept` et `sizeMax` des fichiers, `acceptedCountries`, `unique`.
3. `list_email_templates(operationId)` : e-mails actifs (`PENDING` confirmation, `MISSING` régularisation, `INVALID` refus, `VALID` validation, `REFUND_DONE` remboursement effectué) pour décrire ce que reçoit le participant.

**Rédiger le parcours (partir de zéro)**
Construire les étapes des modalités dans l'ordre du formulaire :
- **Achat** : produits, période (`buying_date` min/max), lieux (liste `enseigne` / points de vente).
- **Connexion** : URL du site, date limite (`date_fin`).
- **Informations à renseigner** : lister les champs obligatoires en langage consommateur (civilité, nom, prénom, adresse, e-mail, téléphone, statut particulier / professionnel, raison sociale si professionnel, date d'achat, point de vente, produit, quantité, diamètre…). Les champs facultatifs peuvent être omis ou signalés comme tels.
- **Justificatifs à télécharger** : un point par champ `File` / `MultipleFiles` (`receipt` preuve d'achat, `bar_code` code-barres, `rib`, `id_proof`…), avec ce qui doit y figurer (R2 : jamais « entourer ») et, si utile, les formats acceptés et la taille maximale.
- **Coordonnées bancaires** : champ `Iban` (et `bic` s'il existe), IBAN France uniquement.
- **Validation** : cases obligatoires (`opt_in_rules` acceptation des modalités, `opt_in_privacy`), case marketing facultative.
- **Après validation** : e-mail de confirmation avec lien de suivi, e-mail de régularisation (formulaire UPDATE, nombre de régularisations, date limite `date_fin_regule`), e-mail de validation, virement.

Si l'opération n'existe pas encore dans Houston, rédiger le parcours à partir du brief, puis le signaler comme « à aligner avec le formulaire CREATE une fois paramétré ».

**Vérifier le parcours (modalités existantes)**
Comparer les deux sens et lister les écarts :
- **Formulaire → modalités** : champ obligatoire ou justificatif demandé sur le site mais absent des modalités (ex. statut particulier / professionnel, point de vente, marque et gamme).
- **Modalités → formulaire** : information ou justificatif annoncé dans les modalités mais absent du formulaire (ex. « IBAN et BIC » sans champ BIC ; limite « par numéro d'immatriculation » sans champ immatriculation, donc impossible à contrôler).
- **Contradictions de contenu** : options de liste qui contredisent l'éligibilité (ex. modalités « pneus été, hiver ou 4 saisons » mais option « gamme hiver non éligible » dans le formulaire), bornes de dates, quantités proposées, pays acceptés, conditions d'affichage (`displayIf`).
- **Libellés** : vocabulaire de jeu dans une ODR (« gestion du jeu »), lien vers les modalités ou la politique de confidentialité dans les cases à cocher.
- **Parcours courrier** : s'il existe un formulaire `paper: true` ou une participation postale, vérifier que les éléments demandés sur papier sont les mêmes.

### 4.5 Annexes produits porteurs, enseignes et points de vente (depuis l'Excel client)

Quand le client fournit un Excel (produits porteurs, enseignes, points de vente), l'annexe se construit **à partir du fichier**, jamais en recopiant à la main.

**Lire le fichier**
- Ouvrir tous les onglets (`pd.read_excel(f, sheet_name=None, dtype=str)`) : **toujours en texte** pour ne pas perdre les 0 en tête des EAN ni transformer un code en `3.46E+12`. Repérer la ligne d'en-tête réelle (lignes de titre ou logo au-dessus), les cellules fusionnées, les lignes masquées ou barrées et les couleurs qui signifient « exclu » : les signaler, ne pas deviner.
- Annoncer au chef de projet ce qui a été lu : onglets, nombre de lignes par onglet, colonnes retenues.

**Annexe produits porteurs**
- Colonnes selon la mécanique : EAN / désignation / (gamme ou marque) / montant remboursé ou prime ; ou diamètre / montant (pneus) ; ou référence / désignation seulement si le montant ou la prime est unique et écrit dans le texte. Largeurs par défaut `[3.6, 11.4, 3.4]`.
- Regrouper par gamme ou par montant si la liste est longue (un intertitre par groupe), trier comme le client (ou par désignation), montants au format « 15,00 € ».
- Titre : « Annexe 1 : Produits éligibles exclusivement », avec la phrase « Seuls les produits listés ci-dessous sont éligibles à l'offre. »

**Annexe enseignes et / ou points de vente**
- Enseignes seules : liste à puces ou tableau une colonne (enseigne, et « magasins et site internet » ou « magasins physiques uniquement » si le brief le précise).
- Points de vente : tableau enseigne / nom du magasin / adresse / code postal / ville, trié par code postal (ou par département avec un intertitre par département si la liste dépasse une centaine de lignes). Code postal sur 5 caractères en texte (« 04100 », pas « 4100 »).
- Phrase type : « Offre valable uniquement dans les points de vente participants listés ci-dessous (Annexe 2) » et, si c'est vrai, « hors achats sur les sites internet et marketplaces ».
- Si Houston a une liste `enseigne` / `magasin` (`list_datalists`), l'annexe doit contenir les mêmes points de vente.

**Contrôles sur le fichier** (à lister dans le message de livraison, sans corriger d'office)
- Nombre de lignes du fichier = nombre de lignes de l'annexe (hors en-têtes et lignes vides).
- EAN : 13 chiffres uniquement ; 12 chiffres (0 perdu ou UPC), notation scientifique, espaces, lettres, clé de contrôle EAN-13 fausse.
- Doublons : même EAN deux fois (surtout avec deux montants différents), même point de vente deux fois.
- Cellules vides : EAN sans désignation, produit sans montant, magasin sans code postal ou ville.
- Montants cohérents avec la mécanique (§4.1) et le plafond ; comparer avec la liste Houston des produits (`list_datalists`, `metadata.refund_amount` **en centimes** : 1500 = 15,00 €) et avec la formule `odr_options` : produits absents d'un côté ou de l'autre, montants différents.
- Territoire : codes postaux cohérents avec le territoire des modalités (20xxx / 2A / 2B = Corse, 97x / 98x = DROM COM, 98000 = Monaco).
- Renvois : le texte cite « Annexe 1 » / « Annexe 2 » et les annexes portent bien ces numéros ; le nombre de produits ou de magasins annoncé dans le texte correspond.

Si le chef de projet a aussi besoin du fichier d'import de la liste Houston, utiliser le skill `houston-datalist` avec le même Excel.

## 5. Clauses communes réutilisables

**Régularisation**
> Tout dossier partiellement non conforme mais régularisable (pièce manquante, information incomplète ou justificatif illisible) pourra faire l'objet d'une demande de régularisation adressée au participant par e-mail. Le participant dispose d'un maximum de trois (3) régularisations par dossier. Au-delà de ces trois (3) régularisations, le dossier sera définitivement invalidé. Les dossiers non conformes et non régularisables au regard des présentes modalités seront invalides immédiatement, sans possibilité de régularisation.

**Contrôle des originaux**
> La Société Organisatrice se réserve le droit de demander l'envoi par voie postale de tout justificatif original et physique (notamment le ticket de caisse original ou la facture d'achat originale et les codes-barres originaux) nécessaire à établir que le participant remplit bien les conditions imposées par les présentes modalités. Tout participant qui refuserait de présenter les justificatifs dans un délai de 8 jours calendaires à compter de la demande serait considéré comme renonçant à sa participation et donc, le cas échéant, à son remboursement, sans pouvoir en faire grief à la Société Organisatrice. Sous réserve de conformité du dossier reçu, la Société Organisatrice remboursera les frais postaux à hauteur de {1,51 €} (lettre verte base 20 g), tarif postal lent en vigueur en {AAAA}.

**Données personnelles (version longue, conforme à R1)**
> Les données à caractère personnel collectées dans le cadre de la présente offre sont traitées par {RAISON SOCIALE}, {adresse du siège}, en qualité de responsable de traitement, pour la gestion de l'offre : enregistrement et contrôle des participations, versement des remboursements ou envoi des primes et réponse aux demandes des participants. Ce traitement est fondé sur {l'exécution du contrat / le consentement du participant, qui dispose du droit de le retirer à tout moment}. Les données demandées sont obligatoires : à défaut, la participation ne peut pas être prise en compte.
> La société PROMO.DEV, 276 avenue du Douard, 13400 Aubagne, intervient en qualité de sous-traitant {ou : prestataire}, pour le compte et sur instruction de {RAISON SOCIALE}, pour la gestion de l'offre (saisie et contrôle des participations, service consommateurs, versement des remboursements ou envoi des primes).
> Les données sont conservées pendant {durée indiquée par le client}.
> Vous disposez, dans les conditions et limites prévues par la réglementation, d'un droit d'accès, de rectification, d'effacement, de portabilité des données vous concernant et d'opposition ou de limitation à leur traitement. Vous disposez également du droit de définir des directives relatives au sort de vos données après votre décès. Pour exercer ces droits, vous pouvez écrire à {adresse DPO de la Société Organisatrice ; dpo@promo.dev seulement en cas de délégation écrite confirmée : R1}. Vous disposez enfin du droit d'introduire une réclamation auprès de la CNIL.
> Pour plus d'informations, consultez la politique de confidentialité de {RAISON SOCIALE} disponible sur {site}.
> Les personnes qui exercent leur droit d'effacement ou d'opposition avant la fin de l'offre et le versement de leur remboursement sont réputées renoncer à leur participation.
> *(si démarchage téléphonique possible)* Vous disposez d'un droit d'inscription sur la liste Bloctel d'opposition au démarchage téléphonique : bloctel.gouv.fr.

**Données personnelles (version courte, style `articles`)**
> Les données à caractère personnel collectées auprès des Participants sont traitées par {RAISON SOCIALE}, en qualité de responsable de traitement, pour la gestion de l'offre. La société PROMO.DEV (276 avenue du Douard, 13400 Aubagne) intervient en qualité de sous-traitant {ou : prestataire}, pour le compte et sur instruction de {RAISON SOCIALE}. Pour exercer leurs droits, les Participants peuvent écrire à {adresse DPO : R1}. Les conditions et modalités de ce traitement sont précisées dans la Politique de confidentialité de {RAISON SOCIALE} accessible sur le site {site}.

La version courte suffit si la politique de confidentialité du client contient déjà les trois informations de R1 ; les rôles et l'adresse DPO peuvent alors ne figurer que dans la politique. Si la clause données vient du DPO du client, garder sa formulation, mais la règle R1 s'applique quand même : ajouter ou corriger la phrase sur les rôles (responsable de traitement / sous-traitant) en suivi des modifications, avec un commentaire, et signaler les autres points douteux (§9).

## 6. Offres à primes

Une offre à primes donne une **dotation** (objet, carte énergie ou carburant, carte cadeau, prime digitale) au lieu d'un remboursement en argent. Tout le reste du skill s'applique : règles R1 et R2, brief, styles, parcours utilisateur, trois limites (la 3e devient « limite de dotation »), annexes, retours client, contrôles. Cette section ne décrit que ce qui change.

Dans Houston, ces opérations sont de type `PRIME`, parfois `ODR` (cartes énergie, cartes carburant). Les stats suivent `prime_dispatch` / `prime_to_ship`, le formulaire de régularisation affiche les statuts logistiques (`SENT_TO_LOGISTIC`, `SHIPPED`, `DISTRIBUTION_FAILURE`) et la valeur des primes n'est en général **pas** dans Houston : la demander au client. Certaines opérations n'ont pas de formulaire CREATE dans Houston (site hébergé chez le client, saisie ou API) : le parcours se vérifie alors sur le site ou avec le chef de projet.

Hors périmètre : une « prime énergie » versée en argent par virement est une ODR (§4.1 bis). Une dotation attribuée par tirage au sort ou instant gagnant relève d'un règlement de jeu.

### 6.1 Mécaniques de primes (relevé Houston, septembre 2026)

Pour chacune : ce que les modalités doivent préciser.

1. **Cadeau fixe pour l'achat d'un produit porteur** (ex. vidéoprojecteur offert pour un smartphone, accessoire offert en précommande, SSD et housse offerts). Nommer la prime et sa valeur TTC indicative, lister les produits porteurs (tableau ou annexe), dire si la prime est donnée **par produit acheté** (IMEI ou numéro de série unique) et le maximum par foyer. Variantes : achat couplé à un abonnement opérateur (contrat ou avenant en justificatif) ; **précommande / lancement** (période d'achat précise, confirmation de commande acceptée si le produit ou la facture arrive après la période).
2. **Prime qui dépend du modèle acheté** (ex. abri selon le robot, batterie selon le voltage de l'outil, housse 14" ou 16"). Tableau produit porteur / prime correspondante, en annexe si la liste est longue. Dans Houston, la prime est souvent encodée dans la valeur de la liste produits (`réf#EAN#libellé#réf prime`) : la grille des modalités doit être identique.
3. **Prime au choix** (ex. carte carburant ou badge de recharge électrique ; boules, vin, console ou TV ; un jeu vidéo parmi 5). Lister toutes les primes proposées, dire que le choix se fait au moment de l'inscription et qu'il est **définitif**, et décrire chaque prime (valeur, conditions d'utilisation). Dans Houston : champ `reward` (`RewardSelector` ou `Radio`), parfois `question_1` ou `produit_achete` ; des champs peuvent dépendre du choix (ex. numéro d'un badge de recharge existant).
4. **Carte énergie / carburant dont la valeur est calculée** : selon le diamètre et le nombre de pneus (tableau diamètre × 2 ou 4 pneus, rien pour 1 pneu), par tranche d'achat (ex. 30 € par tranche de 200 € TTC). Tableau des valeurs + exemple chiffré, comme une ODR (§4.1). Comparer avec la formule `odr_options` et les metadata `refund_amount` (en centimes) de la liste Houston.
5. **Paliers selon la quantité achetée** (ex. 1 verre, puis duo de verres et pailles, puis plateau). Tableau quantité / prime, quantité minimale, produits pouvant être panachés ou non, stock par palier s'il existe.
6. **Primes réservées aux professionnels** : personnes morales, raison sociale et SIRET, limite par SIRET, adresse de livraison de l'entreprise (§4.1 n° 24).

Si une opération ne rentre dans aucune case, la décrire simplement et la faire relire au chef de projet.

### 6.2 Clauses propres aux primes

- **Description de la prime** : désignation exacte (marque, modèle, couleur si utile), valeur TTC indicative (« d'une valeur de 199,99 € TTC »), identique partout (titre, étapes, bloc légal). « Visuel non contractuel » si un visuel est utilisé.
- **Quota et stock** : « Offre valable pour les N premières inscriptions » et/ou « dans la limite des stocks disponibles », avec compteur s'il existe (§4.1 F).
- **Rupture de stock** : c'est **au client** de décider. Garder une phrase courte et générale qui reprend sa demande (par ex. « En cas d'indisponibilité de la prime, la Société Organisatrice se réserve le droit de la remplacer par une dotation de valeur équivalente ») ; ne pas détailler la procédure et ne rien imposer par défaut. Si le client ne dit rien, ne rien ajouter et le signaler simplement dans le message d'envoi.
- **Prime non échangeable** : « La prime ne pourra être ni échangée, ni remboursée, ni convertie en espèces, ni faire l'objet d'une contrepartie de quelque nature que ce soit. »
- **Envoi** : mode (courrier, colis, e-mail pour une prime digitale), délai (« dans un délai de 4 à 6 semaines / 6 à 8 semaines suivant la validation de la participation »), adresse de livraison = adresse saisie dans le formulaire, livraison uniquement dans le territoire de l'offre.
- **Colis non distribué ou retourné** : **ne pas détailler** (pas de délai pour se manifester, pas de règle de réexpédition), faute de pratique Promodev établie. Reprendre seulement ce que le client écrit lui-même.
- **Cartes énergie, carburant, cadeau** : réseau ou enseignes où l'utiliser, durée de validité, utilisation en une ou plusieurs fois si le client le précise, non remboursable et non prolongeable, responsabilité du porteur en cas de perte ou de vol. Reprendre les conditions du fournisseur de la carte transmises par le client, sans les inventer.
- **Prime digitale** (code, jeu, carte dématérialisée) : pas encore d'exemple validé. Demander au chef de projet et au client le mode de remise (e-mail, lien), la date limite d'activation et les conditions d'utilisation, et les laisser en `[À COMPLÉTER]` s'ils manquent.
- **Garantie et usage** : si le client le demande, « la garantie de la prime est celle du fabricant » et « la Société Organisatrice décline toute responsabilité liée à l'utilisation de la dotation ».
- **Pas d'IBAN ni de RIB** dans les justificatifs, sauf si le client prévoit un versement de remplacement.

### 6.3 Plan type d'une offre à primes

Même plan que l'ODR (§4.2), avec ces adaptations : « Organisation de l'offre » (offre promotionnelle avec obligation d'achat permettant d'obtenir {prime}) → « Produits porteurs et prime » (tableau) → « Modalités de participation » (§4.4) → « Envoi de la prime » (validation, délai, adresse) → « Conditions de participation » (quota, stock, limites) → « Conditions d'utilisation de la prime » (cartes) → acceptation, annulation, réclamation, données personnelles (§5) → annexes.

## 7. Générer le Word (sans modèle client)

Écrire le helper ci-dessous dans un fichier `modalites_docx.py` (dans le répertoire de travail), puis un court script de construction. `python-docx` est normalement installé ; sinon `pip install python-docx --break-system-packages`. Dans le texte, `**gras**` et `__souligné__` sont interprétés.

```python
# Générateur Word de modalités (python-docx). Usage : from modalites_docx import Modalites
import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

STYLES = {
  # nom       police            taille marges(G/D, H/B) titre_couleur  intertitre
  "articles":  dict(font="Century Gothic", size=10, lr=1.3, tb=1.5, accent="4472C4", head="article"),
  "sections":  dict(font="Calibri", size=11, lr=2.5, tb=2.5, accent=None, head="souligne"),
  "conditions":dict(font="Calibri", size=11, lr=2.5, tb=2.5, accent=None, head="majuscules"),
  "compact":   dict(font="Calibri", size=11, lr=2.5, tb=2.5, accent=None, head="gras"),
}

def _shade(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr(); s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), hex_); tcPr.append(s)

class Modalites:
    def __init__(self, style="articles"):
        self.st = STYLES[style]; self.n_article = 0
        self.doc = Document(); sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.left_margin = sec.right_margin = Cm(self.st["lr"]); sec.top_margin = sec.bottom_margin = Cm(self.st["tb"])
        for name in ("Normal", "List Bullet"):
            s = self.doc.styles[name]; s.font.name = self.st["font"]; s.font.size = Pt(self.st["size"])
            s.element.rPr.rFonts.set(qn("w:eastAsia"), self.st["font"])
            s.paragraph_format.space_after = Pt(6)
        self._page_number()

    def _page_number(self):
        p = self.doc.sections[0].footer.paragraphs[0]; p.alignment = AL.RIGHT
        r = p.add_run()
        for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
            if t: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t)
            else: e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
            r._r.append(e)

    def _runs(self, p, text, size=None, color=None, bold=None, underline=None):
        # **gras** et __souligné__ dans le texte
        for part in re.split(r"(\*\*.+?\*\*|__.+?__)", text):
            if not part: continue
            b, u = bold, underline
            if part.startswith("**"): part, b = part[2:-2], True
            elif part.startswith("__"): part, u = part[2:-2], True
            r = p.add_run(part); r.bold = b; r.underline = u
            if size: r.font.size = Pt(size)
            if color: r.font.color.rgb = RGBColor.from_string(color)
        return p

    def titre(self, lignes):
        """lignes[0] = titre principal, suivantes = sous-titres (nom op, dates…)."""
        for i, l in enumerate(lignes):
            p = self.doc.add_paragraph(); p.alignment = AL.CENTER
            col = self.st["accent"] if i > 0 else None
            self._runs(p, l, size=14 if i < 2 else 11, color=col, bold=True)
        self.doc.add_paragraph()

    def intertitre(self, texte):
        h = self.st["head"]; p = self.doc.add_paragraph(); p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.keep_with_next = True
        if h == "article":
            self.n_article += 1; self._runs(p, f"Article {self.n_article} - {texte}", bold=True, underline=True)
        elif h == "souligne": self._runs(p, texte + " :", bold=True, underline=True)
        elif h == "majuscules": self._runs(p, texte.upper(), bold=True)
        else: self._runs(p, texte, bold=True)
        return self.n_article

    def para(self, texte, justifie=True, taille=None, retrait=0):
        p = self.doc.add_paragraph()
        if justifie: p.alignment = AL.JUSTIFY
        if retrait: p.paragraph_format.left_indent = Cm(retrait)
        return self._runs(p, texte, size=taille)

    def puces(self, items, retrait=1.0):
        for it in items:
            p = self.doc.add_paragraph(style="List Bullet"); p.paragraph_format.left_indent = Cm(retrait)
            p.paragraph_format.space_after = Pt(2); self._runs(p, it)

    def etapes(self, items):
        """Étapes numérotées « 1. … » ; un item peut être (texte, [sous-puces])."""
        for i, it in enumerate(items, 1):
            txt, sous = (it if isinstance(it, tuple) else (it, None))
            p = self.doc.add_paragraph(); p.alignment = AL.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.6); p.paragraph_format.first_line_indent = Cm(-0.6)
            self._runs(p, f"{i}.\t{txt}")
            if sous: self.puces(sous, retrait=1.4)

    def tableau(self, entetes, lignes, largeurs_cm=None, fond_entete="D9E2F3", texte_entete_blanc=False):
        t = self.doc.add_table(rows=1, cols=len(entetes)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for j, h in enumerate(entetes):
            c = t.rows[0].cells[j]; _shade(c, fond_entete); c.text = ""
            self._runs(c.paragraphs[0], h, bold=True, color="FFFFFF" if texte_entete_blanc else None)
        for row in lignes:
            cells = t.add_row().cells
            for j, v in enumerate(row): cells[j].text = ""; self._runs(cells[j].paragraphs[0], str(v))
        tr = t.rows[0]._tr.get_or_add_trPr(); e = OxmlElement("w:tblHeader"); e.set(qn("w:val"), "true"); tr.append(e)
        if largeurs_cm:
            t.autofit = False
            for j, g in enumerate(t._tbl.tblGrid.findall(qn("w:gridCol"))): g.set(qn("w:w"), str(int(largeurs_cm[j] * 567)))
            for row in t.rows:
                for j, w in enumerate(largeurs_cm): row.cells[j].width = Cm(w)
        self.doc.add_paragraph()

    def saut_de_page(self):
        self.doc.add_page_break()

    def enregistrer(self, chemin):
        self.doc.save(chemin)
```

Exemple de construction (style `articles`) :

```python
from modalites_docx import Modalites
m = Modalites("articles")
m.titre(["MODALITÉS", "RENTRÉE MARQUE 2026", "Opération limitée aux 10 000 premières participations"])
m.intertitre("Organisation de l’offre")
m.para("La société SAS MARQUE France (ci-après dénommée « Société Organisatrice ») …")
m.intertitre("Modalités de participation")
m.para("Pour obtenir votre remboursement le Participant doit :")
m.etapes([("**Acheter un produit MARQUE éligible** entre le 31/08/2026 et le 30/09/2026 …", None),
          ("**Se connecter** sur offres-marque.fr avant le 10/10/2026 en renseignant :",
           ["Ses coordonnées complètes (civilité, nom, prénom, adresse e-mail, adresse postale, n° mobile),",
            "Ses informations d’achat (date d'achat et enseigne),", "Le code-barres du produit acheté."])])
# … autres articles …
m.saut_de_page()
m.para("**Annexe 1 : Produits éligibles exclusivement**", justifie=False)
m.tableau(["EAN / Code-barres", "Désignation produit", "Remboursement"], lignes, [3.6, 11.4, 3.4])
m.enregistrer("/mnt/user-data/outputs/2026999 - Modalités ODR Rentrée Marque 2026 - V1.docx")
```

Style `conditions` : tableau calendrier avec `fond_entete="000000", texte_entete_blanc=True`. Pour les annexes depuis un Excel client, suivre le §4.5. Exemple :

```python
import pandas as pd
df = pd.read_excel(xlsx, sheet_name=0, dtype=str, header=2).dropna(how="all")
df = df.apply(lambda c: c.str.strip())
lignes = [[r["EAN"], r["Désignation"], f'{float(r["Montant"].replace(",", ".")):.2f} €'.replace(".", ",")]
          for _, r in df.iterrows()]
print(len(df), "lignes lues")          # à comparer au nombre de lignes de l'annexe
m.tableau(["EAN / Code-barres", "Désignation produit", "Remboursement"], lignes, [3.6, 11.4, 3.4])
```

Les repères `[À COMPLÉTER : …]` se surlignent avec `run.font.highlight_color = WD_COLOR_INDEX.YELLOW`.

Toujours faire un rendu visuel avant l'envoi (conversion PDF avec le script soffice du skill docx, puis `pdftoppm`) et regarder la première page et l'annexe.

## 8. Retour client → version suivante

Charger le skill **docx** pour la mécanique XML (unzip, `merge_runs.py`, `comment.py`, `validate.py --author`).

1. **Lire le retour** : `pandoc --track-changes=all -t markdown fichier.docx` montre les insertions, suppressions et commentaires avec leur auteur. Lire aussi le message du client s'il y en a un.
2. **Dresser la liste des demandes** : pour chacune, noter l'emplacement, la demande et la décision proposée (appliquer / appliquer avec reformulation / à discuter).
3. **Signaler avant d'appliquer** toute demande qui :
   - contredit le paramétrage Houston ou une autre partie du document (date, montant, quota, justificatif) ;
   - supprime une protection importante (limite par foyer, régularisation, contrôle des originaux, clause données) ;
   - n'est pas faisable techniquement sur la plateforme (ex. justificatif ou champ non prévu au formulaire) ;
   - touche aux règles R1 ou R2 (§0) : rôles des données, consigne d'entourer les informations.
   Dans ces cas, demander au chef de projet ce qu'il veut faire.
4. **Produire V(n+1)** à partir du fichier renvoyé par le client, pas d'une version antérieure : il peut avoir modifié des passages sans suivi.
   - Accepter les modifications du client validées (`accept_changes.py` du skill docx, ou suppression des balises dans le XML).
   - Appliquer les changements Promodev **en suivi des modifications**, auteur `Promodev` (`<w:ins>`/`<w:del>`), puis `validate.py --author "Promodev"` pour vérifier que tout est bien suivi.
   - Répondre aux commentaires traités (réponse courte « Modifié : … » avec `comment.py --parent`) ou les supprimer si le client préfère un document propre. Laisser ouverts ceux qui restent à trancher.
   - Répercuter chaque changement partout où l'information apparaît (une date modifiée à l'article 2 se retrouve souvent en 3, 7 et dans le bloc courrier).
   - Si le client envoie un nouvel Excel de produits ou de points de vente, reconstruire l'annexe depuis ce fichier (§4.5) et lister les lignes ajoutées, retirées ou modifiées par rapport à la version précédente.
5. Refaire les contrôles §0 et §9 sur la nouvelle version complète, pas seulement sur les passages modifiés.
6. **Récapitulatif** en fin de réponse, prêt à coller dans l'e-mail au client : tableau Emplacement / Demande / Traitement, puis les points en attente.

Nommage : `{idgame ou N°} - Modalités {Nom opération} - V{n}.docx`. Pour la version validée, suffixe `V{n}DEF`, puis générer une copie propre avec toutes les modifications acceptées et sans commentaires.

## 9. Contrôles avant chaque envoi

Extraire le texte (`pandoc -t plain`) et vérifier point par point. Signaler ce qui est trouvé dans le message, sans corriger en silence ce qui relève d'un choix du client.

**Règles Promodev (§0)**
- R1 : responsable de traitement = la Société Organisatrice, nommée ; sous-traitants ou prestataires mentionnés, nommément (PROMO.DEV) ou de façon générale (bloquant). Adresse pour exercer les droits, e-mail ou postale, du client ; `dpo@promo.dev` seulement en cas de délégation écrite confirmée (alerte, non bloquant). Ces informations peuvent être dans les modalités ou dans la politique de confidentialité citée, qu'il faut alors lire. Résultat : conforme / non conforme / à vérifier (politique non lue). S'il y a plusieurs sociétés organisatrices (ex. une marque et une enseigne), vérifier qu'elles sont identifiées et que le rôle de chacune pour les données est clair.
- R2 (bloquant) : aucune consigne d'entourer, surligner ou encadrer une information sur un justificatif (`grep -n -i -E "entour|surlign|encadr|cercl|stabilo"`). Regarder aussi les images (exemple de ticket annoté).

**Limites (§4.3) : modalités ↔ brief ↔ Houston**

Pour chaque limite, noter ce que disent les modalités, le brief client s'il est fourni, et Houston. Les modalités validées font foi face au paramétrage (guide Houston) : signaler les écarts, ne pas trancher. Où regarder dans Houston :

| Limite | Houston (`operation_info`, `list_forms` puis `get_form`, `list_datalists`) |
|---|---|
| Territoire | `country`, `langs` de l'opération ; champ Adresse `countries` ; `acceptedCountries` des champs Téléphone et IBAN ; datalist des points de vente (ex. présence de magasins en Corse) |
| Type de participants | champ `user_type` (Particulier / Professionnel), `company_name`, `siret` ; `isOver18` ou `birthdate` |
| Période | `date_debut` et `date_fin_achat` (= bornes `min`/`max` du champ `buying_date`), `date_fin` (fin des inscriptions), `date_fin_regule` et `missingRegulMaxDays`, `date_fin_reclamation`. Lire `read_houston_guide` section `operation-dates` avant de comparer |
| Participation | `unique: true` sur `email`, `phone`, `iban`, `receipt_number`, `code_unique`, `imei`, `siret` ; options du champ `quantity` ; nombre d'emplacements produit. Si les modalités annoncent une limite (ex. 1 participation par IBAN) sans `unique` correspondant, l'écrire comme « non paramétré dans le formulaire, peut être contrôlé à la saisie : à confirmer » |
| Remboursement ou dotation | `odr_options` : `max` (plafond par dossier), formule `code_expr` (plafonds, quantités, `min(…, prix)`), montants des datalists (`metadata`, ex. `refund_amount` en centimes), `budget` ; pour les primes, champ de choix `reward` et prime encodée dans la liste produits |

Le quota « N premières participations » n'est pas lisible de façon sûre via le MCP : le demander au chef de projet si les modalités en parlent.

**Parcours utilisateur (§4.4) : modalités ↔ formulaire CREATE Houston**
- Étapes, informations obligatoires, justificatifs, coordonnées bancaires, cases à cocher et e-mails reçus : identiques dans les deux sens.
- Toute limite ou tout contrôle annoncé doit reposer sur une donnée réellement collectée (ex. pas de limite par immatriculation sans champ immatriculation).

**Cohérence interne**
- Chaque date apparaît avec la même valeur partout. Chronologie : début d'achat ≤ fin d'achat < limite de participation ≤ limite de régularisation < limite de réclamation. Les jours et mois correspondent entre « 10 octobre » et « 10/10 ».
- Même nom d'opération (mot pour mot, ex. avec ou sans le nom de la marque), même N° Promodev, même URL de site et même e-mail de contact partout.
- Montants, plafonds, quotas et nombre de produits identiques entre le titre, les articles et l'annexe. Un exemple chiffré doit être juste.
- Une annexe citée existe, et ses numéros de renvoi (« annexe 1 », « article 4 ») pointent au bon endroit. Pas de « article N » dans un document non numéroté.
- Limite par foyer ou par personne : une seule formulation, avec les mêmes critères (nom, adresse, e-mail, IBAN) partout.

**Restes d'autres documents** (fréquents en duplication)
- Vocabulaire de jeu dans une ODR : « Jeu », « lot », « gagnant », « dotation », « tirage », « désignation du participant », « modalités de jeu » (y compris dans les libellés du formulaire Houston, ex. case RGPD « gestion du jeu »). Remplacer par offre, remboursement, participation. « Prime » est accepté (§4.1 bis). Exceptions : ODR avec tirage au sort ou instant gagnant (§4.1 n° 21), où ce vocabulaire est normal ; offres à primes, où « dotation » est normal (mais pas « gagnant », « lot », « tirage »).
- Restes d'ODR dans une offre à primes : « remboursement », « virement », IBAN ou RIB demandé alors que la prime est envoyée (sauf si le client prévoit un versement de remplacement).
- Nom, dates, enseigne, site ou DPO d'une autre opération ou d'un autre client.
- Année précédente (tarif postal, « tarif en vigueur en 2025 »).

**Annexes (§4.5)**
- Nombre de lignes Excel = nombre de lignes de l'annexe ; pas de doublons ni de cellules vides ; EAN à 13 chiffres avec clé valide ; codes postaux sur 5 caractères.
- Montants de l'annexe = mécanique décrite = liste Houston (`refund_amount` en centimes) ; points de vente de l'annexe = liste Houston ; codes postaux dans le territoire annoncé.

**Offres à primes (§6)**
- Prime décrite de la même façon partout (désignation, valeur TTC, nombre par foyer ou par produit) ; primes au choix des modalités = options du champ de choix dans le formulaire Houston (`reward` ou équivalent).
- Grille produit porteur → prime et tableau des valeurs de carte = listes Houston (valeur encodée dans la liste produits, metadata `refund_amount` en centimes, formule `odr_options`).
- Pas d'IBAN, de RIB ni de « remboursement / virement » alors que la prime est envoyée (reste d'ODR), sauf versement de remplacement prévu par le client.
- Territoire de livraison des modalités = pays acceptés par le champ adresse (`countries`, ex. `fr` / `mc`).
- Quota ou stock annoncés cohérents entre le titre, les conditions et Houston ; délai d'envoi identique partout.
- Si le formulaire n'est pas dans Houston (site hébergé chez le client), le dire et vérifier le parcours sur le site ou avec le chef de projet.
- Formulaire dupliqué d'une autre opération : options ou libellés restés sur l'ancien produit ou l'ancien client (ex. options d'une autre marque restées dans le formulaire) : le signaler, la liste liée fait foi.

**Exactitude**
- **IBAN : France uniquement pour le moment.** Un IBAN français fait 27 caractères : « FR » + 25 caractères. « IBAN commençant par FR (27 caractères) » et « FR suivi de 25 caractères » sont justes ; « IBAN commençant par FR (25 caractères) » est faux. Le BIC fait 8 ou 11 caractères (« 8 à 11 » est imprécis : simple remarque). Si le territoire inclut Monaco (IBAN « MC ») ou un autre pays alors que seuls les IBAN FR sont acceptés, signaler l'incohérence. Dans Houston, vérifier `acceptedCountries: ["FR"]` sur le champ IBAN.
- EAN = 13 chiffres. Signaler les codes de 12 chiffres (souvent un UPC ou un 0 perdu par Excel) sans les corriger d'office. IMEI = 15 chiffres.
- Accords et coquilles courantes : « 60 jours calendaires », « force majeure », « opération promotionnelle intitulée », « participant majeur », « personnes physiques majeures », « Règlement (UE) 2016/679 ».
- Mentions données : références d'articles de la loi Informatique et Libertés du type « article 38 », « article 40 », « article 40.1 », ou droits énoncés à l'ancienne (« droit de radiation », loi de 1978 sans le RGPD). Elles datent d'avant la refonte de 2018 : proposer une formulation à jour et le signaler pour validation par le DPO du client. Base légale cohérente dans tout le document.

**Houston** (si l'opération existe) : dates, quota, justificatifs demandés et champs du formulaire concordent avec les modalités. Comparer aussi le calcul du remboursement (`odr_options` : type, pourcentage, montant, `max`, formule `code_expr`) avec la mécanique décrite : paliers, plafonds, quantités, plafond au prix payé. Lister les écarts (ex. une formule qui rembourse aussi 2 produits à 50 % alors que les modalités ne parlent que de 3 produits).

## 10. Livraison

- Écrire le .docx dans `/mnt/user-data/outputs/`. Si un dossier de l'ordinateur de l'utilisateur est connecté, l'enregistrer à côté des versions précédentes, sans écraser un fichier existant.
- Message court : d'abord les manquements bloquants aux règles R1 et R2 s'il y en a, puis les alertes sur l'adresse DPO, puis ce qui a été produit, les `[À COMPLÉTER]` restants, les contrôles de l'Excel (§4.5), les autres alertes du §9 et, pour une V2+, le tableau récapitulatif du §8.