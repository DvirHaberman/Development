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

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb4"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
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

@app.route('/define_function')
def define_function():
    session['current_window_name'] = 'Define Function'
    return render_template('define_func.html')

@app.route('/test_worker')
def test_worker():
    return render_template('worker.html')

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
    # collector.get_projects()
    collector.get_teams()
    collector.get_roles()
    collector.get_users()
    # collector.get_functions()
    # collector.get_function_params()
    # collector.get_tree_names()
    # collector.get_trees_structures()
    # collector.get_groups()
    return 'done'

# @app.route('/init_workers', methods=['GET','POST'])
# def init_workers():
#     processes_dict = init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
#                  tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, update_event, pipes_dict)
#     # t=Thread(target=threaded_app)
#     # t.start()
#     # threaded_app(db)
#         # p=Process(target=init_proccesses)
#         # p.start()
#     return 'done'

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
    function_names = json_input['functions']
    groups_names = json_input['groups']
    additional_names = []
    for group_name in groups_names:
        group = FunctionsGroup.query.filter_by(name=group_name,project=session['current_project_id']).first()
        additional_names = additional_names + [func.name for func in group.functions]
    function_names = list(set(function_names + additional_names))
    functions_ids = db.session.query(OctopusFunction).filter(OctopusFunction.name.in_( function_names)).with_entities(OctopusFunction.id).all()
    functions_ids = list(*zip(*functions_ids))
    runs = json_input['runs']
    # db_name = json_input['db_name']
    # db_id = DbConnections.query.filter_by(name=db_name,project=session['current_project_id']).first().id
    json_data = {'user_id':user_id,'mission_name':mission_name,
                'functions':functions_ids,'runs':runs}
    try:
        return jsonify(Mission.create_mission(json_data,tasks_queue))
        # return 'done'
    except:
        return 'something went wrong'

@app.route('/api/run_setup/<string:setup_name>')
def run_setup(setup_name):
    try:
        setup = AnalyseSetup.query.filter_by(name=setup_name,project=session['current_project_id']).first()
        if not setup:
            return jsonify(status=0, message = ['no setup with this name'], data=None)
        result = setup.create_mission(tasks_queue)
        if result['status']:
            return jsonify(status=1, message = result['message'], data=None)
        else:
            return jsonify(status=0, message = 'something went wrong', data=None)
    except Exception as error:
        db.session.rollback()
    finally:
        db.session.close()

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
            session['projects'] = [project.name for project in user.projects]
            if session['projects']:
                session['current_project'] = session['projects'][0]
                session['current_project_id'] = Project.query.filter_by(name=session['current_project']).first().id

            else:
                session['current_project'] = None
                session['current_project_id'] = None

            return redirect('/welcome')
        else:
            flash('Invalid username or password!')
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/change_project/<int:index>')
def change_project(index):
    session['current_project'] = session['projects'][index-1]
    session['current_project_id'] = Project.query.filter_by(name=session['current_project']).first().id
    if session['current_window_name'] == 'Run Functions':
        return redirect('/run_simple')

    if  session['current_window_name'] == 'Welcome':
        return redirect('/welcome')

    if session['current_window_name'] == 'Define Process':
        return redirect('/define_process')

    if session['current_window_name'] == 'Define Stage':
        return redirect('/run_stage_define')

    if session['current_window_name'] == 'Run Functions':
        return redirect('/run_function')

    if session['current_window_name'] == 'Define Complex Net':
        return redirect('/define_complex_net')

    if session['current_window_name'] == 'Infras':
        return redirect('/infras')

    if session['current_window_name'] == 'Define Connections':
        return redirect('/db_conn_wizard')

    if session['current_window_name'] == 'Define Functions':
        return redirect('/Function_Definition')

    if session['current_window_name'] == 'Define Users':
        return redirect('/user_wizard')


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

@app.route('/define_complex_net')
def define_complex_net():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Define Complex Net'
        return render_template('define_complex_net.html')

@app.route('/infras')
def infras():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'Infras'
        return render_template('infras.html')


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
    connections = DbConnections.query.filter_by(project=session['current_project_id']).all()
    return jsonify([conn.self_jsonify() for conn in connections])

@app.route('/api/delete_conn_by_name/<string:conn_name>', methods=["POST"])
def delete_connection(conn_name):
    conn_to_delete = DbConnections.query.filter_by(name=conn_name,project=session['current_project_id']).first()
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
    try:
        data = request.get_json()
        conn = DbConnector(db_type=data['db_type'], user=data['user'], password=data['password'],
                    hostname=data['hostname'], port=data['port'], schema=data['schema'],
                    name=data['name'])
        conn.save()
        if conn.status == 'valid':
            connections = DbConnections.query.filter_by(project=session['current_project_id']).all()
            conn_data = [conn.self_jsonify() for conn in connections]
            return jsonify(status = 1, msg='connection successfuly saved!', connections=conn_data)
        else:
            return jsonify(status=0, msg='Failed saving the connection!\n' + conn.message)
    except:
        return jsonify(status=0, msg='Failed saving the connection!')
    finally:
        db.session.close()

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

@app.route('/new_analyse')
def new_analyse():
    if session.get('username', None) is None:
        return redirect('/login_first')
    else:
        session['current_window_name'] = 'new_analyse'
        return render_template('new_analyse.html')



@app.route('/api/<string:class_name>/<string:class_method>/<string:args>', methods = ['GET','POST'])
def api_methods_with_args(class_name,class_method,args):
    try:
        data = request.get_json()
    except:
        data = None
    try:
        module = importlib.import_module('python.model')
        req_class = getattr(module,class_name)
        class_method = getattr(req_class, class_method)
        method_args = [arg for arg in args.split(',')]
        if type(method_args) == type([1]):
            if data:
                output = class_method(*method_args, data)
            else:
                output = class_method(*method_args)
        else:
            if data:
                output = class_method(method_args, data)
            else:
                output = class_method(method_args)
        return output
    except Exception as error:
        return jsonify(status=0, message='something went wrong')
    finally:
        db.session.close()

@app.route('/api/<string:class_name>/<string:class_method>', methods = ['GET','POST'])
def api_methods_no_args(class_name,class_method):
    # return OctopusUtils.get_all_functions()
    try:
        data = request.get_json()
    except:
        data = None
    # print(data)
    try:
        module = importlib.import_module('python.model')
        req_class = getattr(module,class_name)
        class_method = getattr(req_class, class_method)
        if data:
            output = class_method(data)
        else:
            output = class_method()
        return output
    except Exception as error:
        return jsonify(status=0, message='something went wrong')
    finally:
        db.session.close()



if __name__ == "__main__":
    freeze_support()
    app.run(debug=True)
    init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
                tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, pipes_dict)
