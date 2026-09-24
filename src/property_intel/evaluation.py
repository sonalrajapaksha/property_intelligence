"""Small, fixed edge-case set for duplicate matching regression checks."""

from .config import AUTO_MATCH
from .db import Property
from .pipeline import match_score

LABELS = [
    ("123 Queen Street, Auckland", "123 Queen St, Auckland", True),
    ("42 Great South Road", "42 Great South Rd", True),
    ("10 Mount Eden Road", "10 Mt Eden Rd", True),
    ("12 Queen St", "123 Queen St", False),
    ("Unit 1, 40 Example Rd", "Unit 2, 40 Example Rd", False),
    ("20 High St", "20 Main Rd", False),
]


def evaluate() -> dict[str, float]:
    tp = fp = fn = tn = 0
    for observation, canonical, same in LABELS:
        score, _ = match_score(
            {"address": observation}, Property(canonical_address=canonical, sector="OTHER")
        )
        predicted = score >= AUTO_MATCH
        tp += predicted and same
        fp += predicted and not same
        fn += not predicted and same
        tn += not predicted and not same
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    return {
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0,
        "false_merge_rate": fp / (fp + tn) if fp + tn else 0,
    }


if __name__ == "__main__":
    for key, value in evaluate().items():
        print(f"{key}: {value:.1%}")
