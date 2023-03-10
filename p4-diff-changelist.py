#!/depot/Python-3.6.2/bin/python
#
# Copyright 2014-2020 Cameron Hart <cameron.hart@gmail.com>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDER ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# GistID: 9337378
#

import argparse
import re
import subprocess


def stripPath(path, count):
    try:
        return '/'.join(path.split('/')[count:])
    except IndexError:
        return path


# Converts p4 describe's unified diff format into GNU unified diff format.
# https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Unified.html
def diff(changelist, stripDepth=0):
    command = ('p4 describe -S -du %d' % changelist).split()

    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = proc.communicate()[0]

    header = re.compile('==== /([^#]+)#\\d+ [^ ]+ ====')
    for bline in output.splitlines(False):
        line = bline.decode('utf-8')
        m = header.match(line)
        if m:
            pathA = stripPath('/a%s' % m.group(1), stripDepth)
            pathB = stripPath('/b%s' % m.group(1), stripDepth)

            # print GNU unified diff compliant header
            print('--- %s' % pathA)
            print('+++ %s' % pathB)
        else:
            print(line)


def main():
    parser = argparse.ArgumentParser(description='Converts p4 describe unified diff format into GNU unified diff format')
    parser.add_argument('changelist', type=int, help='p4 changelist number')
    parser.add_argument('-p', '--strip', dest='stripDepth', type=int, help='Same as GNU patch -pN, pre-strip paths to the given depth.')
    args = parser.parse_args()
    diff(args.changelist, args.stripDepth)


if __name__ == '__main__':
    main()
