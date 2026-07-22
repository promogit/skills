# Playbook PostgreSQL de survie

## Sommaire

- [Source et portée](#source-et-portée)
- [Informations à obtenir](#informations-à-obtenir)
- [Schéma et couche ORM](#schéma-et-couche-orm)
- [Lectures, jointures et index](#lectures-jointures-et-index)
- [Écritures et transactions](#écritures-et-transactions)
- [Migrations de schéma](#migrations-de-schéma)
- [Connexions](#connexions)
- [Planner et plans d’exécution](#planner-et-plans-dexécution)
- [Écritures en volume](#écritures-en-volume)
- [Autovacuum, XID et bloat](#autovacuum-xid-et-bloat)
- [`FOR UPDATE SKIP LOCKED`](#for-update-skip-locked)
- [Partitionnement](#partitionnement)
- [Migration d’une très grande table](#migration-dune-très-grande-table)
- [Requêtes de diagnostic](#requêtes-de-diagnostic)
- [Format d’une recommandation](#format-dune-recommandation)
- [Références](#références)

## Source et portée

Ce playbook constitue une synthèse indépendante de l’article [« The startup’s Postgres survival guide »](https://hatchet.run/blog/postgres-survival-guide), publié par Alexander Belanger le 22 juillet 2026. Il reprend ses retours d’expérience sur les schémas, les requêtes, les connexions, le planner, autovacuum, le partitionnement et les migrations massives.

Traiter les ordres de grandeur de l’article comme des observations propres à Hatchet. Vérifier chaque décision avec le workload réel et la documentation de la version PostgreSQL cible. En cas de conflit, préserver les données et suivre la documentation officielle.

## Informations à obtenir

Recueillir les éléments qui changent le diagnostic :

- Version exacte de PostgreSQL, fournisseur managé, topologie primaire/réplicas et extensions autorisées.
- Environnement, rôle utilisé, droits disponibles et possibilité de reproduire sur une base représentative.
- Schéma, contraintes, index, requête exacte et paramètres représentatifs.
- Taille des relations, cardinalités, distribution des valeurs et taux de création, modification et suppression.
- Débit, concurrence, latences usuelles et dégradées, timeouts, erreurs et objectif de service.
- Configuration des pools, nombre d’instances applicatives et limite totale de connexions.
- État d’autovacuum, âge des transactions, attentes de verrous, consommation CPU, I/O, mémoire, stockage et WAL.
- Fenêtre de maintenance, sauvegarde testée, procédure de retour arrière et capacité d’interrompre une opération.

Ne pas attendre tous ces éléments pour commencer. Émettre un diagnostic provisoire avec un niveau de confiance et demander ensuite la mesure qui départage les hypothèses.

## Schéma et couche ORM

### Concevoir selon les accès

- Partir des lectures, écritures, tris, règles d’intégrité et suppressions attendus.
- Créer une clé primaire sur chaque table applicative sauf exception documentée.
- Choisir une colonne `GENERATED ... AS IDENTITY` ou un UUID natif selon les besoins de localité, de distribution et d’exposition des identifiants. Mesurer au lieu d’affirmer qu’un type est toujours plus rapide.
- Stocker un instant avec `timestamptz`. Réserver `timestamp` sans fuseau aux valeurs volontairement dépourvues d’instant absolu.
- Utiliser les clés étrangères lorsque l’intégrité doit être garantie par la base. Évaluer les verrous, les index côté référence et le volume avant d’activer une suppression en cascade.
- Accepter `jsonb` pour une structure variable ou peu interrogée. Extraire en colonnes les attributs qui portent des contraintes, des jointures ou des filtres fréquents.

### Dépasser l’ORM lorsque nécessaire

Conserver l’ORM pour les opérations courantes. Employer du SQL brut typé ou des requêtes préparées lorsque l’ORM empêche un index, un verrou, un lot ou une migration sûre. Garder le SQL dans le dépôt, paramétré et testé comme le reste du code.

## Lectures, jointures et index

### Analyser la requête complète

- Associer le plan aux paramètres qui déclenchent réellement la lenteur.
- Vérifier la sélectivité des filtres et le nombre de lignes retournées avant d’ajouter un index.
- Examiner les clés de jointure comme les filtres. Une clé primaire constitue souvent un bon côté référencé, mais une jointure correcte peut aussi utiliser une autre clé indexée.
- Considérer les scans séquentiels, index scans, index-only scans et bitmap scans. Un scan séquentiel n’est pas un échec lorsque la requête lit une part importante de la table.

### Concevoir un index composé

Utiliser l’ordre des colonnes comme une hypothèse à tester :

1. Placer souvent les égalités sélectives dans le préfixe exploitable du B-tree.
2. Placer ensuite la plage ou les colonnes qui permettent d’éviter le tri demandé.
3. Aligner les directions lorsque le tri multicolonne mélange `ASC` et `DESC`.
4. Vérifier le plan avec les paramètres et volumes réels.

Un index peut accélérer une lecture tout en ralentissant chaque `INSERT`, `UPDATE`, `DELETE`, autovacuum et sauvegarde. Évaluer les index redondants et le stockage avant d’en ajouter un.

### Créer un index sur une table active

Préférer `CREATE INDEX CONCURRENTLY` lorsque les écritures doivent continuer. Documenter ses contraintes :

- Exécution impossible dans un bloc de transaction.
- Travail et durée supérieurs à une construction non concurrente.
- Attente possible de transactions anciennes.
- Index `INVALID` possible après un échec, à détecter et traiter.
- Une seule construction concurrente par table à la fois selon la version et l’opération.

Ne pas lancer l’opération sans `lock_timeout`, `statement_timeout`, supervision et seuil d’arrêt adaptés au contexte.

## Écritures et transactions

- Ouvrir la transaction au plus près de la première requête qui en a besoin et la valider dès que l’invariant est établi.
- Exécuter les appels HTTP, RPC, stockage objet et calculs longs hors de la transaction.
- Verrouiller seulement les lignes nécessaires. Lorsqu’un traitement verrouille plusieurs lignes, utiliser un ordre stable pour réduire les interblocages.
- Prévoir les reprises sur interblocage et échec de sérialisation lorsque le niveau d’isolation ou la concurrence les rendent possibles.
- Éviter de garder une transaction ouverte pendant que l’application attend un utilisateur, un worker ou une file.
- Rendre les traitements rejouables lorsque le client peut perdre la réponse après un commit réussi.

## Migrations de schéma

### Préférer expand/contract

1. Ajouter la nouvelle structure sans supprimer l’ancienne.
2. Déployer un code compatible avec les deux formes.
3. Remplir ou convertir les données par lots idempotents.
4. Basculer les lectures, puis les écritures.
5. Vérifier le résultat pendant une période définie.
6. Supprimer l’ancienne structure dans une migration distincte.

Exécuter une migration dans une transaction lorsque la commande la supporte et que la durée reste courte. Certaines opérations concurrentes refusent les blocs de transaction.

### Réduire le blocage des contraintes

Pour une contrainte compatible, séparer l’ajout et la validation :

```sql
ALTER TABLE public.orders
    ADD CONSTRAINT orders_total_nonnegative
    CHECK (total_cents >= 0) NOT VALID;

ALTER TABLE public.orders
    VALIDATE CONSTRAINT orders_total_nonnegative;
```

Vérifier le niveau de verrou exact sur la version cible. `NOT VALID` réduit le travail initial, mais les nouvelles lignes doivent déjà respecter la contrainte.

### Évaluer chaque DDL

Documenter avant exécution : verrou demandé, scan ou réécriture, durée probable, espace temporaire, génération de WAL, réplication, compatibilité transactionnelle et état laissé après interruption.

## Connexions

- Réutiliser des connexions longues via un pool borné.
- Additionner les tailles maximales de tous les pools, workers, tâches planifiées, consoles et outils d’administration.
- Limiter la concurrence active à ce que CPU, mémoire et stockage peuvent servir. Une limite serveur élevée ne prouve pas que la base peut travailler efficacement avec autant de sessions.
- Utiliser un pooler externe comme PgBouncer lorsqu’il convient à la topologie. Garder un pool applicatif borné comme solution locale.
- Vérifier le mode de pooling. Le mode transaction peut changer le comportement des états de session, tables temporaires, verrous consultatifs et certaines stratégies de requêtes préparées.
- Appliquer du backpressure dans l’application au lieu de transformer un pic en tempête de connexions.

Dimensionner par mesure de latence et de débit. Commencer bas, augmenter progressivement, puis s’arrêter lorsque le débit plafonne ou que la latence et la contention montent.

## Planner et plans d’exécution

### Vérifier les statistiques

Le planner estime les cardinalités à partir des statistiques collectées par `ANALYZE`, souvent déclenché par autovacuum. Une forte divergence entre lignes estimées et réelles peut indiquer :

- Statistiques périmées après un chargement ou une forte modification.
- Distribution corrélée que les statistiques simples décrivent mal.
- Paramètre atypique ou plan générique inadapté.
- Expression qui masque une colonne indexée ou conversion de type défavorable.

Ne pas lancer `ANALYZE` par réflexe sur toute la base. Cibler la relation, mesurer le coût et vérifier si un réglage par colonne ou des statistiques étendues répondent mieux au problème.

### Utiliser `EXPLAIN` sans déclencher d’incident

Commencer par une planification sans exécution :

```sql
EXPLAIN (COSTS, VERBOSE, SETTINGS, FORMAT JSON)
SELECT id, created_at
FROM public.events
WHERE tenant_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

Ajouter `ANALYZE` et `BUFFERS` seulement sur une requête autorisée à s’exécuter :

```sql
EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)
SELECT id, created_at
FROM public.events
WHERE tenant_id = $1
ORDER BY created_at DESC
LIMIT 50;
```

`EXPLAIN ANALYZE` exécute la requête. Pour un `INSERT`, `UPDATE`, `DELETE`, `MERGE`, une fonction volatile ou une requête très coûteuse, préférer une copie représentative ou une réplica adaptée. Un `ROLLBACK` n’annule pas toutes les conséquences possibles, notamment les appels externes de déclencheurs ou l’avancement de séquences.

Comparer au minimum :

- Écart entre lignes estimées et réelles par nœud.
- Temps passé, boucles, lignes supprimées par filtre et type de jointure.
- Blocs lus, trouvés en cache, écrits et fichiers temporaires.
- Temps de planification et d’exécution, attentes de verrous observées séparément.

Nettoyer les littéraux et identifiants sensibles avant de partager un plan avec un service externe.

## Écritures en volume

Amortir l’aller-retour réseau, l’acquisition du pool et le traitement par requête avec des lots :

- Envoyer plusieurs lignes par requête, utiliser le batching du pilote ou évaluer `COPY` pour l’ingestion.
- Borner le nombre de lignes et d’octets par lot pour limiter mémoire, verrouillage, WAL et temps de reprise.
- Valider par lot lorsque l’atomicité globale n’est pas requise.
- Préserver l’idempotence avec une clé unique, `ON CONFLICT` ou une table de progression.
- Mesurer débit, p95/p99, CPU, I/O, WAL et réplication avant d’augmenter la concurrence.

Le gain d’environ 10× cité par Hatchet décrit leur benchmark. Ne pas le promettre sur un autre système.

## Autovacuum, XID et bloat

### Comprendre le signal

MVCC conserve les anciennes versions de lignes tant qu’une transaction peut encore les voir. Autovacuum récupère les tuples morts, met à jour la visibility map, contribue aux statistiques et protège contre le wraparound des identifiants de transaction.

Surveiller ensemble :

- `n_dead_tup`, créations de tuples morts et rythme auquel le vacuum les traite.
- Derniers vacuum/analyze automatiques et nombre d’exécutions.
- Progression des vacuum actifs et temps passé en attente.
- Anciennes transactions et réplication qui retiennent l’horizon de nettoyage.
- Âge des XID/MXID, espace disque, WAL, I/O et latence applicative.

Un autovacuum de plus d’une heure constitue le signal d’enquête proposé par l’article, pas une preuve de mauvais réglage. Une grande table peut demander plus d’une heure tout en progressant correctement. Le critère utile est sa capacité à suivre le churn avant épuisement des ressources ou des identifiants.

### Régler avec prudence

- Garder autovacuum activé.
- Régler d’abord les tables à fort churn avec des paramètres de stockage spécifiques lorsque les valeurs globales conviennent au reste de la base.
- Ajuster seuils et facteurs à partir du nombre de lignes modifiées entre deux passages acceptables.
- Vérifier que les workers et leur budget I/O peuvent terminer le travail sans affamer la charge applicative.
- Traiter les transactions anciennes qui empêchent la récupération avant d’augmenter aveuglément les ressources du vacuum.

### Traiter le bloat

Prévenir le bloat par un vacuum qui suit le rythme. Pour un index réellement gonflé, évaluer `REINDEX INDEX CONCURRENTLY` selon la version. Pour une table, comparer une reconstruction contrôlée, une migration vers une nouvelle table ou une extension telle que `pg_repack` si le fournisseur l’autorise.

`VACUUM FULL` réécrit la table et prend un verrou `ACCESS EXCLUSIVE`. Le réserver à une fenêtre explicitement préparée. Ne jamais supprimer un index sur le seul constat d’un faible `idx_scan`.

## `FOR UPDATE SKIP LOCKED`

Utiliser ce motif pour réclamer plusieurs travaux indépendants sans attendre les lignes déjà prises :

```sql
WITH claimed AS (
    SELECT id
    FROM public.jobs
    WHERE state = 'ready'
      AND available_at <= clock_timestamp()
    ORDER BY available_at, id
    FOR UPDATE SKIP LOCKED
    LIMIT $1
)
UPDATE public.jobs AS job
SET state = 'running',
    claimed_at = clock_timestamp()
FROM claimed
WHERE job.id = claimed.id
RETURNING job.id;
```

Garder la transaction courte et indexer la recherche des travaux éligibles. Ajouter une reprise après expiration du lease, une clé d’idempotence et une stratégie contre la famine.

`SKIP LOCKED` donne volontairement une vue incohérente des données. Ne pas l’utiliser pour une lecture métier qui exige un instantané complet ou pour masquer une contention non comprise.

## Partitionnement

Envisager le partitionnement lorsque la taille, la rétention ou la maintenance le justifie :

- Partitionner par une colonne présente dans les filtres usuels afin que le planner élague les partitions.
- Aligner les bornes temporelles sur la politique de rétention pour détacher ou supprimer une partition entière.
- Profiter de tables physiques distinctes pour vacuum, analyse et index par partition.
- Vérifier que les contraintes `PRIMARY KEY` ou `UNIQUE` incluent les colonnes de partition requises par la version.
- Précréer les partitions et prévoir le comportement lorsqu’aucune partition ne couvre une ligne.
- Mesurer le temps de planification, le nombre de partitions touchées et le coût d’exploitation.

Ne pas partitionner une table seulement parce qu’elle est grande. Une mauvaise clé, trop de partitions ou des filtres incompatibles peuvent ralentir les requêtes et compliquer les migrations.

## Migration d’une très grande table

Éviter une copie monolithique dans une transaction de plusieurs heures. Elle retient un ancien snapshot, gêne le nettoyage et accumule un retour arrière coûteux.

Construire une migration en ligne :

1. Créer la table cible, ses contraintes et ses index nécessaires à la reprise.
2. Capturer les écritures concurrentes avec un déclencheur, une double écriture contrôlée ou une réplication adaptée.
3. Tester le surcoût et le comportement en cas d’échec de cette capture.
4. Copier par pagination de clé stable, avec commits bornés et reprise persistée.
5. Utiliser une contrainte unique et `ON CONFLICT` pour rendre le backfill rejouable.
6. Réconcilier volumes, invariants, échantillons et écart de réplication.
7. Effectuer une bascule courte avec les verrous et timeouts annoncés.
8. Garder une fenêtre de retour arrière avant de retirer l’ancienne table et la capture.

Ne pas supposer qu’un décompte identique prouve l’équivalence. Vérifier les invariants métier et les écritures arrivées pendant la bascule.

## Requêtes de diagnostic

Adapter les noms de schéma et les droits. Ces vues exposent des instantanés ou des estimations, pas une vérité historique complète.

### Version

```sql
SELECT current_setting('server_version') AS server_version,
       current_setting('server_version_num')::integer AS server_version_num;
```

### Activité, transactions et bloqueurs

```sql
SELECT activity.pid,
       activity.usename,
       activity.application_name,
       activity.state,
       now() - activity.xact_start AS transaction_age,
       now() - activity.query_start AS query_age,
       pg_blocking_pids(activity.pid) AS blocking_pids,
       left(activity.query, 300) AS query
FROM pg_stat_activity AS activity
WHERE activity.pid <> pg_backend_pid()
  AND (activity.state <> 'idle' OR activity.xact_start IS NOT NULL)
ORDER BY activity.xact_start NULLS LAST,
         activity.query_start NULLS LAST;
```

### Répartition des connexions

```sql
SELECT application_name,
       state,
       count(*) AS connections
FROM pg_stat_activity
GROUP BY application_name, state
ORDER BY connections DESC;
```

### Tuples morts et activité de maintenance

```sql
SELECT relid::regclass AS relation,
       n_live_tup,
       n_dead_tup,
       last_autovacuum,
       autovacuum_count,
       last_autoanalyze,
       autoanalyze_count
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 50;
```

### Âge des XID par base

```sql
SELECT datname,
       age(datfrozenxid) AS oldest_xid_age
FROM pg_database
WHERE datallowconn
ORDER BY oldest_xid_age DESC;
```

Comparer ce résultat aux paramètres et alertes de la version cible. Ne pas dériver un seuil universel de cette seule requête.

### Statistiques d’une table

```sql
SELECT schemaname,
       tablename,
       attname,
       null_frac,
       n_distinct,
       most_common_vals,
       most_common_freqs
FROM pg_stats
WHERE schemaname = 'public'
  AND tablename = 'events';
```

### Utilisation et taille des index

```sql
SELECT indexrelid::regclass AS index_name,
       idx_scan,
       idx_tup_read,
       idx_tup_fetch,
       pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relid = 'public.events'::regclass
ORDER BY pg_relation_size(indexrelid) DESC;
```

Vérifier la dernière remise à zéro des statistiques et le rôle éventuel de contrainte avant toute suppression.

## Format d’une recommandation

Utiliser ce gabarit :

```markdown
Diagnostic : <cause la plus probable et niveau de confiance>

Preuves :
- <plan, métrique ou comportement observé>

Action proposée :
- <commande ou changement>
- Type : lecture seule | DML | DDL | maintenance
- Verrou et impact attendus : <faits vérifiés sur la version cible>
- Préconditions : <sauvegarde, espace, fenêtre, droits>

Validation :
- <mesure avant/après et critère de réussite>

Arrêt et retour arrière :
- <seuil d’arrêt, commande ou bascule de repli>

Inconnues :
- <fait qui pourrait changer le diagnostic>
```

## Références

- [Article source Hatchet](https://hatchet.run/blog/postgres-survival-guide)
- [PostgreSQL : utiliser `EXPLAIN`](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL : `CREATE INDEX`](https://www.postgresql.org/docs/current/sql-createindex.html)
- [PostgreSQL : maintenance par vacuum](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- [PostgreSQL : `ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html)
- [PostgreSQL : verrouillage dans `SELECT`](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL : partitionnement](https://www.postgresql.org/docs/current/ddl-partitioning.html)
