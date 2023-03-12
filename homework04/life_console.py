import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                symbol = "*" if self.life.curr_generation[row][col] else " "
                screen.addstr(row + 1, col + 1, symbol)

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.curs_set(0)
        curses.noecho()
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            self.life.step()
            curses.napms(100)
        curses.endwin()
