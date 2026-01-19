def knapsack_dp(items, capacity):
    n = len(items)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]

            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)

    max_value = dp[n][capacity]

    selected_indices = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_indices.append(i - 1)
            w -= items[i - 1][0]

    selected_indices.reverse()
    return max_value, selected_indices


def main():
    with open('input.txt', 'r') as f:
        n, w = map(int, f.readline().split())
        items = []
        for _ in range(n):
            weight, value = map(int, f.readline().split())
            items.append((weight, value))

    max_value, selected_indices = knapsack_dp(items, w)

    selected_indices_1based = [i + 1 for i in selected_indices]

    with open('output.txt', 'w') as f:
        f.write(f"{max_value}\n")
        f.write(' '.join(map(str, selected_indices_1based)) + '\n')

if __name__ == "__main__":
    main()
