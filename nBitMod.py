import math

def main():
    n, e, m = getInput()
    e_bin = bin(e)
    first_reminder = 1
    second_reminder = n
    print(1, first_reminder, second_reminder)
    for e_bit in str(e_bin)[3:]:
        first_reminder = (second_reminder * second_reminder) % m
        if e_bit == '1':
            second_reminder = (first_reminder * n) % m
        else:
            second_reminder = first_reminder
        print(e_bit, first_reminder, second_reminder)
    print("n^e mod m = ", second_reminder)
    return


def getInput():
    print("n^e mod m")
    n = int(input("n = "))
    e = int(input("e = "))
    m = int(input("m = "))
    return n, e, m

if __name__ == "__main__":
    main()
