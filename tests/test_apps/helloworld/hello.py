from pboot import Pboot

app = Pboot(__name__)


@app.route("/")
def hello():
    return "Hello World!"
