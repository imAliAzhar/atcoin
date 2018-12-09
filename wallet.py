import os
import ecdsa


class Wallet:
    def __init__(self, name):
        self.name = name.lower().title()
        self.private_key, self.public_key = self.get_keys()

    def generate_keys(self, private_file, public_file):
        print("Creating a new wallet...")
        signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        private_key = signing_key.to_string().hex()
        public_key = verifying_key.to_string().hex()
        with open(private_file, 'w') as f:
            f.write(private_key)
        print("Private keys have been stored in", private_file)
        with open(public_file, 'w') as f:
            f.write(public_key)
        print("Public keys have been stored in", public_file)


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
        pr_file = "keys/private/" + self.name.lower() + ".key"
        pu_file = "keys/public/" + self.name.lower() + ".key"
        if not os.path.isfile(pr_file) or not os.path.isfile(pu_file):
            print("Wallet for {0} does not exist.".format(self.name))
            self.generate_keys(pr_file, pu_file)
        with open(pr_file, 'r') as f:
            private_key = f.readline()
        with open(pu_file, 'r') as f:
            public_key = f.readline()
        return private_key, public_key

#########################################

# w = Wallet("Ali")
# w.get_keys()

# pr, pu = get_keys()

# s, d = sign_message(pr, "ali")
# print(validate_signature(pu, s, d))
