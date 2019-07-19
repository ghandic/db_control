import json

import yaml
from jinja2 import Template


class BaseModel(object):
    def __repr__(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)


class DataBase(BaseModel):
    def __init__(self, db_config):
        self.type = db_config["type"].strip().upper()
        self.version = db_config["version"].strip().upper()


class Source(BaseModel):
    def __init__(self, source_config):
        self.id = source_config["id"].strip().upper()
        self.name = source_config["name"].strip().upper()
        self.database = DataBase(source_config["database"])


class Object(BaseModel):
    def __init__(self, objects_config):
        self.schema = objects_config["schema"].strip().upper()
        self.table = objects_config["table"].strip().upper()
        self.zone = objects_config["zone"].strip().upper()
        self.region = objects_config["region"].strip().upper()


class ExtractConfig(BaseModel):
    def __init__(self):
        with open("extract.yaml", 'r') as config_file:
            try:
                self.config = yaml.safe_load(config_file)
            except yaml.YAMLError as exc:
                print(exc)
        self.source = Source(self.config["source"])
        self.objects = [Object(o) for o in self.config["objects"]]
        self.control_sql = self._load_extract_template('extract_control.sql')
        self.mapping = self._load_mapping()

    def _load_extract_template(self, filename):
        with open(f'src/databases/{self.source.database.type}/{filename}', 'r') as sql_template:
            return Template(sql_template.read())

    def _load_mapping(self):
        with open(f'src/databases/{self.source.database.type}/data_mapping.yaml', 'r') as mapping_file:
            try:
                return yaml.safe_load(mapping_file)
            except yaml.YAMLError as exc:
                print(exc)


