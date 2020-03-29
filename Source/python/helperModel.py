from python.model import *
###########################################
########### OCTOPUSUTILS CLASS ############
###########################################


class OctopusUtils:

    @staticmethod
    def get_all_functions():
        functions = OctopusFunction.query.all()
        # owner_id = functions[0].owner
        # owner = User.query.get(owner_id).name
        # , owners=owner)
        return jsonify(names=[func.name for func in functions])


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
        self.get_functions()
        self.get_function_params()
        self.get_projects()
        self.get_users()
        self.get_teams()
        self.get_roles()
        self.get_tree_names()
        self.get_trees_structures()

        # self.get_trees()

    def get_functions(self):
        df = pd.read_excel(self.file_handler, 'Functions')
        try:
            for index, row in df.iterrows():
                func = OctopusFunction(
                    name=row.func_name,
                    callback=row.callback,
                    location=row.location,
                    owner=row.owner,
                    status=row.status,
                    # tree=row.tree,
                    kind=row.kind,
                    tags=row.tags,
                    description=row.description,
                    # project=row.project,
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
                    function = row.function
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
