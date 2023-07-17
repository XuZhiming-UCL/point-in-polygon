# CEGE0096 Assignment 1
# main_from_user
# 2021.11.21

from plotter import Plotter
import csv
import matplotlib.pyplot as plt


def main():
    plotter = Plotter()
    print('1. read polygon.csv')
    path_polygon = "polygon.csv"
    poly_data = list(csv.reader(open(path_polygon)))
    len_row_poly = len(poly_data)
    poly_id, poly_x, poly_y = [], [], []
    for i in range(1, len_row_poly):
        poly_id.append(int(poly_data[i][0]))
        poly_x.append(float(poly_data[i][1]))
        poly_y.append(float(poly_data[i][2]))
    print('Finish reading polygon.csv')

    print('2. Insert point information')
    print('Please input the point coordinate:')
    try:
        poi_x = float(input('x coordinate: '))
    except ValueError:
        print('WARNING: input must be numbers!')

    print('Please input the point coordinate:')
    try:
        poi_y = float(input('y coordinate: '))
    except ValueError:
        print('WARNING: input must be numbers!')

    print('The point user input is:', poi_x, poi_y)

    print('3. categorize point')
    """
    kind used to represent the category of point
    kind = 0: unknown
    kind = 1: point outside polygon
    kind = 2: point inside polygon
    kind = 3: point on the boundary
    kind = 4: point in MBR
    """
    kind = 0
    poi = [poi_x, poi_y, kind]
    poly_num = len(poly_x)       # number of polygon vertex
    """
    1st, creat MBR
    test whether point is in the MBR
    """
    mbr_x = [min(poly_x), max(poly_x), max(poly_x), min(poly_x), min(poly_x)]
    mbr_y = [min(poly_y), min(poly_y), max(poly_y), max(poly_y), min(poly_y)]
    if min(poly_x) <= poi[0] <= max(poly_x) and min(poly_y) <= poi[1] <= max(poly_y):
        poi[2] = 4   # point in MBR
    else:
        # point outside MBR
        poi[2] = 1   # outside polygon
    """
    2nd, if point in MBR
    test whether point is on boundary
    """
    if poi[2] == 4:
        for i in range(1, poly_num):
            if poi[0] == poly_x[i-1] and poi[1] == poly_y[i-1]:
                poi[2] = 3      # point on vertex
            # point on edge(except vertex)
            if poly_x[i-1] - poly_x[i] == 0:  # edge vertical to the x axe
                if poi[0] == poly_x[i-1] and min(poly_y[i-1], poly_y[i]) < poi[1] < max(poly_y[i-1], poly_y[i]):
                    poi[2] = 3  # point on boundary
            else:
                # Intersection of ray and edge
                y_temp = poly_y[i] - (poly_x[i] - poi[0]) * (poly_y[i] - poly_y[i-1]) / (poly_x[i] - poly_x[i-1])
                if poi[1] == y_temp and min(poly_x[i], poly_x[i-1]) < poi[0]< max(poly_x[i], poly_x[i-1]):
                    poi[2] = 3  # point on boundary
    """
    3rd, if point in MBR but not on boundary
    test whether inside or outside the polygon 
    """
    if poi[2] == 4:
        cross_num = 0  # count the times that a certain ray cross the edges
        for i in range(1, poly_num):
            if poly_y[i] == poly_y[i-1]:  # ray parallel or coincident with edge
                cross_num = cross_num
            elif poly_y[i-1] > poi[1] and poly_y[i] > poi[1]:  # edge above the ray
                cross_num = cross_num
            elif poly_y[i-1] < poi[1] and poly_y[i] < poi[1]:  # edge below the ray
                cross_num = cross_num
            elif poi_y == min(poly_y[i-1], poly_y[i]) and poi[1] < max(poly_y[i-1], poly_y[i]):
                cross_num = cross_num  # intersection is the endpoint of edge where y is smaller
            elif poly_x[i-1] < poi[0] and poly_x[i] < poi[0]:  # edge on the left hand of the ray
                cross_num = cross_num
            else:
                # compute the x coordinate of cross point(since y is the same as poi_y)
                x_temp = poly_x[i] - (poly_y[i] - poi[1]) * (poly_x[i] - poly_x[i-1]) / (poly_y[i] - poly_y[i-1])
                if x_temp < poi[0]:  # intersection on the left of the starting point of ray
                    cross_num = cross_num
                else:
                    cross_num = cross_num + 1
        if cross_num % 2 == 1:  # cross_num is odd: point in the polygon
            poi[2] = 2
        else:                   # cross_num is even: point not in the polygon
            poi[2] = 1

    print('4. plot polygon and point')
    print('result:')
    plotter.add_polygon(poly_x, poly_y)
    plotter.add_MBR(mbr_x, mbr_y)
    if poi[2] == 0:
        print('point:', poi[0], poi[1], 'position is unknown')
        print('Classification failed, please check the codes!!!')
    if poi[2] == 1:
        print('point:', poi[0], poi[1], 'is outside the polygon')
        plotter.add_point(poi[0], poi[1], 'outside')
    if poi[2] == 2:
        print('point:', poi[0], poi[1], 'is inside the polygon')
        plotter.add_point(poi[0], poi[1], 'inside')
    if poi[2] == 3:
        print('point:', poi[0], poi[1], 'is on the boundary of the polygon')
        plotter.add_point(poi[0], poi[1], 'boundary')
    if poi[2] == 4:
        print('point:', poi[0], poi[1], 'is in the MBR of polygon')
        print('Classification failed, please check the codes!!!')
    end_x = max(max(mbr_x) + 1, poi_x)
    """
    if point is on the left side of polygon, max(mbr_x)+1 will be enough to let the ray reach the right side of polygon
    if point is on the right side of polygon, there is no need to plot the Ray(for they won't cross at all!)
    """
    plt.plot([poi_x, end_x], [poi_y, poi_y], 'darkorange', linewidth=0.75, label='Ray')
    plt.title('Point-in-Polygon test')
    plt.axis('equal')
    plotter.show()


if __name__ == '__main__':
    main()
