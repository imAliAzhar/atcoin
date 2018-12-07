import sys
from flask import Flask

node = Flask(__name__)

@node.route('/helo')
def hello():
    return 'Hello World'

node.run()

class Miner:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port




# main
# if len(sys.argv) < 3:
#     print('Please enter IP and Port for the miner to run on.')
#     sys.exit()
# else:
#     miner = Miner(sys.argv[1], sys.argv[2])
