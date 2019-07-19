db_control
----------

Beginnings of a standardised module to extract data from many databases and have a standardised schema that can be used to load into a single database.

## Requirements
- Python 3.6+
- Packages installed from the `requirements.txt`
- Connectivity to the database

## How to run
```bash
python main.py --output-dir <output-dir>
```

## How to configure
1. Update the credentials in creds.yaml (note: creds will need protecting when not in PoC)
2. Update the extract.yaml with source specific information such as; database type, source name and id, and the objects you want to extract

## How to extend
1. Create a folder for the database you wish to build a module for in `src/databases`
2. Create a `data_mapping.yaml` within that folder which has the database data types and how to map to Hive data types.
3. Create a `extract.py` module which subclasses `src.common.base_extract.BaseExtract` and overwrites the control and data methods
4. Create a `extract_control.sql` which is a database specific SQL statement to return a table with  the required columns
5. Add the module into the `Extractors` in `src/database/__init__.py` so it is available from the main function when given as a configuration in `extract.yaml`

## Common functionality
All common functionality is kept within the `src/common` directory

## Testing
To run the unit tests simply run `pytest`

## Test environments
Within `tests/databases` each database should have a folder for tests and test environments, in here there should be:
- A `docker-compose.yaml` that can be used to start the database service
- A `test_data.sql` which can used to enter some test data into the database using its own procedures.
- A Test `extract.yaml` and `creds.yaml` to access the database and pull information
- A series of PyTest scripts to run 
