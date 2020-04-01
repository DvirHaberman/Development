# from python.model import *
from python.helperModel import *
import os

# app = create_app()
app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///OctopusDB.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dvirh@localhost:5432/OctopusDB"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append('C' + basedir[1:-7] + '\\Functions')
sys.path.append('C' + basedir[1:-7] + '\\Infras\\Fetches')
sys.path.append('C' + basedir[1:-7] + '\\Infras\\Utils')

@app.route('/create_all')
def create_tables():
    db.create_all()
    return 'done'


@app.route('/collect_all')
def collect_data():
    collector = DataCollector(basedir + r"\..\Data\DataToCollect.xlsx")
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

@app.route('/run_functions')#, methods=['POST'])
def run_functions():
    # json_data = request.get_json()
    json_data = {'functions':[1,3,5],'runs':[1122,1122,3344], 'db_name':'db_name'}
    functions = db.session.query(OctopusFunction).filter(OctopusFunction.id.in_( json_data['functions'])).all()
    runs = json_data['runs']
    conn = OctopusUtils.get_db_conn(json_data['db_name'])
    result_arr = []
    for run in runs:
        for func in functions:
            data = func.run(conn,run)
            print(data)
            result_arr.append({'db_name':json_data['db_name'], 'run_id':run, 'function':func.name, 'function_id':func.id, 'result':data})
    return jsonify(result_arr)


@app.route('/')
def index():
    return render_template('Function_Definition.html')

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
