from pydriller import RepositoryMining
from reporover import collect

def collect(path,save=None):
    """Path can take only one repo as well as list of repos"""
    commit_data = pd.DataFrame(get_commit_data(path))   
    print(commit_data)
    if path:
        commit_data.to_feather(save)
    return (commit_data)