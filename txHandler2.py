import copy
from UTXOPool import UTXOPool
from UTXO import UTXO
from Transaction import Transaction
from keys import *
import hashlib

class txHandler:

  def __init__(self, utxoPool):
    if isinstance(utxoPool,UTXOPool):
      self.utxoPool = copy.copy(utxoPool)
    
    try:
      self.utxoPool
    except AttributeError: 
      print('Argument must be UTXOPool')


  def isValid(self, tx):
    existUtxo = []
    inputValue=0
    outputValue=0
    index=0

    for i in tx.getInputs():
        l = 0
        for w in self.utxoPool.H:
          if (i.prevTxHash == w.txHash and i.outputIndex == w.index):
            tsUtxo = w
            l = 1
        if l == 0:
          return False

        m = hashlib.sha256()
        m.update(str.encode(tx.getRawDataToSign(index)))
        dg = int(m.hexdigest(),16)

        if tsUtxo in existUtxo:
          return False
        
        elif not verify(i.signature, self.utxoPool.getTxOutput(tsUtxo).address, dg ,g, q):
          return False
        
        existUtxo.append(tsUtxo)
        inputValue += self.utxoPool.getTxOutput(tsUtxo).value
        index += 1
    
    for j in tx.getOutputs():
        if j.value < 0:
          return False
        outputValue += j.value

    if outputValue > inputValue:
      return False

    return True




  def handleTxs(self, possibleTxs):
    invalidTxs = []
    validTxs = []

    if isinstance(possibleTxs, dict):
      possibleTxs = list(possibleTxs.values())
    
    for tx in possibleTxs:
      if self.isValid(tx):
        validTxs.append(tx)

        for i in tx.getInputs():
          for w in self.utxoPool.H:
            if (i.prevTxHash == w.txHash and i.outputIndex == w.index):
                iUtxo = w
          self.utxoPool.remove(iUtxo)
        
        index = 0
        txHash = tx.getHash()
        for o in tx.getOutputs():
          oUtxo = UTXO(txHash,index)
          out = tx.getOutput(index)
          self.utxoPool.addUTXO(oUtxo,out)
          index += 1

      
      else:
        invalidTxs.append(tx)
      
    return {'Valid':validTxs, 'Invalid':invalidTxs}



