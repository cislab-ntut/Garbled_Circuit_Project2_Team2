import random
import enigma
import server_enigma
import server
import postfix
from tabulate import tabulate
import xor_hash
import server_xor_hash

char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
exist = []  # 存已經用過的隨機字串
exist2 = []  # 存重複的char
toserver = []


def create_randomstring():  # 產生不會重複的字串
    temp = ''.join(str(hex(random.randint(0, 2**128-1))))
    while (1):
        if temp in exist:
            temp = ''.join(str(hex(random.randint(0, 2**128-1))))
        elif temp not in exist:
            exist.append(temp)
            # print(temp)
            break
    return temp


def input_counting(count, input_l, inputstring):
    for i in range(input_l):  # 數input要幾個
        if inputstring[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and (inputstring[i] not in exist2):
            count = count + 1
        if inputstring[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            exist2.append(inputstring[i])
    return count


def INPUT(count):
    while (1):  # 輸入input
        inputvalue = input("input(EX.10110): ")
        if len(inputvalue) != count:
            print("wrong length!")
            continue
        break
    return inputvalue

Dict = dict()
def dict_construct(count):
    A = []
    for a in range(count):
        for b in range(2):
            A = []
            A.append(create_randomstring())  # 隨機產生3個字元的字串
            A.append(create_randomstring())  # 隨機產生3個字元的字串
            if (char_list[a] in Dict):
                A = (Dict[char_list[a]]).copy()
            Dict.update({char_list[a]: A})
    print("dic", Dict)


def LtoB(input_l,inputstring,inputvalue):
    c = 0
    for i in range(input_l):  # 將ABC...Z替換成01
        if inputstring[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            inputstring = inputstring.replace(inputstring[i], inputvalue[c])
            c = c + 1
    postfix_r = postfix.infix_to_postfix(inputstring)  # 中序式轉後序式
    print("pos: ", postfix_r)
    return postfix_r

def Create_Truth_Table(postfix_r,i,string_stack,op_check):
    A = []  # 存inputA
    B = []  # 存inputB
    # 產生input(A0,A1,B0,B1)
    # 判斷postfix[i]的前一個是否為運算子，是的話即為下一層
    if postfix_r[i - 1] not in "*+-":
        for i in range(2):
            A.append(create_randomstring())  # 隨機產生字串
            B.append(create_randomstring())  # 隨機產生字串
    elif postfix_r[i - 1] in "*+-":  # 是運算子的話表示到了下一層，需要上一層的output當作此層的input
        B.append(string_stack.pop())
        B.append(string_stack.pop())
        A.append(string_stack.pop())
        A.append(string_stack.pop())

    F = []  # 存output
    zero = create_randomstring()
    one = create_randomstring()  # 隨機產生字串
    gatename = ["AND gate", "OR gate", "NAND gate"]
    if op_check == "*":
        for i in range(3):
            F.append(zero)  # 前面3個是0
        F.append(one)  # 最後一個是1
        gatename_index = 0
    elif op_check == "+":
        F.append(zero)  # 第一個是0
        for i in range(3):
            F.append(one)  # 最後3個是1
        gatename_index = 1
    elif op_check == "-":
        for i in range(3):
            F.append(one)  # 前面3個是1
        F.append(zero)  # 最後一個是0
        gatename_index = 2

    string_stack.append(one)
    string_stack.append(zero)

    truth_table = []
    c = 0  # outputF的counter
    combine = []
    for i in range(2):
        for j in range(2):
            combine.append(A[i])
            combine.append(B[j])
            combine.append(F[c])  # 產生truth table的每一排
            truth_table.append(combine)
            combine = []
            c = c + 1
    # print(truth_table)
    random.shuffle(truth_table)
    # print(truth_table)
    return truth_table, combine,A,B,gatename_index,gatename


def main():
    inputstring = "((A*B)-((C+D)*(D-E)))"  # ppt範例
    print("circuit:", inputstring)
    #print("postcircuit:",postfix.infix_to_postfix(inputstring))
    postcircuit = postfix.infix_to_postfix(inputstring)
    Count = 0
    Count = input_counting(Count, len(inputstring), inputstring)
    dict_construct(Count)
    postfix_r = LtoB(len(inputstring), inputstring, inputvalue=INPUT(Count))

    l = len(postfix_r)  # 後序式長度
    stack = []  # 計算用(只會存0,1)
    string_stack = []  # 放隨機字串用
    for i in range(l):  # 從後序式第一個字元開始讀到最後一個
        if postfix_r[i] in "01":  # 為0或1的話就放到stack
            stack.append(postfix_r[i])
        elif postfix_r[i] == "*" or postfix_r[i] == "+" or postfix_r[i] == "-":
            op_check = postfix_r[i]
            if len(stack) >= 2:
                temp2 = int(stack.pop())
                temp1 = int(stack.pop())  # 遇到運算子就將stack最上面2個拿出來運算
            if op_check == "*":  # 運算結果
                temp3 = temp1 * temp2
            elif op_check == "+":
                temp3 = temp1 + temp2
                if temp3 == 2:
                    temp3 = 1
            elif op_check == "-":
                if temp1 == 0 or temp2 == 0:
                    temp3 = 1
                elif temp1 == 1 and temp2 == 1:
                    temp3 = 0
            stack.append(str(temp3))

            truth_table,combine ,A,B,gatename_index,gatename = Create_Truth_Table(postfix_r,i,string_stack,op_check)

            print(gatename[gatename_index])
            print(tabulate(truth_table, headers=['A', 'B', 'F'], tablefmt='orgtbl'))
            print(server_xor_hash.s_x_h(A[temp1], B[temp2], xor_hash.x_h(truth_table)))
            # combine.append(A[temp1])
            # combine.append(B[temp2])
            # combine.append(xor_hash.x_h(truth_table))
            # toserver.append(combine)
    #server_xor_hash.s_x_h(toserver)
    print("answer: ",temp3)


if __name__ == '__main__':
    main()
