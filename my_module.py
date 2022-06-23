import numpy
from math import sqrt
from numba.pycc import CC

CC.output_dir = './'
#指定cc输出的编译 pyd文件的存放目录
from numba import njit

cc = CC('my_module')  #my_module就是我们编译之后的pyd文件的名字，也是我们后续import mu_module的库名

# Uncomment the following line to print out the compilation steps
#cc.verbose = True


@cc.export('multf', 'f8(f8, f8)')  #这里支类似与c中的多态，根据输入数据的数据类型设置不同的函数名
@cc.export('multi', 'i4(i4, i4)')  #我们在调用的时候，根据输入数据的数据类型分开调用my_module.multi和my_module.multf
@njit
def mult(a, b):
    for i in range(1000):
        a * b
    return a * b


@cc.export('square', 'f8(f8)')  #意义同上
@njit
def square(a):
    return a**2


if __name__ == "__main__":
    cc.compile()  #通过cc.compile进行编译
