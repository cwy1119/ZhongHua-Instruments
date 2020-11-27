#!/usr/bin/env python3
import os

from application import create_app,db
# from application import AddInstrument
# from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)


db.create_all(app=app) 
if __name__ == "__main__":
    
    app.run(debug=True)
    # app.run(debug=True)
