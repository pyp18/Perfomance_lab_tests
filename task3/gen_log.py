import random
import time
import datetime as dt

METADATA = """META DATA:
2000 (объем бочки)
1000 (текущий объем воды в бочке)
"""

N_ACTIONS = 14000
USERNAMES = ['username1', 'username2', 'username3']
ACTION_TYPES = ['wanna top up', 'wanna scoop']
ACTION_CODES = ['фейл', 'успех']

capacity = {'total_cap': 2000, 'current_cap': 1000, 'actions': []}

ts = str(time.time())
last_dt = dt.datetime.now()
with open(f'log_{ts}.log', 'w') as writer:
    writer.write(METADATA)
    for i in range(N_ACTIONS):
        act_time = last_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        username = random.choice(USERNAMES)
        act_cap = random.randint(4, 30)
        act_type = random.choice(ACTION_TYPES)

        if act_type == ACTION_TYPES[0]:
            if (capacity['current_cap'] + act_cap) <= capacity['total_cap']:
                capacity['current_cap'] += act_cap
                act_success = 'успех'
            else:
                act_success = 'фейл'
        else:
            if (capacity['current_cap'] - act_cap) >= 0:
                capacity['current_cap'] -= act_cap
                act_success = 'успех'
            else:
                act_success = 'фейл'

        action = f'{act_time} - [{username}] - {act_type} {act_cap}l ({act_success})\n'
        capacity['actions'].append(action)

        last_dt = last_dt + dt.timedelta(seconds=random.randint(1, 10))
    
    writer.writelines(capacity['actions'])
