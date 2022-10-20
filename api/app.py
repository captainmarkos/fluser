import os
from time import gmtime, strftime
from flask import Flask

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'fluser.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# health check
@app.route('/status')
def status():
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return { 'timestamp': now }

import db
db.init_app(app)

import auth
app.register_blueprint(auth.bp)

#from . import blog
#app.register_blueprint(blog.bp)
#app.add_url_rule('/', endpoint='index')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

