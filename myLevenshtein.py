import numpy as np
from Config import KEYBOARD


def Levenshtein_modified(str1, str2, use_for_get_master=False):
    str1, str2 = ''.join(filter(str.isalnum, str1.lower())), ''.join(filter(str.isalnum, str2.lower()))

    if use_for_get_master:
        if str1 in str2 or str2 in str1:
            return 0

    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    matrix = np.zeros(shape=(len_str1, len_str2))

    for i in range(len_str1):
        for j in range(len_str2):
            if min(i, j) == 0:
                matrix[i][j] = max(i, j)
            else:
                if str1[i - 1] == str2[j - 1]:
                    cost = 0
                else:
                    cost = 2
                    if str1[i - 1].isalpha() and str2[j - 1].isalpha():
                        if str1[i - 1] in KEYBOARD[str2[j - 1]] or str2[j - 1] in KEYBOARD[str1[i - 1]]:
                            cost = 1
                matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
                if i > 1 and j > 1 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1]:
                    matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + 1)

    # the last element of matrix is the editing distance
    # the condition is considering the length of string
    # the distance between 2 short words is small although they are totally different
    if (matrix[-1][-1] - abs(len_str1 - len_str2)) > min(len(str1), len(str2)) / 3:
        return 1000

    # return matrix[-1]
    return matrix[-1][-1]
