# Deployment Guide

## 1. Environment Requirements

The L10 Automatic Warranty Request Classification prototype uses Docker for reproducible execution.

Requirements:
- Windows 10/11, Linux, or macOS.
- Docker Desktop with Docker Compose support, or Docker Engine with Docker Compose.
- WSL 2 when using Docker Desktop on Windows.
- Internet connection during the initial image build.
- Sufficient disk space for dependencies, datasets, and model artifacts.

The Docker image uses Python 3.11. Python does not need to be installed separately on the host machine.

## 2. Setup and Execution Steps

Clone the public GitHub repository and open its root directory.

Build the image and start the runtime service:

`docker compose up -d --build`

Run the machine learning pipeline:

`docker compose --profile pipeline run --rm pipeline`

The pipeline performs:
1. Raw dataset validation.
2. Train, validation, and test splitting.
3. Dataset split verification.
4. Logistic Regression training.
5. Multinomial Naive Bayes training.
6. Linear SVM training.
7. Model comparison.

Generated datasets, models, and reports are persisted through Docker bind mounts.

## 3. Environment Variables

The current prototype does not require environment variables for Docker execution.

| Variable | Required | Description |
|---|---|---|
| None | No | The current ML pipeline uses project configuration and files directly. |

No credentials, API keys, or private tokens are required.

## 4. Sample Data

The sample dataset is located at:

`data/raw/issue_descriptions.csv`

Required columns:
- `desc_id`: Unique issue description identifier.
- `issue_desc`: Warranty issue description.
- `issue_category`: Target classification label.

Supported categories:
- `MAN_HINH`
- `PIN`
- `SAC`
- `PHAN_MEM`
- `NUOC_VAO`
- `KHAC`

The dataset is included in the repository and copied into the Docker image.

## 5. Verification

Check the runtime service:

`docker compose ps`

Expected result:
- `l10-runtime` is running.
- Runtime health status becomes `healthy`.

Run the pipeline:

`docker compose --profile pipeline run --rm pipeline`

Expected result:
- All pipeline stages finish without errors.
- Processed datasets are available in `data/processed/`.
- Trained model artifacts are available in `models/`.
- Evaluation reports are available in `reports/`.

Run automated tests:

`docker compose run --rm --no-deps runtime python -m unittest discover -s tests -v`

Expected result: all 19 tests pass in the verified environment.
