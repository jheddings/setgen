import random
import os

################################################################################
def parse_args():
    import argparse

    argp = argparse.ArgumentParser(description='setgen: random set generator')

    argp.add_argument('--config', default='setgen.yaml',
                       help='configuration file (default: setgen.yaml)')

    argp.add_argument('--stats', action='store_true', default=False)

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
class Statistics(object):

    #---------------------------------------------------------------------------
    def __init__(self, items):
        self.total = 0
        self.counts = dict()

        for item in items:
            title = item['title']
            self.counts[title] = 0

    #---------------------------------------------------------------------------
    def collect(self, items):
        for item in items:
            title = item['title']
            self.counts[title] += 1

        self.total += len(items)

################################################################################
class Builder(object):

    #---------------------------------------------------------------------------
    def __init__(self, items):
        self.items = items
        self.stats = Statistics(items)

    #---------------------------------------------------------------------------
    def _select_items(self, items, length):
        # assign a weighted order to each item for sorting
        for item in items:
            item['__order'] = random.random() * item['priority']

        population = sorted(items, key=lambda x: x['__order'], reverse=True)

        # slice the population for the desired length
        return population[:length]

    #---------------------------------------------------------------------------
    def build_set(self, length, allow_repeat=False):
        priority = [entry['priority'] for entry in self.items]

        # use built in functions for generating random sets where possible...
        if allow_repeat:
            current_set = random.choices(self.items, priority, k=length)
        else:
            current_set = self._select_items(self.items, length)

        self.stats.collect(current_set)

        return current_set

################################################################################
def main(conf):
    num_sets = conf.get('total_sets', 1)
    set_size = conf.get('set_size', 3)
    allow_repeat = conf.get('allow_repeat', False)

    items = conf.get('items')
    builder = Builder(items)

    for set_num in range(num_sets):
        set = builder.build_set(set_size, allow_repeat=allow_repeat)

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

    if args.stats:
        print(f'== Item Distribution ==')
        counts = builder.stats.counts
        for title in counts:
            print(f'{title} => {counts[title]}')
