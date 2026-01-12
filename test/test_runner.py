import os
import sys
import time
import shutil
import signal
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'solutions'))

from backtracking import knapsack_backtracking
from dp import knapsack_dp
from greedy_partial_result import knapsack_greedy


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("Timeout")


def read_input(filepath):
    with open(filepath, 'r') as f:
        n, capacity = map(int, f.readline().split())
        items = []
        for _ in range(n):
            weight, value = map(int, f.readline().split())
            items.append((weight, value))
    return items, capacity


def read_expected_output(filepath):
    try:
        with open(filepath, 'r') as f:
            expected_value = int(f.readline().strip())
            return expected_value
    except (FileNotFoundError, ValueError):
        return None


def verify_solution(items, capacity, selected_indices, claimed_value):
    total_weight = 0
    total_value = 0

    for idx in selected_indices:
        if idx < 0 or idx >= len(items):
            return False, "Index invalid"

        weight, value = items[idx]
        total_weight += weight
        total_value += value

    if total_weight > capacity:
        return False, f"Greutate depășită: {total_weight} > {capacity}"

    if total_value != claimed_value:
        return False, f"Valoare incorectă: {total_value} != {claimed_value}"

    return True, "OK"


def run_solution(solution_func, items, capacity, timeout=300):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        start_time = time.time()
        max_value, selected_indices = solution_func(items, capacity)
        end_time = time.time()

        signal.alarm(0)

        elapsed = end_time - start_time
        return max_value, selected_indices, elapsed, "OK"
    except TimeoutError:
        signal.alarm(0)  # Cancel the alarm
        elapsed = time.time() - start_time
        return None, None, elapsed, "TIMEOUT"
    except Exception as e:
        signal.alarm(0)  # Cancel the alarm
        return None, None, 0, f"ERROR: {str(e)}"


def run_test(test_num, test_dir):
    input_path = os.path.join(test_dir, "input.txt")
    expected_output_path = os.path.join(test_dir, "expected_output.txt")

    if not os.path.exists(input_path):
        return None

    items, capacity = read_input(input_path)
    expected_value = read_expected_output(expected_output_path)
    n = len(items)

    results = {
        'test_num': test_num,
        'n': n,
        'capacity': capacity,
        'expected_value': expected_value,
        'solutions': {}
    }

    print(f"  Backtracking...", end='', flush=True)
    value, indices, elapsed, status = run_solution(knapsack_backtracking, items, capacity, timeout=60)

    if status == "OK":
        valid, msg = verify_solution(items, capacity, indices, value)

        # Compară cu expected_output.txt
        if expected_value is not None:
            if value == expected_value:
                correctness = "CORRECT"
            else:
                correctness = f"WRONG (expected {expected_value}, got {value})"
        else:
            correctness = "NO_EXPECTED_OUTPUT"

        print(f" {elapsed:.4f}s - Valoare: {value} - {msg} - {correctness}")
    else:
        valid = False
        msg = status
        correctness = status
        print(f" {status}")

    results['solutions']['backtracking'] = {
        'value': value,
        'indices': indices,
        'time': elapsed,
        'status': status,
        'valid': valid,
        'correctness': correctness if status == "OK" else status
    }

    print(f"  DP...", end='', flush=True)
    value_dp, indices_dp, elapsed_dp, status_dp = run_solution(knapsack_dp, items, capacity, timeout=300)

    if status_dp == "OK":
        valid_dp, msg_dp = verify_solution(items, capacity, indices_dp, value_dp)

        # Compară cu expected_output.txt
        if expected_value is not None:
            if value_dp == expected_value:
                correctness = "CORRECT"
            else:
                correctness = f"WRONG (expected {expected_value}, got {value_dp})"
        else:
            correctness = "NO_EXPECTED_OUTPUT"

        print(f" {elapsed_dp:.4f}s - Valoare: {value_dp} - {msg_dp} - {correctness}")
    else:
        valid_dp = False
        correctness = status_dp
        print(f" {status_dp}")

    results['solutions']['dp'] = {
        'value': value_dp,
        'indices': indices_dp,
        'time': elapsed_dp,
        'status': status_dp,
        'valid': valid_dp,
        'correctness': correctness if status_dp == "OK" else status_dp
    }

    print(f"  Greedy...", end='', flush=True)
    value_greedy, indices_greedy, elapsed_greedy, status_greedy = run_solution(knapsack_greedy, items, capacity, timeout=300)

    if status_greedy == "OK":
        valid_greedy, msg_greedy = verify_solution(items, capacity, indices_greedy, value_greedy)

        reference_value = expected_value
        if reference_value is None:
            if status_dp == "OK":
                reference_value = value_dp
            elif results['solutions']['backtracking']['value'] is not None:
                reference_value = results['solutions']['backtracking']['value']

        if reference_value is not None:
            if value_greedy == reference_value:
                correctness_greedy = "OPTIMAL"
            else:
                percentage = (value_greedy / reference_value * 100) if reference_value > 0 else 0
                correctness_greedy = f"SUBOPTIMAL ({percentage:.1f}% din optim)"
        else:
            correctness_greedy = "NO_EXPECTED_OUTPUT"

        print(f" {elapsed_greedy:.4f}s - Valoare: {value_greedy} - {msg_greedy} - {correctness_greedy}")
    else:
        valid_greedy = False
        correctness_greedy = status_greedy
        print(f" {status_greedy}")

    results['solutions']['greedy'] = {
        'value': value_greedy,
        'indices': indices_greedy,
        'time': elapsed_greedy,
        'status': status_greedy,
        'valid': valid_greedy,
        'correctness': correctness_greedy if status_greedy == "OK" else status_greedy
    }

    return results


def run_all_tests(start_test=1, end_test=100):
    all_results = []

    print(f"\n{'='*80}")
    print(f"Rulare teste {start_test}-{end_test}")
    print(f"Backtracking va fi oprit după 1 minut (timeout)")
    print(f"{'='*80}\n")

    for test_num in range(start_test, end_test + 1):
        test_dir = f"test_{test_num:03d}"

        if not os.path.exists(test_dir):
            print(f"Test {test_num:3d}: NU EXISTĂ")
            continue

        print(f"\nTest {test_num:3d} ({test_dir}):")
        result = run_test(test_num, test_dir)

        if result:
            all_results.append(result)

    return all_results


def generate_report(results, output_file="test_results.txt"):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write(" "*30 + "RAPORT TESTARE KNAPSACK\n")
        f.write("="*100 + "\n\n")

        total_tests = len(results)
        f.write(f"Total teste rulate: {total_tests}\n\n")

        for algo in ['backtracking', 'dp', 'greedy']:
            f.write(f"\n{'='*100}\n")
            f.write(f"ALGORITM: {algo.upper()}\n")
            f.write(f"{'='*100}\n\n")

            ok_count = sum(1 for r in results if r['solutions'][algo]['status'] == 'OK')
            error_count = sum(1 for r in results if r['solutions'][algo]['status'].startswith('ERROR'))
            timeout_count = sum(1 for r in results if r['solutions'][algo]['status'] == 'TIMEOUT')
            skipped_count = sum(1 for r in results if r['solutions'][algo]['status'] == 'SKIPPED')

            f.write(f"Teste OK: {ok_count}/{total_tests}\n")
            f.write(f"Teste ERROR: {error_count}/{total_tests}\n")
            f.write(f"Teste TIMEOUT: {timeout_count}/{total_tests}\n")
            f.write(f"Teste SKIPPED: {skipped_count}/{total_tests}\n\n")

            times = [r['solutions'][algo]['time'] for r in results if r['solutions'][algo]['status'] == 'OK']
            if times:
                f.write(f"Timp mediu: {sum(times)/len(times):.4f}s\n")
                f.write(f"Timp minim: {min(times):.4f}s\n")
                f.write(f"Timp maxim: {max(times):.4f}s\n\n")

        f.write(f"\n{'='*100}\n")
        f.write("DETALII TESTE\n")
        f.write(f"{'='*100}\n\n")

        for result in results:
            test_num = result['test_num']
            n = result['n']
            capacity = result['capacity']

            f.write(f"\nTest {test_num:3d}: n={n:5d}, capacitate={capacity:8d}\n")
            f.write(f"{'-'*100}\n")

            for algo in ['backtracking', 'dp', 'greedy']:
                sol = result['solutions'][algo]
                f.write(f"  {algo.upper():15s}: ", )

                if sol['status'] == 'OK':
                    f.write(f"Valoare={sol['value']:8d}, Timp={sol['time']:8.4f}s, ")
                    f.write(f"Correctness={sol.get('correctness', 'N/A')}\n")
                else:
                    f.write(f"{sol['status']}\n")

        f.write(f"\n{'='*100}\n")
        f.write("COMPARAȚIE TIMPURI DE EXECUȚIE\n")
        f.write(f"{'='*100}\n\n")
        f.write(f"{'Test':<8} {'n':<8} {'Backtracking':<15} {'DP':<15} {'Greedy':<15}\n")
        f.write(f"{'-'*100}\n")

        for result in results:
            test_num = result['test_num']
            n = result['n']

            bt_time = result['solutions']['backtracking']['time']
            dp_time = result['solutions']['dp']['time']
            gr_time = result['solutions']['greedy']['time']

            bt_str = f"{bt_time:.4f}s" if result['solutions']['backtracking']['status'] == 'OK' else result['solutions']['backtracking']['status']
            dp_str = f"{dp_time:.4f}s" if result['solutions']['dp']['status'] == 'OK' else result['solutions']['dp']['status']
            gr_str = f"{gr_time:.4f}s" if result['solutions']['greedy']['status'] == 'OK' else result['solutions']['greedy']['status']

            f.write(f"{test_num:<8} {n:<8} {bt_str:<15} {dp_str:<15} {gr_str:<15}\n")

    print(f"\n\nRaport salvat în: {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Rulează teste pentru problema knapsack')
    parser.add_argument('--start', type=int, default=1, help='Testul de start')
    parser.add_argument('--end', type=int, default=100, help='Testul final')
    parser.add_argument('--report', type=str, default='test_results.txt',
                       help='Fișierul pentru raport')

    args = parser.parse_args()

    results = run_all_tests(args.start, args.end)

    if results:
        generate_report(results, args.report)
    else:
        print("\nNu s-au rulat teste!")


if __name__ == "__main__":
    main()
