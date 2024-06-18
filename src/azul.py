from game import Game


def menu():
    menu_art = r"""
      ___   _______   _ _       _____  _     _____      _____   ___  ___  ___ _____
     / _ \ |___  / | | | |     /  __ \| |   |_   _|    |  __ \ / _ \ |  \/  ||  ___|
    / /_\ \   / /| | | | |     | /  \/| |     | |______| |  \// /_\ \| .  . || |__
    |  _  |  / / | | | | |     | |    | |     | |______| | __ |  _  || |\/| ||  __|
    | | | |./ /__| |_| | |____ | \__/\| |_____| |_     | |_\ \| | | || |  | || |___
    \_| |_/\_____/\___/\_____/  \____/\_____/\___/      \____/\_| |_/\_|  |_/\____/
    """

    menu_options = ["Play Game", "Play Game with AI", "Exit"]
    print(menu_art)
    print(f"{" " * 34 } Welcome to Azul")
    print(f"{" " * 33 } Select an option:")
    print()
    for i, option in enumerate(menu_options, 1):
        print(f"{' ' * 33  } {i}. {option}")


def main():
    menu()
    option = input("Option: ")
    if option == "1":
        game = Game()
        game.play_game()
    elif option == "2":
        game = Game()
        game.play_with_ai()
    elif option == "3":
        print("Goodbye!")
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
