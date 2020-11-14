import random
import os

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='setgen: random set generator')

    argp.add_argument('--config', default='setgen.yaml',
                       help='configuration file (default: setgen.yaml)')

    return argp.parse_args()

################################################################################
def load_config(config_file):
    import yaml

    try:
        from yaml import CLoader as YamlLoader
    except ImportError:
        from yaml import Loader as YamlLoader

    if not os.path.exists(config_file):
        print(f'!! config file does not exist: {config_file}')
        return None

    with open(config_file, 'r') as fp:
        conf = yaml.load(fp, Loader=YamlLoader)

    return conf

################################################################################
class Builder(object):
    
    #---------------------------------------------------------------------------
    def __init__(self, items):
        self.items = items
    
    #---------------------------------------------------------------------------
    def build_set(self, length, allow_repeat=False):
        priority = [1 / entry['priority'] for entry in self.items]
        set = random.choices(self.items, priority, k=length)
    
        # TODO don't repeat items in a set
    
        return set
    
################################################################################
## MAIN ENTRY

if __name__ == "__main__":
    args = parse_args()
    conf = load_config(args.config)
    builder = Builder(conf['items'])
    
    num_sets = conf['total_sets']
    set_length = conf['set_length']
    
    for set_num in range(num_sets):
        set = builder.build_set(set_length)
        print(f'== Set {set_num+1} ==')
    
        for entry in set:
            print(f'- {entry["title"]}')
    
        print()
