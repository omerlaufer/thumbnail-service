from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse, request
import requests
from PIL import Image, ImageOps
from io import BytesIO


app = Flask(__name__)
api = Api(app)


def get_new_ratio(orig_w, orig_h, new_w, new_h):
    ratio = orig_w / orig_h
    new_width = new_h * ratio
    new_height = new_h
    if new_width > new_w:
        new_height = new_w / ratio
        new_width = new_w
    return int(new_width), int(new_height)


def get_new_image(img, new_width, new_height):
    exists_width, exists_height = img.size
    if new_width < exists_width or new_height < exists_height:
        exists_width, exists_height = get_new_ratio(exists_width, exists_height, new_width, new_height)
        img = img.resize((exists_width, exists_height), Image.ANTIALIAS)
    delta_width = new_width - exists_width
    delta_height = new_height - exists_height
    border = (delta_width//2, delta_height//2, delta_width - (delta_width//2), delta_height-(delta_height//2))
    img_with_border = ImageOps.expand(img, border=border, fill="red")
    return img_with_border

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


class Thumbnail(Resource):
    def get(self):
        args = request.args
        url = args.get("url")
        new_width = int(args.get("width"))
        new_height = int(args.get("height"))
        data = requests.get(url)
        img = Image.open(BytesIO(data.content))
        new_img = get_new_image(img, new_width, new_height)
        return serve_pil_image(new_img)


api.add_resource(Thumbnail, "/thumbnail")
app.run(debug=True)
# /thumbnail?url=<url>&width=<width>&height=<height>

