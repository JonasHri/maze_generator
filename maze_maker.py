# %%
from hilbert import hilbert
from math import sin, cos, pi
import numpy as np

#   #####
#   #   #
#   #   #
#   #####


def directions_to_array(curve: str):

    x_pos = [0]
    y_pos = [0]
    facing = 0

    for instruction in curve:
        match instruction:
            case "+":
                facing += 1

            case "-":
                facing -= 1
            case _:
                x_pos.append(x_pos[-1] + int(cos(facing * pi / 2)))
                y_pos.append(y_pos[-1] + int(sin(facing * pi / 2)))

    x_max = np.max(x_pos)
    y_max = np.max(y_pos)
    array = np.zeros((y_max + 1, x_max + 1), dtype=int)

    for i, (x, y) in enumerate(zip(x_pos, y_pos)):
        array[y_max - y, x] = i

    return array


distance_array = directions_to_array(hilbert(4))


maze = [
    [{"up": False, "down": False, "left": False, "right": False} for _ in range(distance_array.shape[1])]
    for _ in range(distance_array.shape[0])
]

maze[-1][0]["left"] = True
maze[-1][-1]["right"] = True

next_steps = [[0, 1, "right", "left"], [0, -1, "left", "right"], [1, 0, "down", "up"], [-1, 0, "up", "down"]]


for y in range(len(maze)):
    for x in range(len(maze[0])):
        cur_dist = distance_array[y][x]
        if x == len(maze[0]) - 1 and y == len(maze) - 1:
            break
        while True:
            next_step = next_steps[np.random.randint(4)]
            x_n = x + next_step[1]
            y_n = y + next_step[0]

            if x_n < 0 or x_n >= len(maze[0]):
                continue

            if y_n < 0 or y_n >= len(maze):
                continue

            if distance_array[y_n][x_n] < cur_dist:
                continue

            maze[y][x][next_step[2]] = True
            maze[y_n][x_n][next_step[3]] = True
            break


def doors_to_text(door: dict):
    w = 3
    up = " " * door["up"] + "#" * (1 - door["up"])
    down = " " * door["down"] + "#" * (1 - door["down"])
    right = " " * door["right"] + "#" * (1 - door["right"])
    left = " " * door["left"] + "#" * (1 - door["left"])

    text = [
        "#" + w * up + "#",
        # left + w * " " + right,
        left + w * " " + right,
        left + w * " " + right,
        "#" + w * down + "#",
    ]

    return text


render = []


for y in range(len(maze)):
    render.append(doors_to_text(maze[y][0]))
    for x in range(1, len(maze[0])):
        next_text = doors_to_text(maze[y][x])
        for i, line in enumerate(next_text):
            render[-1][i] = render[-1][i] + line


render[-1][-2] = "S" + render[-1][-2][1:-1] + "E"

for chunk in render:
    for line in chunk:
        print(line)
