import random
import os

################################################################################
def load_config(config_file):
    import yaml

    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader

    if not os.path.exists(config_file):
        print('!! config file does not exist: %s', config_file)
        return None

    with open(config_file, 'r') as fp:
        conf = yaml.load(fp, Loader=YamlLoader)

    return conf
    
################################################################################
## MAIN ENTRY
conf = load_config('workout.yaml')

exercises = conf['exercises']
priority = [1 / entry['priority'] for entry in exercises]

num_sets = conf['total_sets']
set_length = conf['set_length']

print(sorted(exercises, key=lambda x: x['priority']))

for loop in range(num_sets):
    set = random.choices(exercises, priority, k=set_length)
    print(f'== Set {loop+1} ==')

    for entry in set:
        print(f'- {entry["name"]}')

    print()