import pandas as pd
import numpy as np

data = pd.read_feather("data/gatorgrader.ftr")

random_10 = data.sample(n=10, random_state=1)
random_10.reset_index(level=0, inplace=True)


diffs = random_10[['index', 'diffs']]

commit_metadata = random_10.drop(columns=['diffs', 'commit_author_name',"commit_author_email","commit_msg","commit_type"])

dictionary = commit_metadata.to_dict(orient='records')


for i in dictionary:
    diff = list(diffs.loc[diffs['index'] == i["index"], 'diffs'])[0]
    files = list(random_10.loc[random_10['index'] == i["index"], 'file_paths'])[0]
    
    with open("data/experiment/{}.txt".format(i["index"]),"a+") as f:

        for key,value in i.items():
            f.write("{}:  {}\n".format(key,value))
        for file_ in diff:
            index = np.where(diff==file_)[0][0]
            file_name = files[index]
            f.write("\n\ndiff of {}:\n{}".format(file_name,file_))   

        








