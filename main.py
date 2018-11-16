from flask import Flask
from flask import g

from evestatic import evestatic 
from components.region.routes import region
from components.main.routes import main


app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(region)

@app.teardown_appcontext
def close_connection(exception):
    evestatic.close_evestatic()

	
if __name__ == "__main__":
    app.run(host='0.0.0.0')