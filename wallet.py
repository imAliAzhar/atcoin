import os
import ecdsa


wallet = "wallet.key"

def generate_keys():
    print("Creating a new wallet...")
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) 
    verifying_key = signing_key.get_verifying_key() 
    private_key = signing_key.to_string().hex() 
    public_key = verifying_key.to_string().hex()
    filename = "wallet.key"
    with open(wallet, 'w') as f:
        f.write("{0}\n{1}".format(private_key, public_key))
    print("Private and public keys have been stored in", filename)

def sign_message(private_key, message):
    bmessage = message.encode()
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = signing_key.sign(bmessage)
    return signature, message

def verify_message(public_key, message):
    # message = message.encode()
    verifying_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    return verifying_key.verify

def validate_signature(public_key, signature, message):
    verifying_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
    return verifying_key.verify(signature, message.encode())


def get_keys():
    if not os.path.isfile(wallet):
        print("Wallet does not exist.")
        return
    with open(wallet, 'r') as f:
       private_key = f.readline().strip()
       public_key = f.readline().strip()
       return private_key, public_key

#########################################

if not os.path.isfile(wallet):
    generate_keys()

pr, pu = get_keys()

s, d = sign_message(pr, "ali")
print(validate_signature(pu, s, d))

