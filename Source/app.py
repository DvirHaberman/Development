from python.DataCollector import DataCollector
from python.model import *
from threaded_workers import Worker, init_threads
from DbConnector import DbConnector
import os

# app = create_app()
app = Flask(__name__)
app.secret_key = os.environ.get('PYTHON_SECRET_KEY')
# app.permanent_session_lifetime = timedelta(minutes=int(os.environ.get('SESSION_LIFETIME')))
db.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///OctopusDB.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dvirh@localhost:5432/OctopusDB"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))

if sys.platform.startswith('win'):
    sys.path.append('C' + basedir[1:-7] + '\\Functions')
    sys.path.append('C' + basedir[1:-7] + '\\Infras\\Fetches')
    sys.path.append('C' + basedir[1:-7] + '\\Infras\\Utils')
    sys.path.append(basedir[:-7] + '\\Functions')
    sys.path.append(basedir[:-7] + '\\Infras\\Fetches')
    sys.path.append(basedir[:-7] + '\\Infras\\Utils')
else:
    sys.path.append(basedir[:-7] + r'/Functions')
    sys.path.append(basedir[:-7] + r'/Infras/Fetches')
    sys.path.append(basedir[:-7] + r'/Infras/Utils')

@app.route('/create_all')
def create_tables():
    db.create_all()
    return 'done'


@app.route('/collect_all')
def collect_data():
    if sys.platform.startswith('win'):
        collector = DataCollector(basedir + r"\..\Data\DataToCollect.xlsx")
    else:
        collector = DataCollector(basedir + r"/../Data/DataToCollect.xlsx")
    collector.CollectAll()
    return 'done'

@app.route('/init_workers', methods=['GET','POST'])
def init_workers():
    init_threads()
        # p=Process(target=init_proccesses)
        # p.start()
    return 'done'

@app.route('/run_functions_test')
def run_functions_test():
    functions = OctopusFunction.query.all()
    result_arr = []
    for func in functions:
        data = func.run('conn','run_id')
        print(data)
        result_arr.append(data)
    return jsonify(result_arr)

@app.route('/api/run_functions', methods=['GET','POST'])
def run_functions():
    # json_data = request.get_json()
    json_data = {'user_id':1,'mission_name':'mission1','functions':[1,2,3,4,5],'runs':[1122,1122,3344], 'db_name':'db_name'}
    # mission = Mission(json_data['mission_name'])
    # db.session.add(mission)
    # db.session.commit()
    Mission.create_mission(json_data)
    # if not type(json_data['functions']) == type(list()):
    #     json_data['functions'] = [json_data['functions']]
    # functions = db.session.query(OctopusFunction).filter(OctopusFunction.id.in_( json_data['functions'])).all()
    # names = [func.name for func in functions]
    # runs = json_data['runs']
    # if not type(runs) == type(list()):
    #     runs = [runs]
    
    # conn = DbConnector(json_data['db_name'], 'postgres', 'dvirh', 'localhost', '5432', 'octopusdb')
    # result_arr = []
    # result_arr2 = []
    # for run in runs:
    #     for func in functions:
            # data = func.run(conn,run)
            # result_arr.append({'db_name':json_data['db_name'], 'run_id':run, 'function':func.name, 'function_id':func.id, 'result':data})
            # result_arr2.append(data)
    # overview = OverView(mission_id=10, results=result_arr2)
    # return jsonify({'runs':runs, 'function_names':names, 'results':result_arr})
    return 'done'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login_first')
def login_first():
    return render_template('login_first.html')

@app.route('/login')
def login():
    if session.get('username', None) is None:
        return render_template('login.html')
    else:
        return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('welcome.html')
    

@app.route('/logout')
def logout():
    if session.get('username', None) is None:
        return redirect('/login')
    else:
        session.pop('username', None)
        flash('you were logged out')
        return redirect('/login')

@app.route('/validate_user', methods=["POST"])
def validate_user():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=username, password_sha=password).first()
        if user:
            session['username'] = username
            return redirect('/welcome')
        else:
            flash('Invalid username or password!')
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/run_simple')
def run_simple():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('run_simple.html')
    

@app.route('/api/run_queue_test')
def run_queue_test():
    global tasks_queue
    task1 = AnalyseTask(mission_id=5 ,function_id=1,
                 run_id='1212',
                 priority=1, user_id=1)
    db.session.add(task1)
    db.session.commit()
    task1.push()
    task, func, time, task_id = tasks_queue.get_nowait()

    return 'done'

@app.route('/db_conn_wizard')
def db_conn_wizard():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('db_conn_wizard.html')    

@app.route('/api/get_conn_data')
def get_conn_data():
    connections = DbConnections.query.all()
    return jsonify([conn.self_jsonify() for conn in connections])

@app.route('/api/delete_connection/<string:conn_name>', methods=["POST"])
def delete_connection(conn_name):
    conn_to_delete = DbConnections.query.filter_by(name=conn_name).first()
    if conn_to_delete:
        try:
            # db.session.delete(conn_to_delete)
            # db.session.commit()
            return jsonify(message=conn_name +' was deleted')
        except Exception as error:
            return jsonify(message='something went wrong while deleting ' +conn_name)
    return jsonify(message='connectiong name not found')

@app.route('/api/save_connection', methods = ['POST'])
def save_connection():
    data = request.get_json()
    conn = DbConnector(db_type=data['db_type'], user=data['user'], password=data['password'],
                hostname=data['hostname'], port=data['port'], schema=data['schema'], name=data['name'])
    conn.save()
    if conn.status == 'valid':
        connections = DbConnections.query.all()
        conn_data = [conn.self_jsonify() for conn in connections]
        return jsonify(status = 1, message='connection successfuly saved!', connections=conn_data)
    else:
        return jsonify(status=0, message='Failed saving the connection!\n' + conn.message)

@app.route('/Function_Definition')
def Function_Definition():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('Function_Definition.html')
    
    # return jsonify(data = [num for num in range(10)])

@app.route('/Function_Analysis')
def Function_Analysis():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('Function_Analysis.html')
   


@app.route('/api/<string:class_name>/<string:class_method>/<string:args>', methods = ['GET','POST'])
def api_methods_with_args(class_name,class_method,args):
    module = importlib.import_module('python.model')
    req_class = getattr(module,class_name)
    class_method = getattr(req_class, class_method)
    method_args = [arg for arg in args.split(',')]
    return class_method(*method_args)


@app.route('/api/<string:class_name>/<string:class_method>', methods = ['GET','POST'])
def api_methods_no_args(class_name,class_method):
    # return OctopusUtils.get_all_functions()
    try:
        data = request.get_json()
    except:
        data = None
    # print(data)
    module = importlib.import_module('python.model')
    req_class = getattr(module,class_name)
    class_method = getattr(req_class, class_method)
    if data:
        return class_method(data)
    else:
        return class_method()


@app.route('/api', methods = ['GET','POST'])
def api():
    return jsonify(data = [num for num in range(10)])


if __name__ == "__main__":
    app.run(debug=True)
