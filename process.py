#!/usr/bin/env python3
import json
import sys


def process(argv):
    try:
        file = open(argv[1], encoding="utf8")
    except OSError:
        print("Cannot open file", file=sys.stderr)
        return 84
    data = json.load(file)
    file.close()
    return 0
