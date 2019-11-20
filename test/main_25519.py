import random as Random
import time
import xor_hash
import server_xor_hash


USED_LABEL = []
GATE_COUNT = 0
REPEAT_TIMES = 0
INPUT_TYPE = 0
INPUT_G = 0
INPUT_X = 0
INPUT_P = 0
INPUT_N = 0
INPUT_C = 0
F = 0


def Random_Label():#產出隨機字串以及避免重複
    global USED_LABEL, REPEAT_TIMES
    _temp = hex(Random.randint(0, 2**256 - 1))[2:]
    while (_temp in USED_LABEL):
        REPEAT_TIMES += 1
        _temp = hex(Random.randint(0, 2**256 - 1))[2:]
    USED_LABEL.append(_temp)
    return _temp


def Deal_Type(_num):#存有'0'、'1'的亂數Label，state只有在一開始使用者輸入的值才會是該值的Label，其餘state接預設為0的Label
    _return = []
    for i in range(len(_num)):
        _dic = {}
        _dic['0'] = Random_Label()
        _dic['1'] = Random_Label()
        _dic['state'] = _dic[_num[i]]
        _return.append(_dic)
    return _return


def Type_Fill_Zero(_type, _long):#填滿_long長度的'0'
    _temp = ''.zfill(_long - len(_type))
    _temp = Deal_Type(_temp)
    _return = _temp + _type
    return _return


def Type_Lstrip(_type, _value, _long = 0):#_value : 要移除的值, _long : 要刪除的值的長度
    _count = 0
    if _long == 0:
        _stop = len(_type)
    else:
        _stop = _long

    for _item in range(_stop):
        _temp = '0' if _type[_item]['state'] == _type[_item]['0'] else '1'
        if _temp != _value:
            break
        _count += 1
    return _type[_count:]


def Type_Value(_type):#用state判斷value並計算正確答案
    _value = ''
    for _item in _type:
        _value += '0' if _item['state'] == _item['0'] else '1'
    return int(_value, 2)


def Do_Enc_Dec(_A_State, _B_State, _truth_table):
    _encrypt_table = xor_hash.x_h(_truth_table)#加密truth table, 只傳回加密後的table
    Random.shuffle(_encrypt_table)#打亂table
    _label = server_xor_hash.s_x_h(_A_State, _B_State, _encrypt_table)#input label跟加密混淆後的table進行解密
    return _label


def Type_Singal_And(_A, _B):
    global GATE_COUNT
    GATE_COUNT += 1
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['0']],
        [_A['1'], _B['0'], _return['0']],
        [_A['1'], _B['1'], _return['1']]
    ]
    _return['state'] = Do_Enc_Dec(_A['state'], _B['state'], _truth_table)#state等於解出來的label
    return _return


def Type_Singal_Or(_A, _B):
    global GATE_COUNT
    GATE_COUNT += 1
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['1']],
        [_A['1'], _B['0'], _return['1']],
        [_A['1'], _B['1'], _return['1']]
    ]
    _return['state'] = Do_Enc_Dec(_A['state'], _B['state'], _truth_table)#state等於解出來的label
    return _return


def Type_Singal_Xor(_A, _B):
    global GATE_COUNT
    GATE_COUNT += 1
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['1']],
        [_A['1'], _B['0'], _return['1']],
        [_A['1'], _B['1'], _return['0']]
    ]
    _return['state'] = Do_Enc_Dec(_A['state'], _B['state'], _truth_table)#state等於解出來的label
    return _return


def Type_Add(A, B):#加法器
    l = len(A) + 1 if len(A) >= len(B) else len(B) + 1#方便進行加法，以及有進位，把2個input長度增加到較長的input長度+1
    A = Type_Fill_Zero(A, l)
    B = Type_Fill_Zero(B, l)

    S = []
    c_total_out = [Deal_Type('0')[0]]
    c_singal_out = Deal_Type('0')[0]
    for i in range(l - 1, -1, -1):
        s_singal_out = Type_Singal_Xor(Type_Singal_Xor(A[i], B[i]), c_singal_out)
        S = [s_singal_out] + S
        if i != 0:
            c_singal_out = Type_Singal_Or(Type_Singal_And(A[i], B[i]), Type_Singal_And(Type_Singal_Xor(A[i], B[i]), c_singal_out))
            c_total_out = [c_singal_out] + c_total_out
    return S


def Type_Multiply(A, B):#乘法器
    T = []
    for l_B in range(len(B) - 1, -1, -1):#先算出每一個bit乘出來的值
        t_total_out = []
        for l_A in range(len(A) - 1, -1, -1):
            t_singal_out = Type_Singal_And(B[l_B], A[l_A])
            t_total_out = [t_singal_out] + t_total_out
        T.append(t_total_out)

    S = []
    s_temp = []
    for i in range(len(T)):#再一排一排相加
        if i == 0:
            s_temp = T[i]
        else:
            s_temp = Type_Add(T[i], s_temp)
        S = s_temp[-1:] + S
        s_temp = s_temp[:-1]

    S = s_temp + S
    return S


def Pseudocode():
    global INPUT_G, INPUT_X, INPUT_P, INPUT_N, INPUT_C, F

    for times in range(INPUT_X - 1):#X次方
        F = Type_Multiply(INPUT_G, F)
        while len(F) > INPUT_N:
            F = Type_Add(Type_Multiply(F[:len(F) - INPUT_N], INPUT_C), F[len(F) - INPUT_N:])
            F = Type_Lstrip(F, '0')

    value_G = Type_Value(INPUT_G)
    value_C = Type_Value(INPUT_C)
    print('(', value_G, '^', INPUT_X, ') % ( 2 ^', INPUT_N, '-', value_C, ')')
    print('(', value_G ** INPUT_X, ') % (', (2 ** INPUT_N) - value_C, ')')
    print('正確答案 :', (value_G ** INPUT_X) % INPUT_P)

    value_F = Type_Value(F)
    if value_F >= INPUT_P:
        F = Type_Add(F, INPUT_C)
        F = Type_Lstrip(F, '1', 1)
        value_F = Type_Value(F)
    print('我的答案 :', value_F)
    print('Label使用量 :', len(USED_LABEL))
    print('Label重複次數 :', REPEAT_TIMES)
    print('GATE使用量 :', GATE_COUNT)


def Input_Information():
    global INPUT_G, INPUT_X, INPUT_P, INPUT_N, INPUT_C, F
    print("( g ^ x ) mod p")
    INPUT_TYPE = input("Number bases of g x p, (1)BIN (2)DEC : ")
    while(INPUT_TYPE != '1' and INPUT_TYPE != '2'):
        INPUT_TYPE = input("Enter 1 or 2, (1)BIN (2)DEC : ")
    if INPUT_TYPE == '1':
        INPUT_G = int(input("g = "), 2)
        INPUT_X = int(input("x = "), 2)
        INPUT_P = int(input("p = "), 2)
    elif INPUT_TYPE == '2':
        INPUT_G = int(input("g = "))
        INPUT_X = int(input("x = "))
        INPUT_P = int(input("p = "))

    F = Deal_Type(bin(INPUT_G)[2:])
    INPUT_G = Deal_Type(bin(INPUT_G)[2:])
    INPUT_N = len(bin(INPUT_P)[2:])#ex : INPUT_P = 2 ^ 255 - 19, INPUT_N = 255
    INPUT_C = Deal_Type(bin(2 ** INPUT_N - INPUT_P)[2:])#INPUT_P的2's Complement, ex : INPUT_P = 2 ^ 255 - 19, INPUT_C = 19


def main():
    Input_Information()
    Pseudocode()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print(end_time - start_time, 'seconds')

