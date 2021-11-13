from advent_of_code import *

input_value = get_input()
input_lines = get_input_lines()

directions = [
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]

def run(lines, steps, problem):
    grid = Grid(lines)
    neighbors = {
        pos: [
            n
            for direction in directions
            if (n := grid.apply_direction(pos, direction))
        ]
        for (x, y, v) in grid
        if (pos := (x, y))
    }

    def set_corners(grid):
        if problem == 1:
            return
        grid[(0, 0)] = '#'
        grid[(grid.width - 1, 0)] = '#'
        grid[(0, grid.height - 1)] = '#'
        grid[(grid.width - 1, grid.height - 1)] = '#'

    for i in range(steps):
        set_corners(grid)
        next_grid = grid.copy()
        for (x, y, v) in grid:
            pos = (x, y)
            lights = len([
                1
                for n in neighbors[pos]
                if grid[n] == '#'
            ])
            if v == '#':
                is_on = 2 <= lights <= 3
            else:
                is_on = lights == 3

            next_grid[pos] = '#' if is_on else '.'
        grid = next_grid

    set_corners(grid)
    return len([
        1
        for (x, y, v) in grid
        if v == '#'
    ])

example1 = multiline_lines(r"""
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""")

run(example1, 4, 1) | eq(4)
run(input_lines, 100, 1) | debug('Star 1') | eq(814)

run(example1, 5, 2) | eq(17)
run(input_lines, 100, 2) | debug('Star 2') | eq(924)
