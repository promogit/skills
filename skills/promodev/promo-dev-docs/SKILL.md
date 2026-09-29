---
name: promo-dev-docs
description: "Gabarit officiel et charte PROMO.DEV pour tout document écrit au nom de la société PROMO.DEV (promo.dev, SAS à Aubagne — infrastructure des versements aux clients) : lettre, courrier, mémo, note interne, proposition commerciale, devis, réponse à appel d'offres, rapport, compte rendu. Utiliser ce skill dès qu'un document doit être produit au nom de PROMO.DEV ou envoyé à un client/prospect/partenaire de PROMO.DEV, même si l'utilisateur ne mentionne ni gabarit, ni charte, ni modèle — le simple fait d'écrire un document pour cette société suffit. Contient l'en-tête et le pied de page officiels (mentions légales), la bibliothèque de blocs, les règles de ton et le contexte société vérifié. Use this skill whenever writing or formatting any document on behalf of PROMO.DEV."
---

# Documents PROMO.DEV

Produire des documents au nom de PROMO.DEV qui sont fidèles à la charte de la société : même cadre, mêmes couleurs, même ton, mentions légales exactes. Le livrable par défaut est un fichier **.docx**.

## Marche à suivre

1. **Rédiger le contenu d'abord.** Rassembler les faits (demande de l'utilisateur, fichiers fournis, `references/contexte-societe.md`). Écrire le texte du document avant de penser à la mise en forme.
2. **Choisir les blocs.** Assembler le document à partir de la bibliothèque de blocs (ci-dessous). Ne pas inventer d'autres motifs visuels.
3. **Générer le .docx.** Lire le SKILL.md du skill `docx` (pièges docx-js) puis `references/docx-recipes.md` (traduction exacte de la charte en docx-js : tailles, couleurs, en-tête, pied de page, recette de chaque bloc).
4. **Vérifier visuellement.** Rendre le document en images et le regarder page par page avant de le livrer (commandes dans le skill `docx`).

Cas particulier : si l'utilisateur demande explicitement le format doc-page/HTML (par exemple pour claude.ai), partir de `assets/template-doc-page.html` — c'est le gabarit d'origine, à dupliquer et remplir sans toucher aux styles.

## Le cadre — jamais modifié

L'en-tête, le pied de page et les mentions légales sont identiques sur tous les documents et sur toutes les pages. C'est ce qui rend un document PROMO.DEV reconnaissable et légalement conforme ; aucune demande de contenu ne justifie de les changer.

- **En-tête** : mot-symbole PROMO.DEV à gauche (Red Hat Display), sur-titre du document à droite (type de document en capitales ambre, ex. « PROPOSITION COMMERCIALE »), filet dessous.
- **Pied de page** : SAS PROMO.DEV · 276 avenue du Douard, 13400 Aubagne, France · https://promo.dev · SIREN 890 559 883 · SIRET 890 559 883 00024 · TVA FR28890559883 · NAF 7311Z. Filet dessus.

## Règles de forme

- **Typographie** : deux polices, jamais plus. **Red Hat Display** pour tout ce qui structure et attire l'œil : mot-symbole PROMO.DEV, titre du document, titres de section et sous-titres, sur-titres (eyebrows), grands chiffres clés. **Open Sans** pour tout ce qui se lit : corps, tables, légendes, pied de page.
- **Couleurs** : bleu nuit `#00113D` pour les titres, ambre `#D97706` pour les accents et les chiffres, noir en opacité pour le corps. Rien d'autre — pas de vert, pas de rouge, pas de dégradé.
- **Corps** : ~11 pt, interligne 1,7, paragraphes courts.
- **Sur-titres (eyebrows)** : capitales, petits, interlettrés, ambre. Séparateur : point médian (·).
- **Filets et cadres** : 1 px en noir 10 %, angles arrondis discrets. Aucune ombre.
- **Aucun emoji, aucune icône décorative.**

## Règles de rédaction

- Un document = un objet. Si deux objets, deux documents (le signaler à l'utilisateur).
- Titre de niveau 1 en tête, puis un chapô de deux phrases maximum.
- Titres en minuscules de phrase, terminés par un point. (« Ce que change le temps réel. », pas « Ce Que Change Le Temps Réel »)
- **Un titre de section se suffit à lui-même** : il est numéroté (« 2. Ce que change le temps réel. ») et rien ne le surplombe — pas de sur-titre ambre, pas de rubrique au-dessus. Un titre annoncé par une autre ligne se lit comme deux titres empilés ; le numéro fait déjà le travail de repérage.
- **Une lettre ne se découpe pas en sections numérotées.** Un courrier se lit d'un trait : objet, corps en quelques paragraphes, formule de politesse, signature. Les titres numérotés sont pour les documents qu'on parcourt — proposition, rapport, mémo. Une lettre de relance qui tient sur une page vaut mieux qu'une lettre structurée qui déborde sur deux.
- Un titre qui passe sur deux lignes doit rester serré : l'interligne large du corps ne s'applique jamais aux titres (valeurs dans `references/docx-recipes.md`).
- Phrases courtes. Une idée par phrase. Le premier mot porte le sens.
- Chiffres : toujours sourcés et datés. Aucun ordre de grandeur inventé — si l'utilisateur ne fournit pas le chiffre, laisser un emplacement `[…]` visible et le signaler, plutôt que d'inventer. C'est la règle la plus importante du skill : un chiffre inventé dans un document commercial engage la société.
- Vocabulaire maison : pipeline, moteur, temps réel, décision, versement, bénéficiaire, éligibilité, multi-canal, bout en bout.
- Interdits : « transformer votre activité », « leader du marché », « propulsé par l'IA », superlatifs sans chiffre, formules creuses.
- Contexte société : ne citer que les faits de `references/contexte-societe.md`. Noms de clients et partenaires uniquement si l'accord de référencement est confirmé.

## Bibliothèque de blocs

Assembler le document en choisissant les blocs adaptés au type de document — ce sont des structures à remplir, pas des exemples à recopier. Mise en œuvre exacte dans `references/docx-recipes.md`.

| Bloc | Usage | Quand |
|---|---|---|
| A — Destinataire | Adresse, date « Aubagne, le … », objet, référence | Lettres et courriers |
| B — Titre de section | Titre numéroté + paragraphe | Tout document structuré |
| C — Chiffres clés | 3 grands chiffres ambre avec légende sourcée | Propositions, rapports |
| D — Encadré sombre | Une affirmation vérifiable sur fond bleu nuit — **une seule fois par document** | Mise en avant principale |
| E — Avant / après | Table comparant la situation sans et avec PROMO.DEV | Propositions, études de cas |
| F — Étapes numérotées | 01 · 02 · 03, canoniquement Collecter · Décider · Agir | Présentation du pipeline |
| G — Citation | Une phrase attribuée, filet ambre à gauche | Témoignage client |
| H — Prochaines étapes | Liste numérotée [Action] — [responsable], [échéance] | Fin de proposition, compte rendu |
| I — Signature | Formule de politesse française + nom, fonction, coordonnées | Lettres, propositions |

Compositions types : **lettre** = A + corps en prose continue, sans titres de section + I · **proposition commerciale** = chapô + B + C ou E + F + D + H + I · **mémo interne** = chapô + B (+ H) · **rapport** = chapô + B répété + C/E + H.

## Ce qu'il faut demander à l'utilisateur s'il ne l'a pas dit

Le destinataire et le signataire (nom, fonction) ; les chiffres réels à mettre en avant ; si un client peut être nommé. Ne jamais combler ces trous par des valeurs plausibles.
