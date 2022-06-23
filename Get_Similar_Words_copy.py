import datrie
import string

from myLevenshtein import Levenshtein_modified


def check(wrongChar):
    if wrongChar < 3:
        return True
    return False


def change_case(char):
    ascii = ord(char)
    return chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)


def search(trie, state_last, state, word, word_ini, prefix, result, path={}, wrongChar=0, flag=True):
    '''
    iniWord: initial test word
    result: a 3-d list, [word, distance, frequency]
    wrongChar: the number of consecutive incorrect characters, if greater than 3, discard, i.e., pre-pruning
    '''
    print(f'word: {word}, wrongChar: {wrongChar}')
    if len(word) == 1:
        print('info', word, prefix)
        success = state.walk(word)
        it = datrie.Iterator(state)
        while it.next():
            print(success, it.key())
            if success:
                wordInDict = prefix + word + it.key()
            elif not success and check(wrongChar + 1):
                wordInDict = prefix + it.key()
            else:
                continue
            distance = Levenshtein_modified(word_ini, wordInDict)
            result.append([wordInDict, distance, it.data()])
        path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
        for p in path_pass:
            path[p] = 1
        print(result)
    else:
        # can find the first char
        it = datrie.Iterator(state)
        while it.next():
            print(it.key(), end=',')
        print()
        state_before_walk = datrie.State(trie)
        state.copy_to(state_before_walk)
        state_last_before_walk = datrie.State(trie)
        state_last.copy_to(state_last_before_walk)
        char = word[0]
        success = state.walk(word[0])
        print('success:', word[0], success, end=',')
        if not success:
            tmp = change_case(word[0])
            success = state.walk(tmp)
            if success:
                char = tmp
            print(char, success)
        print()
        print('info:', word, prefix, prefix + char, path.keys(), prefix + char in path.keys(), wrongChar)
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
                    print('it.next():', it.key())
                    if not it.key():
                        distance = Levenshtein_modified(word_ini, prefix)
                        wordInDict = prefix + char
                        result.append([wordInDict, distance, it.data()])
                        path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
                        for p in path_pass:
                            path[p] = 1
                        print('dict短,', result)
                    else:
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix + char, result, path, wrongChar, flag)
                        del state_copy, state_last_copy
                        print('finish')
                        if flag:
                            possible_chars = ''
                            it = datrie.Iterator(state_before_walk)
                            # print(state_last_id)
                            while it.next():
                                print(it.key(), end=',')
                                if len(it.key()) and it.key()[0] != word[0] and it.key()[0] not in possible_chars:
                                    possible_chars += it.key()[0]
                            print()
                            # it = datrie.Iterator(state_last_copy)
                            # # print(state_last_id)
                            # while it.next():
                            #     print(it.key(), end=',')
                            print('\npossible:', possible_chars)
                            for char in possible_chars:
                                print(char)
                                print('循环', char, word, prefix, char + word[1:])
                                if check(wrongChar + 1):
                                    state_copy = datrie.State(trie)
                                    state_before_walk.copy_to(state_copy)
                                    state_last_copy = datrie.State(trie)
                                    state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word[1:], word_ini, prefix, result, path, wrongChar + 1, False)
                                    del state_copy, state_last_copy
                                    state_copy = datrie.State(trie)
                                    state_before_walk.copy_to(state_copy)
                                    state_last_copy = datrie.State(trie)
                                    state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word, word_ini, prefix, result, path, wrongChar + 1, False)
                                    del state_copy, state_last_copy
        else:
            # the first char is wrong
            print('wrong/missing:', prefix + char, path.keys(), prefix + char in path.keys(), wrongChar)
            if prefix + char not in path.keys():
                it = datrie.Iterator(state)
                while it.next():
                    print(it.key(), end=',')
                print()
                it = datrie.Iterator(state)
                state_copy_ini = datrie.State(trie)
                state.copy_to(state_copy_ini)
                state_last_copy_ini = datrie.State(trie)
                state.copy_to(state_last_copy_ini)
                while it.next() and it.key():
                    print(it.key(), word, wrongChar)
                    if (it.key()[0] != change_case(word[0]) and check(wrongChar + 1)) or (it.key()[0] == change_case(word[0]) and check(wrongChar)):
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        print('  wrong:')
                        print('else,', it.key(), word, it.key()[0] + word[1:])
                        search(trie, state_last_copy, state_copy, it.key()[0] + word[1:], word_ini, prefix, result, path, wrongChar + 1, flag)
                        del state_copy, state_last_copy
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        print('  missing:')
                        print('else,', it.key(), word, it.key()[0] + word)
                        search(trie, state_last_copy, state_copy, it.key()[0] + word, word_ini, prefix, result, path, wrongChar + 1, flag)
                        del state_copy, state_last_copy
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
tag = 'x_Clien'
# # dict = Dict.empty(key_type=types.unicode_type, value_type=types.unicode_type)
result = search(trie, state_last, state, tag, tag, '', [], {}, 0)
print(tag, result)