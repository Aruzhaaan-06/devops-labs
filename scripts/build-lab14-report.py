"""Бұрынғы команда атауы: бірыңғай академиялық жинақтаушыға бағыттайды."""
import sys
from build_reports import main

if __name__ == "__main__":
    sys.argv[1:1] = ["--only", "lab07-alerts-report"]
    main()
