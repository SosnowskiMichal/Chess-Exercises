from ui import Application, MainWindow


def main() -> None:
    app = Application()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()