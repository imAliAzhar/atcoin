import os
import ecdsa
wallet = "wallet.key"

def generate_keys():
    print("Creating a new wallet...")
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    verrifying_key = signing_key.get_verifying_key() 
    private_key = signing_key.to_string().hex() 
    public_key = verrifying_key.to_string().hex()
    filename = "wallet.key"
    with open(wallet, 'w') as f:
        f.write("{0}\n{1}".format(private_key, public_key))
    print("Private and public keys have been stored in", filename)

def sign_message(private_key, message):
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = signing_key.sign(message)
    return signature, message

def read_keys():
   with open(wallet, 'r') as f:
       private_key = f.readline().strip()
       public_key = f.readline().strip()
       return private_key, public_key

#########################################

if not os.path.isfile(wallet):
    generate_keys()