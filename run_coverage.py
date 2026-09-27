"""
Запуск тестов с подсчётом покрытия и генерацией htmlcov.
Использование:
    python run_coverage.py
"""
import os
import subprocess
import sys


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    print("=" * 60)
    print("ЗАПУСК ТЕСТОВ С COVERAGE")
    print("=" * 60)

    run([sys.executable, '-m', 'coverage', 'run', 'manage.py', 'test', '--verbosity=2'])
    run([sys.executable, '-m', 'coverage', 'report', '-m'])
    run([sys.executable, '-m', 'coverage', 'html'])

    print("\n" + "=" * 60)
    print("HTML-отчёт создан: htmlcov/index.html")
    print("=" * 60)


if __name__ == '__main__':
    main()