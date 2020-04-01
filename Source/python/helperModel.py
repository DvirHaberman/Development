from python.model import *
import math

class Worker:

    def __init__(self, worker_type='analyser'):
        self.worker_type = worker_type
        if worker_type == 'analyser':
            self.thread = Thread(target=Worker.analyser_worker)
            self.thread.start()
    
    @staticmethod
    def analyser_worker():
        global tasks_queue
        global done_queue
        while True:
            if not tasks_queue.empty():
                task, func, time, task_id = tasks_queue.get_nowait()
                # do something - sleep for 0.5 seconds
                sleep(0.5)
                results = func.run_dummy(task.db_conn_string, task.run_id)
                done_queue.put_nowait()
                tasks_queue.task_done()

    def db_writer_worker():
        pass

    def queue_writer_worker():
        global tasks_queue
        while True:
            new_tasks = Task.query.filter_by(status=0)
            if new_tasks():
                [task.push() for task in new_tasks]
                task, func, time, task_id = tasks_queue.get_nowait()
                # do something - sleep for 0.5 seconds
                sleep(0.5)
                results = func.run_dummy(task.db_conn_string, task.run_id)
                done_queue.put_nowait()
                tasks_queue.task_done()



################################################
########### DBCONNECTOR CLASS ###############
################################################

class DbConnector:

    def __init__(self, db_type, schema, user, password, hostname):
        self.db_type = db_type
        self.schema = schema
        self.user = user
        self.password = password
        self.hostname = hostname
        self.connection = None
        if db_type == 'ORACLE':
            self.conn_string =f"oracle+cx_oracle://{self.user}:{self.password}@{self.hostname}/{self.schema}"
        else:
            self.conn_string = None
        
    def connect(self):
        self.connection = create_engine(self.conn_string)


################################################
########### MISSIONHANDLER CLASS ###############
################################################
class MissionHandler():

    def __init__(self, db_connection=None, run_id=None, mission_id=None):
        self.db_connection=db_connection
        self.run_id = run_id
        self.mission_id = mission_id
        self.functions_array = []


    def add_function(self, function_id):
        self.functions_array.append(function_id)

    def remove_function(self, index):
        self.functions_array.pop(index)

    def push_array(self):
        [self.push(function_id) for function_id in self.functions_array]
    
    def push(self, function_id):
        global functions_queue
        func = OctopusFunction.query.get(function_id)




########################################
########### JSONIFIER CLASS ############
########################################


class Jsonifer:

    @staticmethod
    def jsonify_list(list_to_jsonify):
        return jsonify(list_to_jsonify)


############################################
########### DATACOLLECTOR CLASS ############
############################################

class DataCollector():

    def __init__(self, source_file):
        self.file_handler = pd.ExcelFile(source_file)

    def CollectAll(self):
        self.get_projects()
        self.get_teams()
        self.get_roles()
        self.get_users()
        self.get_functions()
        self.get_function_params()
        self.get_tree_names()
        self.get_trees_structures()
        self.get_groups()
        # self.get_trees()
        # db.session.commit()

    def get_functions(self):
        df = pd.read_excel(self.file_handler, 'Functions')
        try:
            for index, row in df.iterrows():
                if not type(row.class_name) == type('str'):
                    if math.isnan(row.class_name):
                        row.class_name=None
                func = OctopusFunction(
                    name=row.func_name,
                    callback=row.callback,
                    file_name = row.file_name,
                    location=row.location,
                    owner=row.owner,
                    status=row.status,
                    # tree=row.tree,
                    kind=row.kind,
                    # tags=row.tags,
                    description=row.description,
                    is_class_method=row.is_class_method,
                    class_name = row.class_name,
                    version=row.version,
                    version_comments=row.version_comments,
                    function_checksum=row.function_checksum,
                    handler_checksum=row.handler_checksum,
                    is_locked=row.is_locked
                )
                db.session.add(func)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the functions table')

    def get_function_params(self):
        df = pd.read_excel(self.file_handler, 'function_parameters')
        try:
            for index, row in df.iterrows():
                param = FunctionParameters(
                    function_id=row.function_id,
                    kind=row.kind,
                    value=row.value,
                    type=row.type
                )
                db.session.add(param)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the function param table')


    def get_projects(self):
        df = pd.read_excel(self.file_handler, 'Projects')
        try:
            for index, row in df.iterrows():
                project = Project(
                    name=row.project_name,
                    version=row.version
                )
                db.session.add(project)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the projects table')

    def get_users(self):
        df = pd.read_excel(self.file_handler, 'Users')
        try:
            for index, row in df.iterrows():
                user = User(
                    name=row.user_name,
                    project=row.project,
                    team=row.team_name,
                    role=row.role_name,
                    state = row.state,
                    max_priority = row.max_priority,
                    password_sha = row.password_sha1,
                    first_name=row.first_name,
                    last_name=row.last_name
                )
                db.session.add(user)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the users table')


    def get_teams(self):
        df = pd.read_excel(self.file_handler, 'Teams')
        try:
            for index, row in df.iterrows():
                team = Team(
                    name=row.team_name,
                )
                db.session.add(team)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the team table')


    def get_roles(self):
        df = pd.read_excel(self.file_handler, 'Roles')
        try:
            for index, row in df.iterrows():
                role = Role(
                    name=row.role_name,
                )
                db.session.add(role)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the role table')
    
    def get_tree_names(self):
        df = pd.read_excel(self.file_handler, 'Trees')
        try:
            for index, row in df.iterrows():
                tree = Trees(
                    name = row.name,
                    function = row.function,
                    # nodes = row.nodes
                )
                db.session.add(tree)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the Trees table')
    
    def get_trees_structures(self):
        df = pd.read_excel(self.file_handler, 'TreeStructre')
        try:
            for index, row in df.iterrows():
                structure = TreeStructre(
                    tree_id = row.tree_id,
                    node_id = row.node_id,
                    node_name = row.node_name,
                    node_data = row.node_data,
                    parent = row.parent
                )
                db.session.add(structure)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the TreeStructure table')

    def get_groups(self):
        df = pd.read_excel(self.file_handler, 'Groups')
        try:
            for index, row in df.iterrows():
                group = FunctionsGroup(
                    name = row.group_name
                )
                db.session.add(group)
            db.session.commit()
            group1 = FunctionsGroup.query.get(1)
            group2 = FunctionsGroup.query.get(2)
            func1 = OctopusFunction.query.get(1)
            func2 = OctopusFunction.query.get(2)
            func3 = OctopusFunction.query.get(3)
            func4 = OctopusFunction.query.get(4)
            group1.functions.append(func1)
            group1.functions.append(func2)
            group2.functions.append(func3)
            group2.functions.append(func4)
            db.session.commit()
        except():
            print(
                'problem in DataCollector - something went wrong with creating the Trees table')