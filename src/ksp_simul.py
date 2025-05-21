# Copyright [2024] Elizabeth Huang & Esteban Baires
# SPDX-License-Identifier: MIT

# Implementation of a landing algorithm for Kerbal Space Program using krpc
# Documentation for the mod used: https://krpc.github.io/krpc/index.html

import krpc  # module to connect with KSP
import time  # module to wait between maneuver steps
import numpy as np
DEBUG = 1

def calculate_gravity(altitude, mass, radius):
    """
    Calculation of gravity according to Newton's Law of Universal Gravitation.
    
    Args:
        mass: Mass of the celestial body
        radius: Radius at the equator of the celestial body
    """
    G = 6.67430e-11  # Gravitational constant
    return -G * mass / ((radius + altitude) ** 2)


def landing(initial_height, initial_velocity, rocket_mass, max_thrust_newtons, velocity_change, height_change, final_height, celestialBody, dt):
    """
    Vertical landing algorithm considering the rocket's mass
    
    Refs:
        (1) https://www.physicsclassroom.com/class/1dkin/Lesson-6/Kinematic-Equations
        (2) https://www.physicsclassroom.com/class/1DKin/Lesson-6/Kinematic-Equations-and-Free-Fall
        (3) https://krpc.github.io/krpc/index.html

    Args:
        initial_height: Initial height in meters
        initial_velocity: Vertical velocity at start, where a value < 0 means descending
        rocket_mass: Rocket mass in kg
        max_thrust_newtons: Maximum thrust force in Newtons
        max_thrust_newtons
        velocity_change: Sensitivity parameter applied to terminal velocity
        height_change: Sensitivity parameter applied to the minimum height needed for the rocket
        to stop
        celestialBody: CelestialBody object, see (3) for more info 
        dt: Time step
    
    Returns:
        True or False depending on whether the maneuver should continue or not
    """
    # If this is 0, it means the rocket has no active engines or it exploded
    if max_thrust_newtons == 0:
        return
    # Convert maximum thrust to maximum acceleration based on rocket mass
    max_thrust = max_thrust_newtons / rocket_mass  # m/s^2
    
    # End condition for the maneuver
    if initial_height <= final_height:
        # If we're very close to the ground, end the maneuver
        return False
        
    # Calculate gravity at current altitude
    g = calculate_gravity(initial_height, celestialBody.mass, celestialBody.equatorial_radius)
    
    # See (1), if we have (v_f)^2 = (v_i)^2 + 2*a*d
    # then replacing v_f with 0 and rearranging to solve for d:
    required_distance = initial_velocity**2 / (2 * (max_thrust + g))
    # Calculate the distance needed to stop, based on maximum thrust

    # Using the same formula, this time we'll get the final velocity
    # assuming we don't stop
    terminal_velocity = -np.sqrt((-initial_velocity)**2 + 2 * -g * initial_height) * velocity_change
    # Our target velocity is less than this, hence it's reduced by a factor

    # Calculation of required thrust (in terms of acceleration)
    if initial_height <= required_distance * height_change:
        # If we're within the minimum range + extra height, decelerate at maximum
        thrust = max_thrust
    elif -initial_velocity < terminal_velocity:
        # If we're not going too fast, decelerate less
        thrust = max_thrust * 0.8
    else:
        # If none of the above applies, don't decelerate
        thrust = 0
        
    # Net acceleration (g is negative)
    acceleration = thrust + g
    
    # To avoid accelerating too much and starting to ascend, we reduce thrust
    if (initial_velocity + acceleration*dt) > 0:
        velocity_error = terminal_velocity - initial_velocity
        acceleration = g + thrust * (velocity_error / abs(velocity_error))
        # Also reduce maximum thrust to increase granularity
        max_thrust = max_thrust / -g

    # Now execute the maneuver

    # Rocket thrust isn't immediate, so we must calculate burn time
    # Thrust proportion relative to max_thrust
    impulse = thrust/max_thrust

    # See (1), now we use v_f = v_i + a*t 
    # Solve for time

    impulse_time = abs(terminal_velocity) - abs(initial_velocity)
    if thrust > 0:
        impulse_time = impulse_time / abs(thrust)
        if impulse_time < 0:
            impulse_time = 0
        
        # Activate engines at the calculated range
        conn.space_center.active_vessel.control.throttle = impulse
        # The program reactivates until impulse time ends
        time.sleep(impulse_time)
        # Engines are deactivated
        conn.space_center.active_vessel.control.throttle = 0
    else:
        impulse_time = 0

    # Debug prints, activated with the variable
    if DEBUG:
        print("\n\n--------------------------DEBUG----------------------------------")
        print(f"Rocket mass: {rocket_mass} kg")
        print(f"Maximum thrust: {max_thrust_newtons} N")
        print(f"Maximum acceleration: {max_thrust} m/s^2")
        print(f"Thrust: {thrust} N")
        print(f"g: {g}")
        print(f"required_distance: {required_distance}")
        print(f"terminal_velocity: {terminal_velocity}")
        print(f"initial_height: {initial_height}")
        print(f"initial_velocity: {initial_velocity}")
        print(f"acceleration: {acceleration}")
        print(f"impulse_time: {impulse_time}")
        print(f"impulse: {impulse}")
        print(f"impulse_time: {impulse_time}")
        print("------------------------------------------------------------------\n\n")
    
    return True


if __name__ == "__main__":
    # Connects to the mod's server
    conn = krpc.connect(name='Unnecessary-Import')
    vessel = conn.space_center.active_vessel
    print(vessel.name)

    # Gets the celestial body object where the vessel is located, see (3) for more info
    celestialBody = vessel.orbit.body

    # Reference frame to get velocity relative to the landing body
    referenceFrame = conn.space_center.ReferenceFrame.create_hybrid(
        position = celestialBody.reference_frame,
        rotation = vessel.surface_reference_frame
    )

    # The landing function now returns True or False
    # ends when a landing is detected or something worse...
    while (
        landing(
            vessel.flight(referenceFrame).surface_altitude,
            vessel.flight(referenceFrame).vertical_speed,
            vessel.mass,
            vessel.max_vacuum_thrust,
            1.9,  # Velocity change, constant during maneuver
            1.0,  # Height change, constant during maneuver
            3.0, # Height at which the maneuver stops
            vessel.orbit.body, # CelestialBody object containing info about landing target
            dt = 1 # wait time
        )
    ):
        time.sleep(0.01) # waits for 1 second

    print("Maneuver completed!!!")
    # Disables automatic control upon landing
    vessel.control.sas = False

# Simulation results:
# Minmus Success: latitude 25, longitude 145, dv = 1.9, da = 1.0
# Minmus Failure: latitude 25, longitude 145, dv = 1.9, da = 0.8
