import sys

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
    return points

def write_points(points, faktor, file):
    for point in points:
        file.write(f'{point[0]}, {point[1] * faktor}\n')

def main():

    assert len(sys.argv) == 2, f'The programm takes one argument, a file to read points from. {len(sys.argv)} arguments where given'
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        points = read_points(file)



    with open(f'{filename[ : -4]}faktor25.txt', 'w') as new_file:
        write_points(points, 2.5, new_file)

if __name__ == '__main__':
    main()