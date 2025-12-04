from cli.cli import start, hub


def run_cli():
    """Entry point wrapper that keeps the CLI flow predictable."""
    while True:
        save = start()
        if save is None:
            print("Exited start")
            return
        
        if hub(save) is None:
            print("Exited hub")
            return


if __name__ == "__main__":
    run_cli()
