VALID_LABELS = {
    "MAN_HINH",
    "PIN",
    "SAC",
    "PHAN_MEM",
    "NUOC_VAO",
    "KHAC",
}


def predict_issue(model, description: str) -> str:
    """Predict the warranty issue category from a non-empty description."""
    if not isinstance(description, str):
        raise TypeError("Description must be a string.")

    description = description.strip()

    if not description:
        raise ValueError("Description must not be empty.")

    prediction = model.predict([description])

    if len(prediction) == 0:
        raise ValueError("Model returned an empty prediction.")

    label = str(prediction[0])

    if label not in VALID_LABELS:
        raise ValueError(f"Model returned an invalid label: {label}")

    return label