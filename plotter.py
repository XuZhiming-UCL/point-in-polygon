from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

# if plotting does not work comment the following line
matplotlib.use('TkAgg')


class Plotter:

    def __init__(self) -> object:
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_MBR(self, xs, ys):  # plot MBR of the polygon
        plt.fill(xs, ys, 'red', fill=None, label='MBR')

    def add_point(self, x, y, kind=None):
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')

    def add_Ray(self, xs, ys, end_x):  # plot Ray of each point
        num = len(xs)
        for i in range(1, num):
            plt.plot([xs[i-1], end_x], [ys[i-1], ys[i-1]], 'darkorange', linewidth = 0.75, label='Ray')





    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()
