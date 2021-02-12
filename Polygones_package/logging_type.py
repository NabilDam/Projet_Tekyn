import logging
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    return parser.parse_args()


def create_logging():
    args = get_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
        return logging
    return logging

logging = create_logging()
