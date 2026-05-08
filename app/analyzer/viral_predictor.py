from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased"
)


def predict_viral_score(text):

    result = classifier(text)

    return result
