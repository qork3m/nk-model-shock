import pandas as pd

PARAMS = {
    "shock_size": -2,
    "a": 0.55,
    "alpha": 0.3,
    "phi_pi": 1.5,
    "phi_y": 0.5,
    "y_e": 0,
    "A": 5,
    "rho": 0.7,
    "pi_star": 2,
    "shock_start": 5,
    "periods": 20,
}


def neutral_rate(params: dict = PARAMS):
    """Calculate the neutral real rate from the given parameters."""
    A = params["A"]
    y_e = params["y_e"]
    a = params["a"]
    r_star = (A - y_e) / a
    return r_star


def simulate(anchored: bool, params: dict = PARAMS):
    """
    Simulate a demand shock under anchored or unanchored expectations.
    params must contain: a, alpha, phi_pi, phi_y, y_e, A, rho,  pi_star, shock_size, shock_start, periods.
    """
    shock_size = params["shock_size"]
    a = params["a"]
    alpha = params["alpha"]
    phi_pi = params["phi_pi"]
    phi_y = params["phi_y"]
    y_e = params["y_e"]
    A = params["A"]
    rho = params["rho"]
    pi_star = params["pi_star"]
    shock_start = params["shock_start"]
    periods = params["periods"]

    # Variables
    r_star = neutral_rate(params=params)
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
