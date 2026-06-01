#!/usr/bin/env python3
"""
AI-Powered Academic Study Assistant

Self-executable portfolio project for CSU Global.

What it does:
- Accepts text from a file or pasted input
- Builds a simple knowledge base from the text
- Uses intelligent search (TF-IDF-like scoring + cosine similarity)
- Classifies sentences into study-friendly categories
- Produces a summary, key concepts, practice questions, and answers to queries

This project uses lightweight classical AI methods so it can run without online APIs.
"""

from __future__ import annotations

import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "because", "been", "but", "by", "for",
    "from", "had", "has", "have", "he", "her", "his", "i", "if", "in", "into", "is",
    "it", "its", "of", "on", "or", "our", "she", "so", "that", "the", "their", "them",
    "there", "these", "they", "this", "to", "was", "we", "were", "what", "when", "which",
    "who", "will", "with", "you", "your", "than", "then", "also", "can", "could", "should",
    "would", "do", "does", "did", "not", "more", "most", "very", "about", "through", "many",
    "such", "each", "other", "may", "might", "some", "any", "all", "much", "while", "during"
}

SAMPLE_TEXT = """
Machine learning is a branch of artificial intelligence that enables systems to learn patterns from data.
Supervised learning uses labeled examples to predict outcomes.
Unsupervised learning looks for structure in unlabeled data.
Classification is used when the goal is to assign items to categories.
Regression is used when the goal is to predict a continuous value.
Neural networks are useful for tasks that involve complex patterns and high-dimensional inputs.
A neural network usually contains an input layer, one or more hidden layers, and an output layer.
Training adjusts weights so the model can reduce error on a task.
Overfitting happens when a model memorizes training data and performs poorly on new data.
Good evaluation practices include splitting data into training and test sets.
Precision measures how many predicted positive results were correct.
Recall measures how many actual positive cases were identified.
""".strip()


@dataclass
class SentenceInfo:
    text: str
    tokens: List[str]
    category: str
    score: float = 0.0


def clean_text(text: str) -> str:
    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def classify_sentence(sentence: str) -> str:
    s = sentence.lower()
    if " is " in s or " are " in s or " refers to " in s or " means " in s:
        if any(k in s for k in ["defined", "definition", "refers to", "is a", "is an", "are used"]):
            return "definition"
    if any(k in s for k in ["for example", "for instance", "such as", "example"]):
        return "example"
    if any(k in s for k in ["first", "second", "third", "step", "process", "procedure", "training"]):
        return "process"
    if any(k in s for k in ["cause", "effect", "because", "therefore", "leads to", "results in"]):
        return "relationship"
    if any(k in s for k in ["measure", "evaluate", "accuracy", "precision", "recall", "test"]):
        return "evaluation"
    return "concept"


class StudyAssistant:
    def __init__(self, text: str) -> None:
        self.raw_text = clean_text(text)
        self.sentences = split_sentences(self.raw_text)
        if not self.sentences:
            raise ValueError("No usable sentences were found in the input text.")
        self.docs = [SentenceInfo(s, tokenize(s), classify_sentence(s)) for s in self.sentences]
        self.idf = self._build_idf()
        self.vectors = [self._vectorize_tokens(doc.tokens) for doc in self.docs]

    def _build_idf(self) -> Dict[str, float]:
        doc_count = len(self.docs)
        df: Dict[str, int] = defaultdict(int)
        for doc in self.docs:
            for token in set(doc.tokens):
                df[token] += 1
        return {term: math.log((1 + doc_count) / (1 + count)) + 1 for term, count in df.items()}

    def _vectorize_tokens(self, tokens: List[str]) -> Dict[str, float]:
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        return {term: (count / total) * self.idf.get(term, 1.0) for term, count in tf.items()}

    @staticmethod
    def _cosine(v1: Dict[str, float], v2: Dict[str, float]) -> float:
        common = set(v1).intersection(v2)
        dot = sum(v1[t] * v2[t] for t in common)
        n1 = math.sqrt(sum(v * v for v in v1.values()))
        n2 = math.sqrt(sum(v * v for v in v2.values()))
        if n1 == 0 or n2 == 0:
            return 0.0
        return dot / (n1 * n2)

    def summarize(self, top_n: int = 5) -> List[str]:
        centroid = Counter()
        for doc in self.docs:
            centroid.update(doc.tokens)
        centroid_vec = self._vectorize_tokens(list(centroid.elements()))
        scored: List[Tuple[float, int, str]] = []
        for idx, doc in enumerate(self.docs):
            score = self._cosine(self.vectors[idx], centroid_vec)
            score += 0.08 if doc.category == "definition" else 0.0
            score += 0.05 if doc.category == "evaluation" else 0.0
            scored.append((score, idx, doc.text))
        chosen = sorted(scored, reverse=True)[: max(1, min(top_n, len(scored)))]
        ordered = [text for _, _, text in sorted(chosen, key=lambda x: x[1])]
        return ordered

    def extract_key_concepts(self, top_n: int = 8) -> List[Tuple[str, int]]:
        tokens = []
        for doc in self.docs:
            tokens.extend(doc.tokens)
        counts = Counter(tokens)
        common = [(term, freq) for term, freq in counts.most_common() if len(term) > 3]
        return common[:top_n]

    def retrieve(self, query: str, top_n: int = 3) -> List[SentenceInfo]:
        q_tokens = tokenize(query)
        if not q_tokens:
            return self.docs[:top_n]
        q_vec = self._vectorize_tokens(q_tokens)
        scored = []
        for i, doc in enumerate(self.docs):
            sim = self._cosine(q_vec, self.vectors[i])
            keyword_bonus = sum(1 for t in q_tokens if t in doc.tokens) * 0.05
            total = sim + keyword_bonus
            scored.append((total, i, doc))
        top = sorted(scored, reverse=True)[: max(1, min(top_n, len(scored)))]
        return [doc for _, _, doc in top]

    def generate_practice_questions(self, top_n: int = 5) -> List[str]:
        questions: List[str] = []
        used = set()
        for doc in self.docs:
            sentence = doc.text.rstrip(".?!")
            if sentence in used:
                continue
            if doc.category == "definition":
                subject = sentence.split(" is ")[0].split(" are ")[0].strip()
                if 2 <= len(subject.split()) <= 6:
                    questions.append(f"What is {subject}?")
                    used.add(sentence)
            elif doc.category == "evaluation":
                lead = sentence.split()[0:4]
                if lead:
                    questions.append(f"Explain the significance of {' '.join(lead).lower()}.")
                    used.add(sentence)
            elif doc.category == "process":
                questions.append(f"Describe the process discussed in this idea: {sentence}.")
                used.add(sentence)
            if len(questions) >= top_n:
                break
        if not questions:
            for doc in self.docs[:top_n]:
                questions.append(f"Explain this concept in your own words: {doc.text.rstrip('.')}.")
        return questions[:top_n]

    def classify_overview(self) -> Dict[str, int]:
        counts = Counter(doc.category for doc in self.docs)
        return dict(sorted(counts.items(), key=lambda x: (-x[1], x[0])))

    def answer_query(self, query: str) -> str:
        hits = self.retrieve(query, top_n=3)
        if not hits:
            return "I could not find a strong match in the study material."
        combined = " ".join(hit.text for hit in hits)
        return combined


def read_user_text() -> str:
    print("Choose input option:")
    print("1 - Use built-in sample text")
    print("2 - Paste your own study text")
    print("3 - Load text from a .txt file")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        return SAMPLE_TEXT
    if choice == "2":
        print("Paste your text below. Type END on its own line when finished:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()
    if choice == "3":
        path = input("Enter the path to your .txt file: ").strip().strip('"')
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    print("Invalid choice. Defaulting to sample text.\n")
    return SAMPLE_TEXT


def print_report(assistant: StudyAssistant) -> None:
    print("\n" + "=" * 72)
    print("AI-POWERED ACADEMIC STUDY ASSISTANT")
    print("=" * 72)

    print("\nSUMMARY")
    for i, sentence in enumerate(assistant.summarize(), start=1):
        print(f"{i}. {sentence}")

    print("\nKEY CONCEPTS")
    for term, freq in assistant.extract_key_concepts():
        print(f"- {term} (frequency: {freq})")

    print("\nCLASSIFICATION OVERVIEW")
    for category, count in assistant.classify_overview().items():
        print(f"- {category}: {count}")

    print("\nPRACTICE QUESTIONS")
    for i, question in enumerate(assistant.generate_practice_questions(), start=1):
        print(f"{i}. {question}")

    print("\nINTELLIGENT SEARCH DEMO")
    sample_queries = [
        "main idea",
        "definition of neural networks",
        "evaluation measures",
    ]
    for q in sample_queries:
        print(f"\nQuery: {q}")
        print(assistant.answer_query(q))


def interactive_query_loop(assistant: StudyAssistant) -> None:
    print("\nAsk a question about your study text. Press Enter on a blank line to finish.")
    while True:
        query = input("Question: ").strip()
        if not query:
            break
        print("Answer:")
        print(assistant.answer_query(query))
        print()


def main() -> int:
    try:
        text = read_user_text()
        if not text.strip():
            raise ValueError("No text was provided.")
        assistant = StudyAssistant(text)
        print_report(assistant)
        interactive_query_loop(assistant)
        print("Goodbye.")
        return 0
    except KeyboardInterrupt:
        print("\nProcess cancelled by user.")
        return 1
    except Exception as exc:
        print(f"\nError: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
