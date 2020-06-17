from python.model import *
import math


############################################
########### DATACOLLECTOR CLASS ############
############################################

class DataCollector():

    def __init__(self, mockup_db_file_path):
        self.mockup_db_file_handler = pd.ExcelFile(mockup_db_file_path)
        # self.test_params_file_handler = pd.ExcelFile(tests_params_file_path)

    @staticmethod
    def get_tests_params(tests_params_file_path):
        try:
            return pd.read_excel(pd.ExcelFile(tests_params_file_path), 'Tests_Params')
        except:
            return None
    
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
        df = pd.read_excel(self.mockup_db_file_handler, 'Functions')
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
        except:
            print(
                'problem in DataCollector - something went wrong with creating the functions table')
        finally:
            db.session.close()
        
    def get_function_params(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'function_parameters')
        try:
            for index, row in df.iterrows():
                param = FunctionParameters(
                    function_id=row.function_id,
                    index = row.param_index,
                    kind=row.kind,
                    value=row.value,
                    param_type=row.type
                )
                db.session.add(param)
            db.session.commit()
        except:
            print(
                'problem in DataCollector - something went wrong with creating the function param table')
        finally:
            db.session.close()

    def get_projects(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Projects')
        try:
            for index, row in df.iterrows():
                project = Project(
                    name=row.project_name,
                    output_dir=row.output_dir
                    # version=row.version
                )
                db.session.add(project)
            db.session.commit()
        except:
            print(
                'problem in DataCollector - something went wrong with creating the projects table')
        finally:
            db.session.close()
        
    def get_users(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Users')
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
        except:
            print(
                'problem in DataCollector - something went wrong with creating the users table')
        finally:
            db.session.close()

    def get_teams(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Teams')
        try:
            for index, row in df.iterrows():
                team = Team(
                    name=row.team_name
                )
                db.session.add(team)
            db.session.commit()
        except:
            print(
                'problem in DataCollector - something went wrong with creating the team table')
        finally:
            db.session.close()

    def get_roles(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Roles')
        try:
            for index, row in df.iterrows():
                role = Role(
                    name=row.role_name
                )
                db.session.add(role)
            db.session.commit()
        except:
            print(
                'problem in DataCollector - something went wrong with creating the role table')
        finally:
            db.session.close()
        
    def get_tree_names(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Trees')
        try:
            for index, row in df.iterrows():
                tree = Trees(
                    name = row.name,
                    function = row.function
                    # nodes = row.nodes
                )
                db.session.add(tree)
            db.session.commit()
        except:
            print(
                'problem in DataCollector - something went wrong with creating the Trees table')
        finally:
            db.session.close()
        
    def get_trees_structures(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'TreeStructre')
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
        finally:
            db.session.close()
            
    def get_groups(self):
        df = pd.read_excel(self.mockup_db_file_handler, 'Groups')
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
        finally:
            db.session.close()