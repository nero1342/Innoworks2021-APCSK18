import base64

def encode_image(img_path):
    with open(img_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode("utf-8")
