import hashlib

def x_h(sign_truth_table):
    encrypt_table = []
    for table_len in range(len(sign_truth_table)):
        sha = hashlib.sha256()
        temp = sign_truth_table[table_len].split(' ')
        s1_t = int(temp[0], 16)
        s2_t = int(temp[1], 16)
        s3_t = int(temp[2], 16)
        x_result = hex(s1_t ^ s2_t ^ s3_t)[2:]
        sha_data = temp[0] + temp[1] + temp[2]
        sha.update(sha_data.encode("utf-8"))
        sha_result = sha.hexdigest()#hash value
        encrypt_table.append(x_result + ' ' + sha_result)
    return(encrypt_table)
