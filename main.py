import os
from datetime import datetime

import psycopg2

from src.common import load_credentials, ExtractConfig
from src.common.cli import get_args
from src.databases import Extractors


def main(output_dir=os.path.dirname(os.path.realpath(__file__))):

    creds = load_credentials()
    extract_config = ExtractConfig()

    Extractor = Extractors[extract_config.source.database.type]

    with psycopg2.connect(**creds) as conn:
        extract = Extractor(conn=conn, extract_config=extract_config, output_dir=output_dir)
        for obj in extract_config.objects:
            extract.datetime = datetime.now().strftime("%Y%m%d%H%M%S")
            extract.data(obj)
            extract.control(obj)


if __name__ ==  "__main__":
    args = get_args()
    main(args.output_dir)
