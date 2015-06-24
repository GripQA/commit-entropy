#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.shell import run
from Naked.toolshed.system import exit_fail
from entropy.parser.git_log_parser import GitLogParser
from datetime import datetime
from datetime import timedelta, date
import statistics
import math
import sys
import csv

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class CsvPrinter:
    def run(self):
        self.ensure_git_repo()
        log_output = self.get_git_log()
        commits = GitLogParser().parse_stream(log_output)
        for commit in commits:
            commit['entropy'] = self.get_entropy(commit)

        daily_commits = self.group_by_day(commits)
        daily_entropies = self.get_running_averages(daily_commits, size=1)
        monthly_entropies = self.get_running_averages(daily_commits, size=30)

        entropies = [(x[0], x[1], monthly_entropies[i][1]) for i, x in enumerate(daily_entropies)]

        with open('entropy.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Day','Entropy','30 Day'])
            for day in entropies:
                writer.writerow(day)

    def ensure_git_repo(self):
        status_output = run('git status', suppress_stdout=True, suppress_stderr=True)
        if not status_output:
            print('Please run this command in a git repository', file=sys.stderr)
            exit_fail()

    def get_git_log(self):
        log_output = run('git log --numstat --reverse', suppress_stdout=True, suppress_stderr=False)
        if not log_output:
            print('Error fetching git log', file=sys.stderr)
            exit_fail()
        return log_output

    def get_entropy(self, commit):
        if commit.get('count', 0) == 0:
            return None
        return math.log(commit['count'], 2)

    def group_by_day(self, commits):
        commits_by_day = {}
        for commit in commits:
            day = commit['date'].strftime('%Y%m%d')
            days_commits = commits_by_day.get(day, [])
            days_commits.append(commit)
            commits_by_day[day] = days_commits
        return commits_by_day

    def get_running_averages(self, commits_by_day, size=1):
        daily_entropies = []
        start_date = datetime.strptime(min(commits_by_day.keys()), '%Y%m%d')
        end_date =  datetime.strptime(max(commits_by_day.keys()), '%Y%m%d')
        for date in daterange(start_date, end_date + timedelta(1)):
            key = date.strftime('%Y%m%d')
            if date < start_date + timedelta(size - 1):
                daily_entropies.append((key, ''))
                continue
            commits = []
            for commit_date in daterange(date, date + timedelta(size)):
                commits += commits_by_day.get(commit_date.strftime('%Y%m%d'), [])
            average = self.get_average_entropy(commits)
            if average is not None:
                daily_entropies.append((key, average))
            else:
                daily_entropies.append((key, ''))
        return daily_entropies

    def get_average_entropy(self, commits):
        entropies = [c['entropy'] for c in commits if 'entropy' in c and not c['entropy'] == None]
        if entropies:
            return statistics.mean(entropies)
        else:
            return None

if __name__ == '__main__':
    pass
