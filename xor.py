#!/usr/bin/env python
# -*- coding: utf-8 -*-
#xor file
import sys

class xor():

  def xor(self, orginal_file, xor_var, new_file):
    l = len(xor_var)
    data = bytearray(open(orginal_file, 'rb').read())
    result = bytearray((
      (data[i] ^ xor_var[i % l]) for i in range(0,len(data))
    ))
    localFile = open(new_file, 'w')
    localFile.write(result)
    localFile.close()


if __name__ == '__main__':
  try:
    orginal_file = sys.argv[1]
    new_file = sys.argv[2]
    ##xor_var bytes are currently hardcoded
    xor_var = bytearray([0xde,0xad,0x13,0x37])
    transform = xor()
    transform.xor(orginal_file, xor_var, new_file)
  except IndexError:
    print('Usage: xor.py <input_file> <output_file>')
    print('Note: xor byte values are currently hardcoded!')
    sys.exit(1)
