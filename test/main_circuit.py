import random as Random

LABEL_NUM = 1
REMOVE_NUM = []
GATE_COUNT = 0
INPUT_G = 0
INPUT_X = 0
INPUT_P = 0
INPUT_N = 0
INPUT_C = 0
F = 0
CIRCUIT = []
CIRCUIT_DIC = {}

def Deal_Type(_num):#存有'0'、'1'的亂數Label，state只有在一開始使用者輸入的值才會是該值的Label，其餘state接預設為0的Label
    global LABEL_NUM
    _return = []
    for i in range(len(_num)):
        _dic = {}
        _dic['num'] = LABEL_NUM
        _dic['state'] = _num[i]
        _return.append(_dic)
        LABEL_NUM += 1
    return _return


def Type_Fill_Zero(_type, _long):#填滿_long長度的'0'
    _temp = ''.zfill(_long - len(_type))
    _temp = Deal_Type(_temp)
    _return = _temp + _type
    return _return


def Type_Lstrip(_type, _value, _long = 0):#_value : 要移除的值, _long : 要刪除的值的長度
    global REMOVE_NUM
    _count = 0
    if _long == 0:
        _stop = len(_type)
    else:
        _stop = _long

    for _item in range(_stop):
        _temp = '0' if _type[_item]['state'] == '0' else '1'
        if _temp != _value:
            break
        _count += 1
        REMOVE_NUM += [_type[_item]['num']]
    return _type[_count:]


def Type_Value(_type):#用state判斷value並計算正確答案
    _value = ''
    for _item in _type:
        _value += '0' if _item['state'] == '0' else '1'
    return int(_value, 2)


def Type_Singal_Op(_A, _B, _OP):
    global GATE_COUNT, CIRCUIT, CIRCUIT_DIC
    _temp = '0'
    if _OP == '&':
        _temp = str(int(_A['state']) & int(_B['state']))
    elif _OP == '|':
        _temp = str(int(_A['state']) | int(_B['state']))
    elif _OP == '^':
        _temp = str(int(_A['state']) ^ int(_B['state']))
    if (str(_A['num']) + ' ' + str(_B['num']) + ' ' + _OP) in CIRCUIT_DIC:
        _return = {}
        _return['num'] = CIRCUIT_DIC[str(_A['num']) + ' ' + str(_B['num']) + ' ' + _OP]
        _return['state'] = _temp
    else:
        GATE_COUNT += 1
        _return = Deal_Type(_temp)[0]
        CIRCUIT_DIC[str(_A['num']) + ' ' + str(_B['num']) + ' ' + _OP] = _return['num']
        CIRCUIT.append(str(_A['num']) + ' ' + str(_B['num']) + ' ' + _OP + ' ' + str(_return['num']))
    return _return


def Type_Add(A, B):#加法器
    #global REMOVE_NUM
    S = []
    c_singal_out = ''
    l = len(A) if (len(A) <= len(B)) else len(B)
    for i in range(- 1, - l - 1, -1):
        if i == -1:
            s_singal_out = Type_Singal_Op(A[i], B[i], '^')
            c_singal_out = Type_Singal_Op(A[i], B[i], '&')
        else:
            s_singal_out = Type_Singal_Op(Type_Singal_Op(A[i], B[i], '^'), c_singal_out, '^')
            c_singal_out = Type_Singal_Op(Type_Singal_Op(A[i], B[i], '&'), Type_Singal_Op(Type_Singal_Op(A[i], B[i], '^'), c_singal_out, '&'), '|')
        S = [s_singal_out] + S
    if c_singal_out['state'] == '0':
        #REMOVE_NUM += [c_singal_out['num'] - 2, c_singal_out['num'] - 1, c_singal_out['num']]
        if len(A) == len(B):
            return S
        return (B[:len(B) - len(A)] + S) if (len(A) < len(B)) else (A[:len(A) - len(B)] + S)
    else:
        if len(A) == len(B):
            return [c_singal_out] + S
        return (Type_Add(B[:len(B) - len(A)], [c_singal_out]) + S) if (len(A) < len(B)) else (Type_Add(A[:len(A) - len(B)], [c_singal_out]) + S)


def Type_Multiply(A, B):#乘法器
    T, S, s_temp = [], [], []
    for l_B in range(len(B) - 1, -1, -1):#先算出每一個bit乘出來的值
        t_total_out = []
        for l_A in range(len(A) - 1, -1, -1):
            t_singal_out = Type_Singal_Op(B[l_B], A[l_A], '&')
            t_total_out = [t_singal_out] + t_total_out
        T.append(t_total_out)

    if len(T[0]) == 1:
        for i in range(len(T)):
            S = T[i] + S
    else:
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
    for times in range(INPUT_X):#X次方
        if times > 0:
            F = Type_Multiply(INPUT_G, F)
        while len(F) > INPUT_N:
            F = Type_Add(Type_Multiply(F[:len(F) - INPUT_N], INPUT_C), F[len(F) - INPUT_N:])
            F = Type_Lstrip(F, '0')

    value_F = Type_Value(F)
    if value_F >= INPUT_P:
        F = Type_Add(F, INPUT_C)
        F = Type_Lstrip(F, '1', 1)
        value_F = Type_Value(F)

    fw_output = open('D:/output.txt', 'w')
    for item in F:
        fw_output.write(str(item['num']) + '\n')
    fw_output.close()

    value_G = Type_Value(INPUT_G)
    value_C = Type_Value(INPUT_C)
    print('(', value_G, '^', INPUT_X, ') % ( 2 ^', INPUT_N, '-', value_C, ')')
    #print('(', value_G ** INPUT_X, ') % (', (2 ** INPUT_N) - value_C, ')')
    print('正確答案 :', (value_G ** INPUT_X) % INPUT_P)
    print('我的答案 :', value_F)
    print('GATE數量 :', GATE_COUNT)


def Input_Information():
    global INPUT_G, INPUT_X, INPUT_P, INPUT_N, INPUT_C, F
    print("( g ^ x ) mod p")
    '''bases = input("Number bases of g x p, (1)BIN (2)DEC : ")
    while(bases != '1' and bases != '2'):
        bases = input("Enter 1 or 2, (1)BIN (2)DEC : ")'''

    fw_input = open('D:/input.txt', 'w')
    '''fw_input.write(bases + ' ')
    if bases == '1':
        INPUT_G = int(input("g = "), 2)
        INPUT_X = int(input("x = "), 2)
        INPUT_P = int(input("p = "), 2)
        fw_input.write(bin(INPUT_G)[2:] + ' ' + bin(INPUT_X)[2:] + ' ' + bin(INPUT_P)[2:])
    elif bases == '2':
        INPUT_G = int(input("g = "))
        INPUT_X = int(input("x = "))
        INPUT_P = int(input("p = "))
        fw_input.write(str(INPUT_G) + ' ' + str(INPUT_X) + ' ' + str(INPUT_P))'''
    y = 12
    INPUT_G = Random.randint(2 ** (y - 1), 2 ** y - 1)
    INPUT_X = Random.randint(2 ** (y - 1), 2 ** y - 1)
    INPUT_P = Random.randint(2 ** (y - 1), 2 ** y - 1)
    fw_input.write(str(INPUT_G) + ' ' + str(INPUT_X) + ' ' + str(INPUT_P))
    fw_input.close()

    F = Deal_Type(bin(INPUT_G)[2:])
    INPUT_G = Deal_Type(bin(INPUT_G)[2:])
    INPUT_N = len(bin(INPUT_P)[2:])#ex : INPUT_P = 2 ^ 255 - 19, INPUT_N = 255
    INPUT_C = Deal_Type(bin(2 ** INPUT_N - INPUT_P)[2:])#INPUT_P的2's Complement, ex : INPUT_P = 2 ^ 255 - 19, INPUT_C = 19


def main():
    Input_Information()
    Pseudocode()
    index_add = len(INPUT_G) * 2 + len(INPUT_C) + 1

    fw_circuit = open('D:/circuit.txt', 'w')
    for i in range(len(CIRCUIT)):
        if (i + index_add) not in REMOVE_NUM:
            fw_circuit.write(CIRCUIT[i] + '\n')
    fw_circuit.close()


if __name__ == '__main__':
    main()
