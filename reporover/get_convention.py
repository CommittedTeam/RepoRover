""" Detect the conventional style.

    guidelines:

    angular: https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit
    atom: https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages
    ember: https://github.com/emberjs/ember.js/blob/master/CONTRIBUTING.md#pull-requests
    eslint: https://eslint.org/docs/developer-guide/contributing/pull-requests
    jshint: https://github.com/jshint/jshint/blob/master/CONTRIBUTING.md#commit-message-guidelines

"""

import re


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



