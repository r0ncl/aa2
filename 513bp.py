import random
import time

#generating 513-bit Miller-Rabin tested safe prime
t0 = time.time();
def miller_rabin(n, k=10):
  """ Miller-Rabin test for primality
  >>> miller_rabin(11)
  True
  >>> miller_rabin(21)
  False
  >>> miller_rabin(130543930748028840018705051047)
  True
  >>> miller_rabin(100**10-1)
  False
  """
  if n == 2:
    return True
  if not n & 1:
    return False

  d = n - 1

  def check(a, d, n):
    while d % 2 == 0:
      d>>=1
      x = pow(a, d, n)
      if x==n-1:
       return True
    if x==1:
      return True
    return False

  for i in range(k):
    a = random.randrange(2, n - 1)
    if not check(a, d, n):
      return False
    return True


def generate_safe_prime(n=200):
    while(True):
        randx=random.getrandbits(n-1)
        if miller_rabin(randx):
            #print(randx, " is prime")
            p = 2*randx + 1
            if miller_rabin(p):
                print(p, " is safe ", n, "-bit prime number")
                return p

for i in range(513,514):
     generate_safe_prime(i)

if __name__ == "__main__":
    import doctest
doctest.testmod(verbose=True)

t1= time.time()
t=t1-t0
