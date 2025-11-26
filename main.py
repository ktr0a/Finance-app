from cli.cli import start, prehub, hub
import cli.prettyprint as pp

if __name__ == "__main__":
    x1 = start()
    x2 = prehub(x1)
    x3 = hub(x2)
