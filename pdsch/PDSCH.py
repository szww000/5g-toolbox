
############################ 初始化参数 ############################

numbits=512
NC=1600
n_RNTI = 2
q= 1
n_ID = 1

############################ 二进制序列生成 ############################

import random
#生成长度numbits的随机01序列x
x = []
for i in range(numbits):
    x.append(random.randint(0,1))
print(x)

############################ bite扰码 ############################
# 38.211
####### 5.2.1 x1序列生成
x_1 = []
x_zero = [0 for _ in range(30+1)]   # 全0列表
x_zeor1 = [[0] * 31]                # 全0列表1
x_1.extend(x_zero)
x_1[0] = 1
#
x_1_len = numbits + NC - 31
for k in range(x_1_len):
    # x_1[k+31] = (x_1[k+3]+x_1[k])%2
    x_1.append((x_1[k+3]+x_1[k])%2)    #  m序列x1

####### 5.2.1 m序列x2生成

c_init = n_RNTI * 2**15 + q * 2**14 + n_ID
# c_init_str = bin(c_init)       # 10进制转2进制，字符串且带前缀
c_init_str = '{:031b}'.format(c_init)  # 10进制转2进制，字符串，不带前缀，高位补0
c_init_str1 = c_init_str[::-1]   # 逆序
x_2 = list(map(int, c_init_str1))  # 取字符串不带前缀部分转int并存放于序列中
x_2_len = numbits + NC - 31
for k in range(x_2_len):
    x_2.append((x_2[k+3]+x_2[k+2]+x_2[k+1]+x_2[k])%2) #  m序列x2

####### 5.2.1  gold序列生成
c_n = []
for k in range(numbits):
    c_n.append((x_1[k + NC] + x_2[k + NC]) % 2)  #  gold序列c(n)

####### 7.3.1.1 扰码
b_i = x
c_i = c_n
b__i = []
for k in range(numbits):
    b__i.append((b_i[k] + c_i[k]) % 2)    # 加扰后序列 b(q)(i)
