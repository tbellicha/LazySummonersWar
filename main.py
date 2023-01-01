#!/usr/bin/env python3
import sys

import process


def print_helper():
    print("USAGE")
    print("\t./lsy file\n")
    print("DESCRIPTION")
    print("\tfile\tPath of the JSON you want to inspect.")
    return 1


def check_args(argc, argv):
    if argc == 2 and argv[1] == "-h":
        return print_helper()
    if argc != 2:
        print("Bad arguments number, try with -h", file=sys.stderr)
        return -1
    return 0


def main(argc, argv):
    args_return = check_args(argc, argv)
    if args_return == -1:
        return 84
    elif args_return == 1:
        return 0
    else:
        return process.process(argv)
