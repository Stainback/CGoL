from .cell import Cell


class Universe:
    def __init__(self, width: int, height: int):
        self.field = [
            [
                Cell(i, j) for i in range(width)
            ]
            for j in range(height)
        ]

    def get_cell(self, x: int, y: int):
        return self.field[y][x]
