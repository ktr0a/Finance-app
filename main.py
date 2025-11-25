from cli import start, prehub, hub

if __name__ == "__main__":
    choice = start()
    save = prehub(choice)
    hub(save)
