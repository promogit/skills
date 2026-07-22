---
name: postgre-survival
description: Diagnostiquer et sécuriser les schémas, requêtes, index, transactions, migrations, pools de connexions, autovacuum, bloat, partitionnement et files de tâches PostgreSQL. Utiliser ce skill pour auditer une requête lente, préparer un changement sans interruption, traiter un incident de performance ou proposer un plan de montée en charge PostgreSQL.
---

# PostgreSQL Survival

Fonder chaque conseil sur le workload, les métriques et la version de PostgreSQL. Transformer les heuristiques de l’article source en hypothèses à vérifier, jamais en recettes universelles.

## Charger le playbook

Lire [references/postgres-survival-playbook.md](references/postgres-survival-playbook.md) dès que la demande touche aux plans d’exécution, aux index, aux verrous, aux migrations, aux connexions, à autovacuum, au bloat, au partitionnement ou aux écritures en volume. Utiliser ses requêtes comme points de départ et les adapter aux noms, droits et versions réels.

## Cadrer la demande

1. Identifier l’objectif : expliquer, auditer, diagnostiquer un incident, préparer une migration ou modifier du SQL.
2. Relever la version majeure, le fournisseur, l’environnement, les réplicas, les extensions disponibles et les droits du rôle.
3. Relever le profil de charge : lectures et écritures par seconde, tailles des tables et index, taux de modification, cardinalités, latence attendue et fenêtres de maintenance.
4. Demander seulement les faits manquants qui changent la sécurité ou la solution. Sinon, avancer avec des hypothèses explicites.
5. Séparer les observations en lecture seule des commandes qui écrivent, verrouillent, réécrivent ou suppriment des données.

## Diagnostiquer avant de prescrire

1. Examiner ensemble la requête, ses paramètres représentatifs, le schéma, les contraintes, les index, les volumes et le plan.
2. Commencer par `EXPLAIN` sans `ANALYZE`. N’utiliser `EXPLAIN ANALYZE` qu’après avoir établi que l’exécution réelle est sûre et autorisée.
3. Comparer estimations et lignes réelles, puis vérifier la fraîcheur des statistiques avant de conclure que le planner se trompe.
4. Accepter un scan séquentiel lorsqu’il lit une grande part d’une petite table ou coûte moins que les accès aléatoires d’un index.
5. Rechercher les causes qui produisent le même symptôme : attente de verrou, transaction longue, saturation du pool, pression CPU ou I/O, statistiques périmées, autovacuum en retard et bloat.
6. Mesurer avant et après avec le même workload, des paramètres comparables et une période assez longue pour éviter un résultat dû au cache.

## Appliquer les principes

- Concevoir les schémas à partir des accès réels. Utiliser des clés primaires, `timestamptz` pour les instants et des contraintes qui protègent les invariants.
- Choisir les index à partir des filtres, jointures, tris et cardinalités. Inclure leur coût en écriture, stockage et maintenance.
- Garder les transactions courtes, verrouiller le minimum de lignes et sortir les appels réseau de la transaction.
- Préférer les migrations additives de type expand/contract. Évaluer le verrou de chaque DDL sur la version cible.
- Réutiliser un nombre borné de connexions. Ajuster le pool à la capacité mesurée du serveur et à la somme de toutes les instances applicatives.
- Regrouper les écritures pour amortir les allers-retours, avec des lots bornés et mesurés.
- Laisser autovacuum actif. Régler les tables à fort churn à partir de leur rythme de création de tuples morts et de la capacité de nettoyage.
- Réserver `FOR UPDATE SKIP LOCKED` aux consommateurs de files ou aux traitements indépendants qui acceptent une vue incohérente.
- Partitionner lorsque la clé permet l’élagage, la rétention ou une maintenance réellement plus simple. Chiffrer aussi le coût de planification et d’exploitation.
- Migrer une très grande table avec un backfill idempotent par lots et une capture des écritures concurrentes, puis valider avant la bascule.

## Respecter les garde-fous

- Ne jamais exécuter de SQL mutatif ou de maintenance sur une base réelle sans demande explicite et cible confirmée.
- Ne pas présenter `CREATE INDEX CONCURRENTLY` comme sans risque : vérifier l’absence de bloc transactionnel, les attentes possibles, le surcoût et les index invalides laissés après un échec.
- Ne pas désactiver autovacuum pour résoudre un incident. Ne pas proposer `VACUUM FULL` sans expliquer son verrou exclusif et la réécriture de la table.
- Ne pas déduire qu’un index est inutile à partir d’un compteur seul. Vérifier la date de remise à zéro des statistiques, les requêtes rares et les contraintes qu’il porte.
- Ne pas envoyer un plan vers un service externe avant d’avoir retiré les littéraux, identifiants ou données sensibles.
- Vérifier la documentation officielle de la version cible pour toute syntaxe ou tout comportement de verrou dépendant de la version.

## Livrer une réponse exploitable

Présenter, dans cet ordre :

1. Le diagnostic principal et son niveau de confiance.
2. Les preuves observées et les informations encore manquantes.
3. Les actions classées par urgence, impact attendu et risque.
4. Le SQL proposé, avec son caractère lecture seule ou mutatif, les verrous attendus et sa compatibilité transactionnelle.
5. La méthode de validation, les seuils d’arrêt et le retour arrière.

Éviter les valeurs magiques. Quand une valeur initiale est nécessaire, la présenter comme point de départ à mesurer, pas comme une vérité PostgreSQL.
