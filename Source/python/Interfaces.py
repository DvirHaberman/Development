# from .model import *
from .Enums import GenerateStageTypes, GenerateStatus
from .Model.GenerateMission import *

class Result():
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

class RunMissionInterface():
    
    @staticmethod
    def handle_mission_request(json_data, generate_requests_queue, run_requests_queue):
        def validate_request_data(json_data):
            try:
                #check that all fields exist in the recieved data
                expected_keys = ['run_needed', 'generate_needed', 'request_content']
                missing_keys = list(filter(lambda x: x not in json_data.keys(), expected_keys))
                if missing_keys:
                    return Result(
                                412,
                                "The keys: "+','.join(missing_keys) + " are missing",
                                None
                                )
                #return 200 if all is validated
                return Result(
                            200,
                            "valid",
                            None
                            )
            except Exception as error:
                return Result(
                            500, 
                            'Server error while validating request data',
                            None
                            )

        
        #validate recieved data and return 416 error code if something is invalid
        result = validate_request_data(json_data)
        if result.status >= 300:
            return result

        #check if generation of scenario is needed
        gen_mission = None
        project_id = session['current_project_id']
        result = create_generate_mission(json_data) if int(json_data['generate_needed']) == 1 else None
        if result:
            if result.status >=300:
                return result
            gen_mission = result.data

        #check if run mission is needed
        run_mission = None
        result = create_run_mission(json_data) if int(json_data['run_needed']) == 1 else None
        if result:
            if result.status >=300:
                return result
            run_mission = result.data

        #create request
        gen_mission_id = gen_mission.id if gen_mission else None
        run_mission_id = run_mission.id if run_mission else None
        requests = json_data['request_content']
        i=0
        k=0
        for request in requests:
            request.update({"gen_mission_id":gen_mission_id, "run_mission_id":run_mission_id,
                            "project_id":project_id})
            if int(request['to_generate']) == 1:
                i=i+1
                print(f"pushed gen request {i}")
                if request['to_run'] == 0:
                    request['run_mission_id'] = None
                db.session.close()
                generate_requests_queue.put_nowait(request)
            else:
                k=k+1
                print(f"pushed run request {k}")
                request.update({"generate_status_id":None, "gen_mission_id":None})
                run_requests_queue.put_nowait(request)
        return Result(200,'Mission created', {"gen_mission_id":gen_mission_id,"run_mission_id":run_mission_id})

    @staticmethod
    def log_request(run_request):
        try:
            
            if "stage_id" in run_request:
                stage_id = run_request['stage_id']
            else:
                stage_name = run_request['stage_name']
                stage = StageRunMani.query.filter_by(name=stage_name,
                                                project_id=run_request['project_id']).first()
                if not stage:
                    return Result(
                                404, 
                                "stage with name " + stage_name + " was not found",
                                None
                                )
                stage_id = stage.id
            run_status = RunMissionStatus(
                stage_id=stage_id,
                generate_mission_id=run_request['gen_mission_id'],
                generate_status_id=run_request['generate_status_id'],
                delete_after=run_request['run_delete_after'],
                updated_time=datetime.utcnow(),
                run_mission_id=run_request['run_mission_id'],
                priority=run_request['priority']
            )
            return Result(200, None, run_status)
        except:
            return Result(500, 'error creating the run request', None)

    @staticmethod
    def execute_request(run_status):
        try:
            # run_status = RunMissionStatus(
                
            # )
            print(f'run mission status: {run_status.id} executed!')
            return Result(200, None, "blaaa")
        except:
            return Result(500, 'error creating the run request', None)
            
def create_generate_mission(json_data):
    project_id = session['current_project_id']
    user_id = User.query.filter_by(name=session['username']).first().id
    try:
        #log a generate_mission in OctopusDb
        gen_mission = GenerateMission(
                                    created_by=user_id,
                                    created_time=datetime.utcnow(),
                                    project_id=project_id,
                                    gen_stages=[]
                                    )
        db.session.add(gen_mission)
        db.session.commit()
        return Result(200, None, gen_mission)
    except:
        db.session.rollback()
        return Result(500, 'error creating the GenerateMission object', None)

def create_run_mission(json_data):
    #check that the requested stage exists
    project_id = session['current_project_id']
    user_id = User.query.filter_by(name=session['username']).first().id

    try:
        #log a generate_mission in OctopusDb
        run_mission = RunMission(
                    name = session['username'],
                    created_by=user_id,
                    project_id=project_id,
                    run_stages = [],
                    created_time = datetime.utcnow()
                    )
        db.session.add(run_mission)
        db.session.commit()
        return Result(200, None, run_mission)
    except:
        db.session.rollback()
        return Result(500, 'error creating the RunMission object', None)
    


class GenerateMissionInterface():
    
    @staticmethod
    def log_request(gen_request):

        # validating the data             
        result = GenerateMissionInterface.validate_gen_request(gen_request)
        if result.status >=300:
            return result
        
        # initialize variables
        run_mission_id = int(gen_request['run_mission_id']) if gen_request['run_mission_id'] else None
        gen_mission_id = int(gen_request['gen_mission_id'])
        stage_name = gen_request['stage_name']
        ext_events_folder = gen_request['ext_events_folder']
        
        results = []
        statistics = {"failed": 0, "succeeded": 0}

        #get the gen project_id from the gen mission
        gen_mission = GenerateMission.query.get(gen_mission_id)
        if not gen_mission:
            return Result(404, 'No gen mission was found with id:' + str(gen_mission_id), None)
        project_id = gen_mission.project_id

        # check that the stage exists - if not then return error
        stage = StageRunMani.query.filter_by(name=stage_name,project_id=project_id).first()
        if not stage:
            result=Result(
                        404, 
                        "stage with name " + stage_name + " was not found",
                        None
                        )
        
        #update the request with the stage id
        gen_request.update({"stage_id":stage.id})

        #if path ext_events_folder exists, generate the mission status
        if Path(ext_events_folder).exists():
            #get all sub-folders if request asks for all of them
            if int(gen_request['is_generate_subfolders']) > 0:
                folders = list(set(get_subfolders(ext_events_folder,'').split(',')))
            else:
                folders = [ext_events_folder]
            #for every folder requests, create the mission status row
            for folder in folders:
                result = GenerateMissionInterface.generate_mission_status(gen_request)
                results.append(result)
                if result.status >= 300:
                    statistics['failed'] += 1
                else:
                    statistics['succeeded'] += 1
        else:
            result = Result(416, f'external events folder: {ext_events_folder} was not found',None)
            statistics['failed'] += 1
            results.append(result)
        return Result(200,None,{"results":results, "statistics":statistics})
    
    @staticmethod
    def execute_request(gen_status):
        stage_id = gen_status.stage_id
        stage = StageRunMani.query.get(stage_id)
        if not stage:
            return Result(
                        404, 
                        "stage with name " + stage.name + " was not found",
                        None
                        )
        return Result(200, None, {"generate_status_id" : gen_status.id,
                                  "gen_process":{
                                        "is_validated":{
                                                "failed":1, "succeeded":2, "total":3,
                                                "stage_type": GenerateStageTypes.VALIDATING, "status": GenerateStatus.PARTIAL_SUCCESS
                                                },
                                        "is_in_db":{
                                                "failed":1, "succeeded":2, "total":3, 
                                                "stage_type": GenerateStageTypes.DB_INSERT, "status": GenerateStatus.PARTIAL_SUCCESS
                                                },
                                        "is_generated":{
                                                "failed":1, "succeeded":1, "total":1,
                                                "stage_type": GenerateStageTypes.GENERATE, "status": GenerateStatus.SUCCESS
                                                },
                                        }
                                 }
                    )
    @staticmethod
    def generate_mission_status(gen_request):
        try:
            stage_id = gen_request['stage_id']
            run_mission_id = gen_request['run_mission_id']
            priority = int(gen_request['priority'])
            ext_events_folder = gen_request['ext_events_folder']
            is_generate_subfolders = int(gen_request['is_generate_subfolders'])
            generate_mission_id = gen_request['gen_mission_id']
            is_validated = None
            is_in_db = None
            is_generated = None
            statistics = []
            delete_after = int(gen_request['gen_delete_after'])
            updated_time = datetime.utcnow()

            gen_status = GenerateMissionStatus(
                                        stage_id=stage_id,
                                        run_mission_id=run_mission_id,
                                        ext_events_folder=ext_events_folder,
                                        is_generate_subfolders=is_generate_subfolders,
                                        generate_mission_id=generate_mission_id,
                                        is_validated=is_validated,
                                        is_in_db=is_in_db,
                                        is_generated=is_generated,
                                        statistics=statistics,
                                        delete_after=delete_after,
                                        updated_time=updated_time,
                                        priority=priority
                                        )     
            db.session.add(gen_status)  
            return Result(200, None, gen_status)
        except Exception as error:
            return Result(
                        500, 
                        'Server error while creating gen mission status for mission id:' + str(gen_mission_id),
                        None
                        )
    @staticmethod
    def validate_gen_request(gen_request):
        try:
            
            expected_keys = [
                        "number",
                        "to_run",
                        "to_generate",
                        "stage_name",
                        "ext_events_folder",
                        "gen_delete_after",
                        "run_delete_after",
                        "is_generate_subfolders",
                        "priority"
                        ]
            missing_keys = list(filter(lambda x: x not in gen_request.keys(), expected_keys))
            if missing_keys:
                error_string = f'The keys: {",".join(missing_keys)} are missing in gen_request{str(gen_request["number"])}' \
                        if "number" in gen_request else \
                        f'The keys: {",".join(missing_keys)} are missing'
                return Result(
                            412,
                            error_string,
                            None
                            )
            return Result(200, "valid", None)
        except:
            error_string = f'error while validating gen_request{str(gen_request["number"])}' \
                        if "number" in gen_request else \
                        f'error while validating gen_request'
            return Result(500, error_string, None)

def get_subfolders(basedir,folders):
    folders += ',' + basedir if len(folders) > 0 else basedir
    if not [f for f in listdir(basedir) if not isfile(basedir + sep + f)]:
        return folders
    return ','.join([get_subfolders(basedir+sep+f, folders) for f in listdir(basedir) if not isfile(basedir + sep + f)])

