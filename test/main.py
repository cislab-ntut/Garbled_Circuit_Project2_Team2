import random
import enigma
from tabulate import tabulate

char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
def main():
    gatenumber = input("Gate case (1.AND 2.OR 3.NAND) :") # 選擇要用哪個gate
    # 產生F
    len_of_F = 10  # F的字串長度
    if gatenumber == '1':
        F = [] # 存output的list
        zero = ''.join(random.sample(char_list,len_of_F))  # 隨機產生字串
        for i in range(3):
            F.append(zero) # ANDgate前面3個是0
        one = ''.join(random.sample(char_list,len_of_F))
        F.append(one) # 最後一個是1
        # print(F)
    elif gatenumber == '2':
        F = []
        zero = ''.join(random.sample(char_list, len_of_F))
        F.append(zero) # ORgate第一個是0
        one = ''.join(random.sample(char_list, len_of_F))
        for i in range(3):
            F.append(one) # ORgate後面三個是0
        # print(F)
    elif gatenumber == '3':
        F = []
        one = ''.join(random.sample(char_list, len_of_F))
        for i in range(3):
            F.append(one) # NANDgate前面三個是1
        zero = ''.join(random.sample(char_list, len_of_F))
        F.append(zero) # NANDgate最後一個是0
        # print(F)

    A = [] # 存inputA
    B = [] # 存inputB

    # 產生input(A0,A1,B0,B1)
    for i in range(2):
        A.append(''.join(random.sample(char_list,3)))  # 隨機產生3個字元的字串
        B.append(''.join(random.sample(char_list,3)))  # 隨機產生3個字元的字串
    print('A0=', A[0],'  A1=', A[1])
    print('B0=', B[0],'  B1=', B[1])
    print('F0=', zero,'  F1=',one)
    truth_table = []
    c=0 # outputF的counter
    for i in range(2):
        for j in range(2):
            combine = []
            combine.append(A[i])
            combine.append(B[j]) 
            combine.append(F[c]) # 產生truth table的每一排
            truth_table.append(combine)
            c=c+1

    print('\n(Only User)')
    print(tabulate(truth_table, headers=['A','B','F'],tablefmt='orgtbl'))

    w = input("\nplease input AB (ex.00,01,10,11): ")
    w_num = [] # 存輸入的值
    w_num.append(int(w[0])) # inputA轉成int並存入
    w_num.append(int(w[1])) # inputB轉成int並存入
    print(F[w_num[0]*2+w_num[1]],'\n↓')
    enigma.main(A[w_num[0]],B[w_num[1]],F[w_num[0]*2+w_num[1]]) # 把A B F轉成的字串傳到enigma

if __name__ == '__main__':
    main()
