import server_xor_hash

LABEL_DIC = {}

def Label_Check(_str):
    global LABEL_DIC
    if _str in LABEL_DIC:
        return LABEL_DIC[_str]
    else:
        print('damn', _str)

def main():
    global LABEL_DIC
    fr_garbled_input = open('D:/garbled_input.txt', 'r')
    line = fr_garbled_input.readline()
    while line:
        line = line[:-1]
        temp = line.split(', ')
        LABEL_DIC[temp[0]] = temp[1]
        line = fr_garbled_input.readline()
    fr_garbled_input.close()

    output_dic = {}
    fr_garbled_output = open('D:/garbled_output.txt', 'r')
    line = fr_garbled_output.readline()
    while line:
        line = line[:-1]
        temp = line.split(', ')
        output_dic[temp[0]] = temp[1]
        line = fr_garbled_output.readline()
    fr_garbled_output.close()

    fr_garbled_circuit = open('D:/garbled_circuit.txt', 'r')
    line = fr_garbled_circuit.readline()
    while line:
        line = line[:-1]
        temp = line.split(', ')
        enc_truth_table = [temp[0], temp[1], temp[2], temp[3]]
        answer_label = server_xor_hash.s_x_h(Label_Check(temp[-3]), Label_Check(temp[-2]), enc_truth_table)
        LABEL_DIC[temp[-1]] = answer_label
        line = fr_garbled_circuit.readline()
    fr_garbled_circuit.close()

    fw_answer = open('D:/answer.txt', 'w')
    for item in output_dic:
        value = '0' if LABEL_DIC[item] == (output_dic[item]).split(' ')[0] else '1'
        fw_answer.write(item + ', ' + LABEL_DIC[item] + ', ' + value + '\n')
    fw_answer.close()

    print('finish')

if __name__ == '__main__':
    main()
