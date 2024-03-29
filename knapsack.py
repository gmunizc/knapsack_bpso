import argparse
import pyswarms as ps
import numpy as np
import datetime

knapsack_dict = {}


def knapsack_solver(W, wt, val, n):
    """Function from: https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/"""
    # Base Case
    if n == 0 or W == 0:
        return 0

    # If weight of the nth item is more than Knapsack of capacity
    # W, then this item cannot be included in the optimal solution
    if wt[n - 1] > W:
        return knapsack_solver(W, wt, val, n - 1)

        # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(val[n - 1] + knapsack_solver(W - wt[n - 1], wt, val, n - 1),
                   knapsack_solver(W, wt, val, n - 1))


def fitness_per_particle(mask):
    value = 9999999999
    weight = 0
    for idx, bit in enumerate(mask):
        value = value + bit * knapsack_dict["values"][idx]
        weight = weight + bit * knapsack_dict["weights"][idx]

    value = 1 / value

    if weight > knapsack_dict["max_weight"]:
        value = 9999999999*value*weight

    return value


def fitness_function(x):
    n_particles = x.shape[0]
    j = [fitness_per_particle(x[i]) for i in range(n_particles)]
    return np.array(j)


def bpso_solution(best_pos):
    sum_values = 0
    weight = 0
    for idx, bit in enumerate(best_pos):
        sum_values += bit * knapsack_dict["values"][idx]
        weight += + bit * knapsack_dict["weights"][idx]

    if weight > knapsack_dict["max_weight"]:
        sum_values = "Knapsack Exploded"

    return sum_values


def main(args):
    knapsack_dict["values"] = eval(args.values)
    knapsack_dict["weights"] = eval(args.weights)
    knapsack_dict["max_weight"] = args.max_weight

    # Set-up hyperparameters
    options = {'c1': args.c1, 'c2': args.c2, 'w': args.w, 'k': args.k, 'p': args.p}
    # Call instance of PSO
    dimensions = len(knapsack_dict["values"])
    optimizer = ps.discrete.BinaryPSO(n_particles=args.n_particles, dimensions=dimensions, options=options)
    # Perform optimization
    bpso_before = datetime.datetime.now()
    best_cost, best_pos = optimizer.optimize(fitness_function, iters=args.iters)
    bpso_after = datetime.datetime.now() - bpso_before
    non_bpso_before = datetime.datetime.now()
    non_bpso_solution = knapsack_solver(knapsack_dict["max_weight"], knapsack_dict["weights"],
                                        knapsack_dict["values"], len(knapsack_dict["values"]))
    non_bpso_after = datetime.datetime.now() - non_bpso_before

    print("BPSO Solution: {0}".format(bpso_solution(best_pos)))

    print("Time BPSO: {0}".format(bpso_after))
    print("Non-BPSO Solution: {0}".format(non_bpso_solution))
    print("Time Non-BPSO: {0}".format(non_bpso_after))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--values', type=str, default="[60, 100, 120, 90, 11, 70]",
                        help='List containing the value of each item.')
    parser.add_argument('--weights', type=str, default="[10, 20, 30, 40, 50, 60]",
                        help='List containing the weight of each item.')
    parser.add_argument('--max_weight', type=int, default=100, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--c1', type=float, default=0.5, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--c2', type=float, default=0.3, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--w', type=float, default=0.9, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--k', type=int, default=15, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--p', type=int, default=1, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--n_particles', type=int, default=30, help='Maximum weight sustained by the knapsack.')
    parser.add_argument('--iters', type=int, default=100, help='Maximum weight sustained by the knapsack.')

    args = parser.parse_args()
    main(args)
