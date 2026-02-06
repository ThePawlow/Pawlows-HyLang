#!/usr/bin/env python
import argparse
from cli.main import Cli
from gui.main import Gui


def main():
    parser = argparse.ArgumentParser(description="HyLang - GUI or CLI")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--input", "-i", type=str, help="Input file (CLI mode)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.cli:
        cli = Cli(args)
        cli.run()
    else:
        app = Gui()
        app.mainloop()


if __name__ == "__main__":
    main()
