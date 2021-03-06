import math
import sys
from to_rgb import wavelength_to_rgb
import pygame

pygame.init()

def read_points(file):
    points = []
    for line_number, line in enumerate(file):

        if line_number == 0:
            list_for_line = line.strip().split()
            list_for_line[0] = list_for_line[0].replace(' ', '')
            assert (list_for_line[0].replace('.','',1).isdigit() and list_for_line[0].count('.') < 2),\
                f'In the first line must be the upper limit of the y axis.'
            upper_limit_y_axis = float(list_for_line.pop())
            continue

        point = line.strip().split(',')
        assert len(point) == 2, f'A point has to be separated by a comma and contains only two numbers.'\
            + f' There can only be one point per line. (line: {line_number + 1})'

        point[0] = point[0].replace(' ', '')
        point[1] = point[1].replace(' ', '')

        point[1].startswith('-')
        original = point[1]
        point[1] = point[1].replace('-', '', 1)

        assert (point[0].replace('.','',1).isdigit() and point.count('.') < 2),\
            f'A point has to be a number of some kind (line: {line_number + 1})'
        assert (point[1].replace('.','',1).isdigit() and point.count('.') < 2),\
            f'A point has to be a number of some kind (line: {line_number + 1})'
        
        points.append([float(point[0]), float(original)])

    points.sort(key=lambda point: point[0])
    assert 375 <= points[0][0] <= 385 and 775 <= points[-1][0] <= 785, 'The first x should be around 380 (+-5) and the last x should be around 755 (+-5).'
    return points, upper_limit_y_axis

def calc_slope(point1, point2):
    if (point2[0] - point1[0]) == 0:
        print(f'there can\'t be to equal x values: {point1[0]}, {point1[0]}; {point2[0]}, {point2[0]}')
        sys.exit(1)

    return (point2[1] - point1[1]) / (point2[0] - point1[0])

def calc_y(x, from_point, slope):
    return slope * (x - from_point[0])  + from_point[1]

def get_area_under_curve(points, precision):
    area_left = 0
    area_right = 0
    prev_point = 0
    next_point = 1
    slope = calc_slope(points[prev_point], points[next_point])

    x = points[prev_point][0]
    while points[0][0] <= x <= points[-1][0]:
        if x > points[next_point][0]:
            prev_point += 1
            next_point += 1
            slope = calc_slope(points[prev_point], points[next_point])

        y = calc_y(x, points[prev_point], slope)
        if x < (points[0][0] + points[-1][0]) / 2:
            area_left += 1 / precision * y
        else:
            area_right += 1 / precision * y

        x += 1 / precision

    return round(area_left, 2), round(area_right, 2)

def get_total_area(points, upper_limit_y_axis):
    return round((points[-1][0] - points[0][0]) * upper_limit_y_axis, 2)

def get_point_max_min(points):
    point_max_absorbtion = points[0]
    point_min_absorbtion = points[0]

    for point in points:
        if point[1] > point_max_absorbtion[1]:
            point_max_absorbtion = point

        if point[1] < point_min_absorbtion[1]:
            point_min_absorbtion = point

    return point_max_absorbtion, point_min_absorbtion

def get_average_wave_length(points, area_left, area_right, upper_limit_y_axis):
    return round((points[0][0] + points[-1][0]) / 2 - (area_left / upper_limit_y_axis) + (area_right / upper_limit_y_axis), 2)

def get_share(points, area, upper_limit_y_axis):
    return round(area / get_total_area(points, upper_limit_y_axis), 2)

def get_intensity(points, area_above_curve, upper_limit_y_axis):
    return round(math.sqrt(get_share(points, area_above_curve, upper_limit_y_axis)), 2)

def get_saturation(y_max, y_min, upper_limit_y_axis):
    return round((y_max - y_min) / upper_limit_y_axis, 2)

def main():
    assert len(sys.argv) == 2, f'The programm takes one argument, a file to read points from. {len(sys.argv)} arguments where given'
    with open(sys.argv[1]) as file:
        points, upper_limit_y_axis = read_points(file)

    precision = 10000

    area_left_under_curve, area_right_under_curve = get_area_under_curve(points, precision)    
    area_under_curve = area_left_under_curve + area_right_under_curve
    print(f'\narea under curve: {area_under_curve}')

    area_left_above_curve = round((get_total_area(points, upper_limit_y_axis) / 2) - area_left_under_curve, 2)
    area_right_above_curve = round((get_total_area(points, upper_limit_y_axis) / 2) - area_right_under_curve, 2)

    area_above_curve = round(area_left_above_curve + area_right_above_curve, 2)
    print(f'\narea above curve: {area_above_curve}')

    average_wave_length_under_curve = get_average_wave_length(points, area_left_under_curve, area_right_under_curve, upper_limit_y_axis)
    print(f'\naverage wave length under curve: {average_wave_length_under_curve}')

    average_wave_length_above_curve = get_average_wave_length(points, area_left_above_curve, area_right_above_curve, upper_limit_y_axis)
    print(f'\naverage wave length above curve: {average_wave_length_above_curve}')

    intensity = get_intensity(points, area_above_curve, upper_limit_y_axis)
    print(f'\nintensity: {intensity}')

    point_max, point_min = get_point_max_min(points)
    print(f'\nx of maximum: {point_max[0]}, y of maximum: {point_max[1]}')
    print(f'x of minimum: {point_min[0]}, y of minimum: {point_min[1]}\n')


    saturation = get_saturation(point_max[1], point_min[1], upper_limit_y_axis)
    print(f'\nsaturation: {saturation}')

    visible_color = wavelength_to_rgb(average_wave_length_above_curve, intensity, 1)

    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption(f'{sys.argv[1]}')
    window.fill(visible_color)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()