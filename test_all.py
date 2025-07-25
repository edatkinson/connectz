import os
import subprocess

def run_tests():
    test_dir = os.path.join(os.path.dirname(__file__), 'test_advanced')
    test_files = [f for f in os.listdir(test_dir) if f.endswith('.txt')]
    results = []
    for test_file in sorted(test_files):
        path = os.path.join(test_dir, test_file)
        try:
            result = subprocess.run(
                ['python3', 'connectz.py', path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=5
            )
            output = result.stdout.strip()
        except Exception as e:
            output = f'Error: {e}'
        results.append((test_file, output))
    print('Test Results:')
    for test_file, output in results:
        print(f'{test_file}: {output}')

if __name__ == '__main__':
    run_tests()
