import argparse


def knapsack_bpso_solver(knapsack_max_weight, weights, values, n):
    return "To Be Continued..."


def knapsack_solver(W, wt, val, n):
    """Function from: https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/"""
    # Base Case
    if n == 0 or W == 0:
        return 0

    # If weight of the nth item is more than Knapsack of capacity
    # W, then this item cannot be included in the optimal solution
    if (wt[n - 1] > W):
        return knapsack_solver(W, wt, val, n - 1)

        # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(val[n - 1] + knapsack_solver(W - wt[n - 1], wt, val, n - 1),
                   knapsack_solver(W, wt, val, n - 1))


def main(args):
    values = eval(args.values)
    weights = eval(args.weights)
    knapsack_max_weight = args.max_weight
    print("Values: {0}".format(values))
    print("Weights: {0}".format(weights))
    print("Max_weight: {0}".format(knapsack_max_weight))
    n = len(values)
    bpso_solution = knapsack_bpso_solver(knapsack_max_weight, weights, values, n)
    non_bpso_solution = knapsack_solver(knapsack_max_weight, weights, values, n)
    print("BPSO Solution: {0}".format(bpso_solution))
    print("Non-BPSO Solution: {0}".format(non_bpso_solution))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--values', type=str, default="[60, 100, 120, 90, 11, 70]",
                        help='List containing the value of each item.')
    parser.add_argument('--weights', type=str, default="[10, 20, 30, 40, 50, 60]",
                        help='List containing the weight of each item.')
    parser.add_argument('--max_weight', type=int, default=100, help='Maximum weight sustained by the knapsack.')

    args = parser.parse_args()
    main(args)
