#!/usr/bin/env python
#Adds 4digits to the end of the common word lists
import os, sys


class Wordlist_Add_Digits():

	def add_digits(self, wordlist, outfile):
		#File to start with
		file=wordlist
		#Output file
		out=open(outfile, 'w')
		#Start loop of 0000-9999 added to each word
		with open(file) as f:
			content = f.read().splitlines()
			for x in content:
				for a in range(10):
					x0=x+str(a)
					for b in range(10):
						x1=x0+str(b)
						for c in range (10):
							x2=x1+str(c)
							for d in range (10):
								x3=x2+str(d)
								# print final combo
								out.write(str(x3)+"\n")


if __name__ == '__main__':
	try:
		wordlist = sys.argv[1]
		outfile = sys.argv[2]
		wordz = Wordlist_Add_Digits()
		wordz.add_digits(wordlist, outfile)
	except IndexError:
		print('Usage: wordlist_add_digits.py wordlist.txt output.txt')
		sys.exit(1)
