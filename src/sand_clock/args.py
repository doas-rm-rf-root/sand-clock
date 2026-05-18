import argparse

def parse():

    parser = argparse.ArgumentParser(description="sand clock")

    parser.add_argument(
        'number',
        type=int,
        nargs='?',
        default=15,
        help="число для обработки"
    )

    args = parser.parse_args()
    return args.number
