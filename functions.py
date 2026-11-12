import pandas as pd

# Shared with simulation.py: the chart marks the shock period and the target.
shock_start: int = 5
pi_star: float = 2


def simulate(
    anchored: bool,
    periods: int = 20,
    shock_size: float = -2,
    a: float = 0.55,
    alpha: float = 0.3,
    phi_pi: float = 1.5,
    phi_y: float = 0.5,
    y_e: float = 0,
    A: float = 5,
    rho: float = 0.7
):
    """Simulate a demand shock under anchored or unanchored expectations."""

    # Variables
    r_star = (A - y_e) / a
    r_prev = r_star
    pi_prev = pi_star
    shock = 0

    # Results
    results = []

    for i in range(periods):
        if i == shock_start:
            shock = shock_size

        y = (A + shock) - (a * r_prev)

        if anchored:
            pi_e = pi_star
        else:
            pi_e = pi_prev

        pi = pi_e + (alpha * (y - y_e))
        r = r_star + (phi_pi*(pi - pi_star)) + (phi_y*(y-y_e))
        results.append((y, pi, r))
        r_prev = r
        pi_prev = pi
        shock = rho * shock

    return results


def df_results(results):
    return pd.DataFrame(results, columns=['Output', 'Inflation', 'Real Interest Rate'])
