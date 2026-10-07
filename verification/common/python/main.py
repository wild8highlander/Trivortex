"""Main entry point for Python verification."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import get_config, SECTION_NAMES


def main():
    section = int(sys.argv[sys.argv.index("--section") + 1]) if "--section" in sys.argv else 1
    preset = sys.argv[sys.argv.index("--preset") + 1] if "--preset" in sys.argv else "default"
    config = get_config(section, preset)
    print(f"Section {section}: {SECTION_NAMES.get(section, 'Unknown')}")
    print(f"Preset: {preset}, Config: {config}")
    print("Verification complete.")


if __name__ == "__main__":
    main()
