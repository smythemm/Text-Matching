import datrie
import string

from numba import jit, njit, types
# from numba.typed import Dict
# from numba.pycc import CC
from myLevenshtein import Levenshtein_modified


def check(word, word_ini, wrongChar):
    # print(word, word_ini, wrongChar, Levenshtein_modified(word, word_ini) < len(word_ini) // 2)
    len1, len2 = len(word), len(word_ini)
    if wrongChar < 3:
        if len1 > len2 // 2 & len1 <= len2:
            if Levenshtein_modified(word, word_ini) < len2 // 2:
                return True
            return False
        return True
    return False


def change_case(char):
    ascii = ord(char)
    return chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)


# @jit(nopython=False)
def search(trie, state_last, state, word, word_ini, prefix, result, path, wrongChar=0, flag=True):
    '''
    iniWord: initial test word
    result: a 3-d list, [word, distance, frequency]
    wrongChar: the number of consecutive incorrect characters, if greater than 3, discard, i.e., pre-pruning
    '''
    print('words:', prefix, word, wrongChar)
    if len(word) == 1:
        success = state.walk(word)
        it = datrie.Iterator(state)
        tmp = False
        while it.next():
            if success:
                wordInDict = prefix + word + it.key()
                tmp = True
            elif not success and check(prefix + it.key(), word_ini, wrongChar + 1):
                wordInDict = prefix + it.key()
                wrongChar += 1
                tmp = True
            else:
                continue
            distance = Levenshtein_modified(word_ini, wordInDict)
            result.append([wordInDict, distance, it.data(), wrongChar])
            print(result)
        if tmp:
            path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
            for p in path_pass:
                path[p] = 1
    else:
        state_before_walk = datrie.State(trie)
        state.copy_to(state_before_walk)
        state_last_before_walk = datrie.State(trie)
        state_last.copy_to(state_last_before_walk)
        char = word[0]
        success = state.walk(word[0])
        if not success:
            tmp = change_case(word[0])
            success = state.walk(tmp)
            if success:
                char = tmp
        print(success, word, prefix + char, path.keys())
        if success:
            if prefix + char not in path.keys():
                if len(prefix) == 0:
                    state_last.walk('')
                else:
                    state_last.walk(prefix[-1])
                state_copy_ini = datrie.State(trie)
                state.copy_to(state_copy_ini)
                state_last_copy_ini = datrie.State(trie)
                state_last.copy_to(state_last_copy_ini)
                it = datrie.Iterator(state)
                while it.next():
                    if not it.key():
                        distance = Levenshtein_modified(word_ini, prefix)
                        wordInDict = prefix + char
                        result.append([wordInDict, distance, it.data()])
                        path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
                        for p in path_pass:
                            path[p] = 1
                        print(result)
                    else:
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix + char, result, path, wrongChar, flag)
                        del state_copy, state_last_copy
                        if word == word_ini:
                            state_copy = datrie.State(trie)
                            state_before_walk.copy_to(state_copy)
                            state_last_copy = datrie.State(trie)
                            state_last_before_walk.copy_to(state_last_copy)
                            search(trie, state_last_copy, state_copy,
                                   change_case(word[0]) + word[1:], word_ini, prefix, result, path, wrongChar, flag)
                            del state_copy, state_last_copy
                        if flag:
                            possible_chars = ''
                            it = datrie.Iterator(state_before_walk)
                            while it.next():
                                if len(it.key()) and it.key()[0] != word[0] and it.key()[0] not in possible_chars:
                                    possible_chars += it.key()[0]
                            # for char in possible_chars:
                            #     if check(prefix + char, word_ini, wrongChar + 1):
                            #         state_copy = datrie.State(trie)
                            #         state_before_walk.copy_to(state_copy)
                            #         state_last_copy = datrie.State(trie)
                            #         state_last_before_walk.copy_to(state_last_copy)
                            #         search(trie, state_last_copy, state_copy, char + word[1:], word_ini, prefix, result, path, wrongChar + 1, False)
                            #         del state_copy, state_last_copy
                            #         state_copy = datrie.State(trie)
                            #         state_before_walk.copy_to(state_copy)
                            #         state_last_copy = datrie.State(trie)
                            #         state_last_before_walk.copy_to(state_last_copy)
                            #         search(trie, state_last_copy, state_copy, char + word, word_ini, prefix, result, path, wrongChar + 1, False)
                            #         del state_copy, state_last_copy
        else:
            if prefix + char not in path.keys():
                it = datrie.Iterator(state)
                state_copy_ini = datrie.State(trie)
                state.copy_to(state_copy_ini)
                state_last_copy_ini = datrie.State(trie)
                state.copy_to(state_last_copy_ini)
                while it.next():
                    # print(it.key())
                    if (check(prefix + it.key()[0], word_ini, wrongChar + 1) and
                        (it.key()[0] != change_case(char))) or (check(prefix + it.key()[0], word_ini, wrongChar) and
                                                                (it.key()[0] == change_case(char))):
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, it.key()[0] + word[1:], word_ini, prefix, result, path, wrongChar + 1, flag)
                        del state_copy, state_last_copy
                        # state_copy = datrie.State(trie)
                        # state_copy_ini.copy_to(state_copy)
                        # state_last_copy = datrie.State(trie)
                        # state_last_copy_ini.copy_to(state_last_copy)
                        # search(trie, state_last_copy, state_copy, it.key()[0] + word, word_ini, prefix, result, path, wrongChar + 1, flag)
                        # del state_copy, state_last_copy
                del state_copy_ini, state_last_copy_ini
    return result


# trie = datrie.Trie(string.ascii_letters + ' -_')
# trie['Absa'] = 100
# trie['Client'] = 5
# trie['ABSACF'] = 50
# trie['x_Client'] = 20
trie = datrie.Trie.load('./result/Tag Master Name Trie.txt')

state = datrie.State(trie)
state_last = datrie.State(trie)
it = datrie.Iterator(state)
# while it.next():
#     print(it.key(), end=',')
# print()
# tag = 'ABSACLOUD313'
tag = 'x_clien'
tag = ''.join(filter(str.isalnum, tag))
# # dict = Dict.empty(key_type=types.unicode_type, value_type=types.unicode_type)
result = search(trie, state_last, state, tag, tag, '', [], {}, 0)
print(tag, result)
