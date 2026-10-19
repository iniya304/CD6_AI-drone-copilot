# ArduPilot SITL: Human–AI Shared Control

A simulation-based project exploring human–AI shared control for obstacle avoidance using ArduPilot SITL and `pymavlink`.

## Overview

The project compares human-only control with shared control, which combines human commands and AI-generated obstacle-avoidance commands using an alpha-blending coefficient.

- **Environment:** ArduPilot Software-in-the-Loop (SITL)
- **Interface:** `pymavlink`
- **Control:** Velocity setpoints in the local North-East-Down frame

## Setup

1. Start ArduPilot SITL:
   ```bash
   cd ~/ardupilot/ArduCopter
   sim_vehicle.py -v ArduCopter --console
   ```

2. Activate the Python virtual environment:
   ```bash
   source ~/venv-ardupilot/bin/activate
   ```

3. Run scripts from the repository directory.

## Scripts

| Script | Purpose |
|---|---|
| `test_drone.py` | Basic connection, takeoff, and landing test |
| `test_move.py` | Tests northward movement using velocity setpoints |
| `test_shared.py` | Demonstrates human–AI command blending |
| `test_keyboard.py` | Keyboard-based human-in-the-loop control |
| `test_obstacle.py` | Virtual-obstacle shared-control experiment |
| `telemetry_reader.py` | Reads vehicle telemetry |

The obstacle script supports shared and manual modes. The `auto` option supplies a scripted human command.

## Experimental Results

These values are from existing SITL simulation runs and are preliminary.

| Metric | Human-only | Shared control |
|---|---:|---:|
| Minimum distance from obstacle centre | 0.99 m | 3.09 m |
| Recorded samples inside the 2 m radius | 23 | 0 |
| Approximate time inside the 2 m radius | 2.34 s | 0 s |

In the recorded shared-control run, the trajectory remained outside the defined 2 m obstacle-centre radius. The human-only run entered that radius.

The runs had