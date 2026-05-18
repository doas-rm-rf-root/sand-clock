import argparse

def parse():

    parser = argparse.ArgumentParser(description="A small hourglass app based on cellular automate and taichi. CPU renderer currently")

    parser.add_argument(
        'number',
        type=int,
        nargs='?',
        default=15,
        help="Number of timed minuted"
    )

    args = parser.parse_args()
    return args.number
