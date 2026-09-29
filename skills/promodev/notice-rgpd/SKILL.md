---
name: notice-rgpd
description: "Rédige et vérifie la notice RGPD affichée sur les sites de participation Promodev (ODR, Promocard, primes, jeux), client ou Promodev responsable de traitement, en Word + texte à coller."
---

# Notice RGPD des sites de participation

> **Aucune donnée client dans ce skill.** Les exemples sont fictifs ou génériques : aucun nom de client, d'agence, d'adresse, de DPO, de numéro d'opération ni de formulation propre à un client. Quand une information nécessaire manque dans les documents fournis ou dans Houston (société organisatrice, agence, adresse DPO ou délégation écrite à Promodev, durée de conservation, étude de dépôt, montants, dotations, formulation déjà validée pour ce client…), **poser la question** au chef de projet avant de rédiger. Ne jamais la reprendre d'une autre opération ni l'inventer.

La notice est le court texte d'information RGPD affiché sur le site de participation d'une opération (sous le formulaire). C'est un document distinct des modalités (skill **modalites-operation**), du règlement de jeu (skill **reglement-jeu**) et de la politique de confidentialité (skill **politique-confidentialite**). Elle doit rester cohérente avec eux.

Le skill fait deux choses : **rédiger** une notice à partir de la trame du §4, et **vérifier** une notice existante (§7).

La notice n'est pas un document Promodev : pas de charte promo-dev-docs, ni en-tête ni logo. Écrire en français, guillemets « », PROMODEV en majuscules.

**À faire en premier, avant toute rédaction : poser les questions du §1 au chef de projet (AskUserQuestion).** Ne jamais deviner le responsable de traitement ni la mécanique.

## 1. Questions systématiques au chef de projet

Toujours poser ces questions, même si le contexte semble évident. Quand un document validé ou Houston donne déjà une réponse, la proposer comme première option pour que le chef de projet la confirme d'un clic.

1. **Qui est responsable de traitement ?**
   - le client (cas `ClientRT`, la très grande majorité) ;
   - PROMODEV (cas `PromodevRT`).
   → commande toute la trame (§4).
2. **Quelle est la mécanique de l'opération, et y a-t-il un virement ?**
   - ODR remboursée par virement ;
   - Promocard (remboursement sur carte, pas d'IBAN) ;
   - offre à primes (préciser : prime envoyée, ou remboursement par virement) ;
   - jeu dont un gain est versé par virement ;
   - jeu sans virement (lots physiques, bons de réduction…).
   → commande le paragraphe « remboursement / 10 ans » (§4.3). **Ce paragraphe n'est mis que s'il y a un virement**, donc un IBAN collecté. Pour un jeu, il est adapté au « versement du gain ».
3. **As-tu un document validé pour récupérer les infos client ?**
   - modalités validées par le client ;
   - règlement de jeu validé ;
   - non, pas encore → on part de Houston.
   Demander le fichier s'il existe. Un document validé **fait foi** sur Houston en cas de divergence (raison sociale, adresse, nom de l'opération).
4. **Idgame ou lien test.promo.dev** de l'opération (si pas déjà fourni).
5. **Durée de conservation** des données : toujours la demander, jamais de valeur par défaut. Proposer celle des modalités / du règlement s'ils en indiquent une (ex. « 12 mois à compter de la date de fin de l'opération »), et la formule « 1 an à compter de la fin de l'opération ou du dernier échange avec le participant » comme alternative. Si aucun document ne la donne, poser la question.
6. **Adresse pour exercer les droits** : e-mail DPO du client, adresse postale, ou les deux. Toujours la demander, en proposant celle des modalités. En cas `PromodevRT`, proposer `dpo@promo.dev` comme réponse attendue. Si le client n'a pas de DPO connu, demander s'il a délégué par écrit l'exercice des droits à Promodev : dans ce cas seulement, c'est `dpo@promo.dev`, et le client reste responsable de traitement.
7. **Agence** : une agence intervient-elle comme sous-traitant ? Si oui, son nom exact.
8. **Partenaire / marque** : l'opération associe-t-elle une marque partenaire du responsable de traitement (ex. un distributeur qui organise l'offre avec une marque de smartphones) ? Une marque propre du client (ex. une gamme ou sous-marque du groupe organisateur) n'est pas un partenaire.

Les questions 1, 2, 5 et 6 sont **toujours** posées. Les questions 3, 4, 7 et 8 ne le sont que si la demande ou le document fourni ne donnent pas clairement la réponse (ex. le chef de projet joint les modalités validées et elles ne mentionnent aucune agence → ne pas demander).

AskUserQuestion accepte 4 questions par appel : mettre les questions 1, 2, 5 et 6 dans le premier appel, et les éventuelles questions restantes dans un second appel envoyé tout de suite après. Ne pas commencer à rédiger entre les deux.

Si personne ne peut répondre (session automatique) : retenir `ClientRT`, déduire la mécanique du document validé et du formulaire Houston (champ IBAN), laisser durée et adresse des droits en `[À COMPLÉTER]` surligné jaune, et annoncer ces hypothèses en tête de la livraison.

## 2. Récupérer les informations

Ordre de priorité :

1. **Document validé** (modalités ou règlement de jeu) fourni par le chef de projet : raison sociale exacte, adresse du siège, nom de l'opération, marque partenaire, mécanique, mode de remboursement ou nature des gains, opt-in éventuel, durée de conservation, adresse DPO.
2. **Houston**, pour compléter et contrôler :
   - `find_operation` (idgame, nom ou client) puis `operation_info` : idgame, nom de l'opération, client, dates, type ;
   - `list_forms` / `get_form` sur le formulaire CREATE : présence d'un champ `Iban` (→ virement), d'une case opt-in marketing (`marketing_opt_in_…`, newsletter → phrase sur le consentement), des champs collectés.
   Si les infos client (raison sociale, adresse) ne sont pas dans Houston, les demander au chef de projet ou les chercher (site officiel, société.com / Pappers) et le signaler dans le récapitulatif.
3. **Ancienne notice** du même client, si elle existe : pour reprendre ses choix (durée, adresse des droits), à confirmer.

**Contrôle mécanique / Houston** : si la réponse du chef de projet sur le virement ne concorde pas avec le formulaire (virement annoncé mais aucun champ IBAN, ou champ IBAN présent sur une opération annoncée sans virement), le signaler avant de livrer. La réponse du chef de projet commande la rédaction.

**Nom de l'opération** : celui du document validé, précédé de l'idgame sous sa forme numérique (ex. `2026999 – ODR Noël 2026`). Le titre Houston peut être plus restrictif (ex. une seule enseigne) : le document validé fait foi, le signaler.

Ne jamais inventer une information manquante : `[À COMPLÉTER]` surligné en jaune, et le signaler.

Si les modalités ne sont pas encore validées, le dire dans le récapitulatif : la notice pourra devoir être reprise après validation.

Anomalies vues au passage dans le formulaire Houston (ex. libellé demandant d'entourer les infos du ticket, lien vers la politique d'une ancienne opération, dates d'une année précédente) : les signaler brièvement en fin de livraison, sans les corriger.

## 3. Identifier le cas

| Critère | Valeurs |
|---|---|
| Responsable de traitement | `ClientRT` · `PromodevRT` |
| Sous-traitants | `PromodevSeul` · `Agence` (agence + PROMODEV) |
| Mécanique | `ODR` (virement) · `Promocard` (remboursement sur carte, pas d'IBAN) · `Prime` · `JeuVirement` (gain versé par virement) · `JeuSansVirement` |
| Options | Virement (oui/non) · Opt-in / newsletter (oui/non) · Marque partenaire (oui/non) |

## 4. Trame de référence

Légende : `{RT}` = responsable de traitement ; `{ADRESSE_RT}` = son adresse postale ; `{PARTENAIRE}` = marque partenaire ; `{AGENCE}` = agence ; `{IDGAME}` / `{NOM_OP}` = idgame et nom de l'opération ; `{DUREE}` = durée donnée par le chef de projet ; `{ADRESSE_DROITS}` = adresse donnée par le chef de projet ; `[si …]` = bloc conditionnel. Les éléments en **gras** dans la trame sont en gras dans la notice.

### 4.1 Cas `ClientRT` (deux modèles validés)

**NOTICE** (centré)

Les informations recueillies dans le cadre de cette opération sont enregistrées dans un fichier informatisé sous la responsabilité de **{RT}, {ADRESSE_RT}**, en sa qualité de responsable de traitement, afin de permettre le traitement et le suivi de votre participation à l'opération **{IDGAME} – {NOM_OP}**.

La base légale de ce traitement est **l'exécution du contrat** auquel vous êtes partie, résultant de votre participation à l'opération.[si opt-in : L'envoi d'informations commerciales de {RT} repose sur **votre consentement**, que vous pouvez retirer à tout moment.]

Les données collectées sont accessibles uniquement aux destinataires qui en ont besoin dans le cadre de l'opération : **{RT}**[si partenaire : , ainsi que son partenaire **{PARTENAIRE}**], et les sous-traitants intervenant pour son compte, dont [PromodevSeul : **PROMODEV** | Agence : **{AGENCE}** et **PROMODEV**]. Au sein de ces sociétés, l'accès aux données est limité aux seules personnes habilitées et aux équipes ayant besoin d'en connaître pour assurer le traitement des participations, leur suivi et, le cas échéant, le support aux participants.

Les données à caractère personnel collectées sont conservées pendant la durée nécessaire au traitement de l'opération, puis pendant une durée maximale de **{DUREE}**.

[si virement de remboursement — ODR, prime remboursée par virement :] Lorsque la participation donne lieu à un **remboursement**, les données nécessaires à la traçabilité et à la justification de l'opération de paiement, notamment les **nom, prénom, coordonnées bancaires (IBAN) ainsi que les informations relatives au remboursement**, sont conservées pendant une durée de **10 ans à compter de la date du remboursement**. À l'issue de leur période de conservation courante, ces données sont placées dans une **base d'archives distincte de la base active**, dont l'accès est strictement limité aux seules personnes habilitées. Elles ne sont alors accessibles qu'aux fins de satisfaire aux obligations légales applicables, d'établir la preuve des opérations réalisées ou de répondre à une demande des autorités compétentes.

[si jeu dont un gain est versé par virement :] Lorsque la participation donne lieu au **versement d'un gain par virement**, les données nécessaires à la traçabilité et à la justification de l'opération de paiement, notamment les **nom, prénom, coordonnées bancaires (IBAN) ainsi que les informations relatives au versement du gain**, sont conservées pendant une durée de **10 ans à compter de la date du versement du gain**. À l'issue de leur période de conservation courante, ces données sont placées dans une **base d'archives distincte de la base active**, dont l'accès est strictement limité aux seules personnes habilitées. Elles ne sont alors accessibles qu'aux fins de satisfaire aux obligations légales applicables, d'établir la preuve des opérations réalisées ou de répondre à une demande des autorités compétentes.

Vous disposez, dans les conditions prévues par la réglementation applicable, d'un **droit d'accès, de rectification, d'effacement et de limitation du traitement** de vos données ainsi que, lorsque les conditions sont réunies, d'un **droit à la portabilité de vos données et d'un droit d'opposition**.

Pour exercer vos droits, vous pouvez adresser votre demande écrite à **{ADRESSE_DROITS}**, en précisant l'objet de votre demande.

Pour plus d'informations sur vos droits, vous pouvez consulter le site de la **CNIL**.

Si vous estimez, après avoir contacté {RT}, que vos droits en matière de protection des données personnelles ne sont pas respectés, vous pouvez adresser une réclamation à la **CNIL**.

### 4.2 Cas `PromodevRT` (adapté de la trame client — à faire valider par Audrey GILARDI, DPO Promodev, au premier usage)

Même texte que le §4.1, avec ces changements :
- `{RT}` = **PROMODEV** ; `{ADRESSE_RT}` = adresse du siège reprise de la dernière politique de confidentialité Promodev validée (ne pas la retaper de mémoire) ;
- destinataires : « **PROMODEV**, ainsi que **{CLIENT}**[si partenaire : et son partenaire **{PARTENAIRE}**], organisateur de l'opération[si agence : , et **{AGENCE}**] » ; supprimer « les sous-traitants intervenant pour son compte, dont PROMODEV » ;
- adresse des droits : réponse du chef de projet (attendu : `dpo@promo.dev`) ;
- dernière phrase : « après avoir contacté PROMODEV ».

Tant qu'aucune notice `PromodevRT` n'a été validée par Audrey, le signaler dans le récapitulatif. Quand une version est validée, proposer au chef de projet de la reporter dans ce skill comme modèle.

### 4.3 Paragraphe « remboursement / 10 ans » selon la mécanique

Le paragraphe dépend **uniquement de la présence d'un virement** (donc d'un IBAN collecté), d'après la réponse du chef de projet à la question 2.

| Mécanique | Paragraphe |
|---|---|
| ODR remboursée par virement | Oui — version « remboursement », « à compter de la date du remboursement » |
| Offre à primes avec remboursement par virement | Oui — version « remboursement » |
| Offre à primes sans virement (prime envoyée) | **Non** |
| Promocard | **Non** (remboursement sur carte, pas d'IBAN) |
| Jeu dont un gain est versé par virement | Oui — version « versement du gain », « à compter de la date du versement du gain » |
| Jeu sans virement (lots, bons de réduction…) | **Non** |

Sans virement, supprimer le paragraphe en entier : ne pas garder une phrase isolée sur l'archivage ou les autorités.

## 5. Règles Promodev (bloquantes en rédaction comme en vérification)

- **R1 Rôles** : un seul responsable de traitement, nommé avec son adresse. En `ClientRT`, PROMODEV (et l'agence le cas échéant) apparaît **uniquement comme sous-traitant**, jamais comme responsable ou co-responsable.
- **R2 Base légale** : exécution du contrat ; consentement uniquement pour l'opt-in / newsletter, jamais pour la participation elle-même.
- **R3 Archivage bancaire** : paragraphe présent **si et seulement si** il y a un virement (§4.3), avec le point de départ des 10 ans : « à compter de la date du remboursement » (jeu : « du versement du gain »). Ne jamais écrire « 10 ans » seul — un ancien modèle l'omettait.
- **R4 Durée courante** : toujours celle donnée par le chef de projet, jamais inventée.
- **R5 Adresse des droits** : toujours celle donnée par le chef de projet. `dpo@promo.dev` hors `PromodevRT` → demander au chef de projet si le client a délégué par écrit l'exercice des droits à Promodev ; sans confirmation, alerte à signaler.
- **R6 Cohérence** : raison sociale, adresse, nom de l'opération et durée identiques à ceux des modalités / du règlement / de la politique de confidentialité de l'opération quand ils existent. Divergence → le document validé fait foi, le signaler.

## 6. Livrer

Deux livrables, générés depuis **un seul script** (même liste de paragraphes pour le Word et le HTML) :

1. **Word** (lire le skill **docx** avant de générer), sur le modèle de l'exemple :
   - A4, marges 2,5 cm (1417 DXA), police Aptos 12 pt ;
   - deux lignes vides, puis « NOTICE » centré en gras ;
   - le texte en paragraphes courts, gras sur les éléments de la trame ;
   - infos manquantes : `[À COMPLÉTER]` surligné en jaune ;
   - nom : `NOTICE_{IDGAME numérique}_{Client}.docx` (ex. `NOTICE_2026999_Marque.docx` ; V1, V2… si demandé).
2. **Texte à coller sur le site de participation** : un fragment HTML simple (`<p>`, `<strong>`, sans style ni `<html>`, sans le titre « NOTICE »), dans le message de réponse sous forme de bloc de code, et en fichier `NOTICE_{IDGAME}_{Client}.html`. Même texte, mot pour mot, que le Word.

Enregistrer dans le dossier connecté s'il y en a un, sinon dans les sorties de la session.

Après génération : convertir le Word en PDF et le regarder, puis relire le texte avec les contrôles du §7 (surtout R3 : paragraphe présent seulement s'il y a un virement, et point de départ des 10 ans). Vérifier par `diff` que le texte du Word et celui du HTML sont identiques.

Message de livraison court : cas retenu (responsable, mécanique, virement oui/non), sources utilisées (document validé ou Houston), points `[À COMPLÉTER]`, alertes éventuelles, puis le bloc HTML.

## 7. Vérifier une notice existante

1. Extraire le texte (`pandoc -t plain --wrap=none`).
2. Demander le responsable de traitement et la mécanique si la notice ne permet pas de les confirmer (§1, questions 1 et 2).
3. Contrôler R1 à R6, puis : nom de l'opération et idgame corrects (comparer à Houston), aucune trace d'un autre client (copie d'un ancien modèle), paragraphe 10 ans présent seulement s'il y a un virement et dans la bonne version (remboursement / versement du gain).
4. Classer : **bloquant** (R1), **écart à signaler** (R2 à R6), **remarque** (coquilles, formulations).
5. Livrer le Word corrigé en **suivi des modifications** (auteur `Promodev`) avec un commentaire par correction, et un message qui commence par les points bloquants.

Ne pas trancher seul un point juridique nouveau (base légale inhabituelle, transfert hors UE, données sensibles) : le signaler.