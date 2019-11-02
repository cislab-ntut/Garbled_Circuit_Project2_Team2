import hashlib

def x_h(sign_truth_table):
    encrypt_table = []
    for table_len in range(len(sign_truth_table)):
        sha = hashlib.md5()
        x_result = ''#A ^ B ^ F
        s1_t = [ord(a) for a in sign_truth_table[table_len][0]]
        s2_t = [ord(a) for a in sign_truth_table[table_len][1]]
        s3_t = [ord(a) for a in sign_truth_table[table_len][2]]
        for sign_len in range(len(s1_t)):
            x_result += (chr(s1_t[sign_len] ^ s2_t[sign_len] ^ s3_t[sign_len]))
        sha_data = sign_truth_table[table_len][0] + sign_truth_table[table_len][1] + sign_truth_table[table_len][2]
        sha.update(sha_data.encode("utf-8"))
        sha_result = sha.hexdigest()#hash value
        encrypt_table.append([x_result, sha_result])
    return(encrypt_table)
