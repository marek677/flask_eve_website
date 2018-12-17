from flask import Flask
from flask import g

from evestatic import evestatic 
from components.region.routes import region
from components.main.routes import main
from components.industry.routes import industry
import pkg_resources

app = Flask(__name__)

app.config.update(dict(
    BASE_DIR=pkg_resources.resource_filename(__name__,""),
))
app.register_blueprint(main)
app.register_blueprint(region)
app.register_blueprint(industry)

@app.teardown_appcontext
def close_connection(exception):
	evestatic.close_evestatic()
	g._blueprint = None
	
if __name__ == "__main__":
    app.run(host='0.0.0.0')