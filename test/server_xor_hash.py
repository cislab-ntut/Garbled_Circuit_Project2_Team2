import hashlib

def s_x_h(input_A, input_B, encrypt_table):
    for table_len in range(len(encrypt_table)):
        sha = hashlib.md5()
        s1_t = int(input_A, 16)
        s2_t = int(input_B, 16)
        s3_t = int(encrypt_table[table_len][0], 16)
        x_result = hex(s1_t ^ s2_t ^ s3_t)[2:]
        sha_data = input_A + input_B + x_result
        sha.update(sha_data.encode("utf-8"))
        sha_result = sha.hexdigest()#hash value
        if sha_result == encrypt_table[table_len][1]:
            return x_result
