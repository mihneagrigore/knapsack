def knapsack_greedy(items, capacity):
    n = len(items)

    indexed_items = [(i, items[i][0], items[i][1], items[i][1] / items[i][0])
                     for i in range(n)]

    indexed_items.sort(key=lambda x: x[3], reverse=True)

    total_value = 0
    current_weight = 0
    selected_indices = []

    for idx, weight, value, _ in indexed_items:
        if current_weight + weight <= capacity:
            selected_indices.append(idx)
            current_weight += weight
            total_value += value

    selected_indices.sort()

    return total_value, selected_indices


def main():
    with open('input.txt', 'r') as f:
        n, w = map(int, f.readline().split())
        items = []
        for _ in range(n):
            weight, value = map(int, f.readline().split())
            items.append((weight, value))

    total_value, selected_indices = knapsack_greedy(items, w)

    selected_indices_1based = [i + 1 for i in selected_indices]

    with open('output.txt', 'w') as f:
        f.write(f"{total_value}\n")
        f.write(' '.join(map(str, selected_indices_1based)) + '\n')

if __name__ == "__main__":
    main()
