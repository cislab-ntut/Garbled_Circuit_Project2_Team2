import server_enigma

def order_to_letter(order):
    return chr(order%26+65)

def letter_to_ord (alphabet):
    return ord(alphabet)-65

def pos_count (start,letter):
    return (26 - letter_to_ord(start) + letter_to_ord(letter))%26

def pointer_count(start,pointer):
    if (ord(pointer)>ord(start)):
        return ord(pointer)-ord(start)
    elif (ord(pointer)<ord(start)):
        return 26-(ord(start)-ord(pointer))
    return 25
def plugboard(list):
    i = 65
    j = i+1
    for i in range(90):
        for j in range(90):
            c1 = chr(i)
            c2 = chr(j)
            list[list.index(c1)] = c2
            list[list.index(c2)] = c1
def main(start1,start2, Input):
    start = []
    start.append(start1)
    start.append(start2)
    INPUT = Input  # 輸入第一個密碼
    for s_pointer in range(2):
        order_list  = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        plugboard_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        R_rotor_list = ['B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q','O']
        D_rotor_list = ['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E']
        L_rotor_list = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
        reflector_list = ['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T']
        s1 = start[s_pointer][0]
        s2 = start[s_pointer][1]
        s3 = start[s_pointer][2]
        r1 = 'W'
        r2 = 'F'
        r3 = 'R'
        r1_count = pointer_count(s1, r1)
        r2_count = pointer_count(s2, r2)
        r3_count = pointer_count(s3, r3)
        # print(pointer_count(s1, r1))
        # print(pointer_count(s2, r2))
        # print(pointer_count(s3, r3))


        i = 0
        output=[]
        output=[]
        for i in range(len(INPUT)):

            r1_count -= 1
            if ((ord(s1) + 1) > 90):
                s1 = chr(65)
            else:
                s1 = chr(ord(s1) + 1)  # input後輪盤1轉動
            if (r2_count == 1):
                r2_count -= 1
                if (r2_count == 0):
                    r2_count = 26
                    r3_count -= 1
                    if ((ord(s3) + 1) > 90):
                        s3 = chr(65)
                    else:
                        s3 = chr(ord(s3) + 1)  # 轉盤2一圈後輪盤3轉動
                if ((ord(s2) + 1) > 90):
                    s2 = chr(65)
                else:
                    s2 = chr(ord(s2) + 1)  # 轉盤1一圈後輪盤2轉動
            if (r1_count == 0):
                r1_count = 26
                r2_count -= 1
                if (r2_count == 0):
                    r2_count = 26
                    r3_count -= 1
                    if ((ord(s3) + 1) > 90):
                        s3 = chr(65)
                    else:
                        s3 = chr(ord(s3) + 1)  # 轉盤2一圈後輪盤3轉動
                if (ord(s2) + 1) > 90:
                    s2 = chr(65)
                else:
                    s2 = chr(ord(s2) + 1)  # 轉盤1一圈後輪盤2轉動


            step1 = (order_to_letter(letter_to_ord(s1)+letter_to_ord(INPUT[i])))  # 從s1開始數input的位置
            # print(step1)  # 轉盤1外圈

            step2 = R_rotor_list[letter_to_ord(step1)]
            # print(step2)  # 轉盤1內圈

            a = pos_count(s1, step2)
            step3 = order_to_letter(letter_to_ord(s2) + a)
            # print(step3)  # 轉盤2外圈

            step4 = D_rotor_list[letter_to_ord(step3)]
            # print(step4)  # 轉盤2內圈

            b = pos_count(s2, step4)
            step5 = order_to_letter(letter_to_ord(s3) + b)
            # print(step5)  # 轉盤3外圈

            step6 = L_rotor_list[letter_to_ord(step5)]
            # print(step6)  # 轉盤3內圈



            c = pos_count(s3, step6)
            step7 = order_to_letter(letter_to_ord('A') + c)
            # print(step7)  # 反射器input
            step7 = reflector_list[letter_to_ord(step7)]
            # print(step7)  # 反射器output



            d = pos_count('A',step7)
            step8 = order_to_letter(letter_to_ord(s3) + d)
            # print(step8)  # 轉盤3內圈

            step9 = order_list[L_rotor_list.index(step8)]
            # print(step9)  # 轉盤3外圈

            e = pos_count(s3, step9)
            step10 = order_to_letter(letter_to_ord(s2) + e)
            # print(step10)  # 轉盤2內圈

            step11 = order_list[D_rotor_list.index(step10)]
            # print(step11)  # 轉盤2外圈

            f = pos_count(s2, step11)
            step12 = order_to_letter(letter_to_ord(s1) + f)
            # print(step12)  # 轉盤1內圈

            step13 = order_list[R_rotor_list.index(step12)]
            # print(step13)  # 轉盤1外圈

            g = pos_count(s1, step13)
            #print(order_list[g] , end='')
            output.append(order_list[g])
        print(*output,sep='')
        print('↓')
        INPUT = output
    print('(server)','\n↓',)
    server_enigma.main(start2,start1,output)




