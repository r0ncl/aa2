import random
import time

t0=time.time()

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

# testing

import hashlib
m = hashlib.sha256()
m.update(b'Message')
m.update(b'Longer Message Sequence Testing To Evaluate!~'*1000)
m.update(b'Longer Message Sequence Testing To Evaluate!~'*1000000)

dg=int(m.hexdigest(),16)
print('Hashed Message: ', dg, end='\n\n')

skx, pkx = genkey(n,g,q)
print('Keys (private, public):\n',skx,'\n\n', pkx, end='\n\n')
sig = sign(skx, dg, g, q)
print('Sign:\n', sig, end='\n\n')

print('Verify True: ', verify(sig, pkx, dg, g, q))
print('Verify False: ', verify(sig, pkx, dg+2, g, q))
t1=time.time()
print('\nExecution Time:\n',t1-t0)
