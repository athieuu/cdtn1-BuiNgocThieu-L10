def predict_issue(model, description: str) -> str:
    """Predict the warranty issue category from a non-empty description."""
    if not isinstance(description, str):
        raise TypeError("Description must be a string.")

    description = description.strip()

    if not description:
        raise ValueError("Description must not be empty.")

    prediction = model.predict([description])
    return str(prediction[0])