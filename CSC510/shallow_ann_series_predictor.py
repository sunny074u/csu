#!/usr/bin/env python3
"""
shallow_ann_series_predictor.py

A hand-made shallow ANN (1 hidden layer + output layer) using NumPy only.
It learns a simple "next number in a series" mapping via batch gradient descent
(static backpropagation).

How it works (high level)
- Build training pairs from a numeric series using a sliding window:
  [x(t-k), ..., x(t-1)]  ->  x(t)
- Normalize inputs/targets (helps gradient descent converge).
- Train a tiny fully-connected network:
  Input -> Hidden(tanh) -> Output(linear)
- Predict the next value after the final window.

Citations in code comments point to standard references for backprop and MSE.
(See References at the bottom.)

Run examples
1) Direct CLI:
   python shallow_ann_series_predictor.py --series "1,2,3,4,5,6,7,8" --window 3 --epochs 5000 --lr 0.03 --hidden 12 --plot

2) Interactive prompt (no args):
   python shallow_ann_series_predictor.py
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Tuple, Optional, List

import numpy as np


def parse_series(series_text: str) -> np.ndarray:
    """
    Parse a comma/space-separated list of numbers into a 1D numpy array.
    Accepts: "1,2,3", "1 2 3", "1, 2, 3.5", etc.
    """
    if not series_text or not series_text.strip():
        raise ValueError("Empty series. Provide numbers like: 1,2,3,4")
    cleaned = series_text.replace(";", ",").replace("\n", " ").strip()
    # split by comma or whitespace
    parts = [p for p in cleaned.replace(",", " ").split() if p]
    try:
        nums = np.array([float(p) for p in parts], dtype=np.float64)
    except ValueError as e:
        raise ValueError("Series must contain only numbers. Example: 1,2,3,4") from e
    if nums.ndim != 1 or nums.size < 2:
        raise ValueError("Series must contain at least 2 numbers.")
    return nums


def build_window_dataset(series: np.ndarray, window: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert a series into supervised learning data using a sliding window.
    X shape: (m, window)
    y shape: (m, 1)
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    if series.size <= window:
        raise ValueError(f"Series is too short for window={window}. Need > window values.")
    m = series.size - window
    X = np.zeros((m, window), dtype=np.float64)
    y = np.zeros((m, 1), dtype=np.float64)
    for i in range(m):
        X[i, :] = series[i:i + window]
        y[i, 0] = series[i + window]
    return X, y


@dataclass
class StandardScaler:
    """
    Simple standardization: (x - mean) / std
    """
    mean_: Optional[np.ndarray] = None
    std_: Optional[np.ndarray] = None
    eps: float = 1e-8

    def fit(self, x: np.ndarray) -> "StandardScaler":
        self.mean_ = x.mean(axis=0, keepdims=True)
        self.std_ = x.std(axis=0, keepdims=True) + self.eps
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("Scaler not fitted.")
        return (x - self.mean_) / self.std_

    def inverse_transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("Scaler not fitted.")
        return x * self.std_ + self.mean_


# ANN Model

@dataclass
class ShallowANN:
    """
    A 2-layer neural network (hidden + output) for regression.

    Architecture
    - Input dimension: n_in
    - Hidden dimension: n_hidden
    - Output dimension: 1

    Forward pass
        Z1 = X W1 + b1
        A1 = tanh(Z1)
        y_hat = A1 W2 + b2

    Loss (MSE)
        L = mean((y_hat - y)^2)

    Backprop gradients follow the chain rule (standard derivations),
    see Nielsen (2015) and Goodfellow et al. (2016).

    Notes on terminology:
    - Some texts call this "2-layer" (counting hidden+output),
      while others say "3-layer" including the input layer.
    """
    n_in: int
    n_hidden: int
    seed: int = 42

    W1: Optional[np.ndarray] = None
    b1: Optional[np.ndarray] = None
    W2: Optional[np.ndarray] = None
    b2: Optional[np.ndarray] = None

    def init_params(self) -> None:
        rng = np.random.default_rng(self.seed)

        # Xavier/Glorot-ish init for tanh tends to behave well in shallow nets.
        # (Common practice; see Goodfellow et al., 2016.)
        limit1 = np.sqrt(6.0 / (self.n_in + self.n_hidden))
        self.W1 = rng.uniform(-limit1, limit1, size=(self.n_in, self.n_hidden)).astype(np.float64)
        self.b1 = np.zeros((1, self.n_hidden), dtype=np.float64)

        limit2 = np.sqrt(6.0 / (self.n_hidden + 1))
        self.W2 = rng.uniform(-limit2, limit2, size=(self.n_hidden, 1)).astype(np.float64)
        self.b2 = np.zeros((1, 1), dtype=np.float64)

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        return np.tanh(x)

    @staticmethod
    def tanh_derivative_from_activated(a: np.ndarray) -> np.ndarray:
        # derivative of tanh(z) is 1 - tanh(z)^2
        return 1.0 - (a ** 2)

    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self.W1 is None:
            raise RuntimeError("Model not initialized. Call init_params().")
        Z1 = X @ self.W1 + self.b1
        A1 = self.tanh(Z1)
        y_hat = A1 @ self.W2 + self.b2
        return Z1, A1, y_hat

    @staticmethod
    def mse(y_hat: np.ndarray, y: np.ndarray) -> float:
        # Mean Squared Error; a standard regression loss (Goodfellow et al., 2016).
        diff = y_hat - y
        return float(np.mean(diff * diff))

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        lr: float = 0.03,
        epochs: int = 5000,
        print_every: int = 500,
        l2: float = 0.0,
        clip_grad: Optional[float] = None,
    ) -> List[float]:
        """
        Batch gradient descent training (static backprop through a fixed graph).
        """
        if self.W1 is None:
            self.init_params()

        m = X.shape[0]
        losses: List[float] = []

        for epoch in range(1, epochs + 1):
            # ---- forward ----
            _, A1, y_hat = self.forward(X)

            # ---- loss ----
            loss = self.mse(y_hat, y)
            if l2 > 0.0:
                # L2 penalty (weight decay) is optional; improves stability on tiny datasets.
                loss += float(l2 * (np.sum(self.W1 * self.W1) + np.sum(self.W2 * self.W2)))
            losses.append(loss)

            # ---- backprop (chain rule) ----
            # dL/dy_hat for MSE: (2/m) * (y_hat - y)
            # (Standard result; see Nielsen, 2015; Goodfellow et al., 2016.)
            dY = (2.0 / m) * (y_hat - y)  # shape (m, 1)

            # Output layer gradients
            dW2 = A1.T @ dY  # (hidden, m) @ (m,1) -> (hidden,1)
            db2 = np.sum(dY, axis=0, keepdims=True)

            # Hidden layer gradients
            dA1 = dY @ self.W2.T  # (m,1) @ (1,hidden) -> (m,hidden)
            dZ1 = dA1 * self.tanh_derivative_from_activated(A1)  # (m,hidden)

            dW1 = X.T @ dZ1  # (in,m) @ (m,hidden) -> (in,hidden)
            db1 = np.sum(dZ1, axis=0, keepdims=True)

            if l2 > 0.0:
                dW2 += 2.0 * l2 * self.W2
                dW1 += 2.0 * l2 * self.W1

            if clip_grad is not None and clip_grad > 0.0:
                # simple global norm clipping
                norm = np.sqrt(
                    np.sum(dW1 * dW1) + np.sum(db1 * db1) + np.sum(dW2 * dW2) + np.sum(db2 * db2)
                )
                if norm > clip_grad:
                    scale = clip_grad / (norm + 1e-12)
                    dW1 *= scale
                    db1 *= scale
                    dW2 *= scale
                    db2 *= scale

            # ---- gradient descent update ----
            self.W1 -= lr * dW1
            self.b1 -= lr * db1
            self.W2 -= lr * dW2
            self.b2 -= lr * db2

            if print_every and (epoch == 1 or epoch % print_every == 0 or epoch == epochs):
                print(f"epoch {epoch:>5}/{epochs} | loss={loss:.6f}")

        return losses

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, _, y_hat = self.forward(X)
        return y_hat


# CLI / App 

def maybe_plot(y_true: np.ndarray, y_pred: np.ndarray, title: str = "Actual vs Predicted") -> None:
    """
    Optional visualization: tries matplotlib; falls back to a tiny text table.
    """
    try:
        import matplotlib.pyplot as plt  # optional dependency
        idx = np.arange(len(y_true))
        plt.figure()
        plt.plot(idx, y_true, label="actual")
        plt.plot(idx, y_pred, label="predicted")
        plt.title(title)
        plt.xlabel("sample")
        plt.ylabel("value")
        plt.legend()
        plt.tight_layout()
        plt.show()
    except Exception:
        # Text fallback (keeps the script runnable without matplotlib).
        print("\n(Plot skipped — matplotlib not available.)")
        print("Last 10 samples (actual vs predicted):")
        for a, p in list(zip(y_true.flatten(), y_pred.flatten()))[-10:]:
            print(f"  actual={a:>10.4f} | pred={p:>10.4f}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Hand-made shallow ANN (NumPy) to predict the next number in a series."
    )
    parser.add_argument("--series", type=str, default="", help='Numeric series, e.g. "1,2,3,4,5"')
    parser.add_argument("--window", type=int, default=3, help="How many previous numbers to use as input")
    parser.add_argument("--hidden", type=int, default=12, help="Hidden layer width")
    parser.add_argument("--epochs", type=int, default=5000, help="Training epochs (>= 1000 recommended)")
    parser.add_argument("--lr", type=float, default=0.03, help="Learning rate")
    parser.add_argument("--l2", type=float, default=0.0, help="Optional L2 regularization strength (e.g., 1e-4)")
    parser.add_argument("--clip", type=float, default=0.0, help="Optional gradient clip norm (e.g., 5.0)")
    parser.add_argument("--print-every", type=int, default=500, help="Print loss every N epochs")
    parser.add_argument("--plot", action="store_true", help="Show a simple plot (requires matplotlib)")
    args = parser.parse_args(argv)

    # Interactive prompt if not provided
    if not args.series.strip():
        print("Enter a numeric series (comma or space separated). Example: 1,2,3,4,5,6")
        args.series = input("series> ").strip()

    series = parse_series(args.series)
    window = int(args.window)

    # Build supervised dataset
    X, y = build_window_dataset(series, window)

    # Train/val split (simple, keeps the output honest)
    m = X.shape[0]
    split = max(1, int(0.8 * m))
    X_train, y_train = X[:split], y[:split]
    X_val, y_val = X[split:], y[split:]

    # Normalize using train stats only
    x_scaler = StandardScaler().fit(X_train)
    y_scaler = StandardScaler().fit(y_train)

    X_train_s = x_scaler.transform(X_train)
    y_train_s = y_scaler.transform(y_train)
    X_val_s = x_scaler.transform(X_val) if X_val.size else X_val
    y_val_s = y_scaler.transform(y_val) if y_val.size else y_val

    # Create and train the ANN
    ann = ShallowANN(n_in=window, n_hidden=int(args.hidden), seed=42)
    ann.init_params()

    epochs = int(args.epochs)
    if epochs < 1000:
        print("Note: epochs < 1000. The assignment asks for at least 1,000 training repeats.")
    clip = float(args.clip) if args.clip and args.clip > 0 else None

    losses = ann.train(
        X_train_s,
        y_train_s,
        lr=float(args.lr),
        epochs=epochs,
        print_every=int(args.print_every),
        l2=float(args.l2),
        clip_grad=clip,
    )

    # Evaluate on validation portion
    if X_val_s.size:
        y_val_pred_s = ann.predict(X_val_s)
        val_loss = ShallowANN.mse(y_val_pred_s, y_val_s)
        print(f"\nValidation loss (standardized MSE): {val_loss:.6f}")
        y_val_pred = y_scaler.inverse_transform(y_val_pred_s)
        if args.plot:
            maybe_plot(y_val, y_val_pred, title="Validation: Actual vs Predicted")
    else:
        print("\n(No validation split — dataset too small.)")

    # Forecast next value after the provided series
    last_window = series[-window:].reshape(1, -1)
    last_window_s = x_scaler.transform(last_window)
    next_pred_s = ann.predict(last_window_s)
    next_pred = float(y_scaler.inverse_transform(next_pred_s)[0, 0])

    print("\n--- Result ---")
    print(f"Input window (last {window} numbers): {series[-window:]}")
    print(f"Predicted next value: {next_pred:.6f}")

    # A simple "visual" output: append prediction to the series
    extended = np.concatenate([series, np.array([next_pred])])
    print("\nSeries with prediction appended:")
    print(extended)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# References 
# Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning. MIT Press.
# Nielsen, M. A. (2015). Neural networks and deep learning. Determination Press.
# Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. Nature, 585, 357–362.
