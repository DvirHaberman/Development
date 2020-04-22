from python.model import *


def threaded_app():
    # threaded_app = Flask(__name__)
    # db.init_app(threaded_app)
    # threaded_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb"
    # threaded_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    threaded_app = create_threaded_app(db)
    with threaded_app.app_context():
        session = db.create_scoped_session()
        d = session.query(User).all()
        print(d)