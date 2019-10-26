import random
import enigma
import postfix
from tabulate import tabulate

char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
exist = [] # 存已經用過的隨機字串
exist2 = [] # 存重複的char
def create_randomstring():  # 用來判斷隨機產生的字串有沒有重複
    temp = ''.join(random.sample(char_list, 3))
    while (1):
        if temp in exist:
            temp = ''.join(random.sample(char_list, 3))
        elif temp not in exist:
            exist.append(temp)
            break
    return temp

def main():
    # inputstring = input("input(ex.(1*0)): ")
    inputstring = "((A*B)-((C+D)*(D-E)))"  # ppt範例
    print("circuit:",inputstring)
    input_l = len(inputstring)
    count = 0
    for i in range(input_l):  # 數input要幾個
        if inputstring[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and (inputstring[i] not in exist2):
            count = count + 1
            exist2.append(inputstring[i])
    while (1):  # 輸入input
        inputvalue = input("input(EX.10110): ")
        if len(inputvalue) != count:
            print("wrong length!")
            continue
        break
    c = 0
    for i in range(input_l):  # 將ABC...Z替換成01
        if inputstring[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            inputstring = inputstring.replace(inputstring[i],inputvalue[c])
            c = c+1
    postfix_r = postfix.infix_to_postfix(inputstring)  # 中序式轉後序式
    print("pos: ",postfix_r)
    l = len(postfix_r)  # 後序式長度
    stack = []  # 計算用(只會存0,1)
    string_stack = []  # 放隨機字串用
    for i in range(l):  # 從後序式第一個字元開始讀到最後一個
        if postfix_r[i] in "01":  # 為0或1的話就放到stack
            stack.append(postfix_r[i])
        elif postfix_r[i] == "*" or postfix_r[i] == "+":
            op_check = postfix_r[i]
            if len(stack) >= 2:
                temp2 = int(stack.pop())
                temp1 = int(stack.pop())  # 遇到運算子就將stack最上面2個拿出來運算
            if op_check == "*": # 運算結果
                temp3 = temp1 * temp2
            elif op_check == "+":
                temp3 = temp1 + temp2
                if temp3 == 2:
                    temp3 = 1
            stack.append(str(temp3))

            A = []  # 存inputA
            B = []  # 存inputB

            # 產生input(A0,A1,B0,B1)
            # 判斷string_stack長度是不是>=4，如果是的話表示目前gate在第二層(含以上)
            if len(string_stack) < 4:
                for i in range(2):
                    A.append(create_randomstring())  # 隨機產生3個字元的字串
                    B.append(create_randomstring())  # 隨機產生3個字元的字串
            elif len(string_stack) >= 4:
                B.append(string_stack.pop())
                B.append(string_stack.pop())
                A.append(string_stack.pop())
                A.append(string_stack.pop())

            F = []  # 存output
            zero = create_randomstring()
            one = create_randomstring()  # 隨機產生字串
            gatename = ["AND gate","OR gate"]
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

            string_stack.append(one)
            string_stack.append(zero)

            truth_table = []
            c = 0  # outputF的counter
            for i in range(2):
                for j in range(2):
                    combine = []
                    combine.append(A[i])
                    combine.append(B[j])
                    combine.append(F[c])  # 產生truth table的每一排
                    truth_table.append(combine)
                    c = c + 1
            print(gatename[gatename_index])
            print(tabulate(truth_table, headers=['A', 'B', 'F'], tablefmt='orgtbl'))
            #print(string_stack)
            #print(exist)

if __name__ == '__main__':
    main()