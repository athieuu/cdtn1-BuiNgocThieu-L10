
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

train = pd.read_csv(DATA_DIR / "train.csv")
validation = pd.read_csv(DATA_DIR / "validation.csv")
test = pd.read_csv(DATA_DIR / "test.csv")

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    lowercase=True,
    min_df=1,
)

all_texts = pd.concat([
    train["issue_desc"],
    validation["issue_desc"],
    test["issue_desc"],
]).fillna("").astype(str)

vectorizer.fit(all_texts)


def check_pairs(left, right, left_name, right_name):
    left_text = left["issue_desc"].fillna("").astype(str)
    right_text = right["issue_desc"].fillna("").astype(str)

    left_matrix = vectorizer.transform(left_text)
    right_matrix = vectorizer.transform(right_text)

    similarities = cosine_similarity(left_matrix, right_matrix)
    rows, cols = (similarities >= 0.90).nonzero()

    print(f"\n{left_name} vs {right_name}")
    print(f"Số cặp có độ tương đồng >= 0.90: {len(rows)}")

    for i, j in zip(rows[:10], cols[:10]):
        print(f"\nSimilarity: {similarities[i, j]:.3f}")
        print(f"{left_name}: {left_text.iloc[i]}")
        print(f"Nhãn: {left['issue_category'].iloc[i]}")
        print(f"{right_name}: {right_text.iloc[j]}")
        print(f"Nhãn: {right['issue_category'].iloc[j]}")


check_pairs(train, validation, "Train", "Validation")
check_pairs(train, test, "Train", "Test")
check_pairs(validation, test, "Validation", "Test")
