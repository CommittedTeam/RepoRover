from reporover import get_commit_data
from reporover import get_convention
import pandas as pd
import collections
from pydriller import RepositoryMining
import typer

app = typer.Typer()

@app.command()
def convention(path):
    """Get counts of conventions in the given repo"""
    conventions = []
    # set order to reverse so that we get the newest commits first
    for commit in RepositoryMining(path,reversed_order=True).traverse_commits():
        conventions.append(get_convention.match(commit.msg))
    convention_count = dict(collections.Counter(conventions))
    return convention_count

@app.command()
def collect(path, save=None):
    """Collect the commit data with pydriller."""
    commits_info = []

    # TODO Pass in reversed to reverese the commits

    for commit in RepositoryMining(path,reversed_order=True).traverse_commits():
        commit_type = get_commit_data.get_commit_types(commit.msg.lower())
        # skip commits that do not follow conventional commit types syntax
        if commit_type is not None:
            file_paths = []
            diffs = []

            commit_message = commit.msg
            author_name = commit.author.name
            author_email = commit.author.email

            for m in commit.modifications:
    
                diffs.append(m.diff)
                path = m.new_path
                # new path may return None if the file was deleted
                if path:
                    file_paths.append(path)
                else:
                    file_paths.append("deleted_file")

            file_extensions = get_commit_data.get_file_extensions(file_paths)
            test_files_count = get_commit_data.test_files(file_paths)

            commit_data = {

                "name": commit.project_name,
                "commit_hash": commit.hash,
                "commit_msg": commit_message,
                "commit_subject": get_commit_data.get_subject_line(commit_message),
                "commit_type": commit_type,
                "commit_author_name": author_name,
                "commit_author_email": author_email,
                "isbot": get_commit_data.isbot(author_name,author_email),               
                "file_paths": file_paths,
                "num_files": commit.files,
                "test_files": test_files_count,
                "unique_file_extensions": file_extensions,
                "num_unique_file_extensions": len(file_extensions),
                "num_lines_added": commit.insertions,
                "num_lines_removed": commit.deletions,
                "num_lines_total": commit.lines,

            }
            commits_info.append(commit_data)

    commit_data = pd.DataFrame(commits_info)
    print(commit_data)
    if save:
        commit_data.to_feather(save)
    return commit_data


