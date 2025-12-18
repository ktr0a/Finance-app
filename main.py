import cli.prompts as pr
from cli.cli import start, hub
from core.engine import build_engine_json


def run_cli():
    """Entry point wrapper that keeps the CLI flow predictable."""
    engine = build_engine_json()
    while True:
        save = start(engine)
        if save is None:
            print(pr.EXITED_START)
            return
        
        if hub(save, engine) is None:
            print(pr.EXITED_HUB)
            return


if __name__ == "__main__":
    run_cli()
