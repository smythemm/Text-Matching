import numpy as np


def Levenshtein_Recursion(a, len_a, b, len_b):
    # 递归回归点
    if (len_a == 0):
        return len_b
    if (len_b == 0):
        return len_a

    if (a[len_a - 1] == b[len_b - 1]):
        cos = 0
    else:
        cos = 1

    re1 = Levenshtein_Recursion(a, len_a - 1, b, len_b) + 1
    re2 = Levenshtein_Recursion(a, len_a, b, len_b - 1) + 1
    re3 = Levenshtein_Recursion(a, len_a - 1, b, len_b - 1) + cos
    # 返回在a中删除一个字符、在b中删除一个字符、ab中均删除一个字符获得结果中取最小值
    if re1 < re2:
        if re1 < re3:
            return re1
        else:
            return re3
    else:
        if re2 < re3:
            return re2
        else:
            return re3


def Levenshtein_modified(str1, str2, use_for_get_master=False):
    str1, str2 = ''.join(filter(str.isalnum, str1.lower())), ''.join(filter(str.isalnum, str2.lower()))
    if use_for_get_master:
        if str1 in str2 or str2 in str1:
            return 0

    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    matrix = np.zeros(shape=(len_str1 * len_str2, ))

    for i in range(len_str1):
        matrix[i] = i

    for j in range(0, len(matrix), len_str1):
        if j % len_str1 == 0:
            matrix[j] = j // len_str1

    # the editing distance is obtained step by step according to the state transition equation
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[j * len_str1 + i] = min(matrix[(j - 1) * len_str1 + i] + 1, matrix[j * len_str1 + (i - 1)] + 1,
                                           matrix[(j - 1) * len_str1 + (i - 1)] + cost)

    # the last element of matrix is the editing distance
    # the condition is considering the length of string
    # the distance between 2 short words is small although they are totally different
    if (matrix[-1] - abs(len_str1 - len_str2)) > min(len(str1), len(str2)) / 3:
        return 1000

    return matrix[-1]