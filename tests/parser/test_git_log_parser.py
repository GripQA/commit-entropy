#!/usr/bin/env python
# coding=utf-8

import unittest
from commit_entropy.parser.git_log_parser import GitLogParser
from datetime import datetime, timezone, timedelta

class GitLogParserTest(unittest.TestCase):

    def setUp(self):
        self.commit_line_without_commit_keyword = '9093ace390c4e44910774ebddef403689435f046'
        self.author_line = 'Author: Some Author <some.author@example.com>'
        self.date_line = 'Date:   Thu Jan 1 12:34:56 2015 +0100'
        self.file_line = '1       1       some/file/path.py'
        self.ignored_file_line = '1       1       ignored/some/file/path.py'
        self.ignored_merge_line = 'Merge: 390c4e4 def4036'
        self.ignored_comment_line = '    Some Comment Line'
        self.ignored_line = 'Ignored Content'
        self.complete_commit = """
commit 9093ace390c4e44910774ebddef403689435f046
Merge: 390c4e4 def4036
Author: Some Author <some.author@example.com>
Date:   Thu Jan 1 12:34:56 2015 +0100

    Some Comment Line

1       1       some/file/path.py
1       0       some/other/path.py
1       1       ignored/some/file/path.py
0       1       yet/another/file/path.py
0       0       yet/another/file/path.py
""".strip()
        self.parser = GitLogParser()

    def parse_test(self):
        """The correct git commit dicts should be retrieved"""
        self.assertEqual(
            [
                {
                    'commit': '9093ace390c4e44910774ebddef403689435f046',
                    'author': 'Some Author <some.author@example.com>',
                    'date': datetime(2015, 1, 1, 12, 34, 56, tzinfo=timezone(timedelta(0, 3600))),
                    'count': 4,
                },
            ],
            self.parser.parse(self.complete_commit, ignore=["ignored/*"])
        )

    def try_fetch_attribute_test(self):
        """The correct attribute k/v pair should be retrieved"""
        self.assertEqual(
            ('commit', '9093ace390c4e44910774ebddef403689435f046'),
            self.parser.try_fetch_attribute(self.commit_line_without_commit_keyword)
        )
        self.assertEqual(
            ('author', 'Some Author <some.author@example.com>'),
            self.parser.try_fetch_attribute(self.author_line)
        )
        self.assertEqual(
            ('date', datetime(2015, 1, 1, 12, 34, 56, tzinfo=timezone(timedelta(0, 3600)))),
            self.parser.try_fetch_attribute(self.date_line)
        )
        self.assertEqual(
            ('count', 1),
            self.parser.try_fetch_attribute(self.file_line)
        )
        self.assertEqual(
            ('count', 1),
            self.parser.try_fetch_attribute(self.ignored_file_line)
        )
        self.assertEqual(
            None,
            self.parser.try_fetch_attribute(self.ignored_file_line, ignore=["ignored/*"])
        )
        self.assertEqual(None, self.parser.try_fetch_attribute(self.ignored_merge_line))
        self.assertEqual(None, self.parser.try_fetch_attribute(self.ignored_comment_line))
        self.assertEqual(None, self.parser.try_fetch_attribute(self.ignored_line))
