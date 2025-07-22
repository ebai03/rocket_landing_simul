# Copyright [2024] Elizabeth Huang & Esteban Baires
# SPDX-License-Identifier: MIT

# Basically all the imports needed are in bruteforce.py
from bruteforce import *

DEBUG = 0

if __name__ == "__main__":
    rocket_mass = 2641  # kg
    max_thrust = 20000  # N - enough to generate ~20 m/s^2 with the given mass

    # Test the simulation with selected parameters
    trajectory = simulate_landing(
        initial_height=5000,
        initial_velocity=0,
        rocket_mass=rocket_mass,
        max_thrust_newtons=max_thrust,
        tolerance=0.5,
        dt=0.05,
        velocity_change=0.5,  # Factor between [0, 1]
        height_change=1.5      # Factor between [1, 2]
    )
    
    final_state = trajectory.states[-1]

    print(f"Landing time: {final_state.time:.4f} seconds")
    print(f"Landing velocity: {final_state.velocity:.4f} m/s")
    print(f"Landing cost: {calculate_landing_cost(trajectory):.4f}")
    
    plot_trajectory(trajectory)