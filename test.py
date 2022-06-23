import datrie
from myLevenshtein import Levenshtein_modified

trie = datrie.Trie.load('./result/Tag Master Name Trie.txt')
tag = 'x_clien'
tag = ''.join(filter(str.isalnum, tag))
test_list = [tag[i:i + 4] for i in range(len(tag))]

res_list = []
for t in test_list:
    res = trie.items(t)
    if len(res):
        master_name = 
        res_list.append([t, res])

print(res_list)