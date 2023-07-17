# CEGE0096 Assignment 1
# Geometry Class
# 2021.11.21

class boundary:
    """
    test whether a point is on the edge of the polygon.
    two steps:
    1st, whether on vertex?
    2nd, whether on edge?
    """
    def __init__(self, point_x, point_y, poly_x, poly_y):
        self.__point_x = point_x
        self.__point_y = point_y
        self.__poly_x = poly_x
        self.__poly_y = poly_y

    def whether_on_edge(self):
        poi_num = len(self.__point_x)
        poly_num = len(self.__poly_x)
        poi_on_edge_x, poi_on_edge_y = [], []
        for i in range(1, poi_num):
            for j in range(1, poly_num):
                # 1st, whether point on vertex:
                if self.__point_x[i-1] == self.__poly_x[j-1] and self.__point_y[i-1] == self.__poly_y[j-1]:
                    poi_on_edge_x.append(self.__point_x[i-1])
                    poi_on_edge_y.append(self.__point_y[i-1])
                # 2nd, whether on edge?
                else:
                    if (self.__poly_x[j-1] - self.__poly_x[j]) == 0:  # edge vertical to the x axe
                        if self.__point_x[i-1] == self.__poly_x[j-1] and min(self.__poly_y[j-1], self.__poly_y[j]) < self.__point_y[i-1] < max(self.__poly_y[j-1], self.__poly_y[j]):
                            poi_on_edge_x.append(self.__point_x[i-1])  # point on boundary
                            poi_on_edge_y.append(self.__point_y[i-1])
                    else:
                        # Intersection of ray and edge
                        y_temp = self.__poly_y[j]-(self.__poly_x[j]-self.__point_x[i-1])*(self.__poly_y[j]-self.__poly_y[j-1])/(self.__poly_x[j]-self.__poly_x[j-1])
                        if self.__point_y[i-1] == y_temp and min(self.__poly_x[j], self.__poly_x[j-1])<self.__point_x[i-1]<max(self.__poly_x[j], self.__poly_x[j-1]):
                            poi_on_edge_x.append(self.__point_x[i-1])
                            poi_on_edge_y.append(self.__point_y[i-1])
        return poi_on_edge_x, poi_on_edge_y


class RCA:
    """
    test whether a point is in the polygon.
    assume the Ray is horizontal to the right(actually it's the same to any direction)
    """
    def __init__(self, point_x, point_y, poly_x, poly_y):
        self.__point_x = point_x
        self.__point_y = point_y
        self.__poly_x = poly_x
        self.__poly_y = poly_y

    def whether_in_poly(self):
        poi_num = len(self.__point_x)
        print('number of whether_in_poly input points:', poi_num)
        poly_num = len(self.__poly_x)
        poi_in_poly_x, poi_in_poly_y = [], []
        poi_in_MBR_out_poly_x, poi_in_MBR_out_poly_y = [], []
        for i in range(0, poi_num):
            cross_num = 0  # count the times that a certain ray cross the edges
            poi_x = self.__point_x[i-1]
            poi_y = self.__point_y[i-1]
            for j in range(1, poly_num):

                s_poly_x = self.__poly_x[j-1]  # x coordinates of the starting point of an edge
                s_poly_y = self.__poly_y[j-1]  # y coordinates of the starting point of an edge
                e_poly_x = self.__poly_x[j]    # x coordinates of the ending point of an edge
                e_poly_y = self.__poly_y[j]    # y coordinates of the ending point of an edge

                if e_poly_y == s_poly_y:                     # ray parallel or coincident with edge
                    cross_num = cross_num
                elif s_poly_y > poi_y and e_poly_y > poi_y:  # edge above the ray
                    cross_num = cross_num
                elif s_poly_y < poi_y and e_poly_y < poi_y:  # edge below the ray
                    cross_num = cross_num
                elif poi_y == min(s_poly_y, e_poly_y) and poi_y < max(s_poly_y, e_poly_y):
                    cross_num = cross_num                    # intersection is the endpoint of edge where y is smaller
                elif s_poly_x < poi_x and e_poly_x < poi_x:  # edge on the left hand of the ray
                    cross_num = cross_num
                else:
                    # compute the x coordinate of cross point(since y is the same as poi_y)
                    x_temp = e_poly_x - (e_poly_y - poi_y) * (e_poly_x - s_poly_x) / (e_poly_y - s_poly_y)
                    if x_temp < poi_x:         # intersection on the left of the starting point of ray
                        cross_num = cross_num
                    else:
                        cross_num = cross_num + 1
            if cross_num % 2 == 1:     # cross_num is odd: point in the polygon
                poi_in_poly_x.append(poi_x)
                poi_in_poly_y.append(poi_y)
            else:                      # cross_num is even: point not in the polygon
                poi_in_MBR_out_poly_x.append(poi_x)
                poi_in_MBR_out_poly_y.append(poi_y)
        return poi_in_poly_x, poi_in_poly_y, poi_in_MBR_out_poly_x, poi_in_MBR_out_poly_y