from python.DataCollector import DataCollector
from python.model import *
from threading import Thread
from multiprocessing import Queue, Event, freeze_support
from python.processes_workers import Worker, init_processes, create_pipes, send_data_to_workers
import os

app = Flask(__name__)
app.secret_key = os.environ.get('PYTHON_SECRET_KEY')
# app.permanent_session_lifetime = timedelta(minutes=int(os.environ.get('SESSION_LIFETIME')))
db.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///OctopusDB.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dvirh@localhost:5432/OctopusDB"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:MySQLPass@localhost:3306/octopusdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

num_of_analyser_workers = 1

pipes_dict = create_pipes(num_of_analyser_workers)

run_or_stop_flag = Event()

run_or_stop_flag.set()

processes_dict = {}
queue_dict = {}
tasks_queue = Queue()
error_queue = Queue()
updates_queue = Queue()
to_do_queue = Queue()
done_queue = Queue()

basedir = os.path.abspath(os.path.dirname(__file__))

if sys.platform.startswith('win'):
    tests_params = DataCollector.get_tests_params(basedir + r"\..\Data\Tests_Params.xlsx")
else:
    tests_params = DataCollector.get_tests_params(basedir + r"/../Data/Tests_Params.xlsx")

send_data_to_workers(tests_params, pipes_dict, num_of_analyser_workers)

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

# init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
#             tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, pipes_dict)

sleep(3)

# update_tests_params()

@app.route('/api/create_all')
def create_tables():
    db.create_all()
    # redirect('/api/collect_data')
    return 'done'

@app.route('/user_wizard')
def user_wizard():
    if session.get('username', None) is None:
        return redirect('/login_first')
    elif not session['userrole'] == 'Admin':
        return redirect('/whoops')
    else:
        session['current_window_name'] = 'Define Users'
        return render_template('user_wizard.html')

@app.route('/whoops')
def whoops():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('whoops.html')


@app.route('/display_results')
def display_results():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        return render_template('display_results.html')

@app.route('/api/start_processes')
def start_processes():
    try:
        if not run_or_stop_flag.is_set():
            if sys.platform.startswith('win'):
                tests_params = DataCollector.get_tests_params(basedir + r"\..\Data\Tests_Params.xlsx")
            else:
                tests_params = DataCollector.get_tests_params(basedir + r"/../Data/Tests_Params.xlsx")

            send_data_to_workers(tests_params, pipes_dict, num_of_analyser_workers)
            run_or_stop_flag.set()
            init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
                tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, pipes_dict)

            return jsonify(status=True, message = '')
        else:
            return jsonify(status=False, message = 'processes are already running')
    except:
        return jsonify(status=False, message = 'technical failure')

@app.route('/api/stop_processes')
def stop_processes():
    try:
        run_or_stop_flag.clear()
        return jsonify(status=True, message = '')
    except:
        return jsonify(status=False, message = 'technical failure')

@app.route('/api/collect_all')
def collect_data():
    if sys.platform.startswith('win'):
        collector = DataCollector(basedir + r"\..\Data\DataToCollect.xlsx")
    else:
        collector = DataCollector(basedir + r"/../Data/DataToCollect.xlsx")
    # collector.CollectAll()
    collector.get_projects()
    collector.get_teams()
    collector.get_roles()
    collector.get_users()
    collector.get_functions()
    collector.get_function_params()
    collector.get_tree_names()
    collector.get_trees_structures()
    collector.get_groups()
    return 'done'

@app.route('/init_workers', methods=['GET','POST'])
def init_workers():
    processes_dict = init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
                 tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, update_event, pipes_dict)
    # t=Thread(target=threaded_app)
    # t.start()
    # threaded_app(db)
        # p=Process(target=init_proccesses)
        # p.start()
    return 'done'

@app.route('/api/update_tests_params', methods=['GET','POST'])
def update_tests_params():
    if sys.platform.startswith('win'):
        tests_params = DataCollector.get_tests_params(basedir + r"\..\Data\Tests_Params.xlsx")
    else:
        tests_params = DataCollector.get_tests_params(basedir + r"/../Data/Tests_Params.xlsx")

    send_data_to_workers(tests_params, pipes_dict, num_of_analyser_workers)

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
    json_input = request.get_json()
    user_id = User.query.filter_by(name=session['username']).first().id
    mission_name = 'mission_' + session['username']
    function_names = json_input['functions'].split(',')
    functions_ids = db.session.query(OctopusFunction).filter(OctopusFunction.name.in_( function_names)).with_entities(OctopusFunction.id).all()
    functions_ids = list(*zip(*functions_ids))
    runs = json_input['runs'].split(',')
    db_name = json_input['db_name']
    db_id = DbConnections.query.filter_by(name=db_name).first().id
    json_data = {'user_id':user_id,'mission_name':mission_name,
                'functions':functions_ids,'runs':runs,
                 'conn_id':db_id, 'db_name':db_name}
    try:
        return jsonify(Mission.create_mission(json_data,tasks_queue))
        # return 'done'
    except:
        return 'something went wrong'

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login_first')
def login_first():
    session['current_window_name'] = 'Login First'
    return render_template('login_first.html')

@app.route('/login')
def login():
    if session.get('username', None) is None:
        session['current_window_name'] = 'Login'
        return render_template('login.html')
    else:
        return redirect('/welcome')

@app.route('/run_function')
def run_function():
    if session.get('username', None) is None:
        return redirect('/login')
    else:
        session['current_window_name'] = 'Run Functions'
        return render_template('run_function.html')

@app.route('/welcome')
def welcome():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Welcome'
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
            session['userrole'] = Role.query.get(user.role).name
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
        session['current_window_name'] = 'Run Functions'
        return render_template('run_simple.html')

@app.route('/define_process')
def define_process():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Define Process'
        return render_template('define_process.html')

@app.route('/run_stage_define')
def run_stage_define():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Define Stage'
        return render_template('run_stage_definition.html')


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
    # session['username'] = 'dvirh'
    # session['password'] = 'dvirh'
    if session.get('username', None) is None:
        return redirect('/login_first')
    elif not session['userrole'] == 'Admin':
        return redirect('/whoops')
    else:
        session['current_window_name'] = 'Define Connections'
        return render_template('db_conn_wizard.html')

@app.route('/api/get_conn_data')
def get_conn_data():
    connections = DbConnections.query.all()
    return jsonify([conn.self_jsonify() for conn in connections])

@app.route('/api/delete_conn_by_name/<string:conn_name>', methods=["POST"])
def delete_connection(conn_name):
    conn_to_delete = DbConnections.query.filter_by(name=conn_name).first()
    if conn_to_delete:
        try:
            db.session.delete(conn_to_delete)
            db.session.commit()
            return jsonify(status=1,msg=conn_name +' was deleted')
        except Exception as error:
            return jsonify(status=0,msg='something went wrong while deleting ' +conn_name)
    return jsonify(status=0,msg='connectiong name not found')

@app.route('/api/save_connection', methods = ['POST'])
def save_connection():
    data = request.get_json()
    conn = DbConnector(db_type=data['db_type'], user=data['user'], password=data['password'],
                hostname=data['hostname'], port=data['port'], schema=data['schema'], name=data['name'])
    conn.save()
    if conn.status == 'valid':
        connections = DbConnections.query.all()
        conn_data = [conn.self_jsonify() for conn in connections]
        return jsonify(status = 1, msg='connection successfuly saved!', connections=conn_data)
    else:
        return jsonify(status=0, msg='Failed saving the connection!\n' + conn.message)

@app.route('/Function_Definition')
def Function_Definition():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Define Functions'
        return render_template('Function_Definition.html')

    # return jsonify(data = [num for num in range(10)])

@app.route('/Function_Analysis')
def Function_Analysis():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Analysis Results'
        return render_template('Function_Analysis.html')



@app.route('/api/<string:class_name>/<string:class_method>/<string:args>', methods = ['GET','POST'])
def api_methods_with_args(class_name,class_method,args):
    module = importlib.import_module('python.model')
    req_class = getattr(module,class_name)
    class_method = getattr(req_class, class_method)
    method_args = [arg for arg in args.split(',')]
    if type(method_args) == type([1]):
        return class_method(*method_args)
    else:
        return class_method(method_args)


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
    freeze_support()
    app.run(debug=True)
    init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
                tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, pipes_dict)
