import argparse

def check_base(base, ex_nb=''):
    is_correct = (len(set(base)) == len(base)) and base and (set(ex_nb).issubset(set(base)))
    return is_correct


def itoBase(nb, base):
    if not check_base(base, nb):
        return
    base_complexity = len(base)
    b = ''
    while nb:
        b += base[nb % base_complexity] 
        nb = nb // base_complexity
    return b[::-1]


def itoDec(nb, base):
    if not check_base(base, nb):
        return
    base_complexity = len(base)
    nb = nb[::-1]
    res = 0
    for i in range(len(nb)):
        res += base.index(nb[i]) * (base_complexity ** i)
    return res


def itoBaseGen(nb, base_src, base_dst):
    if not (check_base(base_src, nb) and check_base(base_dst)):
        return

    nb = itoDec(nb, base_src)
    base_complexity = len(base_dst)
    b = ''
    while nb:
        b += base_dst[nb % base_complexity] 
        nb = nb // base_complexity
    return b[::-1]


def main():
    USAGE = """usage: task1.py [-h] [-s BASESRC] -d BASEDST nb

A program for converting numbers.

A number to convert is positional and mandatory argument.
FLAG ARGS:
--baseSrc, -s: (optional, decimal as default) A string with source base alphabet of the number.
--baseDst, -d: (mandatory) A string with destination base alphabet of the number.

Example:
>>> python <this_src_filename> 10010 -s 01 -d 0123456789
<<< 18
"""

    parser = argparse.ArgumentParser(description='Integer base converting', usage=USAGE)
    parser.add_argument('nb', type=str, help='A number to convert')
    parser.add_argument('-s', '--baseSrc', type=str, default='0123456789', help='The source base of the number')
    parser.add_argument('-d', '--baseDst', type=str, default=None, help='Destination base', required=True)

    args = parser.parse_args()

    res = itoBaseGen(args.nb, args.baseSrc, args.baseDst)
    if res is None:
        print(USAGE)
    else:
        print(res)
