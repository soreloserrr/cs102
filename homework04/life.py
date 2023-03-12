import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        x, y = cell
        deltas = [-1, 0, 1]
        neighbours = []
        for dx in deltas:
            for dy in deltas:
                if dx == 0 and dy == 0:
                    continue
                i = x + dx
                j = y + dy
                if i < 0 or i >= self.cell_height or j < 0 or j >= self.cell_width:
                    continue
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_generation = self.create_grid()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell = self.curr_generation[i][j]
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)
                if cell == 0 and alive_neighbours == 3:
                    new_generation[i][j] = 1
                elif cell == 1 and (alive_neighbours == 2 or alive_neighbours == 3):
                    new_generation[i][j] = 1
                else:
                    new_generation[i][j] = 0
        return new_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.curr_generation = self.get_next_generation()
        self.prev_generation = self.curr_generation.copy()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations == float('inf'):
            return False
        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()

        size = tuple(map(int, lines[0].strip().split()))
        max_generations = float("inf") if len(lines) == 1 else int(lines[1])
        grid = [[int(cell) for cell in row.strip()] for row in lines[2:]]
        game = GameOfLife(size, randomize=False, max_generations=max_generations)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            json.dump(self.curr_generation, f)