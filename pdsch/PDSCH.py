import math
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

############################ 调制 ############################
mod = 8   # 1:BPSK  2:QPSK   4: 16QAM  6: 64QAM  8: 256QAM
d_i = []
if mod == 1:
    for i in range( int(numbits / mod) ):
      d_i.append(math.sqrt(1/2)*(complex(1-2*b__i[i],1-2*b__i[i])))
elif mod == 2:
    for i in range( int(numbits / mod) ):
     d_i.append(math.sqrt(1/2)*(complex(1-2*b__i[2*i],1-2*b__i[2*i+1])))

elif mod == 4:
     for i in range(int(numbits / mod)):
         d_i.append(math.sqrt(1 / 10) * (
             complex((1 - 2 * b__i[4 * i] )    * (2 - (1 - 2 * b__i[4 * i + 2])),
                     (1 - 2 * b__i[4 * i + 1]) * (2 - (1 - 2 * b__i[4 * i + 3])))))
         # d_i.append((
         #     complex((1 - 2 * b__i[4 * i] )* (2 - (1 - 2 * b__i[4 * i + 2])),
         #             (1 - 2 * b__i[4 * i + 1]) * (2 - (1 - 2 * b__i[4 * i + 3])))))
elif mod == 6:
    for i in range( int(numbits / mod) ):
     d_i.append(math.sqrt(1/42)*(complex
                                 (1-2*b__i[6*i]  *(4-(1-2*b__i[6*i+2])*(2-(1-2*b__i[6*i+4]))),
                                  (1-2*b__i[6*i+1])*(4-(1-2*b__i[6*i+3])*(2-(1-2*b__i[6*i+5]))))))
     # d_i.append((complex
     #                             ((1-2*b__i[6*i])  *(4-(1-2*b__i[6*i+2])*(2-(1-2*b__i[6*i+4]))),
     #                              (1-2*b__i[6*i+1])*(4-(1-2*b__i[6*i+3])*(2-(1-2*b__i[6*i+5]))))))

else:
    for i in range( int(numbits / mod) ):
     # d_i.append(math.sqrt(1/170)*(complex
     #                             ((1-2*b__i[8*i])  *(8-(1-2*b__i[8*i+2])*(4-(1-2*b__i[8*i+4]))*(2-(1-2*b__i[8*i+6]))),
     #                              (1-2*b__i[6*i+1])*(4-(1-2*b__i[6*i+3])*(4-(1-2*b__i[8*i+5]))*(2-(1-2*b__i[8*i+7]))))))
     d_i.append((complex
                                 ((1-2*b__i[8*i])  *(8-(1-2*b__i[8*i+2])*(4-(1-2*b__i[8*i+4])*(2-(1-2*b__i[8*i+6])))),
                                  (1-2*b__i[8*i+1])*(8-(1-2*b__i[8*i+3])*(4-(1-2*b__i[8*i+5])*(2-(1-2*b__i[8*i+7])))))))


     ### 解调

d_i_demap = []
# BPSK
if mod == 1:
    for i in range(len(d_i)):
        d_i1 = [x / math.sqrt(1 / 2) for x in d_i]
        real_num = d_i[i].real
        if real_num > 0:
          d_i_demap.append(0)
        else:
          d_i_demap.append(1)
# QAM
if mod == 2:
    for i in range(len(d_i)):
      d_i1 = [x / math.sqrt(1/2) for x in d_i]
      real_num = -d_i[i].real
      imag_num = -d_i[i].imag
      if real_num > 0:
          d_i_demap.append(1)
      else:
          d_i_demap.append(0)
      if imag_num > 0:
          d_i_demap.append(1)
      else:
          d_i_demap.append(0)
# 16QAM
elif mod == 4:
    for i in range(len(d_i)):
      d_i1 = [x / math.sqrt(1 / 10) for x in d_i]
      real_num = d_i1[i].real
      real_num1 = -abs(d_i1[i].real)+2
      imag_num = d_i1[i].imag
      imag_num1 = -abs(d_i1[i].imag)+2
      if real_num > 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if imag_num > 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if real_num1> 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if imag_num1> 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)

# 64Qam
elif mod == 6:
    for i in range(len(d_i)):
      d_i1 = [x / math.sqrt(1/42) for x in d_i]
      real_num = d_i1[i].real
      real_num1 = -abs(d_i1[i].real)+2
      imag_num = d_i1[i].imag
      imag_num1 = -abs(d_i1[i].imag)+2
      if real_num > 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if imag_num > 0:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)

      if real_num1> -2 :
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)

      if imag_num1> -2:
          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if real_num1<0 and real_num1>-4 :

          d_i_demap.append(0)
      else:
          d_i_demap.append(1)
      if imag_num1<0 and imag_num1>-4 :

          d_i_demap.append(0)
      else:
          d_i_demap.append(1)

# 256Qam
else:
    d_i_demap = [0] * numbits
    for i in range(len(d_i)):
        d_i1 = d_i
        real_num = d_i1[i].real
        real_num1 = abs(d_i1[i].real)
        imag_num = d_i1[i].imag
        imag_num1 = abs(d_i1[i].imag)
        if real_num > 0:
            d_i_demap[8*i]=0
        else:
            d_i_demap[8 * i] = 1
        if imag_num > 0:
            d_i_demap[8 * i+1] = 0
        else:
            d_i_demap[8 * i + 1] = 1
        if real_num1 > 0 and real_num1 < 2 :
            d_i_demap[8 * i + 2] = 0
            d_i_demap[8 * i + 4] = 1
            d_i_demap[8 * i + 6] = 1
        elif real_num1 > 2 and real_num1 < 4 :
            d_i_demap[8 * i + 2] = 0
            d_i_demap[8 * i + 4] = 1
            d_i_demap[8 * i + 6] = 0
        elif real_num1 > 4 and real_num1 < 6 :
            d_i_demap[8 * i + 2] = 0
            d_i_demap[8 * i + 4] = 0
            d_i_demap[8 * i + 6] = 0
        elif real_num1 > 6 and real_num1 < 8 :
            d_i_demap[8 * i + 2] = 0
            d_i_demap[8 * i + 4] = 0
            d_i_demap[8 * i + 6] = 1
        elif real_num1 > 8 and real_num1 < 10 :
            d_i_demap[8 * i + 2] = 1
            d_i_demap[8 * i + 4] = 0
            d_i_demap[8 * i + 6] = 1
        elif real_num1 > 10 and real_num1 < 12 :
            d_i_demap[8 * i + 2] = 1
            d_i_demap[8 * i + 4] = 0
            d_i_demap[8 * i + 6] = 0
        elif real_num1 > 12 and real_num1 < 14 :
            d_i_demap[8 * i + 2] = 1
            d_i_demap[8 * i + 4] = 1
            d_i_demap[8 * i + 6] = 0
        else:
            d_i_demap[8 * i + 2] = 1
            d_i_demap[8 * i + 4] = 1
            d_i_demap[8 * i + 6] = 1
        if imag_num1 > 0 and imag_num1 < 2:
            d_i_demap[8 * i + 3] = 0
            d_i_demap[8 * i + 5] = 1
            d_i_demap[8 * i + 7] = 1
        elif imag_num1 > 2 and imag_num1 < 4:
            d_i_demap[8 * i + 3] = 0
            d_i_demap[8 * i + 5] = 1
            d_i_demap[8 * i + 7] = 0
        elif imag_num1 > 4 and imag_num1 < 6:
            d_i_demap[8 * i + 3] = 0
            d_i_demap[8 * i + 5] = 0
            d_i_demap[8 * i + 7] = 0
        elif imag_num1 > 6 and imag_num1 < 8:
            d_i_demap[8 * i + 3] = 0
            d_i_demap[8 * i + 5] = 0
            d_i_demap[8 * i + 7] = 1
        elif imag_num1 > 8 and imag_num1 < 10:
            d_i_demap[8 * i + 3] = 1
            d_i_demap[8 * i + 5] = 0
            d_i_demap[8 * i + 7] = 1
        elif imag_num1 > 10 and imag_num1 < 12:
            d_i_demap[8 * i + 3] = 1
            d_i_demap[8 * i + 5] = 0
            d_i_demap[8 * i + 7] = 0
        elif imag_num1 > 12 and imag_num1 < 14:
            d_i_demap[8 * i + 3] = 1
            d_i_demap[8 * i + 5] = 1
            d_i_demap[8 * i + 7] = 0
        else:
            d_i_demap[8 * i + 3] = 1
            d_i_demap[8 * i + 5] = 1
            d_i_demap[8 * i + 7] = 1
