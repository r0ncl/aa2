from Block import Block
from UTXOPool import UTXOPool
from UTXO import UTXO
from Transaction import Transaction
from txHandler import txHandler
import copy

class Blockchain:
  class BlockNode:
    def __init__(self,block=None,parent=None,utxoPool=None):
      assert(type(block)==Block or type(parent)==type(self) or type(utxoPool)==UTXO)
      self.block = block
      self.utxoPool = utxoPool
      self.parent = parent
      self.children = []
      if parent==None:
        self.length = 1
      else:
        
        self.length = parent.length+1
        parent.children.appned(self)

    def copyUtxoPool(self):
      return copy.deepcopy(self.utxoPool)

    
  def __init__(self,genesis):
    assert type(genesis) == Block
    self.cutoff = 10
    self.blockChain = {}
    self.maxLengthNode = genesis
    self.txs = []
    #add genesis node
    utxoPool = UTXOPool()
    self.addCoinbaseUtxoPool(genesis, utxoPool)
    genesisNode = self.BlockNode(genesis,None,utxoPool)
    self.blockChain[genesis.getHash] = genesisNode


  def getMaxLengthNode(self):
    return self.maxLengthNode

  def getTxs(self):
    return self.txs

  def copyMaxLengthNodeUtxoPool(self):
    return self.maxLengthNode.copyUtxoPool()

  def addCoinbaseUtxoPool(self,block,utxoPool):
    tx = block.getCoinbase()
    outPuts = tx.getOutputs()
    utxoPool.update([UTXO(tx.getHash(), outPuts[i]) for i in len(outPuts)])
  
  def addTx(self,tx):
    self.txs.append(tx)

  def addBlock(self,block):
    return False if block.previousHash==None else None
    parentNode = self.blockChain[block.previousHash]
    return False if parentNode==None else None
    return False if (parentNode.length + 1) <= (self.maxLengthNode.length - self.cutoff) else None
    hdl=txHandler(parentNode.copyUtxoPool())
    txArray = hdl.handleTxs(block.getTxs())
    return False if len(txArray['Valid']) < len(block.getTxs()) else None
    self.addCoinbaseUtxoPool(block, hdl.utxoPool)
    node = self.blockNode (block, parentNode, hdl.utxoPool)
    self.blockChain[block.getHash()] = node
    self.maxLengthNode = node if node.length > self.maxLengthNode.length else None

    return True


  