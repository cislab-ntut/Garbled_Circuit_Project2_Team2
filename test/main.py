import random
import enigma
import postfix
from tabulate import tabulate

char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W', 'X', 'Y', 'Z']
def main():
    '''
    gatenumber = input("Gate case (1.AND 2.OR 3.NAND) :") # 選擇要用哪個gate
    '''
    inputstring = input("input(ex.(1*0)): ")
    # inputstring = "(1+0)"
    postfix_r = postfix.infix_to_postfix(inputstring)
    print("pos: ",postfix_r)
    len_of_F = 3  # F的字串長度
    l = len(postfix_r)  # 後序式長度
    w = []  # 存運算元
    for i in range(l):
        if postfix_r[i] in "01":
            w.append(postfix_r[i])
        if postfix_r[i] == '*':
            F = []
            zero = ''.join(random.sample(char_list,len_of_F))  # 隨機產生字串
            for i in range(3):
                F.append(zero)
            one = ''.join(random.sample(char_list,len_of_F))
            F.append(one)
            # print(F)
            gatename = "AND"
        elif postfix_r[i] == '+':
            F = []
            zero = ''.join(random.sample(char_list, len_of_F))
            F.append(zero)
            one = ''.join(random.sample(char_list, len_of_F))
            for i in range(3):
                F.append(one)
            # print(F)
            gatename = "OR"
        '''
        elif postfix_r[i] == '3':
            F = []
            one = ''.join(random.sample(char_list, len_of_F))
            for i in range(3):
                F.append(one)
            zero = ''.join(random.sample(char_list, len_of_F))
            F.append(zero)
            # print(F)
        '''


    A = []
    B = []
    # 產生input(A0,A1,B0,B1)
    for i in range(2):
        A.append(''.join(random.sample(char_list,3)))  # 隨機產生3個字元的字串
        B.append(''.join(random.sample(char_list,3)))  # 隨機產生3個字元的字串
    print('A0=', A[0],'  A1=', A[1])
    print('B0=', B[0],'  B1=', B[1])
    print('F0=', zero,'  F1=',one)
    truth_table = []
    c=0
    for i in range(2):
        for j in range(2):
            combine = []
            combine.append(A[i])
            combine.append(B[j])
            combine.append(F[c])
            truth_table.append(combine)
            c=c+1

    print('\n(Only User)')
    print(gatename,"gate: ")
    print(tabulate(truth_table, headers=['A','B','F'],tablefmt='orgtbl'))

    '''
    w = input("\nplease input AB (ex.00,01,10,11): ")
    '''
    w_num = []
    w_num.append(int(w[0]))
    w_num.append(int(w[1]))
    print(F[w_num[0]*2+w_num[1]],'\n↓')
    enigma.main(A[w_num[0]],B[w_num[1]],F[w_num[0]*2+w_num[1]])

if __name__ == '__main__':
    main()