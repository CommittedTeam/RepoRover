import pandas as pd


data = pd.read_csv("labeled_critical_repos.csv")

conventions = data["convention"].tolist()
names = data["name"].tolist()
languages = data["language"].tolist()
count = {}

ind = 0
for i in conventions:
    if i != "undefined":
        pl = languages[ind]
        if pl in count.keys():
            count[pl] += 1
        else:
            count.update({pl:0})
    ind += 1


print(count)

# print(names)

# count = 0
# for i in languages:
#     if i == "TypeScript":
#         print(names[count])
#     count += 1

data = pd.read_csv("all.csv")
criticality = data['criticality_score'].tolist()

top = 0

for i in criticality:
    if i > 0.51:
        top += 1

print(top/len(criticality)*100)


