import json

config_vars = {}


def load_config():
    with open('cfg.json') as f:
        data = json.load(f)
        for i in data:
            config_vars[i] = data[i]


def save_config():
    with open('cfg.json', 'w') as f:
        json.dump(config_vars, f)
