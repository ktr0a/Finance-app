import finance_app.cli.ui.text as pr
from finance_app.cli.cli import start, hub
from finance_app.cli.bootstrap import build_cli_engine


def run_cli():
    """Entry point wrapper that keeps the CLI flow predictable."""
    engine = build_cli_engine()
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
