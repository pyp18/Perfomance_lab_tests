import argparse
import datetime
import dateutil.parser as p
from pprint import pprint

USAGE = """
usage: task3.py [-h] file t1 t2

file - path to the file with logs
t1 - time segment specifier in ISOFormat
t2 - time segment specifier in ISOFormat

Example:
>>> python3.7 task3.py log_1625990458.038007.log  2020-01-18T12:00:00 2022-01-18T13:00:00
"""


def parse_action(text):
    fragments = text.strip().split()
    dtime = p.parse(fragments[0]).replace(tzinfo=None)
    action = -1 if 'scoop' in text.split('-')[-1] else 1
    act_cap = int(fragments[-2][:-1])
    is_ok = 'успех' in text.split('-')[-1]
    return dtime, act_cap, action, is_ok


def parse_log(lines):
    lines = list(map(str.strip, lines))
    log_parsed = {}
    log_parsed['total_cap'] = int(lines[1].split()[0])
    log_parsed['current_cap'] = int(lines[2].split()[0])
    log_parsed['actions'] = []
    for i in lines[3:]:
        action = parse_action(i)
        log_parsed['actions'].append(action)
    return log_parsed


def get_segment_state(log, starttime, endtime):
    segment_log = {}
    segment_log['total_cap'] = log['total_cap']
    segment_log['current_cap'] = log['current_cap']

    min_seg_act_idx = 0
    for i in log['actions']:
        if i[0] >= starttime and i[0] <= endtime:
            break
        elif i[0] >= starttime:
            min_seg_act_idx = -1
            break
        if i[-1]:
            segment_log['current_cap'] += i[2] * i[1]
        min_seg_act_idx += 1
    
    if min_seg_act_idx == -1:
        return None
    
    max_seg_act_idx = min_seg_act_idx
    for i in log['actions'][min_seg_act_idx + 1:]:
        if i[0] <= endtime:
            max_seg_act_idx += 1
        else:
            break
    
    segment_log['actions'] = log['actions'][min_seg_act_idx:max_seg_act_idx + 1]
    
    return segment_log


parser = argparse.ArgumentParser(usage=USAGE)
parser.add_argument('file', type=argparse.FileType('r'))
parser.add_argument('t1', type=datetime.datetime.fromisoformat)
parser.add_argument('t2', type=datetime.datetime.fromisoformat)

args = parser.parse_args()

log = parse_log(args.file.readlines())
log['actions'].sort()

t1, t2 = sorted((args.t1, args.t2))

segment_log = get_segment_state(log, t1, t2)

if not segment_log:
    print('Incorrect args provided.')
    print(USAGE)
    exit(0)

stats = {
    'initial_cap': segment_log['current_cap'],
    'top_up': {
        'tries': 0,
        'errors_percent': None,
        'successful_cap': 0,
        'unsuccessful_cap': 0
    },
    'scoop': {
        'tries': 0,
        'errors_percent': None,
        'successful_cap': 0,
        'unsuccessful_cap': 0
    },
    'end_cap': None
}
bad_tries_counter = {'scoop': 0, 'top_up': 0}
for i in segment_log['actions']:
    action_type = 'top_up' if i[2] == 1 else 'scoop'
    
    stats[action_type]['tries'] += 1
    stats[action_type]['successful_cap'] += i[3] * i[1]
    stats[action_type]['unsuccessful_cap'] += i[3] * i[1]
    
    bad_tries_counter[action_type] += not i[3]
    
    segment_log['current_cap'] += i[3] * i[2] * i[1]

stats['end_cap'] = segment_log['current_cap']
stats['top_up']['errors_percent'] = bad_tries_counter['top_up'] / stats['top_up']['tries'] * 100
stats['scoop']['errors_percent'] = bad_tries_counter['scoop'] / stats['scoop']['tries'] * 100

pprint(stats)
