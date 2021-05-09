from reporover import parse
import pandas as pd

def collect(path,save=None):
    """Path can take only one repo as well as list of repos"""
    commit_data = pd.DataFrame(parse.get_commit_data(path))   
    print(commit_data)
    if save:
        commit_data.to_feather(save)
    return (commit_data)