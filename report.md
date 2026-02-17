# Rapport d'exécution — Prototype FR → Wolof TTS

## Actions effectuées
- Scaffold complet du dépôt créé (src/, scripts/, docs/, colab/, tests/, CI).
- Variables d'environnement documentées dans `env.example`.
- Notebook Colab ajouté avec mode repli sans secrets.
- Scripts FR→WO traduction, préparation dataset, entraînement prototype, synthèse ajoutés.
- Dataset d'exemple `dataset/metadata.csv` ajouté.
- CI GitHub Actions minimale (tests + vérification syntaxe) ajoutée.

## Résultats
- Le pipeline prototype fonctionne en mode fallback sans clé externe.
- Génération WAV possible via `src/synthesize.py` (fallback sinusoïde si backend TTS indisponible).

## Erreurs / limites observées
- Accès effectif au dataset HF `galsenai/anta_women_tts` non vérifié dans cet environnement hors token.
- Fine-tuning réel xTTS/SpeechT5 non exécuté ici (wrapper prototype fourni).

## Actions requises côté utilisateur
1. Ajouter secrets GitHub Actions (`HUGGINGFACE_TOKEN`, `GCLOUD_SERVICE_KEY_JSON`, etc.).
2. Lancer le notebook Colab et fournir les chemins Drive/JSON si nécessaire.
3. Optionnel: pousser checkpoint vers `HF_MODEL_REPO`.
