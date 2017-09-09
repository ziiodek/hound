import hashlib, zlib
import pickle
import urllib

class Hasher:

    def encode(data):
        text = zlib.compress(pickle.dumps(data, 0))
        m = data + str(text)
        m = hashlib.md5(m.encode('utf-8')).hexdigest()[:12]
        return m

