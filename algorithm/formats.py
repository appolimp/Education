import matplotlib.pyplot as pyplot
from matplotlib.animation import FuncAnimation, FFMpegWriter
from math import sin, sqrt, exp

func1Label = r'$2^x+5x^7$'


def funcOne(x):
    return 2 ** x + 5 * x ** 7


func2Label = r'$4\cdot 2^x$'


def funcTwo(x):
    return 4 * (2 ** x)


def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 500:
        cnt += 1
        alpha = cnt / 300
        t += 0.2
        yield t, funcOne(t), funcTwo(t)


data_gen.t = 1

data_list = list(data_gen())

fig, ax = pyplot.subplots()

initial_limit = 10

xdata = [x for x, y1, y2 in data_list[:initial_limit]]
y1data = [y1 for x, y1, y2 in data_list[:initial_limit]]
y2data = [y2 for x, y1, y2 in data_list[:initial_limit]]


ax.set_xlim(xdata[0], xdata[-1])
ax.set_ylim(1.0, 1.2 * max([y1data[-1], y2data[-1]]))

line1, = ax.plot(xdata, y1data, 'b', lw=2, label=func1Label)
line2, = ax.plot(xdata, y2data, 'g', lw=2, label=func2Label)

# ax.grid()

legend = ax.legend(loc='upper left')


def run(data):
    x, y1, y2 = data
    xdata.append(x)
    y1data.append(y1)
    y2data.append(y2)
    xmin, xmax = ax.get_xlim()

    if x >= xmax:
        ax.set_xlim(xdata[0], xdata[-1])
        ax.set_ylim(1.0, 1.2 * max([y1data[-1], y2data[-1]]))
        ax.figure.canvas.draw()
    line1.set_data(xdata, y1data)
    line2.set_data(xdata, y2data)

    return line1, line2


ani = FuncAnimation(fig, run, data_list[initial_limit:], blit=True, repeat=False, interval=40)

# ani.save(r'C:\Users\Alex\Videos\matplotlib\mymovie.mp4', writer=FFMpegWriter(fps=15,bitrate=500000), dpi=300)

pyplot.show()