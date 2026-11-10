def simulate(anchored, periods=20, shock_period=5, shock_size=2, shock_duration=4):
    # Parameters
    a = 0.55
    alpha = 0.3
    phi_pi = 1.5
    phi_y = 0.5
    pi_star = 2
    y_e = 0
    A = 5

    # Variables
    r_star = (A - y_e) / a
    r_prev = r_star
    pi_prev = pi_star

    # Results
    results = []
    for i in range(periods):
        if i >= shock_period and i < shock_period+shock_duration:
            A_t = A - shock_size
        else:
            A_t = A

        y = A_t - (a * r_prev)
        if anchored:
            pi_e = pi_star
        else:
            pi_e = pi_prev
        pi = pi_e + (alpha * (y - y_e))
        r = r_star + (phi_pi*(pi - pi_star)) + (phi_y*(y-y_e))
        results.append((y, pi, r))
        r_prev = r
        pi_prev = pi

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
