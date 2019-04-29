from random import randint
from bitarray import bitarray
from math import ceil, log

ELEMENTS_NO = 10_000
U_SIZE = 1000_000
FACTOR = 10
K = 6

class BloomFilter:

	def primary_gt_than(self, M):
		x = M + 1
		while(True):
			is_prim = True
			for i in range(2,x//2+1):
				if x%i == 0:
					is_prim = False
					x += 1
					break
			if is_prim == True:
				break
		return x

	def hash_function(self, a,b,p, n):
		def func(x):
			return ((a*x + b ) % p ) % n
		return func

	def __init__(self, np, kp):
		self.n = np 
		self.k = kp 
		self.bits = bitarray(self.n) # vector of bits
		self.bits.setall(False)
		self.p = self.primary_gt_than(U_SIZE) # prime p
		# array of hash functions
		self.functions = []
		for i in range(self.k):
			a=randint(1,self.p-1)
			b=randint(0,self.p-1)
			self.functions.append( self.hash_function(a, b, self.p, self.n) )

	def get_bits_keys(self, val):
		result = []
		for f in self.functions:
			result.append(f(val))
		return result

	def add(self, key):
		bits_keys = self.get_bits_keys(key)
		for v in bits_keys:
			self.bits[v] = True

	def __contains__(self, key):
		contains = True
		bits_keys = self.get_bits_keys(key)
		for v in bits_keys:
			if not(self.bits[v]):
				contains = False
				break
		return contains

	def test(self, u):
		# generate random numbers
		hs_set = set()
		while(len(hs_set) < ELEMENTS_NO):
			hs_set.add(randint(0,u))

		# add generated data to Bloom filter bit array
		for i in hs_set:
			self.add(i)

		TP = 0
		FP = 0
		TN = 0
		FN = 0
		
		for i in range(u):
			key = randint(0,u)
			containsBF = key in self
			containsHS = (key in hs_set)
			
			if containsBF and containsHS:
				TP += 1
			elif not(containsBF) and not(containsHS):
				TN += 1
			elif not(containsBF) and containsHS:
				FN += 1
			elif containsBF and not(containsHS):
				FP += 1

		print( "TP = {:6d} \t TPR = {:1.4f}".format( TP, TP/ELEMENTS_NO) )
		print( "TN = {:6d} \t TNR = {:1.4f}".format( TN, TN/(u - ELEMENTS_NO) ) )
		print( "FN = {:6d} \t TNR = {:1.4f}".format( FN, FN/ELEMENTS_NO) )
		print( "FP = {:6d} \t FPR = {:1.4f}".format( FP, FP/(u - ELEMENTS_NO) ))
		

if __name__ == "__main__": 
	size = round(FACTOR * ELEMENTS_NO)
	bf = BloomFilter(size, K)
	bf.test(U_SIZE)