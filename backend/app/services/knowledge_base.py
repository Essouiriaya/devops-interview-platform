KNOWLEDGE_BASE = {
    "python": [
        "Python est un langage interprété, typé dynamiquement. Le GIL (Global Interpreter Lock) "
        "limite l'exécution parallèle des threads CPU ; pour le parallélisme réel on utilise le "
        "module multiprocessing ou asyncio pour l'asynchrone.",
        "Les générateurs (mot-clé yield) produisent des itérateurs paresseux : idéaux pour traiter "
        "de gros fichiers ou flux sans charger tout en mémoire. Une liste est mutable, un tuple est "
        "immuable et hachable (utilisable comme clé de dictionnaire).",
        "La gestion des exceptions suit try / except / else / finally. On capture des exceptions "
        "précises plutôt que except nu, et on utilise raise pour propager. PEP8 recommande snake_case.",
    ],
    "java": [
        "La JVM exécute du bytecode. Le Garbage Collector libère la mémoire heap des objets sans "
        "références fortes. ArrayList = tableau dynamique (accès O(1)), LinkedList = liste chaînée "
        "(insertion O(1) en tête).",
        "Les Streams Java 8 (filter, map, collect) permettent un style déclaratif avec des lambdas ; "
        "les opérations intermédiaires sont paresseuses, l'opération terminale déclenche le calcul.",
    ],
    "devops": [
        "L'intégration continue (CI) exécute tests et builds à chaque commit via des pipelines "
        "(GitHub Actions, GitLab CI, Jenkins). Le déploiement continu (CD) automatise la mise en "
        "production après validation.",
        "Docker : une image est un modèle immuable (Dockerfile), un conteneur en est une instance "
        "d'exécution isolée. Un build multi-stage réduit la taille de l'image finale en séparant "
        "compilation et runtime.",
        "Kubernetes : un Deployment gère le nombre de réplicas (desired state) de pods ; un Service "
        "expose les pods et fait du load balancing via des labels/selectors.",
    ],
    "data-science": [
        "Traitement des valeurs manquantes : suppression (dropna) si peu nombreuses, imputation "
        "par la moyenne/médiane (fillna) sinon. Toujours analyser le mécanisme d'absence avant de "
        "traiter.",
        "Corrélation ≠ causalité : deux variables peuvent varier ensemble sans lien de cause. On "
        "confirme avec des expérimentations ou des modèles causaux.",
    ],
    "machine-learning": [
        "Supervisé : on apprend depuis des exemples étiquetés (cible connue). Non supervisé : "
        "découverte de structure (clustering, réduction de dimension).",
        "L'overfitting survient quand le modèle mémorise le bruit des données d'entraînement. "
        "Contre-mesures : plus de données, régularisation (L1/L2), validation croisée, early "
        "stopping.",
        "La normalisation (StandardScaler, MinMaxScaler) met les features à la même échelle pour "
        "stabiliser et accélérer la convergence du gradient.",
    ],
    "sql": [
        "INNER JOIN retourne les lignes ayant une correspondance dans les deux tables ; LEFT JOIN "
        "retourne toutes les lignes de la table de gauche, avec NULL à droite si pas de correspondance.",
        "Un index (souvent B-tree) accélère les recherches WHERE/JOIN en évitant le full table scan, "
        "au prix d'un coût d'écriture et de stockage.",
        "ACID : Atomicité (tout ou rien), Cohérence (règles respectées), Isolation (transactions "
        "concurrentes sans interférence), Durabilité (survie aux pannes).",
    ],
}