# nk-model-shock

A three-equation New Keynesian model. It simulates a negative demand shock and
compares what happens when inflation expectations are anchored and when they
are not.

The model is not trying to measure a real shock. The shock size is an input I
choose. The output is the comparison between the two regimes.

## The model

IS curve:

```
y_t = A - a * r_(t-1)
```

Phillips curve:

```
pi_t = pi_e + alpha * (y_t - y_e)
```

Taylor rule:

```
r_t = r* + phi_pi * (pi_t - pi*) + phi_y * (y_t - y_e)
```

The real rate enters the IS curve with a one-period lag. A rate change today
does not move demand today: credit has to reprice and firms have to revise
budgets, and that takes time. The output gap enters the Phillips curve with no
lag, because a firm setting prices today can already see whether demand is
strong.

That lag is where the dynamics come from. Without it the model jumps straight
to equilibrium.

The neutral rate is not a free parameter. Setting the output gap to zero in the
IS curve gives:

```
r* = (A - y_e) / a
```

## The two regimes

One line is different between them:

- **Anchored:** `pi_e = pi*`. People expect the target whatever inflation does.
- **Unanchored:** `pi_e = pi_(t-1)`. People expect last period's inflation.

Everything else is the same.

## Parameters

| Parameter | Value | What it is |
|---|---|---|
| `a` | 0.55 | Interest sensitivity of demand |
| `alpha` | 0.3 | Slope of the Phillips curve |
| `phi_pi` | 1.5 | Taylor rule response to inflation |
| `phi_y` | 0.5 | Taylor rule response to the output gap |
| `pi_star` | 2 | Inflation target |
| `y_e` | 0 | Potential output, set to zero |
| `A` | 5 | Autonomous demand |
| `rho` | 0.7 | Persistence of the shock |

`phi_pi` has to be above 1. If the central bank raises rates less than
one-for-one with inflation, the real rate falls when inflation rises, policy
does not actually tighten, and the model does not settle.

I did not take `a` and `alpha` from data. I first ran the model with both set
to 1 and it blew up: output and inflation oscillated into the hundreds. I
lowered them until the oscillations died out. So these are values that keep the
model stable, not estimates of any economy.

## The shock

Demand falls by 2 in period 5, then decays:

```
shock_t = rho * shock_(t-1)
```

With `rho = 0.7` the shock goes -2.00, -1.40, -0.98, -0.69 and so on toward
zero. This is an AR(1) process.

The first version held the shock at full size for four periods and then
switched it off. That put a jump in demand on the period it ended, and some of
the oscillation in the results was coming from that jump instead of from the
model. With decay there is no end date to pick, and `rho` says how persistent
the shock is.

The shock is temporary. A permanent fall in `A` would also lower the neutral
rate, and since the Taylor rule keeps targeting the old `r*`, the chart would
end up showing the cost of a stale neutral rate instead of the cost of
unanchored expectations. That is a different question.

## Results

Both regimes take the same hit in period 5: output 2 below potential, inflation
0.6 points below target.

| | Anchored | Unanchored |
|---|---|---|
| Period 10, output gap / inflation | -0.16 / 1.95 | +0.23 / 1.33 |
| Period 19, output gap / inflation | -0.01 / 2.00 | +0.11 / 1.85 |

With anchored expectations inflation is back at target in about ten periods.
With unanchored expectations it is still below target fourteen periods later,
and by then the output gap has turned positive. The central bank closed the gap
and overshot it, and inflation still has not come back.

The output gap panel looks backwards at first: the unanchored line recovers
faster and goes positive. The rate panel explains it. Inflation falls further
when expectations are unanchored, so the Taylor rule cuts the real rate harder,
and that extra stimulus pulls demand back faster. The central bank is easing
more in the unanchored case and still cannot get inflation back to target.

The reason is that a fall in inflation becomes next period's expectation, which
pushes inflation down again. The disinflation outlives the shock that caused
it. The problem is not weak demand, so closing the output gap does not fix it.

## Running it

```bash
python simulation.py
```

`functions.py` has the model and a helper that splits the results into separate
series. `simulation.py` runs both scenarios and draws the chart.

## Limitations

- There is no lower bound on the interest rate.
- The shock size is a choice, not a measurement.
- Backward-looking expectations are a simplification. Real expectations sit
  somewhere between the two cases here.
- This is not a model of any country. The parameters were picked for stability.