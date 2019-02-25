import random
safe_prime_513 = 8943938320423611270099436734062740589060062021153730609410037915132880236500958868474090824253675906425897787013229680906438005688812810206779297656565043

g, q, n = 2, safe_prime_513, 513

def genkey(n,g,q):
  sk = random.getrandbits(n)
  pk = pow(g, sk,q)
  return sk, pk

def sign(sk, msg, g, q):
  return pow(g, (msg - sk) % (q-1), q)

def verify(sig, pk, msg, g, q):
   return (sig * pk)%q == pow(g,msg % (q-1),q)
