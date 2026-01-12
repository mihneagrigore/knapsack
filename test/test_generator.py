import random
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'solutions'))
from dp import knapsack_dp

def generate_test(test_num, n, max_weight, max_value, capacity_ratio=0.5):
    items = []
    total_weight = 0

    for _ in range(n):
        weight = random.randint(1, max_weight)
        value = random.randint(1, max_value)
        items.append((weight, value))
        total_weight += weight

    capacity = int(total_weight * capacity_ratio)
    capacity = max(1, capacity)

    test_dir = f"test_{test_num:03d}"
    os.makedirs(test_dir, exist_ok=True)

    input_path = os.path.join(test_dir, "input.txt")
    with open(input_path, 'w') as f:
        f.write(f"{n} {capacity}\n")
        for weight, value in items:
            f.write(f"{weight} {value}\n")

    max_value, selected_indices = knapsack_dp(items, capacity)

    expected_path = os.path.join(test_dir, "expected_output.txt")
    selected_indices_1based = [i + 1 for i in selected_indices]
    with open(expected_path, 'w') as f:
        f.write(f"{max_value}\n")
        f.write(' '.join(map(str, selected_indices_1based)) + '\n')

    return test_dir, n, capacity, max_value


def generate_all_tests():
    test_configs = []

    for i in range(1, 11):
        n = random.randint(5, 15)
        test_configs.append((i, n, 50, 100, random.uniform(0.3, 0.7)))

    for i in range(11, 21):
        n = random.randint(15, 25)
        test_configs.append((i, n, 100, 200, random.uniform(0.3, 0.7)))

    for i in range(21, 41):
        n = random.randint(25, 100)
        test_configs.append((i, n, 200, 500, random.uniform(0.3, 0.7)))

    for i in range(41, 61):
        n = random.randint(100, 500)
        test_configs.append((i, n, 500, 1000, random.uniform(0.3, 0.7)))

    for i in range(61, 81):
        n = random.randint(500, 1000)
        test_configs.append((i, n, 1000, 2000, random.uniform(0.3, 0.7)))

    for i in range(81, 91):
        n = random.randint(500, 1000)
        test_configs.append((i, n, 1000, 2000, random.uniform(0.3, 0.7)))

    for i in range(91, 101):
        n = random.randint(500, 1000)
        test_configs.append((i, n, 1000, 2000, random.uniform(0.3, 0.7)))

    print("Generare teste...")
    print("(Pentru fiecare test se calculează și soluția optimă cu DP)\n")

    for test_num, n, max_w, max_v, ratio in test_configs:
        test_dir, items_count, capacity, optimal_value = generate_test(test_num, n, max_w, max_v, ratio)
        print(f"Test {test_num:3d}: {items_count:5d} obiecte, capacitate {capacity:8d}, valoare optimă {optimal_value:8d} - {test_dir}")

    print(f"\nTotal: {len(test_configs)} teste generate cu soluții optime!")


if __name__ == "__main__":
    random.seed(42)
    generate_all_tests()
