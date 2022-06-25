import datrie
import string

from myLevenshtein import Levenshtein_modified


def check(prefix, word_ini, index):
    if Levenshtein_modified(prefix, word_ini[:index + 1]) < 2:
        return True
    return False


def state_backup(trie, state):
    state_copy = datrie.State(trie)
    state.copy_to(state_copy)
    return state_copy


# def change_case(char):
#     ascii = ord(char)
#     return chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)


def search(trie, state_last, state, word, word_ini, prefix, index, result, path={}, wrongChar=0, flag=True):
    '''
    iniWord: initial test word
    result: a 3-d list, [word, distance, index of wordInDict]
    wrongChar: the number of consecutive incorrect characters, if greater than 3, discard, i.e., pre-pruning
    '''
    # print(f'word: {word}, wrongChar: {wrongChar}')
    if len(word) == 1:
        # print('info', word, prefix)
        success = state.walk(word)
        it = datrie.Iterator(state)
        wordInDict = ''
        while it.next():
            # print(success, it.key())
            if success:
                if len(prefix) < 3:
                    if prefix == word_ini[:index + 1]:
                        wordInDict = prefix + word + it.key()
                else:
                    wordInDict = prefix + word + it.key()
            elif not success and check(prefix + it.key(), word_ini, index + 1):
                wordInDict = prefix + it.key()
            else:
                continue
            distance = Levenshtein_modified(word_ini, wordInDict)
            result.append([wordInDict, distance, it.data()])
        if wordInDict != '':
            path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
            for p in path_pass:
                path[p] = 1
            print(result)
    else:
        # can find the first char
        # it = datrie.Iterator(state)
        # while it.next():
        #     print(it.key(), end=',')
        # print()
        state_before_walk = state_backup(trie, state)
        state_last_before_walk = state_backup(trie, state_last)
        # state_before_walk = datrie.State(trie)
        # state.copy_to(state_before_walk)
        # state_last_before_walk = datrie.State(trie)
        # state_last.copy_to(state_last_before_walk)
        char = word[0]
        success = state.walk(word[0])
        # print('success:', word[0], success, end=',')
        # if not success:
        #     tmp = change_case(word[0])
        #     success = state.walk(tmp)
        #     if success:
        #         char = tmp
        #     print(char, success)
        # print()
        # print('info:', word, prefix, prefix + char, path.keys())
        if success:
            if prefix + char not in path.keys():
                if len(prefix) == 0:
                    state_last.walk('')
                else:
                    state_last.walk(prefix[-1])
                state_copy_ini = state_backup(trie, state)
                state_last_copy_ini = state_backup(trie, state_last)
                # state_copy_ini = datrie.State(trie)
                # state.copy_to(state_copy_ini)
                # state_last_copy_ini = datrie.State(trie)
                # state_last.copy_to(state_last_copy_ini)
                it = datrie.Iterator(state)
                while it.next():
                    # print('it.next():', it.key())
                    if not it.key():
                        distance = Levenshtein_modified(word_ini, prefix)
                        wordInDict = ''
                        if len(prefix) < 3:
                            if prefix == word_ini[:len(prefix)]:
                                wordInDict = prefix + char
                        else:
                            wordInDict = prefix + char
                        if wordInDict != '':
                            result.append([wordInDict, distance, it.data()])
                            path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
                            for p in path_pass:
                                path[p] = 1
                            # print('dict短,', result)
                    else:
                        state_copy = state_backup(trie, state_copy_ini)
                        state_last_copy = state_backup(trie, state_last_copy_ini)
                        # state_copy = datrie.State(trie)
                        # state_copy_ini.copy_to(state_copy)
                        # state_last_copy = datrie.State(trie)
                        # state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix + char, index + 1, result, path, wrongChar, flag)
                        del state_copy, state_last_copy
                        # print('finish')
                        if flag:
                            possible_chars = ''
                            it = datrie.Iterator(state_before_walk)
                            # print(state_last_id)
                            while it.next():
                                # print(it.key(), end=',')
                                if len(it.key()) and it.key()[0] != word[0] and it.key()[0] not in possible_chars:
                                    possible_chars += it.key()[0]
                            # print()
                            # it = datrie.Iterator(state_last_copy)
                            # # print(state_last_id)
                            # while it.next():
                            #     print(it.key(), end=',')
                            # print('\npossible:', possible_chars)
                            for char in possible_chars:
                                # print(char)
                                # print('循环', char, word, prefix, char + word[1:])
                                if check(prefix, word_ini, index):
                                    state_copy = state_backup(trie, state_before_walk)
                                    state_last_copy = state_backup(trie, state_last_before_walk)
                                    # state_copy = datrie.State(trie)
                                    # state_before_walk.copy_to(state_copy)
                                    # state_last_copy = datrie.State(trie)
                                    # state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word[1:], word_ini, prefix, index, result, path, wrongChar + 1,
                                           False)
                                    del state_copy, state_last_copy
                                    state_copy = state_backup(trie, state_before_walk)
                                    state_last_copy = state_backup(trie, state_last_before_walk)
                                    # state_copy = datrie.State(trie)
                                    # state_before_walk.copy_to(state_copy)
                                    # state_last_copy = datrie.State(trie)
                                    # state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word, word_ini, prefix, index, result, path, wrongChar + 1,
                                           False)
                                    del state_copy, state_last_copy
                                if check(prefix, word_ini, index + 1):
                                    state_copy = state_backup(trie, state_before_walk)
                                    state_last_copy = state_backup(trie, state_last_before_walk)
                                    # state_copy = datrie.State(trie)
                                    # state_before_walk.copy_to(state_copy)
                                    # state_last_copy = datrie.State(trie)
                                    # state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix, index + 1, result, path, wrongChar + 1,
                                           False)
                                    del state_copy, state_last_copy
        else:
            # the first char is wrong
            # print('wrong/missing:', prefix + char, path.keys(), prefix + char in path.keys(), wrongChar)
            if prefix + char not in path.keys():
                # it = datrie.Iterator(state)
                # while it.next():
                #     print(it.key(), end=',')
                # print()
                state_copy_ini = state_backup(trie, state)
                state_last_copy_ini = state_backup(trie, state_last)
                # state_copy_ini = datrie.State(trie)
                # state.copy_to(state_copy_ini)
                # state_last_copy_ini = datrie.State(trie)
                # state.copy_to(state_last_copy_ini)
                it = datrie.Iterator(state)
                while it.next() and it.key():
                    # print(it.key(), word, wrongChar)
                    state_copy = state_backup(trie, state_copy_ini)
                    state_last_copy = state_backup(trie, state_last_copy_ini)
                    # state_copy = datrie.State(trie)
                    # state_copy_ini.copy_to(state_copy)
                    # state_last_copy = datrie.State(trie)
                    # state_last_copy_ini.copy_to(state_last_copy)
                    if check(prefix, word_ini, index + 1):
                        search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix, index + 1, result, path, wrongChar + 1, flag)
                    del state_copy, state_last_copy
                    if check(prefix, word_ini, index):
                        state_copy = state_backup(trie, state_copy_ini)
                        state_last_copy = state_backup(trie, state_last_copy_ini)
                        # state_copy = datrie.State(trie)
                        # state_copy_ini.copy_to(state_copy)
                        # state_last_copy = datrie.State(trie)
                        # state_last_copy_ini.copy_to(state_last_copy)
                        # print('  wrong:')
                        # print('else,', it.key(), word, it.key()[0] + word[1:])
                        search(trie, state_last_copy, state_copy, it.key()[0] + word[1:], word_ini, prefix, index, result, path, wrongChar + 1, flag)
                        del state_copy, state_last_copy
                        state_copy = state_backup(trie, state_copy_ini)
                        state_last_copy = state_backup(trie, state_last_copy_ini)
                        # state_copy = datrie.State(trie)
                        # state_copy_ini.copy_to(state_copy)
                        # state_last_copy = datrie.State(trie)
                        # state_last_copy_ini.copy_to(state_last_copy)
                        # print('  missing:')
                        # print('else,', it.key(), word, it.key()[0] + word)
                        search(trie, state_last_copy, state_copy, it.key()[0] + word, word_ini, prefix, index, result, path, wrongChar + 1, flag)
                        del state_copy, state_last_copy
                del state_copy_ini, state_last_copy_ini
    return result


trie = datrie.Trie(string.ascii_letters + ' -_')
trie['001'] = 100
trie['Client'] = 5
trie['ABSACF'] = 50
trie['xClient'] = 20
# trie = datrie.Trie.load('./result/MO Code Trie.txt')

state = datrie.State(trie)
state_last = datrie.State(trie)
# it = datrie.Iterator(state)
# while it.next():
#     print(it.key(), end=',')
# print()
tag = 'APPL001'
# tag = 'x_xlien'
tag = ''.join(filter(str.isalnum, tag.lower()))
for i in range(len(tag)):
    if str.isdigit(tag[i]):
        break
    else:
        state.walk(tag[i])
        if i > 0:
            state_last.walk(tag[i - 1])
# # dict = Dict.empty(key_type=types.unicode_type, value_type=types.unicode_type)
result = search(trie, state_last, state, tag[i:], tag[i:], '', 0, [], {}, 0)
print(tag, result)