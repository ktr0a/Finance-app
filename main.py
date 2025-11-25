from cli.cli import start, prehub, hub

if __name__ == "__main__":
    hub(prehub(start()))
