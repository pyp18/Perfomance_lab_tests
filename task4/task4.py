import argparse
import re


def reduce_asterisks(pattern):
    reduced = ''
    asterisk_now = False
    for i in pattern:
        if not asterisk_now and i == '*':
            reduced += i
            asterisk_now = True
        elif i != '*':
            reduced += i
            asterisk_now = False

    return reduced


def check_sameness(str1, str2):
    str2 = re.escape(reduce_asterisks(str2))
    str2 = str2.replace('\*', '.*')
    return bool(re.match(str2, str1))


parser = argparse.ArgumentParser()
parser.add_argument('str1', type=str)
parser.add_argument('str2', type=str)

args = parser.parse_args()

if check_sameness(args.str1, args.str2):
    print('OK')
else:
    print('KO')
