SELECT
   c.column_name AS attribute_name,
   c.ordinal_position AS column_order,
   c.data_type,
   c.character_maximum_length AS length,
   c.numeric_precision AS precision,
   c.numeric_scale AS scale,
   CASE WHEN c.is_nullable = 'NO' THEN FALSE ELSE TRUE END AS nullable,
   CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN TRUE ELSE FALSE END AS is_primary_key,
   CASE WHEN fk.COLUMN_NAME IS NOT NULL THEN TRUE ELSE FALSE END AS is_foreign_key,
   CASE WHEN c.data_type LIKE 'timestamp%' THEN '%Y-%m-%d %H:%M:%S.%f' WHEN c.data_type LIKE 'time%' THEN '%H:%M:%S' WHEN c.data_type LIKE 'date%' THEN '%Y-%m-%d' END AS datetime_format

   FROM INFORMATION_SCHEMA.COLUMNS c
LEFT JOIN (
            SELECT ku.TABLE_CATALOG,ku.TABLE_SCHEMA,ku.TABLE_NAME,ku.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS ku
                ON tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
                AND tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
         )   pk
ON  c.TABLE_CATALOG = pk.TABLE_CATALOG
            AND c.TABLE_SCHEMA = pk.TABLE_SCHEMA
            AND c.TABLE_NAME = pk.TABLE_NAME
            AND c.COLUMN_NAME = pk.COLUMN_NAME

LEFT JOIN (
            SELECT ku.TABLE_CATALOG,ku.TABLE_SCHEMA,ku.TABLE_NAME,ku.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
            INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS ku
                ON tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
                AND tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
         )   fk
ON  c.TABLE_CATALOG = fk.TABLE_CATALOG
            AND c.TABLE_SCHEMA = fk.TABLE_SCHEMA
            AND c.TABLE_NAME = fk.TABLE_NAME
            AND c.COLUMN_NAME = fk.COLUMN_NAME

WHERE
   UPPER(c.TABLE_SCHEMA) = '{{obj.schema}}' AND UPPER(c.TABLE_NAME) = '{{obj.table}}'
ORDER BY c.TABLE_SCHEMA,c.TABLE_NAME, c.ORDINAL_POSITION ;
