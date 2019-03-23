from Transaction import Transaction
import hashlib

class Block:
  coinBase = 25
  previousHash=None
  Hash=None
  coinBaseTx = Transaction()
  txs=[]

  def __init__(self,prevHash, publicKey):
    self.previousHash = prevHash
    self.coinBaseTx.Output(self.coinBase, publicKey)
    self.coinBaseTx.finalize()
  
  def getCoinbase(self):
    return self.coinBase

  def getHash(self):
    return self.Hash

  def getPreviousHash(self):
    return self.previousHash

  def getTxs(self):
    return self.txs

  def getTx(self,index):
    return self.txs[index]

  def addTx(self,tx):
    self.txs.append(tx)

  def getRawBlock(self):
    rawBlock = ''
    rawBlock += self.previousHash if self.previousHash != None else None
    rawBlock += ''.join([i.getRawTx() for i in self.txs])
    return rawBlock

  def finalize(self):
    m = hashlib.sha256()
    m.update(self.getRawBlock().encode('utf-8'))
    self.Hash = m.hexdigest()
  
