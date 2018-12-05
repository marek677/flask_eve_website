from flask import Flask
from flask import g

from evestatic import evestatic 
from components.region.routes import region
from components.main.routes import main
from components.industry.routes import industry


app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(region)
app.register_blueprint(industry)

@app.teardown_appcontext
def close_connection(exception):
	evestatic.close_evestatic()
	blueprint_json = getattr(g, '_blueprint', None)
	if blueprint_json is not None:
		blueprint_json = None
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')