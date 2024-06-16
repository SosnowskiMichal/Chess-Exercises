import re

from PyQt6.QtWidgets import QStackedWidget, QMessageBox

from data_managers import UserDataManager


class UIController:
    def __init__(self, main_window) -> None:
        self.main_window = main_window
        self.central_widget: QStackedWidget = main_window.central_widget
        self.user_data_manager = UserDataManager()
        self.current_user_id = 1

        self.initialize_board_theme()
        self.initialize_custom_practice_settings()
        self.connect_main_menu_signals()
        self.connect_practice_window_signals()
        self.connect_custom_practice_settings_signals()
        self.connect_statistics_window_signals()
        self.connect_settings_menu_signals()

    def initialize_board_theme(self) -> None:
        user_settings = self.user_data_manager.get_user_settings(self.current_user_id)
        board_style = user_settings.board_style
        piece_style = user_settings.piece_style
        self.main_window.practice_window.board_widget.set_style(board_style, piece_style)

    def initialize_custom_practice_settings(self) -> None:
        puzzle_manager = (
            self.main_window.practice_window.board_widget.board_controller.puzzle_manager
        )
        custom_practice_settings = self.main_window.custom_practice_settings
        min_rating, max_rating = puzzle_manager.get_rating_range()
        themes = puzzle_manager.get_puzzle_themes()
        themes = ['--all--'] + self.parse_db_themes(themes, list=True)
        custom_practice_settings.min_rating_value.setRange(min_rating, max_rating)
        custom_practice_settings.max_rating_value.setRange(min_rating, max_rating)
        custom_practice_settings.min_rating_value.setValue(min_rating)
        custom_practice_settings.max_rating_value.setValue(max_rating)
        custom_practice_settings.theme_value.addItems(themes)

    def connect_main_menu_signals(self) -> None:
        main_menu = self.main_window.main_menu
        main_menu.free_practice_button.clicked.connect(self.show_practice_window)
        main_menu.custom_practice_button.clicked.connect(self.show_custom_practice_settings)
        main_menu.statistics_button.clicked.connect(self.show_statistics_window)
        main_menu.settings_button.clicked.connect(self.show_settings_menu)
        main_menu.quit_button.clicked.connect(self.main_window.close)

    def connect_practice_window_signals(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.new_puzzle_button.clicked.connect(self.initialize_puzzle)
        practice_window.return_button.clicked.connect(self.close_practice_window)
        practice_window.board_widget.board_status_signal.connect(self.update_board_status)

    def connect_custom_practice_settings_signals(self) -> None:
        custom_practice_settings = self.main_window.custom_practice_settings
        custom_practice_settings.start_button.clicked.connect(
            self.initialize_custom_practice_window
        )
        custom_practice_settings.reset_choice_button.clicked.connect(
            self.reset_custom_practice_settings
        )
        custom_practice_settings.return_button.clicked.connect(self.show_main_menu)

    def connect_statistics_window_signals(self) -> None:
        statistics_window = self.main_window.statistics_window
        statistics_window.reset_progress_button.clicked.connect(self.reset_progress)
        statistics_window.return_button.clicked.connect(self.show_main_menu)

    def connect_settings_menu_signals(self) -> None:
        settings_menu = self.main_window.settings_menu
        settings_menu.save_button.clicked.connect(self.save_settings)
        settings_menu.return_button.clicked.connect(self.show_main_menu)

    def show_main_menu(self) -> None:
        widget = self.main_window.main_menu
        self.central_widget.setCurrentWidget(widget)
    
    def show_practice_window(self) -> None:
        widget = self.main_window.practice_window
        self.central_widget.setCurrentWidget(widget)

    def show_custom_practice_settings(self) -> None:
        widget = self.main_window.custom_practice_settings
        self.central_widget.setCurrentWidget(widget)

    # def show_time_modes_menu(self) -> None:
    #     widget = self.main_window.time_modes_menu
    #     self.central_widget.setCurrentWidget(widget)

    def show_statistics_window(self) -> None:
        widget = self.main_window.statistics_window
        self.central_widget.setCurrentWidget(widget)
        self.initialize_statistics()

    def show_settings_menu(self) -> None:
        widget = self.main_window.settings_menu
        self.central_widget.setCurrentWidget(widget)

    def save_settings(self) -> None:
        board_theme = None
        piece_theme = None
        # TODO: implement

    def initialize_custom_practice_window(self) -> None:
        custom_practice_settings = self.main_window.custom_practice_settings
        min_rating = custom_practice_settings.min_rating_value.value()
        max_rating = custom_practice_settings.max_rating_value.value()

        if min_rating > max_rating:
            self.show_error_popup_window('Invalid rating range')
            return
        
        theme = custom_practice_settings.theme_value.currentText()
        theme = None if theme == '--all--' else self.parse_theme(theme)
        board_controller = self.main_window.practice_window.board_widget.board_controller
        board_controller.set_puzzle_filters(min_rating, max_rating, theme)
        self.show_practice_window()

    def reset_custom_practice_settings(self) -> None:
        custom_practice_settings = self.main_window.custom_practice_settings
        min_rating = custom_practice_settings.min_rating_value.minimum()
        max_rating = custom_practice_settings.max_rating_value.maximum()
        custom_practice_settings.min_rating_value.setValue(min_rating)
        custom_practice_settings.max_rating_value.setValue(max_rating)
        custom_practice_settings.theme_value.setCurrentIndex(0)

    def initialize_puzzle(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.board_widget.initialize_puzzle()
        puzzle_rating, puzzle_themes = (
            practice_window.board_widget.get_current_puzzle_info()
        )
        if puzzle_rating is None or puzzle_themes is None:
            return
        practice_window.rating_value.setText(str(puzzle_rating))
        practice_window.themes_value.setText(self.parse_db_themes(puzzle_themes))

    def parse_db_themes(self, themes: str, list: bool = False) -> str:
        result = []
        if not list:
            themes = themes.split()
        for theme in themes:
            theme = re.sub(r'([A-Z0-9])', r' \1', theme)
            theme = ' '.join(word for word in theme.split()).capitalize()
            result.append(theme)
        return result if list else '\n'.join(result)
    
    def parse_theme(self, theme: str) -> str:
        theme = ''.join(word.capitalize() for word in theme.split())
        return theme[0].lower() + theme[1:]
    
    def update_board_status(self, status: int) -> None:
        practice_window = self.main_window.practice_window
        _, puzzle_themes = practice_window.board_widget.get_current_puzzle_info()
        if status == 0:
            status_text = 'Make a move!'
        elif status == 1:
            status_text = 'Correct move!'
        elif status == 2:
            status_text = 'Incorrect move\nTry again'
        elif status == 3:
            status_text = 'Puzzle solved!'
            self.user_data_manager.update_user_puzzle_statistics(
                self.current_user_id, puzzle_themes, False
            )
        elif status == 4:
            status_text = 'Puzzle solved on the first try!'
            self.user_data_manager.update_user_puzzle_statistics(
                self.current_user_id, puzzle_themes, True
            )
        elif status == -1:
            self.show_error_popup_window('No puzzles available')
            return
        practice_window.status_label.setText(status_text)

    def close_practice_window(self) -> None:
        practice_window = self.main_window.practice_window
        practice_window.board_widget.clear_board()
        practice_window.rating_value.clear()
        practice_window.themes_value.clear()
        practice_window.status_label.clear()
        practice_window.board_widget.board_controller.clear_puzzle_filters()
        self.show_main_menu()

    def initialize_statistics(self) -> None:
        statistics_window = self.main_window.statistics_window
        user_puzzle_statistics = (
            self.user_data_manager
            .get_user_puzzle_statistics(self.current_user_id)
        )
        user_theme_statistics = (
            self.user_data_manager
            .get_user_theme_statistics(self.current_user_id)
        )
        most_popular, best_percentage, worst_percentage = user_theme_statistics

        statistics_window.puzzles_played_value.setText(
            str(user_puzzle_statistics.puzzles_played)
        )
        statistics_window.puzzles_solved_value.setText(
            str(user_puzzle_statistics.puzzles_solved)
        )
        if user_puzzle_statistics.puzzles_played == 0:
            statistics_window.percent_solved_value.setText('-')
        else:
            percent_solved = (
                user_puzzle_statistics.puzzles_solved 
                / user_puzzle_statistics.puzzles_played * 100
            )
            statistics_window.percent_solved_value.setText(f'{percent_solved:.2f}%')

        if most_popular is None:
            statistics_window.most_popular_value.setText('-')
            statistics_window.best_percentage_value.setText('-')
            statistics_window.worst_percentage_value.setText('-')
        else:
            most_popular_text = '\n'.join(
                f'» {self.parse_db_themes(row[0].theme)} ({row[0].puzzles_played} played)'
                for row in most_popular
            )
            best_percentage_text = '\n'.join(
                f'» {self.parse_db_themes(row[0].theme)} ({row[1] * 100:.2f}%)'
                for row in best_percentage
            )
            worst_percentage_text = '\n'.join(
                f'» {self.parse_db_themes(row[0].theme)} ({row[1] * 100:.2f}%)'
                for row in worst_percentage
            )
            statistics_window.most_popular_value.setText(most_popular_text)
            statistics_window.best_percentage_value.setText(best_percentage_text)
            statistics_window.worst_percentage_value.setText(worst_percentage_text)

    def reset_progress(self) -> None:
        self.user_data_manager.reset_user_progress(self.current_user_id)
        self.initialize_statistics()

    def show_error_popup_window(self, text: str = None) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle('Error')
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()