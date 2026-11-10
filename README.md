# nk-model-shock

A three-equation New Keynesian model simulating how a negative demand shock
propagates through an economy under two different expectation regimes.

## The question

The question here is not "how big was the shock?" but "how do two different
expectation regimes change the way a shock plays out?" The shock size is not
observable and is not what this project tries to measure — it is a fixed input,
and the comparison between regimes is the output.

## The model

**IS curve** — demand side:

```
y_t = A - a * r_(t-1)
```

**Phillips curve** — prices:

```
pi_t = pi_e + alpha * (y_t - y_e)
```

**Taylor rule** — policy:

```
r_t = r* + phi_pi * (pi_t - pi*) + phi_y * (y_t - y_e)
```

The real interest rate is what matters here, and it enters the IS curve with a
**one-period lag**. A rate change today does not move demand today: credit has
to reprice, firms have to revise budgets, households have to reconsider large
purchases. That chain takes time. The output gap, by contrast, is
contemporaneous in the Phillips curve — a firm setting prices today can already
observe whether demand is strong, so there is nothing to wait for.

That single lag is where all of the model's dynamics come from. Without it the
system would jump straight to equilibrium and there would be nothing to watch.

The neutral rate is not a free parameter. In equilibrium the output gap is zero,
so the IS curve gives:

```
r* = (A - y_e) / a
```

This is the real rate that holds output at potential.

## The two regimes

The only difference between the two scenarios is one line — how expected
inflation is formed:

- **Anchored:** `pi_e = pi*`. Agents believe the central bank and expect the
  target regardless of what inflation actually does.
- **Unanchored (backward-looking):** `pi_e = pi_(t-1)`. Agents expect whatever
  happened last period, so a fall in inflation feeds into the next period's
  expectation and pushes inflation down further.

Everything else — parameters, shock, policy rule — is identical.

## Parameters

| Parameter | Value | What it is |
|---|---|---|
| `a` | 0.55 | Interest sensitivity of demand |
| `alpha` | 0.3 | Slope of the Phillips curve |
| `phi_pi` | 1.5 | Taylor rule response to inflation |
| `phi_y` | 0.5 | Taylor rule response to the output gap |
| `pi_star` | 2 | Inflation target |
| `y_e` | 0 | Potential output (normalised to zero) |
| `A` | 5 | Autonomous demand |

The Taylor coefficients are the values Taylor originally proposed. `phi_pi > 1`
is required — if the central bank responds less than one-for-one to inflation,
a rate rise does not actually tighten in real terms and the system does not
stabilise.

`a` and `alpha` were not picked first and tested later. The model was first run
with both set to 1, and it **diverged**: output and inflation oscillated with
growing amplitude until they ran into the hundreds. With pass-through that
strong, the central bank over-corrects every period and the lag turns each
correction into a larger error in the opposite direction. Lowering both until
the oscillations damped gave the current values. This is a stability exercise,
not a calibration to data — the parameters sit in a region where the model
behaves, not in a region estimated from any economy.

## The shock

Autonomous demand drops by 2 for four periods (periods 5 through 8), then
returns to its original level.

The shock is **temporary** by design. A permanent drop in `A` would also lower
the neutral rate, and since the Taylor rule keeps targeting the old `r*`, the
simulation would end up showing what a stale neutral rate does rather than what
anchoring does. That is a different question. With a temporary shock the neutral
rate is unchanged once the shock passes, so what the chart shows is the
expectation channel on its own.

## Running it

```bash
python simulation.py
```

`functions.py` holds the model (`simulate`) and a helper that splits the results
into separate series. `simulation.py` runs both scenarios and draws the chart.

## Limitations

- **No lower bound on the interest rate.** Nominal rates cannot go far below
  zero in reality; the model has no such constraint, so over a long enough
  simulation the rate can drift into territory that would not be possible.
- **The shock size is arbitrary.** Two units of autonomous demand is a choice,
  not a measurement.
- **Backward-looking expectations are a simplification.** Real expectations are
  neither fully anchored nor purely adaptive; these two cases are the endpoints
  of a spectrum, not descriptions of any actual economy.
- **This is not a model of any particular country.** The parameters were chosen
  for stability, and a 2% inflation target does not describe Türkiye.