"""Тапсыру қосымшасын бірыңғай үлгімен қайта құру."""
import sys
from build_reports import main

if __name__ == "__main__":
    sys.argv[1:1] = ["--only", "submission-summary-kk"]
    main()
