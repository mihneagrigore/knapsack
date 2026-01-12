import os
import shutil
import glob

def cleanup_tests():

    test_dirs = glob.glob("test_*")

    if not test_dirs:
        print("No test directories to delete.")
        return

    print(f"Found {len(test_dirs)} test directories.")
    print("Deleting...")

    deleted_count = 0
    error_count = 0

    for test_dir in sorted(test_dirs):
        try:
            if os.path.isdir(test_dir):
                shutil.rmtree(test_dir)
                deleted_count += 1
                print(f"  ✓ Deleted: {test_dir}")
        except Exception as e:
            error_count += 1
            print(f"Error deleting {test_dir}: {e}")

    print(f"\nSummary:")
    print(f"  Directories deleted: {deleted_count}")
    if error_count > 0:
        print(f"  Errors: {error_count}")

    report_files = glob.glob("results_*.txt") + glob.glob("test_results.txt") + glob.glob("execution_log.txt")
    if report_files:
        print(f"\nDeleting {len(report_files)} report files...")
        for report in report_files:
            try:
                os.remove(report)
                print(f"Deleted: {report}")
            except Exception as e:
                print(f"Error deleting {report}: {e}")


if __name__ == "__main__":
    response = input("Are you sure you want to delete all generated tests? (yes/no): ")
    if response.lower() in ['da', 'yes', 'y', 'd']:
        cleanup_tests()
        print("\nCleanup complete!")
    else:
        print("Operation cancelled.")
