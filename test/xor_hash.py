import hashlib

def x_h(sign_truth_table):
    encrypt_table = []
    for table_len in range(len(sign_truth_table)):
        sha = hashlib.md5()
        s1_t = int(sign_truth_table[table_len][0], 0)
        s2_t = int(sign_truth_table[table_len][1], 0)
        s3_t = int(sign_truth_table[table_len][2], 0)
        x_result = str(hex(s1_t ^ s2_t ^ s3_t))
        sha_data = sign_truth_table[table_len][0] + sign_truth_table[table_len][1] + sign_truth_table[table_len][2]
        sha.update(sha_data.encode("utf-8"))
        sha_result = sha.hexdigest()#hash value
        encrypt_table.append([x_result, sha_result])
        #print(x_result, sha_result)
    return(encrypt_table)
