INPUT_TYPE = ''
INPUT_G = ''
INPUT_X = ''
K = 255
P = bin(19)[2:]

def Input_information():
    global INPUT_G, INPUT_X
    print("g ^ x mod (2 ^ 255 - 19)")
    INPUT_TYPE = input("Number bases of g and x, (1).BIN (2).DEC : ")
    if INPUT_TYPE == '1':
        INPUT_G = input("g = ")
        INPUT_X = int(input("x = "), 2)
    elif INPUT_TYPE == '2':
        INPUT_G = bin(int(input("g = ")))[2:]
        INPUT_X = int(input("x = "))


def BIN_Multiply(A, B):# * = and
    A = A.lstrip('0')
    B = B.lstrip('0')
    T = []
    for l_B in range(len(B) - 1, -1, -1):
        t_total_out = ''
        for l_A in range(len(A) - 1, -1, -1):
            t_singal_out = B[l_B] * A[l_A]#電路
            t_total_out = str(t_singal_out) + t_total_out
        T.append(t_total_out)

    S = ''
    s_temp = ''
    for i in range(len(T)):
        if i == 0:
            s_temp = T[i]
        else:
            s_temp = BIN_Add(T[i], s_temp)
        S = s_temp[-1:] + S
        s_temp = s_temp[:-1]

    S = s_temp + S
    S = S.lstrip('0')
    return S


def BIN_Add(A, B):# ^ = xor, + = or, * = and
    l = len(A) + 1 if len(A) >= len(B) else len(B) + 1
    A = A.zfill(l)
    B = B.zfill(l)
    S = ''
    s_out = ''
    carry = '0'
    for i in range(l - 1, -1, -1):
        s_out = A[i] ^ B[i] ^ carry#電路
        carry = (A[i] * B[i]) + ((A[i] ^ B[i]) * carry)#電路
        S = s_out + S
    return S


def Pseudocode():
    global INPUT_G, INPUT_X
    INPUT_G = INPUT_G.lstrip('0')
    F = INPUT_G
    print(len(INPUT_G))
    for times in range(INPUT_X - 1):#X次方
        F = BIN_Multiply(INPUT_G, F)
        while len(F) > len(INPUT_G):
            F = BIN_Add(BIN_Multiply(F[:len(F) - len(INPUT_G)], P), F[len(F) - len(INPUT_G):])
            F = F.lstrip('0')
    print(F)


def main():
    Input_information()
    Pseudocode()


if __name__ == '__main__':
    main()

