from cli.cli import start, prehub, hub
import cli.prettyprint as pp

if __name__ == "__main__":
    x = start()
    while True:
        x = prehub(x)
        if x is None:
            print("Exited prehub")
            break

        if hub(x) is None:
            print("Exited hub")
            break
