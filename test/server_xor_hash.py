import hashlib

def s_x_h(input_A, input_B, encrypt_table):
    for table_len in range(len(encrypt_table)):
        sha = hashlib.md5()
        x_result = ''#A ^ B ^ E
        s1_t = [ord(a) for a in input_A]
        s2_t = [ord(a) for a in input_B]
        s3_t = [ord(a) for a in encrypt_table[table_len][0]]
        for sign_len in range(len(s1_t)):
            x_result += (chr(s1_t[sign_len] ^ s2_t[sign_len] ^ s3_t[sign_len]))
        sha_data = input_A + input_B + x_result
        sha.update(sha_data.encode("utf-8"))
        sha_result = sha.hexdigest()#hash value
        if sha_result == encrypt_table[table_len][1]:
            return x_result
