import pandas as pd

from ...common.base_extract import BaseExtract


class Extract(BaseExtract):

    def data(self, obj):
        with self.conn.cursor() as curs:
            with open(f"{self.create_file_path(obj)}.csv", 'w') as file:
                curs.copy_to(file, table=f"{obj.schema}.{obj.table}", sep=",", null="NULL")

    def control(self, obj):
        self.metadata = pd.read_sql(self.extract_config.control_sql.render(obj=obj), con=self.conn)
        self.create_control_file(obj)
