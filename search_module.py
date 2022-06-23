import datrie
import string

# from numba import njit, types
# from numba.typed import Dict
from numba.pycc import CC
from Levenshtein import Levenshtein_Dynamic

#指定cc输出的编译 pyd文件的存放目录
from numba import njit, types, typed


def check(wrongChar):
    if wrongChar < 3:
        return True
    return False


def change_case(char):
    ascii = ord(char)
    return chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)


cc = CC('datrie_module')
cc.output_dir = './'
cc.verbose = True

# cc.__class__


@cc.export(
    'search',
    '(trie, state, state, unicode_type, unicode_type, unicode_type, types.DictType(types.unicode_type, types.ListType(types.int32)), types.DictType(types.unicode_type, types.ListType(types.int32)), int64, boolean)'
)
# @cc.export('Trie')
@njit
def search(trie, state_last, state, word, word_ini, prefix, result, path, wrongChar=0, flag=True):
    '''
    iniWord: initial test word
    result: a 3-d list, [word, distance, frequency]
    wrongChar: the number of consecutive incorrect characters, if greater than 3, discard, i.e., pre-pruning
    '''
    if len(word) == 1:
        success = state.walk(word)
        it = datrie.Iterator(state)
        while it.next():
            if success:
                wordInDict = prefix + word + it.key()
            elif not success and wrongChar + 1 < 3:
                wordInDict = prefix + it.key()
            else:
                continue
            # distance = Levenshtein_Dynamic(word_ini, wordInDict)
            # distance = 0
            # result.append([wordInDict, distance, it.data()])
            result[wordInDict] = typed.Dict.empty(types.unicode_type, types.ListType(types.int32))
            result[wordInDict].append(it.data())
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
            ascii = ord(word[0])
            tmp = chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)
            # tmp = change_case(word[0])
            success = state.walk(tmp)
            if success:
                char = tmp
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
                        # distance = Levenshtein_Dynamic(word_ini, prefix)
                        distance = 0
                        wordInDict = prefix + char
                        # result.append([wordInDict, distance, it.data()])
                        result[wordInDict] = typed.Dict.empty(types.unicode_type, types.ListType(types.int32))
                        result[wordInDict].append(it.data())
                        path_pass = [wordInDict[:i + 1] for i in range(len(wordInDict))]
                        for p in path_pass:
                            path[p] = 1
                    else:
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, word[1:], word_ini, prefix + char, result, path, wrongChar, flag)
                        # del state_copy, state_last_copy
                        if flag:
                            possible_chars = ''
                            it = datrie.Iterator(state_before_walk)
                            while it.next():
                                if len(it.key()) and it.key()[0] != word[0] and it.key()[0] not in possible_chars:
                                    possible_chars += it.key()[0]
                            for char in possible_chars:
                                if wrongChar + 1 < 3:
                                    state_copy = datrie.State(trie)
                                    state_before_walk.copy_to(state_copy)
                                    state_last_copy = datrie.State(trie)
                                    state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word[1:], word_ini, prefix, result, path, wrongChar + 1, False)
                                    # del state_copy, state_last_copy
                                    state_copy = datrie.State(trie)
                                    state_before_walk.copy_to(state_copy)
                                    state_last_copy = datrie.State(trie)
                                    state_last_before_walk.copy_to(state_last_copy)
                                    search(trie, state_last_copy, state_copy, char + word, word_ini, prefix, result, path, wrongChar + 1, False)
                                    # del state_copy, state_last_copy
        else:
            if prefix + char not in path.keys():
                it = datrie.Iterator(state)
                state_copy_ini = datrie.State(trie)
                state.copy_to(state_copy_ini)
                state_last_copy_ini = datrie.State(trie)
                state.copy_to(state_last_copy_ini)
                while it.next() and it.key():
                    ascii = ord(word[0])
                    tmp = chr(ascii + 32) if ascii <= 90 else chr(ascii - 32)
                    if (it.key()[0] != tmp and wrongChar + 1 < 3) or (it.key()[0] == tmp and wrongChar < 3):
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, it.key()[0] + word[1:], word_ini, prefix, result, path, wrongChar + 1, flag)
                        # del state_copy, state_last_copy
                        state_copy = datrie.State(trie)
                        state_copy_ini.copy_to(state_copy)
                        state_last_copy = datrie.State(trie)
                        state_last_copy_ini.copy_to(state_last_copy)
                        search(trie, state_last_copy, state_copy, it.key()[0] + word, word_ini, prefix, result, path, wrongChar + 1, flag)
                        # del state_copy, state_last_copy
                # del state_copy_ini, state_last_copy_ini
    return result


if __name__ == "__main__":
    cc.compile()