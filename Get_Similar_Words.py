import datrie
import numpy as np

from myLevenshtein import Levenshtein_modified


def check(prefix, word_ini):
    if Levenshtein_modified(prefix, word_ini[:len(prefix)]) < 3:
        return True
    return False


def state_backup(trie, state):
    state_copy = datrie.State(trie)
    state.copy_to(state_copy)
    return state_copy


def search(trie, state, word_ini, prefix, result):
    if check(prefix, word_ini):
        it = datrie.Iterator(state)
        tmp = True
        state_ini = state_backup(trie, state)
        subnode = ''
        while it.next():
            if it.key():
                if it.key()[0] not in subnode:
                    state = state_backup(trie, state_ini)
                    state.walk(it.key()[0])
                    search(trie, state, word_ini, prefix + it.key()[0], result)
                    del state
                subnode += it.key()[0]
                tmp = False
        if tmp:
            result.append([prefix, it.data()])
    return result


def find_suggestion(trie, tag, number):
    state = datrie.State(trie)
    result = search(trie, state, tag, '', [])
    result = list(np.asarray(result)[:, 0])
    index = result.index(tag)
    result = result[index - int(number // 2):index + number - int(number // 2)]
    return result


# trie = datrie.Trie.load('./result/MO Code Trie.txt')
# state = datrie.State(trie)
# it = datrie.Iterator(state)
# tag = 'MO_APP4512'
# result = find_suggestion(trie, tag, 6)
# print(result)
