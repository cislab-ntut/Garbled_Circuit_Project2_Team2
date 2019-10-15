class Gate:
    def __init__(self, data):
        self.data = data
        self.inp1 = None
        self.inp2 = None
        return
        
    def addGateByInp(self):
        inp = input()
        if inp != 'inp':
            self.inp1 = Gate(inp)
            self.inp1.addGateByInp()
        inp = input()
        if inp != 'inp':
            self.inp2 = Gate(inp)
            self.inp2.addGateByInp()
        return 

    def addGateByFile(self, inpList):
        inp = inpList.pop(0)
        if inp != 'inp':
            self.inp1 = Gate(inp)
            self.inp1.addGateByFile(inpList)
        inp = inpList.pop(0)
        if inp != 'inp':
            self.inp2 = Gate(inp)
            self.inp2.addGateByFile(inpList)
        return 
