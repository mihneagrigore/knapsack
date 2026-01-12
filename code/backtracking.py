def knapsack_backtracking(items, capacity):

    n = len(items)
    max_value = 0
    best_solution = []

    def backtrack(index, current_weight, current_value, selected):
        nonlocal max_value, best_solution

        if index == n:
            if current_value > max_value:
                max_value = current_value
                best_solution = selected.copy()
            return

        backtrack(index + 1, current_weight, current_value, selected)

        weight, value = items[index]
        if current_weight + weight <= capacity:
            selected.append(index)
            backtrack(index + 1, current_weight + weight, current_value + value, selected)
            selected.pop()

    backtrack(0, 0, 0, [])
    return max_value, best_solution


def main():
    with open('input.txt', 'r') as f:
        n, w = map(int, f.readline().split())
        items = []
        for _ in range(n):
            weight, value = map(int, f.readline().split())
            items.append((weight, value))

    max_value, selected_indices = knapsack_backtracking(items, w)

    selected_indices_1based = [i + 1 for i in selected_indices]

    with open('output.txt', 'w') as f:
        f.write(f"{max_value}\n")
        f.write(' '.join(map(str, selected_indices_1based)) + '\n')

if __name__ == "__main__":
    main()
