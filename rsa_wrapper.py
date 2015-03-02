from Crypto.PublicKey import RSA 

class rsa_wrapper():
  
  def keygen(self):
    key = RSA.generate(2048, e=65537) 
    public = key.publickey().exportKey("PEM") 
    private = key.exportKey("PEM") 
    return public, private

if __name__ == '__main__':
  try:
    rsa = rsa_wrapper()
    public, private = rsa.keygen()
    print public
    print private
  except:
    print "error"
