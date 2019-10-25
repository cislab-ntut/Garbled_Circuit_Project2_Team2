from stack import Stack

def infix_to_postfix(infixexpr):
#首先用一個dict來設定各個運算符的優先級
    prec = {}
    prec["*"] = 2
    prec["+"] = 2
    prec["("] = 1

#step one 創建一個新的stack和一個空的list
    opStack = Stack()
    postfixList = []

#將string轉成list
    tokenList = list(infixexpr)

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":                                #檢查是運算元還是運算符
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken) 
                topToken = opStack.pop()
        else:
            while (not opStack.is_empty()) and \
               (prec[opStack.Top()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

#最後將stack清空
    while not opStack.is_empty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)


