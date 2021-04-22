from Core.LibressegeServerCore import LibressegeServerCore

if __name__ == "__main__":
    serverCore = LibressegeServerCore()
    serverCore.start("0.0.0.0", 9090)
    while True: serverCore.handler()
