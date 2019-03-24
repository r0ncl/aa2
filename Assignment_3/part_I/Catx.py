from Encodings import encode
import hashlib

# only approved txs by txHandler continues encodeCatx() interface to encode current tx
# encodeCatx() defined below encodes all pks for scripSig and script
# only the small set of scripts P2PKH, P2PT, P2UCS, P2HS in example is allowed in encodeCatx() interface
class Catx:

    class Input():
        def __init__(self, prevHash, index, pk):
            if (prevHash == None):
                self. prevTxHash = None
            else:
                self.prevTxHash = prevHash
            self.outputIndex = index
            self.pk = pk

        def addSignature(self, sig):
            if (sig == None):
                self.signature = None
            else:
                self.signature = sig
        
        def addScriptSig(self):
            self.scriptSig = [self.signature, self.pk]
        

    class Output():
        def __init__(self, v, pk, script):
            self.value = v;
            self.address = pk
            self.script = script
        

    def __init__(self, tx = None):
        self.inputs = []
        self.outputs = []
        if tx != None:
            self.hash = tx.hash

    # assume approved validate txs by allowed scripts provided
    # assume all keyhash in scripts are ripemd160
    # encode all pks to base58 encoding after scripSig generated and before finalize
    # assume script used are common in structure, e.g. common position 3 for pk in string
    def encodeCatx(self):
        transAddr = []
        for i in self.getOutputs():
          key=i.script.keys()[0]
          assert (key == 'P2PKH' or key == 'P2PT' or key == 'P2UCS' or key == 'P2HS'), 'script type is not allowed'
          transAddr[i] = i.script[key].split()[2]
    
        pkTuple = self.scripSig[1], self.address
        pkHashList = [hashlib.sha256().update(str(i).encode('utf-8')).hexdigest() for i in pkTuple]
        pkHashList160 = [hashlib.new('ripemd160').update(pkHashList(i).encode('utf-8')).hexdigest() for i in pkHashList] + transAddr
        addresses = [encode(int(i,16)) for i in pkHashList160]
        self.scripSig[1], self.address = addresses[0:2]

        for i in self.getOutputs():
          key=i.script.keys()[0]
          scriptStr=i.script.values()[0].split()
          scriptStr[2]=str(addresses[i+2])
          i.script[key]=' '.join(scriptStr)
        
        #return encoded base58 pk address of output
        return self.address


    def addInput(self, prevTxHash, outputIndex):
        inp = self.Input(prevTxHash, outputIndex)
        self.inputs.append(inp)

    def addOutput(self, value, address):
        op = self.Output(value, address)
        self.outputs.append(op)
    
    def removeInputIndex(self, index):
        self.inputs.remove(index)
    

    def removeInput(self, ut):
        for u in self.inputs:
            if (u.equals(ut)):
                self.inputs.remove(u)
            

    def getRawDataToSign(self, index):
        # produces data repr for  ith=index input and all outputs
        sigData = ""
        if (index > len(self.inputs)):
            return None
        inp = self.inputs[index]
        self.prevTxHash = inp.prevTxHash
        sigData += str(inp.outputIndex)
        sigData += self.prevTxHash
        for op in self.outputs:
            sigData += str(op.value)
            sigData += str(op.address)
        return sigData
    

    def addSignature(self, signature, index):
        self.inputs[index].addSignature(signature)
    

    def getRawTx(self):
        rawTx = ""
        for inp in self.inputs:
            rawTx += str(inp.prevTxHash)
            rawTx += str(inp.outputIndex)
            rawTx += str(inp.signature)
        
        for op in self.outputs:
            rawTx += str(op.value)
            rawTx += str(op.address)

        return rawTx


    def finalize(self):
        import hashlib
        md = hashlib.sha256()
        md.update(self.getRawTx().encode('utf-8'))
        self.hash = md.hexdigest()

    def getHash(self):
        return self.hash

    def getInput(self, index):
        if (index < len(self.inputs)):
            return self.inputs[index]
        return None
    def getInputs(self):
        return self.inputs
    

    def getOutput(self, index):
        if (index < len(self.outputs)):
            return self.outputs[index]
        return None
    
    def getOutputs(self):
        return self.outputs
