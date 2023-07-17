# CEGE0096 Assignment 1
# main_from_file
# 2021.11.21

from plotter import Plotter
import csv
from class_geometry import*
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

    print('2. read input.csv')
    path_input = "input.csv"
    input_data = list(csv.reader(open(path_input)))
    len_row_poi = len(input_data)
    poi_id, poi_x, poi_y = [], [], []
    for i in range(1, len_row_poi):
        poi_id.append(int(input_data[i][0]))
        poi_x.append(float(input_data[i][1]))
        poi_y.append(float(input_data[i][2]))
    points = list(zip(poi_id, poi_x, poi_y))
    print('Finish reading input.csv')

    print('3. categorize points')
    """
    creat MBR
    divide points into two groups: points_in_MBR & points_out_MBR
    """
    poi_in_MBR_id, poi_in_MBR_x, poi_in_MBR_y = [], [], []
    poi_out_MBR_id, poi_out_MBR_x, poi_out_MBR_y = [], [], []
    for i in range(1, len_row_poi):
        if min(poly_x) <= poi_x[i-1] <= max(poly_x) and min(poly_y) <= poi_y[i-1] <= max(poly_y):
            poi_in_MBR_id.append(poi_id[i-1])
            poi_in_MBR_x.append(poi_x[i-1])
            poi_in_MBR_y.append(poi_y[i-1])
        else:
            poi_out_MBR_id.append(poi_id[i-1])
            poi_out_MBR_x.append(poi_x[i-1])
            poi_out_MBR_y.append(poi_y[i-1])
    points_in_MBR = list(zip(poi_in_MBR_x, poi_in_MBR_y))   #-----poi_in_MBR_id
    points_out_MBR = list(zip(poi_out_MBR_x, poi_out_MBR_y))#-----poi_out_MBR_id
    # print(points_in_MBR)
    # print(points_out_MBR)
    print('number of points_in_MBR & points_out_MBR:', len(poi_in_MBR_x), '&', len(poi_out_MBR_x))
    mbr_x = [min(poly_x), max(poly_x), max(poly_x), min(poly_x), min(poly_x)]
    mbr_y = [min(poly_y), min(poly_y), max(poly_y), max(poly_y), min(poly_y)]
    """
    for points_in_MBR, test: whether on the edge of polygon.
    """
    test = boundary(poi_in_MBR_x, poi_in_MBR_y, poly_x, poly_y)
    result_edge = test.whether_on_edge()
    poi_on_edge_x, poi_on_edge_y = result_edge[0], result_edge[1]
    # print(poi_on_edge_x)
    # print(poi_on_edge_y)
    print('number of points on edge:', len(poi_on_edge_x))

    point_on_edge = list(zip(poi_on_edge_x, poi_on_edge_y))    #
    poi_inMBR_not_edge = list(set(points_in_MBR) - set(point_on_edge))
    # print(point_on_edge)
    # print(poi_inMBR_not_edge)
    num_poi_inMBR_not_edge = len(poi_in_MBR_x) - len(poi_on_edge_x)
    poi_inMBR_not_edge_x, poi_inMBR_not_edge_y = [], []
    for i in range(0, num_poi_inMBR_not_edge):
        poi_inMBR_not_edge_x.append(poi_inMBR_not_edge[i][0])
        poi_inMBR_not_edge_y.append(poi_inMBR_not_edge[i][1])
    # print(num_poi_inMBR_not_edge)
    # print(poi_inMBR_not_edge_x)
    # print(poi_inMBR_not_edge_y)
    """
    for other points(poi_inMBR_not_edge), go to next step:
    whether in the polygon.
    RCA
    """
    test = RCA(poi_inMBR_not_edge_x, poi_inMBR_not_edge_y, poly_x, poly_y)
    result_in_poly = test.whether_in_poly()
    poi_in_poly_x, poi_in_poly_y, poi_in_MBR_out_poly_x, poi_in_MBR_out_poly_y = \
        result_in_poly[0], result_in_poly[1], result_in_poly[2], result_in_poly[3],
    print('number of points in polygon:', len(poi_in_poly_x))
    print('number of points poi_in_MBR_out_poly:', len(poi_in_MBR_out_poly_x))
    """
    summary:
    """
    poi_out_poly_x, poi_out_poly_y = [], []
    poi_out_poly_x.extend(poi_in_MBR_out_poly_x)
    poi_out_poly_x.extend(poi_out_MBR_x)
    poi_out_poly_y.extend(poi_in_MBR_out_poly_y)
    poi_out_poly_y.extend(poi_out_MBR_y)
    point_in_polygon = list(zip(poi_in_poly_x, poi_in_poly_y))     # points in polygon
    point_on_polygon = list(zip(poi_on_edge_x, poi_on_edge_y))     # points on polygon's boundary
    point_out_polygon = list(zip(poi_out_poly_x, poi_out_poly_y))  # points outside polygon
    print('Points have been divided into 3 categories.')

    print('4. write output.csv')
    with open('output.csv', 'w') as f:
        f.write('x')
        f.write(',')
        f.write('y')
        f.write(',')
        f.write('category')
        f.write('\n')
        for i in range(0,len(poi_in_poly_x)):
            f.write('str(poi_in_poly_x[i])')
            f.write(',')
            f.write('str(poi_in_poly_y[i])')
            f.write(',')
            f.write('inside')
            f.write('\n')
        for i in range(0,len(poi_on_edge_x)):
            f.write('str(poi_on_edge_x[i])')
            f.write(',')
            f.write('str(poi_on_edge_y[i]')
            f.write(',')
            f.write('boundry')
            f.write('\n')
        for i in range(0,len(poi_out_poly_x)):
            f.write('str(poi_out_poly_x[i])')
            f.write(',')
            f.write('str2')
            f.write(',')
            f.write('str(poi_out_poly_y[i])')
            f.write('\n')
        f.close()
    print('output.csv finished.')

    print('5. plot polygon and points')
    plotter.add_polygon(poly_x, poly_y)
    plotter.add_MBR(mbr_x, mbr_y)
    plotter.add_point(poi_in_poly_x, poi_in_poly_y, 'inside')
    plotter.add_point(poi_on_edge_x, poi_on_edge_y, 'boundary')
    plotter.add_point(poi_out_poly_x, poi_out_poly_y, 'outside')
    end_x = max(max(mbr_x)+1, max(poi_x))  # max(mbr_x)+1 is enough to let the ray reach the right side of polygon
    plotter.add_Ray(poi_x, poi_y, end_x)
    plt.title('Point-in-Polygon test')
    plotter.show()


if __name__ == '__main__':
    main()