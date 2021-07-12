import re
import ast
import math
import argparse


def solve_quad_eq(a, b, c):
    d = b ** 2 - 4 * a * c
    roots = None
    if d == 0:
        x = (-b+math.sqrt(b**2-4*a*c))/2*a
        roots = (x,)
    elif d > 0:
        x1 = (-b+math.sqrt((b**2)-(4*(a*c))))/(2*a)
        x2 = (-b-math.sqrt((b**2)-(4*(a*c))))/(2*a)
        roots = (x1, x2)
    return roots


def parse(text):
    values_regexps = {
        'line': r'line:\s*{\[.*]}',
        'radius': r'radius:\s*\d+\.{0,1}\d*',
        'center': r'center:\s*\[\s*\d+\.{0,1}\d*\s*,\s*\d+\.{0,1}\d*\s*,\s*\d+\.{0,1}\d*\s*]'
    }
    parsed = {}
    for key, val in values_regexps.items():
        parsed_val = re.findall(val, text)[0]
        clear_parsed_val = parsed_val.split(':')[1].strip()
        if key == 'line':
            clear_parsed_val = '[' + clear_parsed_val[1:-1] + ']'

        parsed[key] = ast.literal_eval(clear_parsed_val)

    return parsed


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))

args = parser.parse_args()

geom = parse(args.file.read())

center = geom['center']
radius = geom['radius']
line_point_0 = geom['line'][0]
line_point_1 = geom['line'][1]
delta = (line_point_1[0] - line_point_0[0], line_point_1[1] -
         line_point_0[1], line_point_1[2] - line_point_0[2])

coeffs = [
    (delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2),

    2 * (line_point_0[0] * delta[0] + line_point_0[1] * delta[1] + line_point_0[2] * delta[2] - delta[1] *
         center[1] - delta[2] * center[2] - delta[1] * center[1]),

    (line_point_0[0] ** 2 + line_point_0[1] ** 2 + line_point_0[2] ** 2 + center[0] ** 2 +
     center[1] ** 2 + center[2] ** 2 - 2 * (line_point_0[0] * center[0] + line_point_0[1] * center[1] +
                                            line_point_0[2] * center[2]) - radius ** 2)
]

roots = solve_quad_eq(*coeffs)

is_intersectioned = False

for i in roots:
    if 0 < i < 1:
        intersection_X = line_point_0[0] + i * delta[0]
        intersection_Y = line_point_0[1] + i * delta[1]
        intersection_Z = line_point_0[2] + i * delta[2]
        coords = (intersection_X, intersection_Y, intersection_Z)
        print(*coords)

        is_intersectioned = True

if not is_intersectioned:
    print('Коллизий не найдено')
