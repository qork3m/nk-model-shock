import pandas as pd

PARAMS = {
    "demand_shock_size": -2,
    "supply_shock_size": 3,
    "a": 0.55,
    "alpha": 0.3,
    "phi_pi": 1.5,
    "phi_y": 0.5,
    "y_e": 0,
    "A": 5,
    "demand_rho": 0.7,
    "supply_rho": 0.5,
    "pi_star": 2,
    "demand_shock_start": 5,
    "supply_shock_start": 8,
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
    Simulate a demand shock and a cost_push shock under anchored or unanchored expectations.
    params must contain: a, alpha, phi_pi, phi_y, y_e, A, pi_star, periods, demand_shock_size, demand_shock_start, demand_rho, supply_shock_size, supply_shock_start, supply_rho.
    """
    demand_shock_size = params["demand_shock_size"]
    supply_shock_size = params["supply_shock_size"]
    a = params["a"]
    alpha = params["alpha"]
    phi_pi = params["phi_pi"]
    phi_y = params["phi_y"]
    y_e = params["y_e"]
    A = params["A"]
    demand_rho = params["demand_rho"]
    supply_rho = params["supply_rho"]
    pi_star = params["pi_star"]
    demand_shock_start = params["demand_shock_start"]
    supply_shock_start = params["supply_shock_start"]
    periods = params["periods"]

    # Variables
    r_star = neutral_rate(params=params)
    r_prev = r_star
    pi_prev = pi_star
    demand_shock = 0
    supply_shock = 0

    # Results
    results = []

    for i in range(periods):
        if i == demand_shock_start:
            demand_shock = demand_shock_size
        if i == supply_shock_start:
            supply_shock = supply_shock_size

        y = (A + demand_shock) - (a * r_prev)

        if anchored:
            pi_e = pi_star
        else:
            pi_e = pi_prev

        pi = pi_e + (alpha * (y - y_e)) + supply_shock
        r = r_star + (phi_pi*(pi - pi_star)) + (phi_y*(y-y_e))
        results.append((y, pi, r))
        r_prev = r
        pi_prev = pi
        demand_shock = demand_rho * demand_shock
        supply_shock = supply_rho * supply_shock

    return results


def df_results(results):
    return pd.DataFrame(results, columns=['Output', 'Inflation', 'Real Interest Rate'])
