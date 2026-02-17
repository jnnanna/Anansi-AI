# Guide d'utilisation — Prototype FR → Wolof TTS (hybride)

## 1) Comptes à créer
- GitHub (obligatoire)
- Hugging Face (recommandé pour dataset/modèle)
- Google Cloud (optionnel, pour traduction automatique FR→WO)
- OpenAI (optionnel, pour reformulation)
- Google Colab (obligatoire pour exécution notebook, Colab Pro optionnel)

## 2) Secrets et variables d'environnement
Ne jamais committer de clés.

### GitHub Secrets (repo > Settings > Secrets and variables > Actions)
Créer exactement ces secrets :
- `HUGGINGFACE_TOKEN`
- `GCLOUD_SERVICE_KEY_JSON`
- `OPENAI_API_KEY`
- `HF_MODEL_REPO`
- `GDRIVE_DATASET_PATH`
- `USE_HF_DATASET`

### Colab
Deux options :
1. **Variables dans Colab**: Runtime > Secrets (ou `os.environ[...]` temporaire)
2. **Drive**: stocker le JSON GCP dans Drive puis définir `GCLOUD_SERVICE_KEY_JSON=/content/drive/MyDrive/.../service_account.json`

## 3) Format dataset audio requis
- WAV PCM 16-bit, mono
- 16 kHz recommandé
- `metadata.csv` délimité par `|` :
  - `00001.wav|texte`
- Nom fichier recommandé : 5 chiffres (`00001.wav`)

### Conversion audio vers 16kHz mono
```bash
ffmpeg -i input.wav -ac 1 -ar 16000 -sample_fmt s16 output.wav
```

## 4) Lancer localement
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python src/prepare_dataset.py --input_dir dataset --output_dir dataset_ready
python src/train.py --dataset_dir dataset_ready --output_dir finetuned --epochs 1 --backend xtts
python src/synthesize.py --text "Nanga def" --model_path finetuned/checkpoint_mock.json --output outputs/demo.wav
```

## 5) Lancer sur Colab
1. Ouvrir `colab/wolof_tts_colab.ipynb`
2. Exécuter les cellules dans l'ordre
3. Option HF : activer `USE_HF_DATASET=true` et fournir `HUGGINGFACE_TOKEN` si dataset privé
4. Option Drive : monter Drive et pointer `GDRIVE_DATASET_PATH`
5. Lancer mini entraînement (1 epoch) puis synthèse de 3 WAVs

## 6) Ajouter des audios locaux et relancer
1. Ajouter vos WAV dans `dataset/audios/`
2. Mettre à jour `dataset/metadata.csv`
3. Lancer préparation + entraînement + inférence
4. (Optionnel) fusionner avec dataset HF chargé dans `dataset_hf/`

## 7) Pousser un checkpoint vers HF Hub
Si `HUGGINGFACE_TOKEN` et `HF_MODEL_REPO` sont définis:
- se connecter avec `huggingface-cli login`
- créer le repo modèle
- uploader `finetuned/`

## 8) Consentement & licence
- Vérifier la licence du dataset public avant usage production.
- Pour audios privés: conserver une preuve explicite de consentement.

Exemple de consentement recommandé:
- identité du locuteur,
- autorisation d’entraînement et de génération de voix,
- périmètre d’usage (R&D / production),
- date et signature.

## 9) Checklist “ready for production”
- [ ] licence dataset validée
- [ ] consentements archivés
- [ ] secrets configurés hors dépôt
- [ ] tests CI verts
- [ ] monitoring qualité audio et biais linguistiques
- [ ] politique de suppression des données définie
