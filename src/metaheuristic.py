# Copyright [2024] Elizabeth Huang & Esteban Baires
# SPDX-License-Identifier: MIT

import numpy as np
import random
from bruteforce import *

def genetic_algorithm(initial_population, generations, initial_height, initial_velocity, rocket_mass, max_thrust_newtons, dt):
    """
    Implementation of the genetic algorithm to optimize rocket landing.
    
    Refs:
        (1) https://www.escom.ipn.mx/docs/oferta/matDidacticoISC2009/AGntcs/apuntesAlgsGeneticos.pdf
    
    Args:
        initial_population: Number of individuals in the initial population
        generations: Number of generations to run the genetic algorithm.
        initial_height: Initial height in meters from which the landing begins.
        initial_velocity: Initial vertical velocity in m/s.
        rocket_mass: Rocket mass in kilograms.
        max_thrust_newtons: Maximum engine thrust in Newtons.
        dt: Time step in seconds for the simulation.

    Returns:
        best_solution: Rocket trajectory with the best found parameters.
        best_cost: Cost associated with the best solution, based on landing time and final velocity.
    """
    
    # Initialize the population with random values for velocity_change and height_change
    population = [(np.random.uniform(), np.random.uniform(1.0, 2.0)) for _ in range(initial_population)]
    best_cost = float('inf')  # Track the best cost (lower is better)
    best_solution = None  # Store the trajectory corresponding to the best solution

    for gen in range(generations):
        print(f"Generation {gen + 1}/{generations}")  # Debug: show current generation
        evaluations = []  # List to store each individual's evaluation

        for id, individual in enumerate(population):
            velocity_change, height_change = individual
            # Simulate landing with the individual's parameters
            trajectory = simulate_landing(initial_height, initial_velocity, rocket_mass, max_thrust_newtons, 0.5, dt, velocity_change, height_change)
            # Calculate the trajectory cost
            cost = calculate_landing_cost(trajectory)
            evaluations.append((individual, cost, trajectory))  # Save the individual, its cost, and trajectory
            print(f"Individual {id + 1}: velocity_change={velocity_change:.4f}, height_change={height_change:.4f}, cost={cost:.4f}")  # Debug: individual details

        # Sort individuals by their cost (lower cost is better)
        evaluations.sort(key=lambda x: x[1])
        best_individual_gen = evaluations[0]
        print(f"  Best cost this generation: {best_individual_gen[1]:.4f}")  # Debug: generation's best cost

        # Update the best solution found so far
        if best_individual_gen[1] < best_cost:
            best_cost = best_individual_gen[1]
            best_solution = best_individual_gen[2]
            print(f"New global best solution found. Cost: {best_cost:.4f}")  # Debug: new best solution

        # Select the top 50% of the population
        population = [x[0] for x in evaluations[:len(population)//2]]

        # Generate the next generation
        new_population = population[:]
        while len(new_population) < initial_population:
            # Randomly select two parents for crossover
            father = random.choice(population)
            mother = random.choice(population)
            # Combine parent values (simple arithmetic mean)
            child = ((father[0] + mother[0]) / 2, (father[1] + mother[1]) / 2)
            # Apply mutation with a small probability
            if random.random() < 0.1:
                child = (child[0] + np.random.uniform(-0.1, 0.1), child[1] + np.random.uniform(-0.1, 0.1))
            new_population.append(child)

        # Replace current population with the new one
        population = new_population

    print(f"Final best solution found: cost={best_cost:.4f}")  # Debug: final best solution cost
    return best_solution, best_cost

if __name__ == "__main__":
    # Define the initial problem parameters
    initial_height = 100
    initial_velocity = -50
    rocket_mass = 1000
    max_thrust = 20000
    dt = 0.05

    # Run the genetic algorithm to find the best landing trajectory
    best_trajectory, best_cost = genetic_algorithm(
        initial_population = 20,
        generations = 50,  # Number of generations to simulate
        initial_height = initial_height,
        initial_velocity = initial_velocity,
        rocket_mass = rocket_mass,
        max_thrust_newtons = max_thrust,
        dt = dt
    )

    # Get the rocket's final state after landing
    final_state = best_trajectory.states[-1]
    # Print the landing results
    print(f"Landing time: {final_state.time:.4f} seconds")
    print(f"Final altitude: {final_state.altitude:.2f} m")
    print(f"Final velocity: {final_state.velocity:.2f} m/s")
    print(f"Landing cost: {best_cost:.2f}")

    # Plot the complete landing trajectory
    plot_trajectory(best_trajectory)
