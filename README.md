# thumbnail-service
sample service for handling images, resizing and padding

## Installation

first create a virtualenv and activate it
```bash
python3 -m venv my-venv
source my-venv/bin/activate
```

now clone the code and install the requirements
```bash
git clone https://github.com/omerlaufer/thumbnail-service.git
cd thumbnail-service/
pip install -r requirements.txt
```

in order to run the web service locally, simply execute

```bash
python app.py
```
### Usage

This is a GET API which get 3 query strings arguments:

*url* - a valid url to the source image

*width* - an integer of the desired image width

*height* - an integer of the desired image height

```bash
curl -i -X GET \
 'http://127.0.0.1:5000/thumbnail?url=<URL>&width=<WIDTH>&height=<HEIGHT>'
```
