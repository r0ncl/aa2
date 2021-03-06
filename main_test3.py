from txHandler import *

# testing 1 wrong key signature, by keeping all other conditions correct e.g. no multiple utxo claims
# key mess up locates at the end of script
keyN=10
keyList=[]
for i in range(keyN):
  k=genkey(n,g,q)
  keyList.append(k)

upl = UTXOPool()
utxoToKeyPair = {}
keyPairMap={}

utxoTx = 10
utxoOutBound=5
valueBound=100

for i in range(utxoTx):
  tx = Transaction()
  outIndex = random.randint(1,utxoOutBound)
  
  for j in range(outIndex):
    value = valueBound * random.random()
    kidx  = random.randint(0, keyN-1)
    addr = keyList[kidx][1]
    tx.addOutput(value, addr)
    keyPairMap[j] = keyList[kidx]
  
  tx.finalize()

  for i in range(outIndex):
    ut = UTXO(tx.getHash() ,i)
    upl.addUTXO(ut, tx.getOutput(i))
    utxoToKeyPair[ut] =  keyPairMap[i]

utxoSet = upl.getAllUTXO()

txN = 7
iBound=2
oBound=3
txList=[]

for i in range(txN):
  tx = Transaction()
  utxoMap = {}

  inpN = 2#random.randint(1,iBound)
  outN = random.randint(1,oBound)
  ivalue=0
  ovalue=0

  for j in range(inpN):
    ut = utxoSet[i*2+j] # non overlap utxo tx inputs, but mess up keys for some txs
    tx.addInput(ut.getTxHash(), ut.getIndex())
    ivalue += upl.getTxOutput(ut).value
    utxoMap[j] = ut

  for i in range(outN):
    value = valueBound * random.random() 
    ovalue+=value
    if ovalue > ivalue:
      break
    kidx  = random.randint(0, keyN-1)
    addr = keyList[kidx][1]
    tx.addOutput(value, addr)

  for i in range(inpN):
    m = hashlib.sha256()
    m.update(str.encode(tx.getRawDataToSign(i)))
    dg = int(m.hexdigest(),16)
    tx.addSignature(sign(utxoToKeyPair[utxoMap[i]][0], dg, g, q),i)
  
  
  tx.finalize()
  txList.append(tx)

tx = txList[0]
m = hashlib.sha256()
m.update(str.encode(tx.getRawDataToSign(1)))
dg = int(m.hexdigest(),16)
 
tx.addSignature(sign(utxoToKeyPair[utxoMap[0]][0], dg, g, q),1)
hdr = txHandler(upl)
record = hdr.handleTxs(txList)
print(record)
