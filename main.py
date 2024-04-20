from src.game import GAME

if __name__ == '__main__':
    status: int = GAME.start()
    print(status)