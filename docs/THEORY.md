# Theory and calculation notes

## Rotor kinematics

Revolutions per second are `n = RPM / 60`. Angular speed is `omega = 2*pi*n`.

## Shaft power

For measured shaft torque `Q`, mechanical shaft power is `P = Q*omega`. This is mechanical power at the measurement plane; it is not electrical input power.

## Non-dimensional coefficients

For propeller diameter `D`, air density `rho`, and freestream speed `V`:

- `J = V/(n*D)`
- `CT = T/(rho*n^2*D^4)`
- `CP = P/(rho*n^3*D^5)`

These definitions use revolutions per second, not angular speed, in the coefficient denominators.

## Propulsive efficiency

`eta = T*V/P`. At static conditions `V=0`, propulsive efficiency by this definition is zero, even though static thrust and power coefficients remain useful. A value greater than one is a warning to review measurement planes, sign conventions, units, and consistency of the operating point.

## Uncertainty

The package currently uses first-order propagation with independent inputs. For `P=Q*2*pi*RPM/60`, it computes:

`u_P^2 = (dP/dQ * u_Q)^2 + (dP/dRPM * u_RPM)^2`

Correlations are not represented in version 0.1. For a formal uncertainty budget, include calibration covariance, resolution, repeatability, environmental corrections, and correlations where applicable.

## Spectral analysis

The FFT routine removes the mean and applies a Hann window before forming a single-sided amplitude spectrum. The Welch estimate is a power spectral density estimate. They have different units and should not be compared numerically as though they were the same quantity.
