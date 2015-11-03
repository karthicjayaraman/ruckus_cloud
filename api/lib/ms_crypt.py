import base64


def decode_hash(hash):
        try:
		hash=base64.b64decode(hash)
        except Exception:
                pass
        return hash

def encode_hash(string):
	try:
		string=base64.b64encode(string)
	except Exception:
		pass
	return string

