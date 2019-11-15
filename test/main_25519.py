import random as Random
import xor_hash
import server_xor_hash


USED_LABEL = []
INPUT_TYPE = 0
INPUT_G = 0
INPUT_X = 0
INPUT_K = 0
INPUT_P = 0
F = 0


def Random_Label():
    global USED_LABEL
    _temp = hex(Random.randint(0, 2**256 - 1))[2:]
    while (_temp in USED_LABEL):
        _temp = hex(Random.randint(0, 2**256 - 1))[2:]
    USED_LABEL.append(_temp)
    return _temp


def Deal_Type(_num):
    _return = []
    _temp = _num
    for i in range(len(_temp)):
        _dic = {}
        _dic['value'] = _temp[i]
        _dic['0'] = Random_Label()
        _dic['1'] = Random_Label()
        _dic['state'] = _dic[_dic['value']]
        _return.append(_dic)
    return _return


def Type_Fill_Zero(_type, _long):
    _return = []
    _temp = ''.zfill(_long - len(_type))
    _temp = Deal_Type(_temp)
    _return = _temp + _type
    return _return


def Type_Lstrip(_type, _value):
    _count = 0
    for _item in _type:
        _temp = '0' if _item['state'] == _item['0'] else '1'
        if _temp != _value:
            break
        _count += 1

    return _type[_count:]


def Type_Value(_type):
    _value = ''
    for _item in _type:
        _value += '0' if _item['state'] == _item['0'] else '1'

    return int(_value, 2)


def Input_Information():
    global INPUT_G, INPUT_X, INPUT_K, INPUT_P, F
    print("( g ^ x ) mod ( 2 ^ 255 - 19 )")
    INPUT_TYPE = input("Number bases of g and x, (1)BIN (2)DEC : ")
    while(INPUT_TYPE != '1' and INPUT_TYPE != '2'):
        INPUT_TYPE = input("Enter 1 or 2, (1)BIN (2)DEC : ")
    if INPUT_TYPE == '1':
        INPUT_G = int(input("g = "), 2)
        INPUT_X = int(input("x = "), 2)
    elif INPUT_TYPE == '2':
        INPUT_G = int(input("g = "))
        INPUT_X = int(input("x = "))

    F = Deal_Type(bin(INPUT_G)[2:])
    INPUT_G = Deal_Type(bin(INPUT_G)[2:])
    INPUT_K = len(INPUT_G)
    INPUT_P = Deal_Type(bin(19)[2:])


def Type_Singal_And(_A, _B):
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['0']],
        [_A['1'], _B['0'], _return['0']],
        [_A['1'], _B['1'], _return['1']]
    ]
    _encrypt_table = xor_hash.x_h(_truth_table)#加密truth table, 只傳回加密後的table
    Random.shuffle(_encrypt_table)#打亂table
    _label = server_xor_hash.s_x_h(_A['state'], _B['state'], _encrypt_table)#input label跟加密後的table進行解密
    _return['state'] = _label#state等於解出來的label
    return _return


def Type_Singal_Or(_A, _B):
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['1']],
        [_A['1'], _B['0'], _return['1']],
        [_A['1'], _B['1'], _return['1']]
    ]
    _encrypt_table = xor_hash.x_h(_truth_table)#加密truth table, 只傳回加密後的table
    Random.shuffle(_encrypt_table)#打亂table
    _label = server_xor_hash.s_x_h(_A['state'], _B['state'], _encrypt_table)#input label跟加密後的table進行解密
    _return['state'] = _label#state等於解出來的label
    return _return


def Type_Singal_Xor(_A, _B):
    _return = Deal_Type('0')[0]
    _truth_table = [
        [_A['0'], _B['0'], _return['0']],
        [_A['0'], _B['1'], _return['1']],
        [_A['1'], _B['0'], _return['1']],
        [_A['1'], _B['1'], _return['0']]
    ]
    _encrypt_table = xor_hash.x_h(_truth_table)#加密truth table, 只傳回加密後的table
    Random.shuffle(_encrypt_table)#打亂table
    _label = server_xor_hash.s_x_h(_A['state'], _B['state'], _encrypt_table)#input label跟加密後的table進行解密
    _return['state'] = _label#state等於解出來的label
    return _return


def Type_Multiply(A, B):# * = and
    T = []
    for l_B in range(len(B) - 1, -1, -1):
        t_total_out = []
        for l_A in range(len(A) - 1, -1, -1):
            t_singal_out = Type_Singal_And(B[l_B], A[l_A])
            t_total_out = [t_singal_out] + t_total_out
        T.append(t_total_out)

    S = []
    s_temp = []
    for i in range(len(T)):
        if i == 0:
            s_temp = T[i]
        else:
            s_temp = Type_Add(T[i], s_temp)
        S = s_temp[-1:] + S
        s_temp = s_temp[:-1]

    S = s_temp + S
    return S


def Type_Add(A, B):# ^ = xor, + = or, * = and
    l = len(A) + 1 if len(A) >= len(B) else len(B) + 1
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


def Pseudocode():
    global INPUT_G, INPUT_X, INPUT_K, INPUT_P, F

    for times in range(INPUT_X - 1):#X次方
        F = Type_Multiply(INPUT_G, F)
        while len(F) > INPUT_K:
            F = Type_Add(Type_Multiply(F[:len(F) - len(INPUT_G)], INPUT_P), F[len(F) - len(INPUT_G):])
            F = Type_Lstrip(F, '0')

    INPUT_G = Type_Value(INPUT_G)
    INPUT_P = Type_Value(INPUT_P)
    print('(', INPUT_G, '^', INPUT_X, ') % ( 2 ^', INPUT_K, '-', INPUT_P, ')')
    print('(', INPUT_G ** INPUT_X, ') % (', (2 ** INPUT_K) - INPUT_P, ')')
    print('正確答案 :', (INPUT_G ** INPUT_X) % ((2 ** INPUT_K) - INPUT_P))
    F = Type_Value(F)
    print('我的答案 :', F)


def main():
    Input_Information()
    Pseudocode()


if __name__ == '__main__':
    main()
    
    
