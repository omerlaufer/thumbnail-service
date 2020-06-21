from flask import Flask, send_file
from flask_restful import Api, Resource, request
import requests
from PIL import Image, ImageOps
from io import BytesIO


app = Flask(__name__)
api = Api(app)

MAX_WIDTH = 5000
MAX_HEIGHT = 5000


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
    img_with_border = ImageOps.expand(img, border=border, fill="black")
    return img_with_border

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


def validate_args(args):
    if "url" not in args:
        return False, {"error": "missing url param"}
    if "width" not in args or not args["width"].isdigit() and int(args["width"]) > MAX_WIDTH:
        return False, {"error": "missing or invalid width param"}
    if "height" not in args or not args["height"].isdigit() and int(args["height"]) > MAX_HEIGHT:
        return False, {"error": "missing or invalid height param"}
    return True, {}



class Thumbnail(Resource):
    def get(self):
        """
        GET /thumbnail?url=<url>&width=<width>&height=<height>
        :return: resized padded image
        """
        args = request.args
        valid, msg = validate_args(args)
        if not valid:
            return msg, 400

        url = args["url"]
        new_width = int(args["width"])
        new_height = int(args["height"])

        try:
            data = requests.get(url, timeout=1)
        except requests.exceptions.ConnectionError:
            return {"error": "url not found"}, 404
        data.raise_for_status()
        try:
            img = Image.open(BytesIO(data.content))
        except OSError:
            return {"error": "url is not an image"}, 400
        new_img = get_new_image(img, new_width, new_height)
        return serve_pil_image(new_img)


api.add_resource(Thumbnail, "/thumbnail")

if __name__ == "__main__":
  app.run()


