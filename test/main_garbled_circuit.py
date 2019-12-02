import random as Random
import xor_hash

LABEL_DIC = {}

def Random_Label():
    _temp = hex(Random.randint(0, 2**256 - 1))[2:]
    return _temp


def Check_Exist(_str):
    global LABEL_DIC
    if _str not in LABEL_DIC:
        _str_0, _str_1 = Random_Label(), Random_Label()
        LABEL_DIC[_str] = _str_0 + ' ' + _str_1
    else:
        temp = LABEL_DIC[_str].split(' ')
        _str_0, _str_1 = temp[0], temp[1]
    return _str_0, _str_1


def Gen_Truth_Table(_In1, _In2, _OP, _Out):
    _In1_0, _In1_1 = Check_Exist(_In1)
    _In2_0, _In2_1 = Check_Exist(_In2)
    _Out_0, _Out_1 = Check_Exist(_Out)

    _truth_table = []
    if _OP == '&':
        _truth_table = [
        _In1_0 + ' ' + _In2_0 + ' ' + _Out_0,
        _In1_0 + ' ' + _In2_1 + ' ' + _Out_0,
        _In1_1 + ' ' + _In2_0 + ' ' + _Out_0,
        _In1_1 + ' ' + _In2_1 + ' ' + _Out_1]
    elif _OP == '|':
        _truth_table = [
        _In1_0 + ' ' + _In2_0 + ' ' + _Out_0,
        _In1_0 + ' ' + _In2_1 + ' ' + _Out_1,
        _In1_1 + ' ' + _In2_0 + ' ' + _Out_1,
        _In1_1 + ' ' + _In2_1 + ' ' + _Out_1]
    elif _OP == '^':
        _truth_table = [
        _In1_0 + ' ' + _In2_0 + ' ' + _Out_0,
        _In1_0 + ' ' + _In2_1 + ' ' + _Out_1,
        _In1_1 + ' ' + _In2_0 + ' ' + _Out_1,
        _In1_1 + ' ' + _In2_1 + ' ' + _Out_0]
    return _truth_table


def main():
    input_value_dic = {}
    fr_input = open('D:/input.txt', 'r')
    input_temp = fr_input.readline().split(' ')
    fr_input.close()
    if input_temp[0] == '2':
        input_temp[1] = bin(int(input_temp[1]))[2:]
        input_temp[3] = bin(int(input_temp[3]))[2:]
    for i in range(len(input_temp[1])):
        input_value_dic[str(i + 1)] = input_temp[1][i]
        input_value_dic[str(len(input_temp[1]) + i + 1)] = input_temp[1][i]
    input_n = len(input_temp[3])
    input_c = bin(2 ** input_n - int(input_temp[3], 2))[2:]
    dic_len = len(input_value_dic)
    for i in range(len(input_c)):
        input_value_dic[str(dic_len + i + 1)] = input_c[i]

    fr_circuit = open('D:/circuit.txt', 'r')
    fw_garbled_circuit = open('D:/garbled_circuit.txt', 'w')
    line = fr_circuit.readline()
    while line:
        line = line[:-1]
        temp = line.split(' ')
        truth_table = Gen_Truth_Table(temp[0], temp[1], temp[2], temp[3])
        enc_truth_table = xor_hash.x_h(truth_table)
        Random.shuffle(enc_truth_table)
        for item in enc_truth_table:
            fw_garbled_circuit.write(item + ', ')
        fw_garbled_circuit.write(temp[0] + ', ' + temp[1] + ', ' + temp[3] + '\n')
        line = fr_circuit.readline()
    fr_circuit.close()
    fw_garbled_circuit.close()

    fw_garbled_input = open('D:/garbled_input.txt', 'w')
    for i in range(len(input_value_dic)):
        temp = LABEL_DIC[str(i + 1)].split(' ')
        fw_garbled_input.write(str(i + 1) + ', ' + temp[int(input_value_dic[str(i + 1)])] + '\n')
    fw_garbled_input.close()

    fr_output = open('D:/output.txt', 'r')
    fw_garbled_output = open('D:/garbled_output.txt', 'w')
    line = fr_output.readline()
    while line:
        line = line[:-1]
        fw_garbled_output.write(line + ', ' + LABEL_DIC[line] + '\n')
        line = fr_output.readline()
    fr_output.close()
    fw_garbled_output.close()

    print('finish')


if __name__ == '__main__':
    main()
