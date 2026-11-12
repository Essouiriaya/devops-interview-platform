DOMAINS = [
    {"id": "python", "name": "Python",
     "description": "Langage, POO, exceptions, itérateurs, bonnes pratiques PEP8."},
    {"id": "java", "name": "Java",
     "description": "JVM, collections, streams, threads, Spring Boot."},
    {"id": "devops", "name": "DevOps",
     "description": "CI/CD, Docker, Kubernetes, monitoring, IaC."},
    {"id": "data-science", "name": "Data Science",
     "description": "Pandas, visualisation, statistiques, feature engineering."},
    {"id": "machine-learning", "name": "Machine Learning",
     "description": "Modèles supervisés/non supervisés, entraînement, métriques."},
    {"id": "sql", "name": "SQL",
     "description": "Requêtes, jointures, index, transactions, optimisation."},
]

LEVELS = {"débutant": "facile", "intermédiaire": "moyen", "avancé": "difficile"}

DEMO_BANK = {
    "python": [
        {"question": "Quelle est la différence entre une liste et un tuple en Python ?",
         "difficulty": "facile", "keywords": ["mutable", "immuable", "modifier"]},
        {"question": "Expliquez le GIL et son impact sur le multithreading en Python.",
         "difficulty": "difficile", "keywords": ["global interpreter lock", "thread", "parallélisme", "processus"]},
        {"question": "Qu'est-ce qu'un générateur et quand l'utiliser ?",
         "difficulty": "moyen", "keywords": ["yield", "mémoire", "itération", "paresseux"]},
        {"question": "Comment gérez-vous les exceptions de manière propre ?",
         "difficulty": "facile", "keywords": ["try", "except", "finally", "raise"]},
        {"question": "Différence entre deepcopy et copy ?",
         "difficulty": "moyen", "keywords": ["copie", "profonde", "référence", "immuables"]},
    ],
    "java": [
        {"question": "Différence entre ArrayList et LinkedList ?",
         "difficulty": "facile", "keywords": ["tableau", "nœud", "accès", "insertion"]},
        {"question": "Expliquez le fonctionnement du Garbage Collector JVM.",
         "difficulty": "moyen", "keywords": ["mémoire", "heap", "références", "collecte"]},
        {"question": "Qu'est-ce qu'un Stream en Java 8 ? Donnez un exemple.",
         "difficulty": "moyen", "keywords": ["lambda", "filter", "map", "intermédiaire"]},
    ],
    "devops": [
        {"question": "Qu'est-ce que l'intégration continue et pourquoi l'utiliser ?",
         "difficulty": "facile", "keywords": ["pipeline", "tests", "automatisation", "commits"]},
        {"question": "Différence entre une image et un conteneur Docker ?",
         "difficulty": "facile", "keywords": ["image", "template", "instance", "runtime"]},
        {"question": "Expliquez le rôle des Deployments et Services dans Kubernetes.",
         "difficulty": "difficile", "keywords": ["réplicas", "pods", "load balancing", "desired state"]},
        {"question": "Qu'est-ce qu'un Dockerfile multi-stage ?",
         "difficulty": "moyen", "keywords": ["étapes", "build", "taille", "runtime"]},
    ],
    "data-science": [
        {"question": "Comment traitez-vous les valeurs manquantes dans un dataset ?",
         "difficulty": "moyen", "keywords": ["dropna", "fillna", "imputation", "médiane"]},
        {"question": "Différence entre corrélation et causalité ?",
         "difficulty": "facile", "keywords": ["relation", "cause", "effet", "hasard"]},
    ],
    "machine-learning": [
        {"question": "Différence entre apprentissage supervisé et non supervisé ?",
         "difficulty": "facile", "keywords": ["étiquettes", "classes", "clustering", "cible"]},
        {"question": "Qu'est-ce que le surapprentissage (overfitting) et comment le limiter ?",
         "difficulty": "moyen", "keywords": ["régularisation", "validation", "validation croisée", "données"]},
        {"question": "Pourquoi normaliser les données avant un entraînement ?",
         "difficulty": "moyen", "keywords": ["échelle", "gradient", "convergence", "features"]},
    ],
    "sql": [
        {"question": "Quelle est la différence entre INNER JOIN et LEFT JOIN ?",
         "difficulty": "facile", "keywords": ["correspondance", "null", "toutes", "gauche"]},
        {"question": "Qu'est-ce qu'un index et comment améliore-t-il les performances ?",
         "difficulty": "moyen", "keywords": ["recherche", "B-tree", "lecture", "WHERE"]},
        {"question": "Expliquez les propriétés ACID d'une transaction.",
         "difficulty": "difficile", "keywords": ["atomicité", "cohérence", "isolation", "durabilité"]},
    ],
}

GENERIC_KEYWORDS = ["exemple", "avantage", "cas", "usage"]


def generate_demo_questions(domain: str, level: str, count: int) -> list:
    bank = DEMO_BANK.get(domain, DEMO_BANK["python"])
    target = LEVELS.get(level, "moyen")
    matching = [q for q in bank if q["difficulty"] == target]
    others = [q for q in bank if q["difficulty"] != target]
    ordered = matching + others
    picked = [ordered[i % len(ordered)] for i in range(count)]
    return [{"question": q["question"], "difficulty": q["difficulty"]} for q in picked]


def find_keywords(domain: str, question: str) -> list:
    for q in DEMO_BANK.get(domain, []):
        if q["question"] == question:
            return q["keywords"]
    return GENERIC_KEYWORDS


def evaluate_demo_answer(question: str, answer: str, keywords: list) -> dict:
    a = (answer or "").strip().lower()
    if len(a) < 20:
        return {
            "score": 5.0,
            "feedback": "Réponse beaucoup trop courte. Développez votre réponse avec des exemples concrets.",
            "strengths": ["Vous avez tenté de répondre"],
            "improvements": [
                "Structurez la réponse : définition, exemple, cas d'usage",
                "Citez au moins 2 concepts techniques liés à la question",
            ],
        }

    hits = sum(1 for k in keywords if k.lower() in a)
    kw_score = (hits / max(1, len(keywords))) * 50
    length_score = min(25.0, len(a) / 8)
    code_bonus = 10.0 if any(t in a for t in ["def ", "class ", "select ", "```", "import ", "docker", "kubectl"]) else 0.0
    score = float(min(100, int(20 + kw_score + length_score + code_bonus)))

    strengths, improvements = [], []
    if score >= 70:
        strengths = ["Réponse structurée et complète", "Bons concepts techniques cités"]
        improvements = ["Ajoutez un exemple concret de votre expérience pour convaincre davantage"]
    elif score >= 40:
        strengths = ["La base de la réponse est présente"]
        improvements = [
            "Développez chaque point clé de la question",
            "Citez les concepts exacts attendus (" + ", ".join(keywords[:3]) + ")",
        ]
    else:
        strengths = ["Tentative de réponse effectuée"]
        improvements = [
            "Revoir les fondamentaux de cette notion",
            "Structurer : définition → mécanisme → exemple",
            "Préparer une réponse d'au moins 4-5 phrases",
        ]

    return {
        "score": score,
        "feedback": (
            f"Évaluation heuristique (mode démo, score {score:.0f}/100). "
            f"Concepts clés détectés : {hits}/{len(keywords)}. "
            + ("Bonne maîtrise apparente." if score >= 70 else "La réponse gagnerait à être approfondie.")
        ),
        "strengths": strengths,
        "improvements": improvements,
    }