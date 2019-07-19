import argparse


def get_args():

    parser = argparse.ArgumentParser(description="Commandline tool for Extracting data and controlfiles from databases")
    parser.add_argument('-o', '--output-dir', required=True, help="Output directory to save the files")

    return parser.parse_args()
