# Copyright [2024] Elizabeth Huang & Esteban Baires
# SPDX-License-Identifier: MIT

import numpy as np
from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt

DEBUG = 0

@dataclass
class RocketState:
    """
    Class representing the rocket's state at a given time

    Attributes:
        altitude:   Height in meters
        velocity:   Velocity in m/s, where value < 0 means descent
        time:       Current time in seconds
    """
    altitude: float
    velocity: float 
    time: float

@dataclass
class Trajectory:
    """
    Class representing a rocket's trajectory, 
    represented as a list of states

    Attributes:
        states: Set of states that make up the maneuver
    """
    states: List[RocketState] = field(default_factory=list)

    def append(self, state):
        self.states.append(state)
        
def calculate_gravity(altitude):
    """
    Gravity calculation according to Newton's Law of Universal Gravitation.
    """
    G = 6.67430e-11  # Gravitational constant
    M = 7.34767309e22  # Moon's mass in kg
    R = 1737100  # Moon's radius in meters
    return -G * M / ((R + altitude) ** 2)

def simulate_landing(initial_height, initial_velocity, rocket_mass, max_thrust_newtons, tolerance, dt, velocity_change, height_change):
    """
    Vertical descent landing algorithm considering rocket mass
    
    Refs:
        (1) https://www.physicsclassroom.com/class/1dkin/Lesson-6/Kinematic-Equations
        (2) https://www.physicsclassroom.com/class/1DKin/Lesson-6/Kinematic-Equations-and-Free-Fall

    Args:
        initial_height: Initial height in meters
        initial_velocity: Initial vertical velocity (value < 0 means descent)
        rocket_mass: Rocket mass in kg
        max_thrust_newtons: Maximum thrust force in Newtons
        dt: Time step
    
    Returns:
        List of rocket states generated in a trajectory
    """
    current_state = RocketState(initial_height, initial_velocity, 0)
    trajectory = Trajectory()
    trajectory.append(current_state)

    # Convert maximum thrust to maximum acceleration based on rocket mass
    max_thrust = max_thrust_newtons / rocket_mass  # m/s^2
    
    while True:
        # End condition for maneuver
        if current_state.altitude <= 0:
            # If we touch the ground, end maneuver
            global solution_found
            solution_found = True
            break
            
        # Calculate gravity at current altitude
        g = calculate_gravity(current_state.altitude)
        
        # See (1), if we have that (v_f)^2 = (v_i)^2 + 2*a*d
        # then replacing v_f with 0 and rearranging to solve for d:
        required_distance = -current_state.velocity**2 / (2 * (max_thrust + g))
        # Calculate the distance needed to stop, based on maximum thrust

        # Using the same formula, this time we'll get the final velocity
        target_velocity = -np.sqrt((-current_state.velocity)**2 + 2 * -g * current_state.altitude) * velocity_change
        # Our target velocity is less than this, so it's reduced by a factor (velocity_change)

        # Calculate required thrust (in terms of acceleration)
        if current_state.altitude <= required_distance * height_change:
            # If within minimum range + extra height, decelerate at maximum
            thrust = max_thrust
        elif current_state.velocity < target_velocity:
            # If not going too fast, decelerate less
            thrust = max_thrust * 0.8
        else:
            # If none of the above, don't decelerate
            thrust = 0
            
        # Net acceleration (g is negative)
        acceleration = thrust + g
        
        # To avoid accelerating too much and starting to ascend, reduce thrust
        if (current_state.velocity + acceleration*dt) > 0:
            velocity_error = target_velocity - current_state.velocity
            acceleration = g + thrust * (velocity_error / abs(velocity_error))
            # Also reduce maximum thrust to increase granularity
            max_thrust = max_thrust / -g

        # New state with new velocity, altitude and time
        new_velocity = current_state.velocity + acceleration * dt
        new_height = current_state.altitude + new_velocity * dt
        new_time = current_state.time + dt

        current_state = RocketState(new_height, new_velocity, new_time)
        trajectory.append(current_state)
        
        # debug prints, activated with the variable
        if DEBUG:
            print("\n\n--------------------------DEBUG----------------------------------")
            print(f"Rocket mass: {rocket_mass} kg")
            print(f"Max thrust: {max_thrust_newtons} N")
            print(f"Max acceleration: {max_thrust} m/s²")
            print(f"g: {g}")
            print(f"required_distance: {required_distance}")
            print(f"target_velocity: {target_velocity}")
            print(f"current_state.altitude: {current_state.altitude}")
            print(f"current_state.velocity: {current_state.velocity}")
            print(f"acceleration: {acceleration}")
            print(f"new_velocity: {new_velocity}")
            print(f"new_height: {new_height}")
            print(f"new_time: {new_time}")
            print("------------------------------------------------------------------\n\n")
        
        # Safety break, doesn't change solution_found variable
        if current_state.time > 1000:
            break
            
    return trajectory
     
def plot_trajectory(trajectory):
    """
    Shows time and velocity of a trajectory in a pair of plots
    """
    import matplotlib.pyplot as plt
    
    times = [state.time for state in trajectory.states]
    heights = [state.altitude for state in trajectory.states]
    velocities = [state.velocity for state in trajectory.states]
    
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(times, heights)
    plt.title('Height vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(times, velocities)
    plt.title('Velocity vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def calculate_landing_cost(trajectory):
    """
    Calculates cost based on time and final velocity
    Lower cost = better landing
    """
    final_state = trajectory.states[-1]
    time_cost = final_state.time
    velocity_cost = abs(final_state.velocity)
    
    # Landing cost depends on velocity and maneuver time
    # velocity is twice as valuable as time
    return time_cost + 2 * velocity_cost


if __name__ == "__main__":
    global solution_found
    solution_found = False
    attempt = 0
    rocket_mass = 1000  # kg
    max_thrust = 20000  # N - enough to generate ~20 m/s^2 with given mass
    
    trajectories = []
    min_cost = -1.0
    solution_trajectory = None
    solution_attempt = -1
    optimal_dv = -1.0
    optimal_dh = -1.0

    velocity_change_range = np.arange(0.0, 1.0, 0.01)
    height_change_range = np.arange(1.0, 2.0, 0.01)
    
    # Iterate over all possible solutions
    for velocity_change in velocity_change_range:
        for height_change in height_change_range:
            # Run simulation with parameters
            trajectory = simulate_landing(
                initial_height=100,
                initial_velocity=-50,
                rocket_mass=rocket_mass,
                max_thrust_newtons=max_thrust,
                tolerance=0.5,
                dt=0.05,
                velocity_change=velocity_change,
                height_change=height_change
            )
            trajectories.append(trajectory)
            
            # Compare this solution's cost with minimum
            current_cost = calculate_landing_cost(trajectory)

            # Case when cycle just started
            if min_cost == -1.0:
                min_cost = current_cost
                solution_trajectory = trajectory
                solution_attempt = attempt
                optimal_dv = velocity_change
                optimal_dh = height_change
            else:
                # If solution is the best found, save it
                if current_cost < min_cost:
                    min_cost = current_cost
                    solution_trajectory = trajectory
                    solution_attempt = attempt
                    optimal_dv = velocity_change
                    optimal_dh = height_change

            attempt += 1

    final_state = solution_trajectory.states[-1]

    if solution_found:
        print(f"\nBest soft landing achieved in attempt {solution_attempt}!")
    else:
        print("\nNo suitable solution found after multiple attempts.")

    print(f"Landing time: {final_state.time:.4f} seconds")
    print(f"Landing velocity: {final_state.velocity:.4f} m/s")
    print(f"Landing cost: {calculate_landing_cost(solution_trajectory):.4f}")
    print(f"Velocity delta: {optimal_dv:.4f}")
    print(f"Height delta: {optimal_dh:.4f}")
    
    plot_trajectory(solution_trajectory)
