from cli import start, ld_save, hub

if __name__ == "__main__":
    choice = start()
    save = ld_save(choice)
    hub(save)
