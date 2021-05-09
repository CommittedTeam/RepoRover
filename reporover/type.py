""" Detect the conventional style.

    guidelines:

    angular: https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
    atom: https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
    ember: https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md#pull-requests
    eslint: https://eslint.org/docs/developer-guide/contributing/pull-requests
    jshint: https://github.com/jshint/jshint/blob/master/CONTRIBUTING.md#commit-message-guidelines

"""

import re
from statistics import mode
from github import Github
import time
import urllib
import calendar
import json
import pandas as pd
import giturlparse
import collections
import statistics

def match(commit_msg):
    """Detremine which convention commit message is follwing"""
    # The regular expressions are adapted from https://github.com/conventional-changelog/conventional-commits-detector
    # Angular and eslint specify that commit tags must be one of the following
    commit_types = {

        "angular": "build|ci|docs|feat|fix|perf|refactor|test|chore|style",
        "eslint": "Fix|Update|New|Breaking|Docs|Build|Upgrade|Chore",

    }
    conventions = {

        "angular": r'^({})(?:\((.*)\))?: (.*)$'.format(commit_types["angular"]),
        "atom": r'^(:.*?:) (.*)$',
        "ember": r'^\[(.*) (.*)] (.*)$',
        "eslint": r'^({}): (.*?)(?:\((.*)\))?$'.format(commit_types["eslint"]),
        "jshint": r'^\[\[(.*)]] (.*)$',

    }
    
    temp_key = ""
    for key in conventions.keys():
        # Take subject line from the multiline commit messages
        if (re.match(conventions[key],commit_msg.split('\n')[0])):
            temp_key = key
            break
        else:
            # If commit message doesn't match any of the conventions return undefined
            temp_key = "undefined"

    return temp_key

def get_ratio(commit_messages):
    """Get frequency of the most common convention in the given commits"""
    #NOTE bug in case equal amounts
    conventions = [match(message) for message in commit_messages]
    convention = collections.Counter(conventions).most_common(1)
    ratio = (convention[0][0],convention[0][1]/len(conventions))

    return ratio

def wait(seconds):
    print("Waiting for {} seconds ...".format(seconds))
    time.sleep(seconds)
    print("Done waiting - resume!")

def api_wait(githb):
    rl = githb.get_rate_limit()
    current_time = calendar.timegm(time.gmtime())
    if  rl.core.remaining <= 10:  # extra margin of safety
        reset_time = calendar.timegm(rl.core.reset.timetuple())
        wait(reset_time - current_time + 10.0)
    elif rl.search.remaining <= 2:
        reset_time = calendar.timegm(rl.search.reset.timetuple())
        wait(reset_time - current_time + 10.0)

def get_repo_path(url):
    """Get full repository name from the url"""
    # The list of repositories that criticality_score gives has repository name but pygithub needs full path for repo
    parsed = giturlparse.parse(url)
    path = parsed.pathname[1:]
    return path

def is_conventional(urls):
    github = Github("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")
    
    i = 0
    conventions = []
    ratios = []
    while i < len(urls):
        path = get_repo_path(urls[i])
        repo = github.get_repo(path)
        commits = repo.get_commits()
        commit_messages = []

        try:
            for commit in commits[:100]:
                commit_messages.append(commit.commit.message)
            i+=1
        except:
            api_wait(github)
            continue

        convention = get_ratio(commit_messages)
        print(urls[i-1],convention[0],convention[1])
        conventions.append(convention[0])
        ratios.append(convention[1])

    return (conventions,ratios)