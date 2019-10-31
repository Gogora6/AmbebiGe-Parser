from flask import Flask
from functions import SaitebiGe

app = Flask(__name__)


@app.route("/<string:name>&<string:lastName>", methods=['GET'])
def index(name, lastName):
    website = SaitebiGe(name, lastName)
    website.parse_site()
    return name


if __name__ == '__main__':
    app.run(debug=True, port=4000)
