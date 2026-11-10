"""Lab QR4-L05-1: Multi-Head Self-Attention and Causal Masking in Transformers (Vaswani et al. 2017).

Demonstrates the core mechanics of the transformer architecture: scaled dot-product attention,
multi-head linear projections, numerical softmax stabilization, and causal autoregressive masking
that prevents sequential forward lookahead in temporal text streams.
"""

from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax along specified axis."""
    max_x = np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x - max_x)
    return np.asarray(exp_x / np.sum(exp_x, axis=axis, keepdims=True), dtype=np.float64)


def scaled_dot_product_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Computes Attention(Q, K, V) = softmax(Q @ K.T / sqrt(d_k) + M) @ V."""
    d_k = q.shape[-1]
    scores = (q @ k.swapaxes(-2, -1)) / np.sqrt(float(d_k))

    if mask is not None:
        scores = scores + mask

    weights = softmax(scores, axis=-1)
    output = weights @ v
    return output, weights


def make_causal_mask(seq_len: int) -> np.ndarray:
    """Creates upper-triangular additive causal mask with -1e9 for future positions."""
    mask = np.triu(np.full((seq_len, seq_len), -1e9, dtype=np.float64), k=1)
    return mask


def main() -> None:
    # 4-token sequence (e.g. ["Inflation", "surged", "above", "target"])
    seq_len = 4
    d_model = 8
    num_heads = 2
    d_k = d_model // num_heads

    rng = np.random.default_rng(42)

    # Simulated input token embeddings X of shape (seq_len, d_model)
    x = rng.normal(0.0, 1.0, size=(seq_len, d_model))

    # Projection weight matrices for Multi-Head Attention
    w_q = rng.normal(0.0, 0.5, size=(d_model, d_model))
    w_k = rng.normal(0.0, 0.5, size=(d_model, d_model))
    w_v = rng.normal(0.0, 0.5, size=(d_model, d_model))
    w_o = rng.normal(0.0, 0.5, size=(d_model, d_model))

    q = x @ w_q
    k = x @ w_k
    v = x @ w_v

    # Reshape into 2 heads: (num_heads, seq_len, d_k)
    q_heads = q.reshape(seq_len, num_heads, d_k).swapaxes(0, 1)
    k_heads = k.reshape(seq_len, num_heads, d_k).swapaxes(0, 1)
    v_heads = v.reshape(seq_len, num_heads, d_k).swapaxes(0, 1)

    causal_mask = make_causal_mask(seq_len)

    # 1. Unmasked Bidirectional Attention (e.g. BERT encoder)
    _out_unmasked, _weights_unmasked = scaled_dot_product_attention(q_heads, k_heads, v_heads, mask=None)

    # 2. Causal Autoregressive Attention (e.g. GPT decoder)
    out_causal, weights_causal = scaled_dot_product_attention(q_heads, k_heads, v_heads, mask=causal_mask)

    print(f"Sequence length: {seq_len} tokens")
    print(f"Model dimension: {d_model} (Heads: {num_heads}, Head dimension d_k: {d_k})")

    # Inspect Head 0 causal attention weight matrix
    h0_causal_weights = weights_causal[0]
    print("\n--- Head 0 Causal Attention Weight Matrix (GPT-style Decoder) ---")
    for row_idx in range(seq_len):
        row_str = "  ".join(f"{h0_causal_weights[row_idx, col]:.4f}" for col in range(seq_len))
        print(f"Token {row_idx}: [{row_str}]")

    # Invariants verification
    row_sums = np.sum(h0_causal_weights, axis=-1)
    future_leakage = float(np.sum(np.triu(h0_causal_weights, k=1)))

    print(f"\nRow sums (probabilistic normalization): {np.round(row_sums, 4)}")
    print(f"Total future position attention weight (Causal Leakage Check): {future_leakage:.8f}")

    # Concatenate heads and project output
    concat_causal = out_causal.swapaxes(0, 1).reshape(seq_len, d_model)
    final_output = concat_causal @ w_o
    print(f"Final Multi-Head Attention output shape: {final_output.shape}")
    print(f"Final output norm per token: {np.round(np.linalg.norm(final_output, axis=1), 4)}")
    print("Verification Invariant: Causal attention strictly eliminates information leakage from j > i.")


main()
