#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import re
import math
from functools import reduce

class GitLogParser:
    COMMIT_REGEXP = r'[a-z0-9]{40}'
    AUTHOR_REGEXP = r'Author:\s+(.*)'
    DATE_REGEXP = r'Date:\s+(.*)'
    FILE_REGEXP = r'(\d+|\-)\s+(\d+|\-)+\s+.+'
    GIT_DATE_FORMAT = '%a %b %d %H:%M:%S %Y %z'

    def parse_stream(self, input_stream, encoding='utf-8'):
        return self.parse(input_stream.decode(encoding))

    def parse(self, input_string):
        commit_strings = input_string[7:].split("\n\ncommit ")
        commits = [self.parse_commit(commit) for commit in commit_strings]
        return commits

    def parse_commit(self, commit_string):
        lines = commit_string.split("\n")
        commit = reduce(self.parse_line, lines, {})
        return commit

    def parse_line(self, commit_dict, line):
        attribute = self.try_fetch_attribute(line)
        if attribute == None:
            return commit_dict
        if attribute[0] == 'count':
            commit_dict['count'] = commit_dict.get('count', 0) + attribute[1]
        else:
            commit_dict[attribute[0]] = attribute[1]
        return commit_dict

    def try_fetch_attribute(self, commit_line):
        if re.match(self.COMMIT_REGEXP, commit_line):
            return ('commit', commit_line)
        elif re.match(self.AUTHOR_REGEXP, commit_line):
            return ('author', re.match(self.AUTHOR_REGEXP, commit_line).group(1))
        elif re.match(self.DATE_REGEXP, commit_line):
            date_str = re.match(self.DATE_REGEXP, commit_line).group(1)
            return ('date', datetime.strptime(date_str, self.GIT_DATE_FORMAT))
        elif re.match(self.FILE_REGEXP, commit_line):
            return ('count', 1)
        return None

if __name__ == '__main__':
    pass
