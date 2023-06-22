import base64
import qrcode

def encode_base64(data):
	# bytes = data.encode('ascii')
	bytes = data.encode('utf-8')
	encoded = base64.b64encode(bytes)
	result = encoded.decode('ascii')
	return result


def str_to_qrcode(data):
	qr = qrcode.QRCode(
	    version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
	qr.add_data(data)
	qr.make(fit=True)
	image = qr.make_image(fill_color="black", back_color="white")
	image.save("static/qr.png")
