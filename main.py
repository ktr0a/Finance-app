import cli.prompts as pr
from cli.cli import start, hub


def run_cli():
    """Entry point wrapper that keeps the CLI flow predictable."""
    while True:
        save = start()
        if save is None:
            print(pr.EXITED_START)
            return
        
        if hub(save) is None:
            print(pr.EXITED_HUB)
            return


if __name__ == "__main__":
    run_cli()
