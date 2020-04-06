# from python.model import *
from python.helperModel import *
import os

# app = create_app()
app = Flask(__name__)
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

@app.route('/run_functions_test')
def run_functions_test():
    functions = OctopusFunction.query.all()
    result_arr = []
    for func in functions:
        data = func.run('conn','run_id')
        print(data)
        result_arr.append(data)
    return jsonify(result_arr)

@app.route('/api/run_functions', methods=['POST'])
def run_functions():
    json_data = request.get_json()
    # json_data = {'functions':[1,2,3,4,5],'runs':[1122,1122,3344], 'db_name':'db_name'}
    if not type(json_data['functions']) == type(list()):
        json_data['functions'] = [json_data['functions']]
    functions = db.session.query(OctopusFunction).filter(OctopusFunction.id.in_( json_data['functions'])).all()
    names = [func.name for func in functions]
    runs = json_data['runs']
    if not type(runs) == type(list()):
        runs = [runs]
    conn = DbConnector(json_data['db_name'], 'postgres', 'dvirh', 'localhost', '5432', 'octopusdb')
    result_arr = []
    result_arr2 = []
    for run in runs:
        for func in functions:
            data = func.run(conn,run)
            result_arr.append({'db_name':json_data['db_name'], 'run_id':run, 'function':func.name, 'function_id':func.id, 'result':data})
            result_arr2.append(data)
    overview = OverView(mission_id=10, results=result_arr2)
    return jsonify({'runs':runs, 'function_names':names, 'results':result_arr})


@app.route('/')
def index():
    return render_template('Function_Definition.html')

@app.route('/run_simple')
def run_simple():
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
    return render_template('db_conn_wizard.html')

@app.route('/api/get_conn_data')
def get_conn_data():
    connections = DbConnections.query.all()
    return jsonify([conn.self_jsonify() for conn in connections])

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
        return jsonify(status=0, message='Failed saving the connection!')

@app.route('/Function_Definition')
def Function_Definition():
    return render_template('Function_Definition.html')
    # return jsonify(data = [num for num in range(10)])

@app.route('/Function_Analysis')
def Function_Analysis():
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
