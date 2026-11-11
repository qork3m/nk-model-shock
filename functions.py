pi_star = 2
shock_period = 5


def simulate(anchored, periods=20, shock_size=-2):
    # Parameters
    a = 0.55
    alpha = 0.3
    phi_pi = 1.5
    phi_y = 0.5
    y_e = 0
    A = 5
    rho = 0.7

    # Variables
    r_star = (A - y_e) / a
    r_prev = r_star
    pi_prev = pi_star
    shock = 0

    # Results
    results = []

    for i in range(periods):
        if i == shock_period:
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


def unpack_results(results):
    y_list = []
    pi_list = []
    r_list = []

    for y, pi, r in results:
        y_list.append(y)
        pi_list.append(pi)
        r_list.append(r)

    return y_list, pi_list, r_list
