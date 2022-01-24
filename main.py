import time
import sys
from to_rgb import wavelength_to_rgb
import pygame

pygame.init()

#TODO: learn how md file works to make readme better
#TODO: get rid of convert.py anstatt let the max y be given in the first line of the textfile
#TODO: see if the blackness works

def read_points(file):
    points = []
    for line_number, line in enumerate(file):
        point = line.strip().split(',')
        assert len(point) == 2, f'A point has to be separated by a comma and contains only two numbers.\
            There can only be one point per line. (line: {line_number + 1})'

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
    return points

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

    return area_left, area_right

def get_total_area(points):
    return (points[-1][0] - points[0][0]) * 2.5

def get_point_max(points):
    point_max_absorbtion = [0, 0]
    for point in points:
        if point[1] > point_max_absorbtion[1]:
            point_max_absorbtion = point
    return point_max_absorbtion

#gives the average wave_length of photons that are not absorbed
#this wave_length can probably be mapped to the color of the particles
def get_average_absorbtion(points, area_not_absorbed):
    return area_not_absorbed / (points[-1][0] - points[0][0])

def get_average_wave_length(points, area_left, area_right):
    return (points[0][0] + points[-1][0]) / 2 - (area_left / 2.5) + (area_right / 2.5)

def get_share(points, area):
    return area / get_total_area(points)

def main():
    assert len(sys.argv) == 2, f'The programm takes one argument, a file to read points from. {len(sys.argv)} arguments where given'
    with open(sys.argv[1]) as file:
        points = read_points(file)

    #the area_under_curve of test points is 4
    #points = [[0, 0], [2, 2], [4, 0]]

    precision = 10000

    area_left_under_curve, area_right_under_curve = get_area_under_curve(points, precision)    
    area_under_curve = area_left_under_curve + area_right_under_curve
    print(f'\narea under curve: {area_under_curve}')

    area_left_above_curve = (get_total_area(points) / 2) - area_left_under_curve
    area_right_above_curve = (get_total_area(points) / 2) - area_right_under_curve

    area_above_curve = area_left_above_curve + area_right_above_curve
    print(f'\narea above curve: {area_above_curve}')

    average_wave_length_under_curve = get_average_wave_length(points, area_left_under_curve, area_right_under_curve)
    print(f'\naverage wave length above curve: {average_wave_length_under_curve}')

    average_wave_length_above_curve = get_average_wave_length(points, area_left_above_curve, area_right_above_curve)
    print(f'\naverage wave length above curve: {average_wave_length_above_curve}')

    intensity = get_share(points, area_above_curve)
    print(f'\nintensity: {intensity}')

#   average_absorbtion = get_average_absorbtion(points, area_under_curve)
#   print(f'\navergae absorbtion: {average_absorbtion}\n')
#
#   point_max = get_point_max(points)
#   print(f'\nx of maximum: {point_max[0]}, y of maximum: {point_max[1]}\n')

    visible_color = wavelength_to_rgb(average_wave_length_above_curve, intensity)

    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('VISIBLE COLOR')
    window.fill(visible_color)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()