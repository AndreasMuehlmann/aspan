import sys

def calc_slope(point1, point2):
    if (point2[0] - point1[0]) == 0:
        print(f'there can\'t be to equal x values: {point1[0]}, {point1[0]}; {point2[0]}, {point2[0]}')
        sys.exit(1)

    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calc_y(x, from_point, slope):
    return slope * (x - from_point[0])  + from_point[1]

def calc_area(points, precision):
    area = 0
    prev_point = 0
    next_point = 1
    slope = calc_slope(points[prev_point], points[next_point])

    x = points[prev_point][0]
    while points[0][0] <= x <= points[-1][0]:
        if x >= points[next_point][0]:
            prev_point += 1
            next_point += 1
            slope = calc_slope(points[prev_point], points[next_point])

        y = calc_y(x, points[prev_point], slope)
        area += 1 / precision * y

        x += 1 / precision

    return area

def main():
    #the x has to be sorted ascending 
    #there can't be to equal x values
    points = [[0, 3], [2, 1], [4, 1], [6, 6], [7, 10], [20, 30]]
    
    #the area of test points is 4
    #test_points = [[0, 0], [2, 2], [4, 0]]

    assert(len(sys.argv) <= 2), f'Programm needs one argument for the precision, {len(sys.argv) - 1} where given'
    if len(sys.argv) == 2:
        assert(sys.argv[1].isdigit())
        precision = 1000000

    else:
        precision = int(sys.argv[1]) if len(sys.argv) == 2 else 100000

    area = calc_area(points, precision)    

    print(f'area: {area}')


if __name__ == "__main__":
    main()