import os
import matplotlib.pyplot as plt
from functions import simulate, df_results, PARAMS, neutral_rate

folder = os.path.dirname(os.path.abspath(__file__))


def graphic(params: dict, graphic_name: str, file_name: str):
    pi_star = params["pi_star"]
    y_e = params["y_e"]
    r_star = neutral_rate(params)
    demand_shock_size = params["demand_shock_size"]
    supply_shock_size = params["supply_shock_size"]
    demand_shock_start = params["demand_shock_start"]
    supply_shock_start = params["supply_shock_start"]

    results_anchored = simulate(anchored=True, params=params)
    results_unanchored = simulate(anchored=False, params=params)

    df_anchored = df_results(results_anchored)
    df_unanchored = df_results(results_unanchored)

    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 11))

    # Panel 1: Output gap
    axes[0].plot(df_anchored['Output'], label="Anchored", color="blue")
    axes[0].plot(df_unanchored['Output'], label="Unanchored", color="red")
    axes[0].axhline(y=y_e, color="black", linewidth=0.8)
    axes[0].set_title("Output Gap")
    axes[0].set_ylabel("Output gap")

    # Panel 2: Inflation
    axes[1].plot(df_anchored['Inflation'], label="Anchored", color="blue")
    axes[1].plot(df_unanchored['Inflation'], label="Unanchored", color="red")
    axes[1].axhline(y=pi_star, color="black", linewidth=0.8, linestyle=":")
    axes[1].set_title("Inflation")
    axes[1].set_ylabel("Inflation (%)")

    # Panel 3: Real Interest Rate
    axes[2].plot(df_anchored['Real Interest Rate'],
                 label="Anchored", color="blue")
    axes[2].plot(df_unanchored['Real Interest Rate'],
                 label="Unanchored", color="red")
    axes[2].axhline(y=r_star,
                    color="black", linewidth=0.8, linestyle=":")
    axes[2].set_title("Real Interest Rate")
    axes[2].set_ylabel("Rate (%)")
    axes[2].set_xlabel("Period")
    axes[2].set_xticks(range(0, len(df_unanchored), 2))

    # Shock marker on all three
    for ax in axes:
        if demand_shock_size != 0:
            ax.axvline(demand_shock_start, color="gray",
                       linestyle="--", label="Demand Shock")
        if supply_shock_size != 0:
            ax.axvline(supply_shock_start, color="green",
                       linestyle="--", label="Cost-Push Shock")

    axes[2].legend()

    fig.suptitle(graphic_name, fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(folder, file_name), dpi=150, bbox_inches="tight")
    plt.show()


demand_only = {**PARAMS, "supply_shock_size": 0}
cost_only = {**PARAMS, "demand_shock_size": 0, "supply_shock_start": 5}


graphic(demand_only, "Demand Shock: Anchored vs Unanchored Expectations",
        "demand_shock.png")
graphic(cost_only, "Cost-Push Shock: Anchored vs Unanchored Expectations",
        "cost_push_shock.png")
