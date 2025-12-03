from cli.cli import start, prehub, hub


def run_cli():
    """Entry point wrapper that keeps the CLI flow predictable."""
    while True:
        choice = start()

        if choice == 0:
            print("Exited start")
            return

        save = prehub(choice)
        if save is None:
            print("Exited prehub")
            return

        if hub(save) is None:
            print("Exited hub")
            return


if __name__ == "__main__":
    run_cli()
