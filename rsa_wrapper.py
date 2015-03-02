import sys
import zlib
import base64
from Crypto.PublicKey import RSA 
from Crypto.Cipher import PKCS1_OAEP


class rsa_wrapper():
  
  def keygen(self):
    key = RSA.generate(2048, e=65537) 
    public = key.publickey().exportKey("PEM") 
    private = key.exportKey("PEM") 
    return public, private

  def encrypt(self, public, plaintext):
    rsakey = RSA.importKey(public) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    offset = 0
    encrypted = ""
    plaintext = zlib.compress(plaintext)
    while offset < len(plaintext):
      encrypted += rsakey.encrypt(plaintext[offset:offset+256])
      offset += 256
    encrypted = base64.b64encode(encrypted)
    return encrypted

  def decrypt(self, private, ciphertext):
    rsakey = RSA.importKey(private)
    rsakey = PKCS1_OAEP.new(rsakey)
    offset = 0
    decrypted = ""
    ciphertext = base64.b64decode(ciphertext)
    while offset < len(ciphertext):
      decrypted += rsakey.decrypt(ciphertext[offset:offset+256])
      offset += 256
    decrypted = zlib.decompress(decrypted)
    return decrypted


if __name__ == '__main__':
  try:
    message = sys.argv[1]
    rsa = rsa_wrapper()
    public, private = rsa.keygen()
    print public
    print private

    encrypted_message = rsa.encrypt(public, message)
    print encrypted_message

    decrypted_message = rsa.decrypt(private, encrypted_message)
    print decrypted_message

  except IndexError:
    print "python rsa_wrapper.py <Test message to encrypt>"
