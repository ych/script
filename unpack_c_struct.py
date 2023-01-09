#!/usr/bin/env python

import sys
import os
import argparse
import struct

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('--format', '-f', required=True, help='struct format')
    parser.add_argument('--bin', '-b', required=True, help='binary file')
    args = parser.parse_args()

    size = struct.calcsize(args.format)
    with open(args.bin, "rb") as fp:
        while True:
            u = fp.read(size)
            if u == b'':
                break
            record = struct.unpack(args.format, u)
            print(record)
