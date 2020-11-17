import random
import os

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='setgen: random set generator')

    argp.add_argument('--config', default='setgen.yaml',
                       help='configuration file (default: setgen.yaml)')

    argp.add_argument('--histogram', action='store_true', default=False)

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
        self.stats = dict()

    #---------------------------------------------------------------------------
    def build_set(self, length, allow_repeat=False):
        priority = [entry['priority'] for entry in self.items]

        # use built in functions for generating random sets where possible...
        if allow_repeat:
            return random.choices(self.items, priority, k=length)

        # generated a weighted list for sorting
        for item in self.items:
            item['__order'] = random.random() * item['priority']
            
        population = sorted(self.items, key=lambda x: x['__order'], reverse=True)
        set = population[:length]

        self.update_stats(set)
        return set

    #---------------------------------------------------------------------------
    def update_stats(self, items):
        for item in items:
            title = item['title']
            if title in self.stats:
                self.stats[title] += 1
            else:
                self.stats[title] = 0

################################################################################
def main(conf):
    num_sets = conf.get('total_sets', 1)
    set_length = conf.get('set_length', 3)
    allow_repeat = conf.get('allow_repeat', False)
    hist = dict()

    items = conf.get('items')
    builder = Builder(items)

    for set_num in range(num_sets):
        set = builder.build_set(set_length, allow_repeat=allow_repeat)

        if num_sets > 1:
            print(f'== Set {set_num+1} ==')
    
        for item in set:
            print(f'- {item["title"]}')
    
        print()
        
    return builder

################################################################################
## MAIN ENTRY

if __name__ == "__main__":
    args = parse_args()
    conf = load_config(args.config)
    builder = main(conf)
    
    if args.histogram:
        for title in builder.stats:
            print(f'{title} => {builder.stats[title]}')
