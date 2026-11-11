import matplotlib.pyplot as plt
from functions import simulate, unpack_results, pi_star, shock_period
import os


folder = os.path.dirname(os.path.abspath(__file__))


results_anchored = simulate(anchored=True)
results_unanchored = simulate(anchored=False)


y_anchored, pi_anchored, r_anchored = unpack_results(results_anchored)
y_unanchored, pi_unanchored, r_unanchored = unpack_results(results_unanchored)


fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 11))

# Panel 1: Output gap
axes[0].plot(y_anchored, label="Anchored", color="blue")
axes[0].plot(y_unanchored, label="Unanchored", color="red")
axes[0].axhline(y=0, color="black", linewidth=0.8)
axes[0].set_title("Output Gap")
axes[0].legend()

# Panel 2: Inflation
axes[1].plot(pi_anchored, label="Anchored", color="blue")
axes[1].plot(pi_unanchored, label="Unanchored", color="red")
axes[1].axhline(y=pi_star, color="black", linewidth=0.8, linestyle=":")
axes[1].set_title("Inflation")
axes[1].set_ylabel("Inflation (%)")

# Panel 3: Real Interest Rate
axes[2].plot(r_anchored, label="Anchored", color="blue")
axes[2].plot(r_unanchored, label="Unanchored", color="red")
axes[2].axhline(y=r_anchored[0], color="black", linewidth=0.8, linestyle=":")
axes[2].set_title("Real Interest Rate")
axes[2].set_ylabel("Rate (%)")
axes[2].set_xlabel("Period")
axes[2].set_xticks(range(0, len(y_anchored), 2))

# Shock marker on all three
for ax in axes:
    ax.axvline(shock_period, color="gray", linestyle="--")

fig.suptitle("Negative Demand Shock: Anchored vs Unanchored Expectations",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(folder, "shock_simulation.png"),
            dpi=150, bbox_inches="tight")
plt.show()
