from reporover import get_convention
import os
import re


def get_commit_types(commit_msg):
    """Check if commit message follows angular conventional syntax and get commit type"""
    try:
        if get_convention.match(commit_msg) != "undefined":
            commit_type = re.findall( r'[a-zA-Z]+', commit_msg)[0]
            return commit_type
    except:
        return None

def parse_for_extension(paths):
    """Parse through file name and returns its extension."""
    formats = [os.path.splitext(path)[1] for path in paths]
    return formats

def get_file_extensions(file_formats):
    """Create a list of unique file extensions."""
    # get unique elements of the list using set method, list will be unordered
    unique_file_formats = list(set(parse_for_extension(file_formats)))
    # sort the set for testing purposes
    sorted_formats = sorted(unique_file_formats)
    return sorted_formats

def get_subject_line(message):
    """Separate commit subject from the commit type"""
    if message:
        subject = re.split(': |] ',message)[1]
        return subject

def isbot(commit_author_name, commit_author_email):
    """Detect bots """
    # If there is keyword bot in the author name or email then that is considered as bot
    isbot = False
    if re.findall( r'.bot.', commit_author_email) or re.findall( r'.bot.', commit_author_name):
        isbot = True
    return isbot

def test_files(paths):
    """
    Get the number of the test related files."
    """
    # This feature assumes that test files contain word "test
    test_files_count = len([path for path in paths if "test" in path.lower()])
    return test_files_count

def get_ratio(numerator,denominator):
    ratio = 0
    try:
        return(numerator/denominator) 
    except:
        ratio



