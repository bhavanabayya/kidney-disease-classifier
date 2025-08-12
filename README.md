# Kidney Disease Classifier (Deep Learning)

A Flask-based deep learning project for classifying kidney disease images using a clean, config-driven pipeline (ingestion → base model → training → evaluation → prediction). Includes DVC for data/versioned stages and Docker/GitHub Actions for CI/CD.

## Project Structure
```
kidney-disease-classifier/
├─ app.py                     # Flask app
├─ templates/                 # Jinja2 templates for web UI
├─ src/cnnClassifier/         # Package: components, pipelines, utils
├─ config/config.yaml         # Paths & training config
├─ params.yaml                # Model hyperparameters
├─ models/model.h5            # Trained Keras model (LFS)
├─ data/
│  ├─ raw/                    # Raw data (place your dataset here)
│  └─ processed/              # Intermediate/ready-to-train (gitignored)
├─ docs/assets/               # Screenshots & sample images
├─ dvc.yaml / dvc.lock        # DVC pipeline
├─ Dockerfile                 # Container build
├─ requirements.txt           # Python dependencies (pip)
├─ setup.py                   # Editable install for src package (-e .)
└─ .github/workflows/         # CI pipeline
```

## Quickstart (pip)
Use the folder you already have locally.

```bash
# 1) (optional) create a virtual environment in this folder
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install --upgrade pip

# 2) install dependencies
pip install -r requirements.txt
```

> Note: `requirements.txt` includes `-e .` so your `src/` package is installed in editable mode.

## Run the Web App
```bash
python app.py
# App runs on http://127.0.0.1:5000 (check console output)
```

## Train / Reproduce the Pipeline
Training is orchestrated via the package in `src/cnnClassifier` and configs.

```bash
python main.py       # runs the end-to-end pipeline as defined in the project
```

If you use **DVC**:
```bash
# if you have a remote: dvc pull
dvc repro             # execute stages from dvc.yaml
```

## Models & Large Files
- Trained model is stored at `models/model.h5`. This repo is configured for **Git LFS** to handle large binaries (`*.h5`, images).
- Place datasets under `data/raw/` and keep outputs in `data/processed/` (already gitignored).

## Docker (optional)
```bash
docker build -t kidney-classifier .
docker run -p 5000:5000 kidney-classifier
```

## Notes
- Frameworks: TensorFlow/Keras, Flask, DVC (optional), MLflow (if configured).
- For reproducibility, pin your data paths in `config/config.yaml` and hyperparameters in `params.yaml`.