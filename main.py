def show_menu():
    """Показать главное меню."""
    print("=" * 30)
    print("   ПОДЗЕМЕЛЬЕ")
    print("=" * 30)
    print("1. Новая игра")
    print("2. Выход")
    print("=" * 30)


def main():
    """Главный цикл игры."""
    while True:
        show_menu()
        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            print("\n[Новая игра пока не реализована]")
            input("Нажмите Enter для продолжения...")
        elif choice == "2":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
