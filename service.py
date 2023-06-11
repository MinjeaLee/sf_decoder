import base64

def encode_base64(data):
	# bytes = data.encode('ascii')
	bytes = data.encode('utf-8')
	encoded = base64.b64encode(bytes)
	result = encoded.decode('ascii')
	return result