from ui import Application, MainWindow


def main():
    app = Application()
    window = MainWindow()
    # app_functions = AppFunctions(window)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()