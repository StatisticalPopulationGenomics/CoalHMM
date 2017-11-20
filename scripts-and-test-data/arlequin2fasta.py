#!/usr/bin/env python

import os
import sys

assert 3 == len(sys.argv), 'usage: {0} <input.arp> <num-sites>'.format(os.path.basename(sys.argv[0]))

input_path = sys.argv[1]
total_sites = int(sys.argv[2])


class Reader:
    def __init__(self, path):
        self.index = 0
        with open(path, 'r') as f:
            self.lines = f.read().splitlines()

    @property
    def end_of_file(self):
        return self.index >= len(self.lines)

    def read_line(self):
        line = self.lines[self.index]
        self.index += 1
        return line

    def skip_lines(self, n):
        self.index += n


def write_fasta(sites, sample_name, line):
    #
    # e.g.
    #   sites:          (465, 10325, ...)
    #   sample_name:    'Sample 1'
    #   line:           '2_1 \t 1 \t ACTG...'
    #
    fields = line.split('\t')
    if len(fields) != 3:
        return

    sample_id, _, sample_data = fields

    output_path, _ = os.path.splitext(os.path.basename(input_path))
    output_path += '-' + sample_name.lower().replace(' ', '_')
    output_path += '-' + sample_id
    output_path += '.fasta'

    print 'Saving "{0}"...'.format(output_path)
    with open(output_path, 'w') as f:
        # f.write('> {0} ({1})\n'.format(sample_name, sample_id))
        f.write('> {0}\n'.format(os.path.basename(input_path).split('.')[0]))

        j = 0
        for i in xrange(total_sites):
            if i in sites:
                f.write(sample_data[j])
                j += 1
            else:
                f.write('a')

            if 0 == (i + 1) % 100:
                f.write('\n')

        f.write('\n')


def main():
    reader = Reader(input_path)

    while not reader.end_of_file:
        if '#Total number of polymorphic sites: ' not in reader.read_line():
            continue

        reader.skip_lines(1)

        sites = frozenset(map(int, reader.read_line()[1:].split(',')))

        while not reader.end_of_file:
            line = reader.read_line()
            if 'SampleName' not in line:
                continue

            sample_name = line.split('"')[1]

            while not reader.end_of_file:
                if 'SampleData' not in reader.read_line():
                    continue

                while not reader.end_of_file:
                    line = reader.read_line()
                    if '}' in line:
                        break

                    write_fasta(sites, sample_name, line)

                break

        break

main()

