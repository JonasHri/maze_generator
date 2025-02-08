# %%
from functools import cache
from matplotlib import pyplot as plt
from math import sin, cos, pi


@cache
def hilbert(level) -> str:
    curve = "A"
    for _ in range(level):
        curve = curve.replace("A", "+bF-AFA-Fb+").replace("B", "-AF+BFB+FA-").replace("b", "B")
    return curve.replace("A", "").replace("B", "")


if __name__ == "__main__":
    curve = hilbert(3)
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

    plt.plot(x_pos, y_pos)
    plt.show()
