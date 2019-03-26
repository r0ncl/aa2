from Node import Node

class CompliantNode(Node):
  self.followees = []
  self.pendingTx = []

  def __init__(self, p_graph, p_malicious, p_txDistribution, numRounds):
    self.p_graph = p_graph
    self.p_malicious = p_malicious
    self.p_txDistribution = p_txDistribution
    self.numRounds = numRounds


  def setFollowees(self, followees):
    self.followees = followees

  
  def setPendingTx(self, pendingTx):
    self.pendingTx = pendingTx

  def sendToFollowers(self):
    tx = self.pendingTx
    self.pendingTx = []
    return tx

  def receiveFromFollowees(self, candidateList):
    candidateFollowees = [i.sender for i in candidateList]
    maliciousTrue = [ [i and i not in candidateFollowees] for i in self.followees]
    self.pendingTx = [None if maliciousTrue[i.sender] else i.tx for i in candidateList]
    self.pendingTx = list(set(self.pendingTx)).remove(None)


  
