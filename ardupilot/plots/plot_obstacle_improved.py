import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

def load_log(filename):
    with open(RESULTS / filename, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"No data in {filename}")
    return {key: np.array([float(row[key]) for row in rows])
            for key in rows[0]}

manual = load_log("obstacle_manual_log.csv")
shared = load_log("obstacle_shared_log.csv")

obstacle_north, obstacle_east = 15.0, 1.0
radius, safe_zone = 2.0, 7.0

fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# 1. Top-down trajectories
ax[0].plot(manual["east"], manual["north"], "r-", label="Human-only")
ax[0].plot(shared["east"], shared["north"], "g-", label="Shared control")
ax[0].add_patch(plt.Circle(
    (obstacle_east, obstacle_north), radius,
    color="black", alpha=0.35, label="Obstacle radius"
))
ax[0].add_patch(plt.Circle(
    (obstacle_east, obstacle_north), safe_zone,
    fill=False, linestyle="--", color="gray", label="Avoidance zone"
))
ax[0].set_xlabel("East (m)")
ax[0].set_ylabel("North (m)")
ax[0].set_title("Drone trajectories")
ax[0].set_aspect("equal", adjustable="datalim")
ax[0].grid(True, alpha=0.3)
ax[0].legend(fontsize=8)

# 2. Distance from obstacle centre
ax[1].plot(manual["t"], manual["dist_obs"], "r-", label="Human-only")
ax[1].plot(shared["t"], shared["dist_obs"], "g-", label="Shared control")
ax[1].axhline(radius, color="black", linestyle="--",
              label="2 m radius threshold")
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("Distance (m)")
ax[1].set_title("Obstacle clearance")
ax[1].grid(True, alpha=0.3)
ax[1].legend(fontsize=8)

# 3. Shared-control alpha
ax[2].plot(shared["t"], shared["alpha"], color="purple")
ax[2].set_ylim(-0.05, 1.05)
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Alpha")
ax[2].set_title("Shared-control blending coefficient")
ax[2].grid(True, alpha=0.3)

fig.suptitle(
    "ArduPilot SITL: Human-only vs Shared Control\n"
    "Existing runs; initial logged human command = 1.5 m/s",
    fontsize=13
)
fig.tight_layout()

output = RESULTS / "obstacle_comparison_improved.png"
fig.savefig(output, dpi=180, bbox_inches="tight")
plt.close(fig)

print(f"Saved plot: {output}")
print("\nExisting-run metrics (not repeated-trial statistics):")

for name, data in [("Human-only", manual), ("Shared control", shared)]:
    inside = data["dist_obs"] < radius
    duration_inside = np.sum(
        np.diff(data["t"]) * inside[:-1]
    ) if len(data["t"]) > 1 else 0.0

    print(f"\n{name}")
    print(f"  Samples: {len(data['t'])}")
    print(f"  Duration: {data['t'][-1] - data['t'][0]:.2f} s")
    print(f"  Minimum centre distance: {data['dist_obs'].min():.2f} m")
    print(f"  Samples below 2 m: {inside.sum()}")
    print(f"  Approx. time below 2 m: {duration_inside:.2f} s")
    print(f"  Final north/east: {data['north'][-1]:.2f}, "
          f"{data['east'][-1]:.2f} m")

print("\nNote: the two existing runs are not necessarily a controlled,")
print("repeatable comparison. Interpret their results cautiously.")
