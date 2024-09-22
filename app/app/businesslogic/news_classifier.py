from pathlib import Path
from joblib import load  # Change to joblib

class NewsClassificationModel:
    def __init__(self, model_path="./app/models"):
        self.model_path = Path(model_path)
        self.clf = None
        self.vectorizer = None
        self.classes = None

    def load_model(self):
        # Load the classifier model
        self.clf = load(self.model_path / "news_classification_model.pkl")

        # Load the vectorizer
        self.vectorizer = load(self.model_path / "news_classification_tokenizer.pkl")

        # Load the classes
        self.classes = load(self.model_path / "news_classification_classes.pkl")

    def predict(self, samples):
        vectors_test = self.vectorizer.transform(samples)
        preds = self.clf.predict(vectors_test)

        return [self.classes[pred] for pred in preds]
