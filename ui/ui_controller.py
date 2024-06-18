import os
import re

from typing import List, TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

from data_managers import UserDataManager

if TYPE_CHECKING:
    from main_window import MainWindow


class UIController:
    def __init__(self, main_window: 'MainWindow') -> None:
        self.main_window = main_window
        self.central_widget = main_window.central_widget
        self.user_data_manager = UserDataManager()
        self.current_user_id = 1

        self.initialize_board_theme()
        self.initialize_custom_puzzles_settings()
        self.initialize_settings_menu()

        self.connect_main_menu_signals()
        self.connect_puzzles_window_signals()
        self.connect_custom_puzzles_settings_signals()
        self.connect_statistics_window_signals()
        self.connect_settings_menu_signals()

    def initialize_board_theme(self) -> None:
        user_settings = self.user_data_manager.get_user_settings(self.current_user_id)
        board_style = user_settings.board_style
        piece_style = user_settings.piece_style
        self.main_window.puzzles_window.board_widget.set_style(board_style, piece_style)

    def initialize_custom_puzzles_settings(self) -> None:
        puzzle_manager = (
            self.main_window.puzzles_window.board_widget.board_controller.puzzle_manager
        )
        custom_puzzles_settings = self.main_window.custom_puzzles_settings
        min_rating, max_rating = puzzle_manager.get_rating_range()
        themes = puzzle_manager.get_puzzle_themes()
        themes = ['--all--'] + self.parse_db_themes(themes, list=True)

        custom_puzzles_settings.min_rating_value.setRange(min_rating, max_rating)
        custom_puzzles_settings.max_rating_value.setRange(min_rating, max_rating)
        custom_puzzles_settings.min_rating_value.setValue(min_rating)
        custom_puzzles_settings.max_rating_value.setValue(max_rating)
        custom_puzzles_settings.theme_value.addItems(themes)

    def initialize_settings_menu(self) -> None:
        user_settings = self.user_data_manager.get_user_settings(self.current_user_id)
        user_board_style = user_settings.board_style
        user_piece_style = user_settings.piece_style

        board_assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'boards'
        )
        piece_assets_dir = os.path.join(
            os.path.dirname(__file__), '..', 'assets', 'pieces'
        )
        board_styles = [
            entry for entry in os.listdir(board_assets_dir)
            if os.path.isdir(os.path.join(board_assets_dir, entry))
        ]
        piece_styles = [
            entry for entry in os.listdir(piece_assets_dir)
            if os.path.isdir(os.path.join(piece_assets_dir, entry))
        ]

        settings_menu = self.main_window.settings_menu
        settings_menu.initialize_board_styles(board_styles, user_board_style)
        settings_menu.initialize_pieces_styles(piece_styles, user_piece_style)

    def connect_main_menu_signals(self) -> None:
        main_menu = self.main_window.main_menu
        main_menu.puzzles_button.clicked.connect(self.show_puzzles_window)
        main_menu.custom_puzzles_button.clicked.connect(self.show_custom_puzzles_settings)
        main_menu.statistics_button.clicked.connect(self.show_statistics_window)
        main_menu.settings_button.clicked.connect(self.show_settings_menu)
        main_menu.quit_button.clicked.connect(self.main_window.close)

    def connect_puzzles_window_signals(self) -> None:
        puzzles_window = self.main_window.puzzles_window
        puzzles_window.hint_button.clicked.connect(self.show_hint)
        puzzles_window.new_puzzle_button.clicked.connect(self.initialize_puzzle)
        puzzles_window.customize_puzzles_button.clicked.connect(self.customize_puzzles)
        puzzles_window.return_button.clicked.connect(self.close_puzzles_window)
        puzzles_window.board_widget.board_status_signal.connect(self.update_board_status)

    def connect_custom_puzzles_settings_signals(self) -> None:
        custom_puzzles_settings = self.main_window.custom_puzzles_settings
        custom_puzzles_settings.start_button.clicked.connect(
            self.initialize_custom_puzzles_window
        )
        custom_puzzles_settings.reset_choice_button.clicked.connect(
            self.reset_custom_puzzles_settings
        )
        custom_puzzles_settings.return_button.clicked.connect(self.show_main_menu)

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
    
    def show_puzzles_window(self) -> None:
        widget = self.main_window.puzzles_window
        self.central_widget.setCurrentWidget(widget)

    def show_custom_puzzles_settings(self) -> None:
        widget = self.main_window.custom_puzzles_settings
        self.central_widget.setCurrentWidget(widget)

    def show_statistics_window(self) -> None:
        widget = self.main_window.statistics_window
        self.central_widget.setCurrentWidget(widget)
        self.initialize_statistics()

    def show_settings_menu(self) -> None:
        widget = self.main_window.settings_menu
        self.central_widget.setCurrentWidget(widget)

    def save_settings(self) -> None:
        settings_menu = self.main_window.settings_menu
        board_style = settings_menu.board_styles_buttons.checkedButton()
        piece_style = settings_menu.pieces_styles_buttons.checkedButton()

        if board_style is None or piece_style is None:
            self.show_popup_window(
                'info', 'No settings selected',
                'Please select a board and piece style'
            )
            return
        else:
            board_style = board_style.objectName()
            piece_style = piece_style.objectName()
            self.user_data_manager.update_user_settings(
                self.current_user_id, board_style, piece_style
            )
            
        self.main_window.puzzles_window.board_widget.set_style(
            board_style, piece_style
        )
        self.show_popup_window(
            'info', 'Settings saved', 'Your settings have been saved!'
        )

    def initialize_custom_puzzles_window(self) -> None:
        custom_puzzles_settings = self.main_window.custom_puzzles_settings
        min_rating = custom_puzzles_settings.min_rating_value.value()
        max_rating = custom_puzzles_settings.max_rating_value.value()

        if min_rating > max_rating:
            self.show_popup_window(
                'info', 'Invalid rating range',
                'The minimum rating must be less than the maximum rating'
            )
            return
        
        theme = custom_puzzles_settings.theme_value.currentText()
        theme = None if theme == '--all--' else self.parse_theme(theme)
        board_controller = self.main_window.puzzles_window.board_widget.board_controller
        board_controller.set_puzzle_filters(min_rating, max_rating, theme)
        self.show_puzzles_window()

    def reset_custom_puzzles_settings(self) -> None:
        custom_puzzles_settings = self.main_window.custom_puzzles_settings
        min_rating = custom_puzzles_settings.min_rating_value.minimum()
        max_rating = custom_puzzles_settings.max_rating_value.maximum()
        custom_puzzles_settings.min_rating_value.setValue(min_rating)
        custom_puzzles_settings.max_rating_value.setValue(max_rating)
        custom_puzzles_settings.theme_value.setCurrentIndex(0)

    def show_hint(self) -> None:
        puzzles_window = self.main_window.puzzles_window
        move = puzzles_window.board_widget.board_controller.get_next_move()
        if move is not None:
            puzzles_window.status_label.setText('Hint: ' + move)

    def initialize_puzzle(self) -> None:
        puzzles_window = self.main_window.puzzles_window
        puzzles_window.board_widget.initialize_puzzle()
        puzzle_rating, puzzle_themes = (
            puzzles_window.board_widget.get_current_puzzle_info()
        )

        if puzzle_rating is None or puzzle_themes is None:
            return
        
        puzzles_window.rating_value.setText(str(puzzle_rating))
        puzzles_window.themes_value.setText(self.parse_db_themes(puzzle_themes))

    def parse_db_themes(self, themes: str, list: bool = False) -> List[str] | str:
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
        puzzles_window = self.main_window.puzzles_window
        _, puzzle_themes = puzzles_window.board_widget.get_current_puzzle_info()

        if status == 0:
            status_text = 'Make a move!'
        elif status == 1:
            status_text = 'Correct move!'
        elif status == 2:
            status_text = 'Incorrect move - Try again'
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
            self.show_popup_window(
                'info', 'No puzzle available',
                'There are no puzzles available with the selected criteria'
            )
            return
        
        puzzles_window.status_label.setText(status_text)

    def customize_puzzles(self) -> None:
        self.clear_puzzle_info()
        self.show_custom_puzzles_settings()

    def close_puzzles_window(self) -> None:
        self.clear_puzzle_info()
        self.show_main_menu()

    def clear_puzzle_info(self) -> None:
        puzzles_window = self.main_window.puzzles_window
        puzzles_window.board_widget.clear_board()
        puzzles_window.rating_value.clear()
        puzzles_window.themes_value.clear()
        puzzles_window.status_label.clear()
        puzzles_window.board_widget.board_controller.clear_puzzle_filters()

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
        confirmation = self.show_popup_window(
            'question', 'Reset progress', 'Are you sure you want to reset your progress?'
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self.user_data_manager.reset_user_progress(self.current_user_id)
            self.initialize_statistics()
            self.show_popup_window('info', 'Reset successful', 'Your progress has been reset!')

    def show_popup_window(self, type: str, title:str, text: str) -> int:
        msg_box = QMessageBox()
        if type == 'warn':
            icon = QMessageBox.Icon.Warning
        elif type == 'question':
            icon = QMessageBox.Icon.Question
        elif type == 'info':
            icon = QMessageBox.Icon.Information
        else:
            icon = QMessageBox.Icon.NoIcon
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        if type == 'question':
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        else:
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg_box.exec()