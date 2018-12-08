import os
import ecdsa


class Wallet:
    def __init__(self, name):
        self.name = name.lower().capitalize()
        self.private_key, self.public_key = self.get_keys()

    def generate_keys(self, filename):
        print("Creating a new wallet...")
        signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        private_key = signing_key.to_string().hex()
        public_key = verifying_key.to_string().hex()
        with open(filename, 'w') as f:
            f.write("{0}\n{1}".format(private_key, public_key))
        print("Private and public keys have been stored in", filename)


    def sign_message(self, private_key, message):
        bmessage = message.encode()
        signing_key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        signature = signing_key.sign(bmessage)
        return signature, message


    def validate_signature(self, public_key, signature, message):
        verifying_key = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
        return verifying_key.verify(signature, message.encode())


    def get_keys(self):
        filename = "keys/" + self.name.lower() + ".key"
        if not os.path.isfile(filename):
            print("Wallet for {0} does not exist.".format(self.name))
            self.generate_keys(filename)
        with open(filename, 'r') as f:
            private_key = f.readline().strip()
            public_key = f.readline().strip()
            return private_key, public_key

#########################################

# w = Wallet("Ali")
# w.get_keys()

# pr, pu = get_keys()

# s, d = sign_message(pr, "ali")
# print(validate_signature(pu, s, d))
