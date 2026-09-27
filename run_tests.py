"""Запуск тестов Django из файла.

Использование:
    python run_tests.py
"""
import os
import subprocess
import sys


def main():
    """Запускает тесты Django через manage.py test."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    print("=" * 60)
    print("ЗАПУСК ТЕСТОВ ИЗ ФАЙЛА run_tests.py")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, 'manage.py', 'test', '--verbosity=2'],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
