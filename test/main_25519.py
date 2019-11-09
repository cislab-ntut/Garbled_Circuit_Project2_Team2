import random as Random

USED_LABEL = []
INPUT_TYPE = 0
INPUT_G = 0
INPUT_X = 0
INPUT_K = 0
INPUT_P = 0


def Random_Label():
    global USED_LABEL
    temp = str(hex(Random.randint(0, 2**20 - 1))[2:])
    while (temp in USED_LABEL):
        temp = str(hex(Random.randint(0, 2**20 - 1))[2:])
    USED_LABEL.append(temp)
    return temp


def Deal_Type(_num):
    _return = []
    _temp = _num
    for i in range(len(_temp)):
        _dic = {}
        _dic['value'] = _temp[i]
        _dic['0'] = Random_Label()
        _dic['1'] = Random_Label()
        _return.append(_dic)
    return _return


def Type_Fill_Zero(_type, _long):
    _return = []
    _temp = ''.zfill(_long - len(_type))
    _temp = Deal_Type(_temp)
    _return = _temp + _type
    return _return


def Type_Lstrip(_type, _value):
    count = 0
    for i in range(len(_type)):
        if _type[i]['value'] != _value:
            break
        count += 1
    return _type[count:]


def Type_Value(_type):
    _value = ''
    for _item in _type:
        _value += _item['value']
    return int(_value, 2)


def Input_Information():
    global INPUT_G, INPUT_X, INPUT_K, INPUT_P
    print("g ^ x mod (2 ^ 255 - 19)")
    INPUT_TYPE = input("Number bases of g and x, (1).BIN (2).DEC : ")
    while(INPUT_TYPE != '1' and INPUT_TYPE != '2'):
        INPUT_TYPE = input("Enter 1 or 2, (1).BIN (2).DEC : ")
    if INPUT_TYPE == '1':
        INPUT_G = int(input("g = "), 2)
        INPUT_X = int(input("x = "), 2)
    elif INPUT_TYPE == '2':
        INPUT_G = int(input("g = "))
        INPUT_X = int(input("x = "))
    
    INPUT_G = Deal_Type(bin(INPUT_G)[2:])
    INPUT_K = len(INPUT_G)
    INPUT_P = Deal_Type(bin(19)[2:])


def BIN_Multiply(A, B):# * = and
    A = Type_Lstrip(A, '0')
    B = Type_Lstrip(B, '0')
    T = []
    for l_B in range(len(B) - 1, -1, -1):
        t_total_out = ''
        for l_A in range(len(A) - 1, -1, -1):
            t_singal_out = str(int(B[l_B]['value']) * int(A[l_A]['value']))#電路
            t_total_out = t_singal_out + t_total_out
        T.append(Deal_Type(t_total_out))

    S = []
    s_temp = []
    for i in range(len(T)):
        if i == 0:
            s_temp = T[i]
        else:
            s_temp = BIN_Add(T[i], s_temp)
        S = s_temp[-1:] + S
        s_temp = s_temp[:-1]

    S = s_temp + S
    S = Type_Lstrip(S, '0')
    return S


def BIN_Add(A, B):# ^ = xor, + = or, * = and
    l = len(A) + 1 if len(A) >= len(B) else len(B) + 1
    A = Type_Fill_Zero(A, l)
    B = Type_Fill_Zero(B, l)
    
    s_total_out = ''
    c_total_out = '0'
    c_singal_out = '0'
    for i in range(l - 1, -1, -1):
        s_singal_out = str(int(A[i]['value']) ^ int(B[i]['value']) ^ int(c_singal_out))#電路
        s_total_out = s_singal_out + s_total_out
        if i != 0:
            c_singal_out = str((int(A[i]['value']) * int(B[i]['value'])) + ((int(A[i]['value']) ^ int(B[i]['value'])) * int(c_singal_out)))#電路
            c_total_out = c_singal_out + c_total_out
    S = Deal_Type(s_total_out)
    C = Deal_Type(c_total_out)
    return S


def Pseudocode():
    global INPUT_G, INPUT_X, INPUT_K, INPUT_P
    F = INPUT_G
    for times in range(INPUT_X - 1):#X次方
        F = BIN_Multiply(INPUT_G, F)
        while len(F) > INPUT_K:
            F = BIN_Add(BIN_Multiply(F[:len(F) - len(INPUT_G)], INPUT_P), F[len(F) - len(INPUT_G):])
            F = Type_Lstrip(F, '0')
    
    INPUT_G = Type_Value(INPUT_G)
    INPUT_P = Type_Value(INPUT_P)
    print((INPUT_G ** INPUT_X) % ((2 ** INPUT_K) - INPUT_P))
    F = Type_Value(F)
    print(F)


def main():
    Input_Information()
    Pseudocode()


if __name__ == '__main__':
    main()

