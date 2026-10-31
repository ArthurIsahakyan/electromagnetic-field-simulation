# Electromagnetic Fields Simulator

A small NumPy and Matplotlib project for calculating and visualizing the electric field of point charges and the magnetic field of long straight wires carrying current perpendicular to the page.

## Features

- Electric and magnetic fields calculated by superposition.
- Separate electric, magnetic, and combined streamline views.
- Matplotlib buttons switch between the three views without editing source code.
- Finite-difference diagnostics for electrostatic curl and magnetostatic divergence.
- Small pytest suite checked against analytical field formulas.
- `physics.py` and `visualization.py` keep the original imports working.

## Physics and assumptions

For point charges in vacuum, the Coulomb field is

$$\vec E(\vec r)=\sum_i \frac{1}{4\pi\epsilon_0}q_i\frac{\vec r-\vec r_i}{|\vec r-\vec r_i|^3}.$$

For infinitely long wires normal to the xy plane,

$$\vec B(\vec r)=\sum_i \frac{\mu_0 I_i}{2\pi\rho_i^2}\left(-(y-y_i),\;x-x_i\right),$$

where positive current points out of the page. The calculations are static, use SI units, assume vacuum, and represent charges/wires as ideal sources. Near-source denominator floors avoid division by zero; results at the sources themselves are not physically meaningful.

The verification module uses second-order finite differences on the supplied coordinates. It reports maximum absolute and RMS residuals on interior points, omitting boundaries and configurable circular neighborhoods around ideal sources. Small nonzero residuals are expected from finite grid spacing and floating-point arithmetic; a small residual does not prove an exact physical law. The curl-zero check applies to electrostatics, not general time-varying electric fields. The divergence check assumes no variation along z.

## Install

Python 3.9 or newer is recommended.

```bash
python -m pip install -r requirements.txt
```

## Run

The default opens a combined field window with three mode buttons:

```bash
python main.py
```

Choose a mode at launch, or disable the buttons:

```bash
python main.py --mode electric
python main.py --mode magnetic --no-gui
python main.py --mode combined --no-gui
```

Run the numerical checks and display their maximum and RMS residuals:

```bash
python main.py --verify
```

Save a static view (useful on a headless machine):

```bash
python main.py --mode combined --save images/electric_magnetic_fields.png
```

![Combined electric and magnetic field example](images/electric_magnetic_fields.png)

## Examples

Standalone examples are in `examples/`:

```bash
python examples/electric_dipole.py
python examples/two_charges.py
python examples/current_carrying_wires.py
```

## Tests

The tests use Python's built-in `unittest`, so they can run even when `pytest`
is not installed:

```bash
python -m unittest discover -s tests -v
```

To use pytest instead, install the packages listed in `requirements.txt` first,
then run `python -m pytest`.

Tests cover point-charge direction and magnitude, superposition, the straight-wire result, finite-difference residuals, source/boundary masking, and invalid inputs.

## Project layout

```text
src/                 field calculations, visualization, and verification
examples/            runnable demonstrations
 tests/              automated numerical tests
images/              generated example figure
backups/              original files preserved before changes
main.py               command-line demo entry point
physics.py             compatibility exports for original calculations
visualization.py       compatibility exports for original plots
```
