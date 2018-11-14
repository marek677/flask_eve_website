from flask import Flask
from components.region.routes import region
from components.main.routes import main


app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(region)


	
if __name__ == "__main__":
    app.run(host='0.0.0.0')