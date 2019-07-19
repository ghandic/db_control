import os
import json

import numpy as np


def mapper(df, mapping):
    df["hive_data_type"] = df["data_type"].map(mapping['hive'])
    return df


def standardize(df):
    df['precision'] = df['precision'].replace(np.nan, 0).map(int)
    df['scale'] = df['scale'].replace(np.nan, 0).map(int)
    df['datetime_format'] = df['datetime_format'].fillna('')

    return df


class BaseExtract(object):

    def __init__(self, conn, extract_config, output_dir):
        self.conn = conn
        self.extract_config = extract_config
        self.output_dir = output_dir
        self._datetime = None

        self.metadata = None

    def create_file_path(self, obj):
        filename = f'{self.extract_config.source.id}-{obj.zone}-{obj.region}-{obj.schema}_{obj.table}-{self.datetime}'
        return os.path.join(self.output_dir, f"{filename}")

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, val):
        self._datetime = val

    def create_control_file(self, obj):
        self.metadata = mapper(self.metadata, self.extract_config.mapping)
        self.metadata = standardize(self.metadata)
        output = {
            "source_id": self.extract_config.source.id,
            "extract_date": self.datetime,
            "attributes": self.metadata.to_dict('records')
        }

        with open(f"{self.create_file_path(obj)}.ctl", 'w') as file:
            file.write(json.dumps(output, indent=2))

    def data(self, obj):
        ...

    def control(self, obj):
        ...

