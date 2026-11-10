import numpy as np

# Lucas (1978) Pure Exchange Economy on a 3-State Markov Endowment Chain
beta = 0.96
gamma = 2.0
# Endowment growth states: recession, normal, expansion
g = np.array([0.97, 1.018, 1.05])
# Markov transition matrix Pi[i, j] = P(s_{t+1} = j | s_t = i)
pi = np.array(
    [
        [0.70, 0.25, 0.05],
        [0.15, 0.70, 0.15],
        [0.05, 0.25, 0.70],
    ]
)

# Lucas pricing operator matrix A_ij = beta * Pi_ij * g_j^(1 - gamma)
A = beta * pi * (g ** (1.0 - gamma))
spectral_radius = float(np.max(np.abs(np.linalg.eigvals(A))))
print(f"Spectral radius rho(A): {spectral_radius:.4f}")

# Equilibrium price-dividend ratio: v = (I - A)^(-1) A 1
identity = np.eye(3)
v = np.linalg.solve(identity - A, A @ np.ones(3))
print("Price-dividend ratios v:", np.round(v, 4).tolist())

# Verification of Euler equation error across all states:
# E_i [ beta * (g_j)^(-gamma) * (v_j + 1) / v_i * g_j ] - 1 = 0
euler_lhs = (A @ (v + np.ones(3))) / v
max_euler_error = float(np.max(np.abs(euler_lhs - 1.0)))
print(f"Max absolute Euler error: {max_euler_error:.2e}")
