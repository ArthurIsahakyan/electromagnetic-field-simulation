"""Run the electromagnetic field demo and optional numerical diagnostics."""
import argparse
import numpy as np

from src.electric_field import electric_field
from src.magnetic_field import magnetic_field_wire
from src.verification import electric_curl_z, magnetic_divergence
from src.visualization import plot_fields


def demo_sources():
    charges = [{"q": 2e-6, "x": -0.03, "y": 0.0}, {"q": -2e-6, "x": 0.03, "y": 0.0}]
    wires = [{"I": 2.0, "x": -0.03, "y": 0.0}, {"I": -2.0, "x": 0.03, "y": 0.0}]
    return charges, wires


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("electric", "magnetic", "combined"), default="combined")
    parser.add_argument("--no-gui", action="store_true", help="do not add mode-switching buttons")
    parser.add_argument("--save", metavar="PATH", help="save the selected view instead of opening a window")
    parser.add_argument("--verify", action="store_true", help="print finite-difference Maxwell-law diagnostics")
    args = parser.parse_args()
    import matplotlib.pyplot as plt

    charges, wires = demo_sources()
    x = np.linspace(-0.1, 0.1, 200)
    y = np.linspace(-0.1, 0.1, 200)
    X, Y = np.meshgrid(x, y)
    Ex, Ey = electric_field(X, Y, charges)
    Bx, By = magnetic_field_wire(X, Y, wires)

    if args.verify:
        e = electric_curl_z(x, y, Ex, Ey, charges, exclusion_radius=0.025)
        b = magnetic_divergence(x, y, Bx, By, wires, exclusion_radius=0.025)
        print(f"curl(E)_z: max |residual|={e['max_abs']:.6g} V/m^2, RMS={e['rms']:.6g} V/m^2 ({e['n_valid']} points)")
        print(f"div(B): max |residual|={b['max_abs']:.6g} T/m, RMS={b['rms']:.6g} T/m ({b['n_valid']} points)")
        print("Residuals reflect finite grid spacing and floating-point error; they are not proof of exact law satisfaction.")

    if args.save:
        fig, _ = plot_fields(x, y, Ex, Ey, Bx, By, charges, wires, mode=args.mode, interactive=False, show=False)
        fig.savefig(args.save, dpi=180, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved {args.mode} view to {args.save}")
    else:
        plot_fields(x, y, Ex, Ey, Bx, By, charges, wires, mode=args.mode, interactive=not args.no_gui)


if __name__ == "__main__":
    main()


