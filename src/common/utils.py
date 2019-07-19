import yaml
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def load_credentials():
    with open("creds.yaml", 'r') as creds_file:
        try:
            return yaml.safe_load(creds_file)
        except yaml.YAMLError as exc:
            print(exc)

