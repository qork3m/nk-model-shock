import matplotlib.pyplot as plt


def simulate(anchored):
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
    for i in range(20):
        if i < 5:
            A_t = A
        else:
            A_t = A - 2
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


results_anchored = simulate(anchored=True)
results_unanchored = simulate(anchored=False)


y_anchored = []
pi_anchored = []
r_anchored = []
for y, pi, r in results_anchored:
    y_anchored.append(y)
    pi_anchored.append(pi)
    r_anchored.append(r)


y_unanchored = []
pi_unanchored = []
r_unanchored = []
for y, pi, r in results_unanchored:
    y_unanchored.append(y)
    pi_unanchored.append(pi)
    r_unanchored.append(r)


fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 11))

# Panel 1: Output gap
axes[0].plot(y_anchored, label="Anchored", color="blue")
axes[0].plot(y_unanchored, label="Unanchored", color="red")
axes[0].axhline(y=0, color="black", linewidth=0.8)
axes[0].set_title("Output Gap")
axes[0].set_ylabel("Output gap")
axes[0].legend()

# Panel 2: Inflation
axes[1].plot(pi_anchored, label="Anchored", color="blue")
axes[1].plot(pi_unanchored, label="Unanchored", color="red")
axes[1].axhline(y=2, color="black", linewidth=0.8, linestyle=":")
axes[1].set_title("Inflation")
axes[1].set_ylabel("Inflation (%)")
axes[1].legend()

# Panel 3: Policy rate
axes[2].plot(r_anchored, label="Anchored", color="blue")
axes[2].plot(r_unanchored, label="Unanchored", color="red")
axes[2].axhline(y=r_anchored[0], color="black", linewidth=0.8, linestyle=":")
axes[2].set_title("Policy Rate")
axes[2].set_ylabel("Rate (%)")
axes[2].set_xlabel("Period")
axes[2].legend()

# Shock marker on all three
for ax in axes:
    ax.axvline(x=5, color="gray", linestyle="--", alpha=0.7)

fig.suptitle("Negative Demand Shock: Anchored vs Unanchored Expectations",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
