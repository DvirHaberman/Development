# from python.model import *
from python.helperModel import *
import importlib

# app = create_app()
app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///OctopusDB.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dvirh@localhost:5432/OctopusDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/create_all')
def create_db():
    db.create_all()
    collector = DataCollector(r"C:\Git_Rep\Development\Data\DataToCollect.xlsx")
    collector.CollectAll()
    # userfound = User.query.all()
    return 'done'


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
