import sys
from utils.cli import main_cli

if __name__ == "__main__":
    try:
        main_cli(sys.argv[1:])
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
