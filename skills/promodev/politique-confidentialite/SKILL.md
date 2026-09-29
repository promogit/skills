---
name: politique-confidentialite
description: "Rédige et vérifie en Word les politiques de confidentialité et cookies Promodev (ODR, Promocard, primes, jeux), client ou Promodev responsable de traitement, avec ou sans agence, et les trames génériques."
---

# Politiques de confidentialité et cookies (Word, validation client)

> **Aucune donnée client dans ce skill.** Les exemples sont fictifs ou génériques : aucun nom de client, d'agence, d'adresse, de DPO, de numéro d'opération ni de formulation propre à un client. Quand une information nécessaire manque dans les documents fournis ou dans Houston (société organisatrice, agence, adresse DPO ou délégation écrite à Promodev, durée de conservation, étude de dépôt, montants, dotations, formulation déjà validée pour ce client…), **poser la question** au chef de projet avant de rédiger. Ne jamais la reprendre d'une autre opération ni l'inventer.

**À faire en premier, avant toute rédaction ou vérification : poser les deux questions du §3.0.**

Deux familles de documents :

- la **politique d'une opération**, rédigée au nom de la Société Organisatrice (le client), qui la valide, parfois après l'avoir retouchée — trame du §4 ;
- les **trames génériques** réutilisables, à placeholders, tenues à jour par Audrey GILARDI (DPO Promodev) — §4bis. Quatre fichiers : client responsable de traitement avec / sans cookies, Promodev responsable de traitement avec / sans cookies.

Le skill fait deux choses : **rédiger** à partir de ces trames, et **vérifier** une politique existante (écrite par Promodev, retouchée par le client, ou rédigée par le client ou son agence).

La politique d'une opération n'est pas un document Promodev : ne pas appliquer la charte promo-dev-docs, et ne mettre ni en-tête ni logo Promodev. Sauf dans le cas `PromodevRT`, PROMODEV n'y apparaît qu'en tant que sous-traitant.

Écrire en français, avec des guillemets « » et « Société Organisatrice » avec une majuscule. PROMODEV s'écrit en majuscules, comme dans les modèles.

Ce skill va de pair avec **modalites-operation** : ce dernier vérifie que les modalités renvoient vers une politique qui contient les rôles et l'adresse DPO. Les règles R1 sont les mêmes dans les deux skills.

## 0. Règles Promodev obligatoires

Ces règles s'appliquent à toute politique, y compris celles écrites ou retouchées par le client. Ne jamais recopier une clause d'un ancien document sans la vérifier : les anciens modèles contiennent des coquilles et des variantes non retenues (voir §6).

### R1. Rôles nommés et adresse DPO (bloquant)

Le cas d'acteurs (§1) vient de la réponse à la première question du §3.0, ou du contrat de sous-traitance : ne jamais le déduire seul.

**Cas `PromodevSeul` et `Agence` (la très grande majorité).** La politique doit dire clairement :
- que la **Société Organisatrice** (raison sociale) est **responsable du traitement** ;
- que PROMODEV est **sous-traitant** (« prestataire » ou « partenaire » sont acceptés si le rôle de sous-traitant ressort de la clause des destinataires) ; avec une agence, l'agence **et** PROMODEV sont nommés comme sous-traitants ;
- une **adresse pour exercer les droits** : l'adresse DPO du client, par e-mail ou par courrier.

Sont non conformes (bloquant) :
- aucun responsable de traitement nommé ;
- PROMODEV ou l'agence présentés comme responsable de traitement ou responsable conjoint ;
- avec une agence, l'agence ou PROMODEV absents de la liste des sous-traitants.

**Cas `PromodevRT`.** PROMODEV est responsable du traitement et le dit : c'est la politique générale PROMODEV tenue par Audrey (version datée, v1.8 du 22.09.2026 à ce jour), pas la politique d'une opération d'un client. L'adresse des droits est `dpo@promo.dev`. Ce cas ne s'applique que si le chef de projet l'indique : dans le doute, c'est le client qui est responsable de traitement.

**Adresse DPO.** La règle générale est l'adresse du client. Exception : un client sans DPO qui a délégué cette partie **par écrit** à Promodev ; c'est alors `dpo@promo.dev`, et le client reste responsable de traitement. Cette délégation ne se présume pas : si le client n'a pas de DPO connu, poser la question au chef de projet avant de rédiger. Les points sur l'adresse DPO sont des **alertes non bloquantes** :
- `dpo@promo.dev` hors cas `PromodevRT`, sans délégation écrite confirmée : le signaler et demander au chef de projet si ce client a délégué par écrit ;
- aucune adresse pour exercer les droits : le signaler ;
- les mentions de l'adresse (section « Droits », section « Sort des données après le décès », bloc « Identité du responsable du traitement ») ne concordent pas : le signaler. Erreur déjà rencontrée : un placeholder « mail dpo du responsable de traitement » resté dans une version `PromodevRT`, où il faut `dpo@promo.dev`.

### R2. Base légale : exécution d'un contrat

La référence est l'exécution du contrat. Deux formulations validées, toutes deux acceptées :
- trame opération : « Les données collectées sont nécessaires au traitement de votre participation à l'opération mise en place. La base légale du service est donc “l'exécution d'un contrat pour traiter votre demande”. »
- trames génériques : « La collecte de vos données étant strictement nécessaire pour traiter votre participation à l'opération mise en place, la base légale du traitement est donc “l'exécution du contrat”. »

- Si l'opération propose une inscription à une newsletter ou un opt-in, ajouter : « et votre consentement en cas d'inscription à la newsletter de [Société Organisatrice] ».
- Ne pas utiliser la phrase « Tant que vous, consommateur, n'avez pas donné votre accord, aucune donnée n'est sauvegardée… ». Elle laisse croire que la base est le consentement et contredit la ligne suivante.
- En vérification : une base « consentement » pour la participation elle-même, ou la phrase ci-dessus, est un **écart à signaler** avec la formulation de référence proposée. Ce n'est pas bloquant : c'est un choix juridique du client, que le chef de projet tranche.

### R3. Données annoncées cohérentes avec la mécanique et le formulaire

La liste « Nature des données traitées » doit correspondre à ce que l'opération collecte vraiment (tableau du §2). En particulier :
- **Données bancaires** annoncées seulement s'il y a un virement (ODR par virement, gain en argent). Jamais pour une Promocard : le remboursement se fait sur la carte, sans IBAN. Pour un jeu, préciser « pour le gagnant d'un virement de [montant] uniquement ».
- **Données de participation** (codes-barres, ticket de caisse, facture) seulement s'il y a une preuve d'achat : pas pour un jeu sans obligation d'achat.
- **Adresse IP** : dans la rédaction v1.8 (§4bis), elle sort de la liste à puces et fait l'objet d'un paragraphe à part, avec sa finalité (prévention et détection de la fraude, sécurisation du dispositif). Dans la trame opération (§4.1), elle reste une puce « Données liées à votre consultation du site ». Les deux sont validées : garder celle du modèle de départ.
- Si un idgame est connu, comparer avec le formulaire Houston (`find_operation`, `list_forms`, `get_form`) : un champ collecté mais non annoncé (téléphone, date de naissance…) ou annoncé mais non collecté est un écart à signaler.

### R4. Durée de conservation

Formule de référence : « Les Données récoltées sont stockées dans la base courante PROMODEV pendant toute la durée de l'opération + [XX] mois ». Formulation v1.8 en deux temps : voir §4bis.
- **XX est choisi par le client** : le demander, ne jamais l'inventer. Les modèles utilisent souvent 12 mois.
- **Données bancaires collectées** → ajouter l'archivage de 10 ans (bloc §4). S'il manque, c'est un écart à signaler.
- **Les 10 ans courent à compter de la date du remboursement**, jamais de la fin de l'opération ni de la date de participation. La phrase exacte à écrire, y compris pour une ODR : « … seront archivées pour une durée de 10 ans **à compter de la date du remboursement** pour des raisons légales ». Ne jamais écrire « archivées pour une durée de 10 ans » sans ce complément : c'est la formulation des anciens modèles, elle est incomplète.
  - Seule adaptation : pour un **jeu** dont le gain est un virement en argent, remplacer « du remboursement » par « du versement du gain » (il n'y a pas de remboursement dans un jeu).
  - Une offre à primes remboursée par virement garde « du remboursement ».
- Une mention « 10 ans » sans point de départ est un écart à signaler : proposer la formulation complète.
- Pas de données bancaires → pas de mention des 10 ans.
- En vérification : une durée absente est un écart à signaler. Une autre formulation choisie par le client (ex. « + 6 mois, puis archivage 1 an pour recours contentieux ») est acceptée, à mentionner dans le récapitulatif, **sauf** si des données bancaires sont collectées sans l'archivage de 10 ans.

### R5. Cookies : selon l'opération

Il n'y a pas de choix par défaut : la réponse vient de la deuxième question du §3.0.
- Aucun cookie → bloc « Absence de cookies » (§4.2 B).
- Cookies ou traceurs (statistiques, pixel…) → charte cookies complète (§4.2 A).
- En vérification : si la politique dit « aucun cookie » alors que le site en dépose, ou l'inverse, c'est un écart à signaler. En cas de doute, demander au chef de projet. Si le navigateur est disponible, on peut regarder le site de l'opération, sans conclure seul.

## 1. Identifier le cas

| Critère | Valeurs |
|---|---|
| Document | `Opération` (politique d'une opération, trame §4) · `TrameGénérique` (modèle à placeholders, §4bis) |
| Acteurs | `PromodevSeul` (client responsable, PROMODEV sous-traitant) · `Agence` (client responsable, agence + PROMODEV sous-traitants) · `PromodevRT` (PROMODEV responsable du traitement — politique générale Promodev, sur indication du chef de projet seulement) |
| Mécanique | `ODR` (offre de remboursement par virement) · `Promocard` (remboursement sur carte de paiement) · `Prime` (offre à primes) · `JeuAvecAchat` · `JeuSansAchat` |
| Version | `Promodev` (rédigée par Promodev) · `Client` (retouchée ou rédigée par le client) |
| Options | Virement / gain en argent (oui/non) · Newsletter ou opt-in (oui/non) · Cookies (oui/non) |

Convention de nommage : `Client_Acteurs_Mécanique_Version.docx` pour une opération (ex. `Marque_PromodevSeul_ODR_Promodev.docx`) ; `Politique de confidentialite - {client | Promodev} responsable de traitement - {AVEC COOKIES | SANS COOKIE}.docx` pour une trame générique.

| Situation | Déroulé |
|---|---|
| Nouvelle politique d'opération | §3.0 les deux questions → §3 brief → §4 trame et blocs → §5 génération Word → §7 contrôles |
| Politique d'un client déjà existante (reconduction) | §3.0, puis partir de la dernière version validée, l'adapter en suivi des modifications, puis contrôles §7 |
| Mise à jour d'une trame générique | Partir des quatre fichiers §4bis, reporter la modification dans **chacun** des fichiers concernés, puis contrôles §7 |
| Le client renvoie une politique retouchée, ou envoie la sienne | §3.0, puis §7 vérification : règles §0, comparaison à la trame, corrections en suivi des modifications et commentaires |
| Le chef de projet demande seulement une relecture | §3.0, puis §7 vérification |

## 2. Ce qui change selon la mécanique et les acteurs

| Élément | ODR | Promocard | Prime | Jeu avec achat | Jeu sans achat |
|---|---|---|---|---|---|
| Finalité | « une offre promotionnelle mise en place » | « une offre promotionnelle mise en place » | « une offre promotionnelle mise en place » | « un jeu promotionnel mis en place » | « un jeu promotionnel mis en place » |
| Identité | Civilité, nom, prénom, adresse postale, e-mail, téléphone (selon formulaire) | Civilité, nom, prénom, adresse postale, e-mail, téléphone, date de naissance (selon formulaire) | Idem ODR, adresse postale pour l'envoi de la prime | Idem ODR (selon formulaire) | Civilité, nom, prénom, e-mail (selon formulaire) |
| Participation | Codes-barres, ticket de caisse, facture | Idem | Idem | Idem | — |
| Bancaires | Oui (virement) | **Non** | Non, sauf virement | Seulement pour un gain en argent (« pour le gagnant d'un virement de [montant] uniquement ») | Seulement pour un gain en argent |
| Conservation | + XX mois, puis archivage bancaire 10 ans **à compter de la date du remboursement** | + XX mois, sans archivage bancaire | + XX mois (si virement : 10 ans à compter de la date du remboursement) | + XX mois (si gain en argent : 10 ans à compter de la date du versement du gain) | + XX mois (si gain en argent : 10 ans à compter de la date du versement du gain) |

**Promocard** (un modèle validé) : même trame que l'ODR, sans la puce « Données bancaires » ni l'archivage de 10 ans. La date de naissance figure dans les données d'identité quand le formulaire la demande. Aucun prestataire de la carte n'est cité dans le modèle : ne pas en ajouter sans demande du chef de projet.

**Prime** : aucun exemple validé pour l'instant. Au premier cas, faire valider par le chef de projet la liste des données avant de finaliser, puis lui proposer d'ajouter la décision à ce skill.

**Avec agence** : l'agence est nommée à cinq endroits (introduction, finalité, anti-fraude, minimisation, destinataires) et les verbes passent au pluriel (« mettent en place », « leur permettent »). Dans la charte cookies complète, « son sous-traitant » devient « ses sous-traitants ».

**Cas `PromodevRT`** : PROMODEV occupe la place du responsable de traitement dans tout le document ; la Société Organisatrice n'apparaît plus que dans les destinataires (« aux personnes habilitées au sein de la Société Organisatrice, notamment son Service Marketing »). Identité légale de PROMODEV : Société par actions simplifiée, capital 321 000 euros, RCS Marseille 890 559 883, siège 276 Avenue du Douard – ZI Les Paluds – Aubagne Cedex, TVA FR28890559883, représentée par Mathieu Margot, Président ; DPO Audrey GILARDI, `dpo@promo.dev`. Reprendre ces mentions du dernier fichier validé plutôt que de les retaper.

## 3.0 Les deux questions systématiques

Avant de rédiger ou de vérifier quoi que ce soit, poser ces deux questions au chef de projet, **ensemble, en un seul message** (AskUserQuestion), même quand le contexte semble évident — elles commandent tout le reste du document :

1. **Qui est le responsable de traitement ?**
   - le client, la Société Organisatrice (cas `PromodevSeul`, ou `Agence` si une agence intervient aussi) ;
   - PROMODEV (cas `PromodevRT`, politique générale Promodev).
   → commande R1, le choix de la trame, l'adresse DPO et le vocabulaire de tout le document.

2. **Y a-t-il des cookies ou des traceurs sur le site de l'opération ?**
   - oui → charte cookies complète (§4.2 A) ;
   - non → bloc « Absence de cookies » (§4.2 B).
   → commande R5. Aucun défaut : ne jamais trancher seul, même si l'ancienne version du client contenait une charte complète.

Y joindre, dans le même message, les questions du brief (§3) encore ouvertes : durée de conservation, newsletter, agence, adresse DPO. Ne pas les saucissonner en plusieurs allers-retours.

Si le chef de projet n'est pas disponible pour répondre (session automatique), retenir « le client est responsable de traitement » et l'état cookies du dernier document validé du même client, puis annoncer ces deux hypothèses en tête de la livraison, comme points à confirmer.

## 3. Rassembler le brief

Récupérer d'abord ce qui existe, puis poser les questions restantes **en une seule fois**, avec celles du §3.0 :

1. **Modalités de l'opération** (fichier fourni, ou via le skill modalites-operation) : elles contiennent en général la raison sociale, la forme, le capital, le siège et le RCS de la Société Organisatrice, ainsi que l'adresse DPO. En cas de divergence avec une ancienne politique (forme sociale, ville du RCS, adresse du siège), **les modalités font foi** : elles sont le document juridique de référence de l'opération. Le signaler dans le récapitulatif.
2. **Houston**, si un idgame ou un lien test.promo.dev est fourni : `find_operation`, `operation_info`, puis le formulaire (`list_forms`, `get_form`) pour la liste exacte des données collectées.
3. **Ancienne politique du client**, si elle existe.

| Information | Remarque |
|---|---|
| Responsable de traitement | Question 1 du §3.0 — toujours posée |
| Cookies | Question 2 du §3.0 — toujours posée |
| Société Organisatrice | Raison sociale exacte, forme, capital, adresse du siège, ville du RCS, numéro RCS. Ne jamais inventer : si l'info manque, laisser `[À COMPLÉTER]` surligné en jaune et le signaler |
| Agence | Nom exact, si cas `Agence` |
| Mécanique | ODR, Promocard, prime, jeu avec ou sans obligation d'achat |
| Données collectées | Depuis le formulaire Houston ou les modalités |
| Virement / gain en argent | Oui/non, montant pour un jeu |
| Newsletter / opt-in | Oui/non |
| Durée de conservation | + XX mois, choisie par le client |
| Archivage bancaire | Automatique dès qu'il y a un virement : 10 ans à compter de la date du remboursement (jeu : du versement du gain). Rien à demander au client |
| Adresse DPO | E-mail ou adresse postale du client (`dpo@promo.dev` seulement en cas de délégation écrite confirmée ou dans le cas `PromodevRT`) |

## 4. Trame de référence (politique d'une opération)

Légende : `{SO}` = raison sociale de la Société Organisatrice ; `{AGENCE}` = nom de l'agence ; `[PromodevSeul | Agence]` = choisir la variante ; `[si …]` = bloc conditionnel. Coquilles des anciens modèles déjà corrigées (§6).

### 4.1 Corps

**POLITIQUE DE CONFIDENTIALITÉ ET COOKIES**

Vous participez à une opération promotionnelle gérée par {SO}[Agence : et son sous-traitant l'agence {AGENCE}]. Cette politique de confidentialité a pour but de vous donner toute la transparence sur les actions qui sont menées sur vos données, et de vous expliquer comment faire valoir vos droits sur celles-ci dans le cadre de la présente opération.

La présente Politique de confidentialité a pour objet de définir les conditions et modalités dans lesquelles sont traitées les Données à caractère personnel que nous allons collecter (ci-après « Données ») dans le cadre de la mise en place de l'opération (ci-après le « Service »).

{SO} veille et s'engage à ce que vos Données soient collectées dans le respect de la loi Informatique et Libertés n° 78-17 du 6 janvier 1978 modifiée (ci-après « Loi Informatique et Libertés »), et du Règlement européen 2016/679 (ci-après « Règlement »).

La présente Politique de confidentialité entre en vigueur à compter du début de l'opération, information que vous pouvez retrouver dans les modalités de l'opération, systématiquement présentes sur le site de l'opération. {SO} se réserve le droit de la modifier à tout moment en fonction des évolutions de la réglementation en matière de protection des données, en publiant une nouvelle version sur le site. Par conséquent, nous vous invitons à visiter régulièrement cette page.

**RESPONSABLE DU TRAITEMENT**

Le traitement est mis en œuvre par {SO}, {forme} au capital de {capital} €, dont le siège social est situé {adresse du siège}, enregistrée au Registre du Commerce et des Sociétés de {ville RCS} sous le numéro {numéro RCS}, en qualité de responsable du traitement.

**FINALITÉ DU TRAITEMENT**

Le traitement a pour finalité de permettre au consommateur de participer à [ODR/Promocard/Prime : une offre promotionnelle mise en place | Jeu : un jeu promotionnel mis en place] par l'éditeur du service, précisé dans les mentions légales.

Le traitement est réalisé sous la responsabilité de {SO}, qui vérifie le traitement et la validation de la participation du consommateur, ainsi que la gestion des primes, remboursements ou gains de points qui peuvent en découler, avec [PromodevSeul : le sous-traitant PROMODEV | Agence : les sous-traitants {AGENCE} et PROMODEV].

Sur certaines opérations, le responsable de traitement peut collecter des informations personnelles dans le but de construire des statistiques lui permettant de mieux vous connaître et vous comprendre. Dans ce cas, les mentions d'information qui apparaîtront obligatoirement avant la collecte des données vous expliqueront qu'un tel traitement aura lieu.

[PromodevSeul] Le responsable de traitement demande à PROMODEV de s'assurer qu'un participant est bien une personne physique, qui effectue une participation légitime telle que détaillée dans les modalités de l'opération. Dans ce contexte, PROMODEV met en place des outils anti-fraude qui lui permettent de contrôler que la participation est conforme afin de ne pas léser les participations légitimes.

[Agence] Le responsable de traitement demande à {AGENCE} et PROMODEV de s'assurer qu'un participant est bien une personne physique, qui effectue une participation légitime telle que détaillée dans les modalités de l'opération. Dans ce contexte, {AGENCE} et PROMODEV mettent en place des outils anti-fraude qui leur permettent de contrôler que la participation est conforme afin de ne pas léser les participations légitimes.

**BASE LÉGALE**

Les données collectées sont nécessaires au traitement de votre participation à l'opération mise en place.

La base légale du service est donc « l'exécution d'un contrat pour traiter votre demande »[si newsletter : et votre consentement en cas d'inscription à la newsletter de {SO}].

**NATURE DES DONNÉES TRAITÉES**

Lors de votre participation sur le Site, certaines Données sont traitées. Il s'agit des Données suivantes :

- Données liées à votre identité : {liste selon le formulaire, ex. Civilité, nom, prénom, adresse postale, adresse email, numéro de téléphone fixe ou mobile, date de naissance}.
- [si preuve d'achat] Données liées à votre participation : code(s)-barres produit(s), ticket de caisse, facture d'achat.
- [si virement] Données bancaires[Jeu : (pour le gagnant d'un virement de {montant} € uniquement)] : votre IBAN, le BIC de votre banque ou votre relevé d'identité bancaire.
- Données liées à votre consultation du site : votre adresse IP.

Les données sont fournies par le consommateur en remplissant un formulaire présent sur le site, et sont nécessaires au traitement de sa participation à l'opération mise en place.

{SO} applique toujours un principe de minimisation des données, ce qui signifie que chaque donnée que nous collectons est nécessaire au traitement que doivent mener {SO} et [PromodevSeul : PROMODEV | Agence : ses sous-traitants {AGENCE} et PROMODEV].

**DURÉE DE CONSERVATION**

Les Données récoltées sont stockées dans la base courante PROMODEV pendant toute la durée de l'opération + {XX} mois[si données bancaires : , puis les données relatives aux transactions bancaires (nom, prénom, IBAN) seront archivées pour une durée de 10 ans à compter de la date du remboursement pour des raisons légales. Ces données ne seront accessibles qu'aux équipes en charge des relations avec l'administration fiscale].

> Le membre de phrase « à compter de la date du remboursement » fait partie du bloc : il s'écrit tel quel pour une ODR et pour une offre à primes remboursée par virement. **Seul cas à adapter** : pour un jeu dont le gain est un virement en argent, remplacer « du remboursement » par « du versement du gain ». Ne jamais supprimer ce membre de phrase (R4).

**DESTINATAIRES DES DONNÉES PERSONNELLES**

[PromodevSeul] Les Données collectées ne sont réservées qu'à l'usage des destinataires suivants : le Service Marketing de la Société Organisatrice, ainsi que les employés et collaborateurs du sous-traitant de la Société Organisatrice (PROMODEV), pour le traitement de tout ou partie des données personnelles dans la limite nécessaire à l'accomplissement de sa prestation.

[Agence] Les Données collectées ne sont réservées qu'à l'usage des destinataires suivants : le Service Marketing de la Société Organisatrice, ainsi que les employés et collaborateurs des sous-traitants de la Société Organisatrice ({AGENCE} et PROMODEV), pour le traitement de tout ou partie des données personnelles dans la limite nécessaire à l'accomplissement de leurs prestations.

**TRANSFERT DES DONNÉES**

Par principe, nous veillons à ce que les Données ne soient pas transférées en dehors de l'Union européenne.

**DROITS SUR VOS DONNÉES PERSONNELLES**

Vous disposez, dans les conditions et limites prévues par la réglementation, d'un droit d'accès, de rectification, de suppression, de portabilité des Données vous concernant et d'opposition ou de limitation à leur traitement. Vous disposez également du droit de définir des directives concernant le sort de vos Données après votre décès dans les conditions définies à l'article 85 de la Loi Informatique et Libertés. Enfin, vous disposez du droit d'introduire une réclamation auprès de l'autorité de contrôle compétente (CNIL).

Pour exercer vos droits, il vous suffit d'écrire à l'adresse {adresse DPO}.

### 4.2 Charte cookies : choisir A ou B (R5)

**A. Cookies ou traceurs présents : charte complète**

**CHARTE D'UTILISATION DES COOKIES**

*Sur quoi porte cette Charte cookies ?* (souligné)

Lors de la consultation de notre site, des cookies (et autres traceurs) sont déposés ou lus sur le terminal que vous utilisez (votre ordinateur, votre mobile ou votre tablette).

Cette charte vous explique quels types de cookies le responsable de traitement et [son sous-traitant | ses sous-traitants] utilisent et à quelles fins.

Nous vous expliquons aussi quels sont vos droits concernant ces cookies et comment vous pouvez les exercer.

Cette charte vous donne des informations complémentaires à celles que vous retrouvez au niveau du bandeau cookies que vous visualisez lorsque vous naviguez sur notre site.

Cette Charte relative aux cookies est rédigée conformément à la loi n° 78-17 du 6 janvier 1978 (dite « Loi Informatique et Libertés » ou « LIL ») et au Règlement Général sur la Protection des Données (« RGPD ») n° 2016/679.

*Qu'est-ce qu'un cookie et à quoi sert-il ?* (souligné)

Le cookie est un traceur. Lorsqu'un internaute navigue sur un site internet, il permet de collecter des informations personnelles à son sujet.

Lorsque l'internaute utilise son ordinateur, les cookies sont gérés par son navigateur internet (Firefox, Safari, Google Chrome, Microsoft Edge…).

Il existe d'autres types de traceurs, en plus des cookies (ex. : pixel invisible, fingerprinting, local storage).

Certains cookies sont internes au site internet, d'autres sont des cookies tiers placés sur le site par des sociétés tierces.

Par simplicité, le responsable de traitement et [son sous-traitant | ses sous-traitants] utiliseront dans cette charte le terme « cookies » pour viser différents types de traceurs.

Un cookie peut collecter différentes données personnelles à votre sujet, par exemple l'adresse IP de votre ordinateur, le navigateur utilisé, la date et l'heure de connexion, les pages visitées sur le site, etc.

Quels sont les types de cookies que le responsable de traitement et [son sous-traitant | ses sous-traitants] utilisent sur ce site internet ?

Les types de cookies utilisés sur le site internet sont les suivants :

1) Des cookies permettant d'évaluer le trafic du site et de développer des ressources pour améliorer les performances. Ils retracent votre parcours sur notre site et nous informent des contenus qui vous intéressent le plus. Grâce à eux, nous sommes en mesure de vous proposer un contenu plus pertinent et de suivre l'évolution de notre plateforme. {Adapter la liste aux cookies réellement déposés.}

Quels sont vos droits en matière de cookies ?

Conformément à l'article 82 de la Loi Informatique et Libertés du 6 janvier 1978, l'internaute est informé des traitements de données personnelles réalisés par le biais de cookies. La présente charte permet de remplir cette obligation d'information.

Par ailleurs, si le responsable de traitement et [son sous-traitant | ses sous-traitants] utilisent des cookies nécessitant le consentement de l'internaute, le recueil du consentement se fait lors de l'apparition d'un bandeau cookies visible sur le site internet.

Tant que l'internaute n'a pas été informé et n'a pas donné son consentement exprès, ce type de cookies n'est pas déposé ou lu sur son terminal.

Le consentement est demandé pour chaque type de cookie (par finalité).

L'utilisateur a la possibilité de retarder son choix et de se décider plus tard. Tant que son consentement n'est pas donné, aucun cookie n'est déposé.

L'utilisateur a la possibilité de refuser le dépôt de ces cookies.

Il lui est possible de retirer son consentement à tout moment et aussi facilement qu'il l'a donné. Les cookies déposés ont une durée de vie maximale de 13 mois. À l'issue de cette durée, le consentement est à nouveau demandé.

Si l'internaute souhaite supprimer les cookies enregistrés sur son terminal et paramétrer son navigateur pour refuser les cookies, il peut le faire via les préférences de son navigateur internet. Ces options se trouvent habituellement dans les menus « Options », « Préférences » ou « Outils » du navigateur.

Pour en savoir plus sur les règles applicables en matière de cookies, l'internaute peut consulter les liens suivants :

https://www.cnil.fr/fr/cookies-et-autres-traceurs-la-cnil-publie-de-nouvelles-lignes-directrices

https://www.legifrance.gouv.fr/affichTexte.do?cidTexte=JORFTEXT000038783337

**B. Aucun cookie**

**CHARTE D'UTILISATION DES COOKIES**

*Absence de cookies* (souligné)

Le site sur lequel vous participez n'installe aucun cookie sur votre appareil. Aucun fichier de suivi, ni technologie similaire, n'est utilisé pour analyser votre navigation, personnaliser votre expérience ou diffuser des contenus publicitaires ciblés. Contrairement à de nombreux sites qui requièrent l'installation de cookies pour fonctionner ou collecter des données utilisateur, ce site fonctionne sans aucun traceur, qu'il soit essentiel, fonctionnel, analytique ou tiers. Ainsi, aucune information n'est enregistrée sur votre appareil à votre insu. Vous n'avez pas besoin de consentir à l'utilisation de cookies ni d'effectuer de paramétrage particulier pour limiter le suivi, puisque celui-ci est inexistant.

### 4.3 Fin de document (dans les deux cas)

Sort des données à caractère personnel après le décès - Droit d'accès, de rectification, de suppression et de portabilité des données :

La personne concernée par un traitement peut définir des directives relatives à la conservation, à l'effacement et à la communication de ses données personnelles après son décès. Ces directives peuvent être générales ou particulières.

La personne concernée par un traitement bénéficie également d'un droit d'accès, d'opposition, de rectification, de suppression et, à certaines conditions, de portabilité de ses données personnelles. La personne concernée a le droit de retirer son consentement à tout moment si le consentement constitue la base légale du traitement.

La demande devra indiquer les nom et prénom, adresse e-mail ou postale de la personne concernée, et être signée et accompagnée d'un justificatif d'identité en cours de validité. Elle peut exercer ces droits en s'adressant au propriétaire du site, {SO en majuscules}, par e-mail à : {adresse DPO}, en indiquant ses nom, prénom, e-mail, adresse et si possible sa référence client.

La personne concernée par un traitement a le droit d'introduire une réclamation auprès de l'autorité de contrôle (CNIL) : https://www.cnil.fr/fr/webform/adresser-une-plainte

## 4bis. Trames génériques (blocs v1.8, septembre 2026)

Quatre fichiers, deux par cas d'acteurs, qui ne diffèrent entre eux que par la charte cookies :

| Fichier | Responsable de traitement | Cookies |
|---|---|---|
| `Politique de confidentialite - client responsable de traitement - AVEC COOKIES.docx` | le client | charte complète |
| `Politique de confidentialite - client responsable de traitement - SANS COOKIE.docx` | le client | absence de cookies |
| `Politiques de confidentialité Promodev responsable de traitement - AVEC COOKIES.docx` | PROMODEV | charte complète |
| `Politiques de confidentialité Promodev responsable de traitement - SANS COOKIE.docx` | PROMODEV | absence de cookies |

Les deux questions du §3.0 désignent directement la ligne à prendre dans ce tableau.

Règles propres à ces trames :
- **Placeholders en clair**, sans surlignage : `[responsable de traitement]`, « forme juridique », « adresse », « RCS de Ville », « 000000000 », « mail dpo du responsable de traitement », « xxxxxx ». Le surlignage jaune `[À COMPLÉTER]` est réservé aux politiques d'opération, où l'information manque vraiment.
- **Pas de sous-titre d'opération** sous le titre : le document commence directement par « POLITIQUE DE CONFIDENTIALITÉ ET COOKIES ».
- La version `PromodevRT` porte une **ligne de version** sous le titre : « Version 1.8 du 22.09.2026 ». L'incrémenter à chaque modification validée par Audrey.
- Le cas client ajoute une section **SOUS TRAITANT** après le responsable du traitement, et un paragraphe sur la transmission aux autorités à la fin des destinataires — deux éléments absents de la version `PromodevRT`.
- Une modification de fond se reporte dans **les quatre fichiers**.

### Blocs réécrits en v1.8

Ces blocs remplacent leurs équivalents du §4.1 dans les trames génériques. Pour une politique d'opération déjà validée par un client, ne les porter que si le chef de projet le demande. `{RT}` = `[responsable de traitement]` ou PROMODEV selon le cas.

**NATURE DES DONNEES TRAITEES**

Dans le cadre de votre participation sur le Site, les données personnelles demandées dans le formulaire sont obligatoires et nécessaires au traitement de votre participation à l'opération. Les données traitées sont les suivantes :

- Données liées à votre identité et vos coordonnées : nom, prénom, adresse postale, adresse email[selon le formulaire : , numéro de téléphone fixe ou mobile, (date de naissance : base légale « intérêt légitime »)].
- Données liées à votre participation : code(s)-barres du ou des produit(s), ticket de caisse et/ou facture d'achat.
- Données bancaires : IBAN, BIC de votre banque et/ou relevé d'identité bancaire, lorsque ces informations sont nécessaires au remboursement.

Ces données sont directement fournies par le consommateur lors de la saisie du formulaire de participation.

Par ailleurs, l'adresse IP est collectée automatiquement lors de votre participation sur le Site. Cette donnée technique est utilisée à des fins de prévention et de détection de la fraude ainsi que de sécurisation du dispositif.

{RT} applique le principe de minimisation des données, conformément à la réglementation applicable en matière de protection des données personnelles. À ce titre, seules les données nécessaires à la gestion de votre participation, à son remboursement et à la sécurisation du dispositif sont collectées et traitées.

**DURÉE DE CONSERVATION**

Les Données collectées sont conservées dans [PromodevRT : la base active de PROMODEV | client : notre base active] pendant toute la durée de l'opération, puis pendant une durée de {XX} mois à compter de sa clôture.

À l'issue de cette période, les Données qui ne sont plus nécessaires sont supprimées. Les données relatives aux remboursements effectués (nom, prénom, IBAN, montant et date du remboursement) sont toutefois conservées sous forme archivée pendant une durée de 10 ans à compter de la date du remboursement, afin de répondre aux obligations légales applicables et de permettre la justification des transactions réalisées.

**DESTINATAIRES DES DONNÉES PERSONNELLES**

Les Données personnelles collectées sont accessibles uniquement aux personnes habilitées à en connaître dans le cadre de leurs fonctions, et dans la stricte limite de ce qui est nécessaire à l'accomplissement de leurs missions.

Elles peuvent ainsi être accessibles :

- aux personnes habilitées au sein de [PromodevRT : la Société Organisatrice | client : {RT}], notamment son Service Marketing ;
- au sein de PROMODEV[client : et, le cas échéant, des autres sous-traitants de {RT}], agissant en qualité de sous-traitant, exclusivement aux équipes en charge du traitement des participations et du support aux consommateurs, ainsi qu'aux personnes habilitées intervenant dans le cadre de la gestion et de la sécurisation de l'opération.

Les accès aux Données sont limités en fonction des habilitations attribuées et des besoins liés aux missions de chaque utilisateur.

[client, à conserver en fin de section] Nous pouvons aussi être amenés à transmettre vos informations aux autorités locales dans le cadre d'une obligation légale ou sur demande d'une autorité administrative habilitée à faire ce type de demande.

**SECURITE DES DONNEES A CARACTERE PERSONNEL**

[PromodevRT : PROMODEV met en œuvre toutes les mesures techniques et organisationnelles appropriées | client : {RT} veille, avec ses sous traitants, à la mise en œuvre de toutes les mesures techniques et organisationnelles appropriées] afin de garantir un niveau de sécurité adapté aux risques, et notamment pour protéger les Données à caractère personnel contre toute destruction, perte, altération, divulgation non autorisée ou accès non autorisé, de manière accidentelle ou illicite.

Ces mesures comprennent notamment, sans s'y limiter :

- des dispositifs de contrôle des accès aux Données, strictement limités aux personnes habilitées et dans le cadre de leurs missions ;
- des mesures de protection des Données lors de leur transmission et de leur stockage, incluant des mécanismes de chiffrement ;
- des procédures de sauvegarde et de restauration permettant d'assurer la disponibilité et l'intégrité des Données en cas d'incident ;
- une journalisation des accès et des actions réalisées sur les systèmes traitant des Données ;
- une gouvernance dédiée à la sécurité des systèmes d'information, associant des procédures internes, des contrôles réguliers et des actions de sensibilisation des équipes.

[PromodevRT : PROMODEV veille | client : {RT} et ses sous traitants veillent] à ce que ces mesures soient régulièrement réévaluées et adaptées, en tenant compte de l'évolution des risques, des technologies et des exigences réglementaires applicables.

[PromodevRT uniquement] Des informations complémentaires relatives aux mesures de sécurité mises en œuvre peuvent être communiquées, le cas échéant, dans un cadre contractuel, aux partenaires ou clients de PROMODEV. — Cette phrase n'a pas de sens quand le client est responsable de traitement : la supprimer dans les trames client.

### Bloc « Identité du responsable du traitement »

La société {RT}

Forme juridique, au capital de {capital} euros

Immatriculée au Registre du Commerce et des Sociétés de {ville} sous le numéro {numéro RCS},

Ayant son siège social : {adresse}

Numéro intracommunautaire : {TVA}

Représentée par {prénom nom}, agissant en qualité de {qualité}.

Coordonnées de la personne en charge de la politique d'utilisation des données personnelles.

{prénom nom} – Délégué(e) à la Protection des Données

Adresse électronique : {adresse DPO}

**Où le placer.** Avec cookies : à l'intérieur de la charte, juste après le paragraphe « Cette Charte relative aux Cookies est rédigée conformément… ». Sans cookies : il sort de la charte, soit en section autonome juste avant elle (modèle client), soit tout à la fin du document après le lien CNIL (modèle Promodev). Les deux placements sont validés : garder celui du fichier de départ plutôt que d'en imposer un.

## 5. Générer le Word

Lire le skill **docx** avant de générer. Mise en forme des modèles Promodev :
- A4, marges de 2,5 cm (1417 DXA), police **Calibri**, corps en 12 pt, alignement à gauche ;
- titre en majuscules, gras, 16 pt, centré ;
- titres de section en majuscules, **gras et soulignés**, avec une ligne vide avant ;
- sous-titres de la charte cookies (« Sur quoi porte… », « Qu'est-ce qu'un cookie… », « Absence de cookies », « Identité du responsable du traitement ») soulignés ;
- listes à puces « ● » (numérotation Word, jamais de puce tapée) ;
- adresses e-mail et URL en liens cliquables ;
- infos manquantes : `[À COMPLÉTER]` surligné en jaune (politiques d'opération seulement — voir §4bis pour les trames).

Nom du fichier : `{Client}_{Acteurs}_{Mécanique}_Promodev.docx`, avec V1, V2… si le chef de projet le demande ; pour une trame générique, le nom du §4bis. Enregistrer dans le dossier connecté s'il y en a un, sinon dans les sorties de la session.

Après génération : convertir en PDF, regarder chaque page, puis faire les contrôles §7 sur le texte généré. En particulier, relire la section « Durée de conservation » : si des données bancaires sont collectées, la phrase doit contenir « à compter de la date du remboursement » (jeu : « du versement du gain »). C'est l'oubli le plus fréquent en génération.

Quand plusieurs variantes d'un même document sont demandées (avec / sans cookies), générer depuis **le même script**, en ne changeant que le bloc concerné, puis vérifier par `diff` que rien d'autre n'a bougé.

## 6. Variantes et coquilles des anciens modèles

À corriger en rédaction, et à signaler en vérification comme **remarques non bloquantes**, regroupées en fin de récapitulatif. Quand le chef de projet demande que deux versions restent strictement alignées, ne pas corriger : signaler seulement.

| Ancien texte | Correction |
|---|---|
| « vous expliquerons » | « vous expliqueront » |
| « PROMODEV mets en place » | « met en place » |
| « qui lui permette » | « qui lui permettent » / « leur permettent » (agence) |
| « systématiquement présent sur le site » | « présentes » |
| « le responsable de traitement et sous-utilisent » | « et son sous-traitant utilisent » |
| « sous la responsabilité {Client}… » | « sous la responsabilité de {Client}… » |
| « chaque donnée que nous collectons sont nécessaires » | « est nécessaire » |
| « les pages visités » | « visitées » |
| « nous, la société X, collecter » / « nous, la société X, vous invitons » | « nous allons collecter » / « nous vous invitons » |
| « tel que détaillé » (participation) | « telle que détaillée » |
| « consentement express » | « exprès » |
| « Commission National » | « Commission Nationale » |
| « en indiquant, au sous-traitant PROMODEV de la société X, vos nom… » | « en indiquant ses nom… » (§4.3) |
| « article 40.1 de la Loi Informatique et Libertés » | article 85 (numérotation en vigueur depuis 2019) : à signaler, sans bloquer |
| Durée de vie des cookies « 14 mois » | 13 mois maximum selon les recommandations CNIL : à signaler, sans bloquer |
| Sans données bancaires (Promocard, jeu sans gain en argent) : phrase « Ces données ne seront accessibles qu'aux équipes en charge des relations avec l'administration fiscale » restée seule après la durée | Supprimer : elle n'a de sens qu'avec l'archivage bancaire de 10 ans |
| « archivées pour une durée de 10 ans pour des raisons légales » (sans point de départ) — formulation de tous les anciens modèles | « archivées pour une durée de 10 ans **à compter de la date du remboursement** pour des raisons légales » (jeu : « du versement du gain ») |
| 10 ans « à compter de la fin de l'opération », « à compter de la participation », « à compter de la collecte » | Point de départ faux : c'est la date du remboursement (jeu : du versement du gain) |
| « mail dpo du responsable de traitement » dans un document `PromodevRT` | Placeholder de la trame client resté à la copie : mettre `dpo@promo.dev` |
| Forme sociale, ville du RCS ou siège différents de ceux des modalités | Les modalités font foi : aligner la politique et le signaler |
| « Internet Explorer », « cookie flash » | Navigateurs et technologies obsolètes : proposer la mise à jour |

Variantes rencontrées chez des clients, **acceptées** si R1 à R5 sont respectées (les mentionner dans le récapitulatif, sans les corriger) :
- titre « Politique de protection des données et cookies » ;
- finalité et base légale fusionnées dans une même section ;
- droits présentés en liste à puces ;
- paragraphe « statistiques » supprimé ;
- anti-fraude déplacé dans la section « Destinataires » ;
- PROMODEV présenté comme « partenaire » qui met à disposition l'opération, s'il est bien nommé parmi les sous-traitants des destinataires ;
- adresse DPO postale (y compris à l'étranger, ex. chez la maison mère) en plus de l'e-mail ;
- rédaction à la première personne (« nous utilisons ») dans la charte cookies.

Exemples de versions conformes : client responsable du traitement, PROMODEV sous-traitant, e-mail DPO + adresse postale, absence de cookies ; client SAS avec RCS, e-mail DPO, ODR par virement.

## 7. Vérifier une politique

1. **Extraire le texte** : `pandoc -t plain --wrap=none fichier.docx`. Pour un PDF, extraire le texte et relire les pages en image si le texte sort abîmé (ligatures « ti », « tt » perdues).
2. **Identifier le cas** (§1) à partir des réponses du §3.0 : document, acteurs, mécanique, virement, newsletter, cookies. Si la politique ne permet pas de trancher (ex. jeu ou ODR), demander.
3. **Si une autre version du même document est fournie** (même début de nom de fichier, ou variante avec / sans cookies), comparer paragraphe par paragraphe (`diff` sur les textes extraits) et lister chaque écart : ce sont soit des changements voulus, soit des oublis de report.
4. **Contrôler, dans cet ordre** :
   - R1 rôles et adresse DPO (y compris la cohérence de toutes les mentions de l'adresse) ;
   - R2 base légale ;
   - R3 données annoncées vs mécanique et formulaire Houston ;
   - R4 durée de conservation, archivage bancaire et son point de départ. Contrôle littéral : chercher « 10 ans » dans le texte et vérifier que la phrase contient « à compter de la date du remboursement » (jeu : « du versement du gain »). Absent ou autre point de départ = écart à signaler ;
   - R5 cookies ;
   - cohérence du nom du responsable de traitement partout (raison sociale identique dans l'introduction, le responsable du traitement, le bloc identité et la fin de document ; pas de nom d'un autre client resté d'un ancien modèle) ;
   - trames génériques : aucun placeholder de l'autre cas resté en place (`[responsable de traitement]` dans un document Promodev, `dpo@promo.dev` dans une trame client) ;
   - avec agence : agence nommée aux cinq endroits du §2 ;
   - jeu : finalité « jeu promotionnel » et non « offre promotionnelle » (écart fréquent dans les modèles Agence) ;
   - identité légale complète (forme, capital, siège, RCS) et conforme aux modalités ;
   - coquilles du §6.
5. **Classer chaque point** :
   - **Bloquant** : R1 rôles. Le document n'est pas présenté comme prêt à valider.
   - **Écart à signaler** : R2 à R5, cohérence des noms, identité légale incomplète. Le chef de projet décide.
   - **Remarque** : coquilles, formulations obsolètes.
6. **Livrer** :
   - le Word du client, avec les corrections en **suivi des modifications** (auteur `Promodev`) et un **commentaire** par correction qui explique la règle (voir le skill docx : suivi des modifications et `comment.py`) ;
   - un message court, qui commence par les points bloquants, puis les écarts, puis un résumé des remarques et des variantes client acceptées.

Ne pas trancher seul un point juridique nouveau (base légale inhabituelle, transfert hors UE annoncé, données sensibles collectées) : le signaler au chef de projet.