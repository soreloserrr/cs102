from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """

    direction = choice((0, 1))
    if coord[1] < len(grid[0]) - 3 and coord[1] % 2 and (coord[0] == 1 or direction == 1):
        grid[coord[0]][coord[1] + 1] = " "
    elif coord[0] > 2 and coord[0] % 2 and (coord[1] == len(grid[0]) - 2 or direction == 0):
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        remove_wall(grid, cell)

    if random_exit:
        x_in = randint(0, rows - 1)
        x_out = randint(0, rows - 1)
        if x_in in (0, rows - 1):
            y_in = randint(0, cols - 1)
        else:
            y_in = choice((0, cols - 1))
        if x_out in (0, rows - 1):
            y_out = randint(0, cols - 1)
        else:
            y_out = choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """

    return [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == "X"]


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """

    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[x][y] == k:
                if x < len(grid) - 1 and not grid[x + 1][y]:
                    grid[x + 1][y] = k + 1
                if x > 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if y < len(grid[0]) - 1 and not grid[x][y + 1]:
                    grid[x][y + 1] = k + 1
                if y > 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1

    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """

    i = exit_coord[0]
    j = exit_coord[1]
    path = [(i, j)]
    k = int(grid[i][j])

    if i >= 1 and i + 2 <= len(grid):
        if grid[i - 1][j] == 1:
            path.append((i - 1, j))
            return path
        elif grid[i + 1][j] == 1:
            path.append((i + 1, j))
            return path

    if j >= 1 and j + 2 <= len(grid[0]):
        if grid[i][j - 1] == 1:
            path.append((i, j - 1))
            return path
        elif grid[i][j + 1] == 1:
            path.append((i, j + 1))
            return path

    while k != 1:
        if grid[i - 1][j] == k - 1:
            i, j = i - 1, j
        elif grid[i + 1][j] == k - 1:
            i, j = i + 1, j
        elif grid[i][j - 1] == k - 1:
            i, j = i, j - 1
        elif grid[i][j + 1] == k - 1:
            i, j = i, j + 1
        path.append((i, j))
        k -= 1

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """

    # Левая стенка
    if coord[0] == 0 and grid[coord[0] + 1][coord[1]] != " ":
        return True
    # Правая стенка
    elif coord[0] == len(grid) - 1 and grid[coord[0] - 1][coord[1]] != " ":
        return True
    # Верхняя стенка
    elif coord[1] == 0 and grid[coord[0]][coord[1] + 1] != " ":
        return True
    # Нижняя стенка
    elif coord[1] == len(grid[0]) - 1 and grid[coord[0]][coord[1] - 1] != " ":
        return True

    # Все окей
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """

    coord = get_exits(grid)
    # Проверка, что выходов несколько
    if len(coord) == 1:
        return grid, coord[0]
    # Проверка на тупик
    if encircled_exit(grid, coord[0]) or encircled_exit(grid, coord[1]):
        return grid, None
    # Находим путь
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == " ":
                grid[x][y] = 0
    # Выставляем начало и конец
    grid[coord[1][0]][coord[1][1]] = 0
    grid[coord[0][0]][coord[0][1]] = 1
    k = 1
    while grid[coord[1][0]][coord[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1
    path = shortest_path(grid, coord[1])
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != "■":
                grid[x][y] = " "
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
