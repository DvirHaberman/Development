from .model import *
# from .Enums import RunTypes
class ReuqestTypes:
    RUN = 'RUN'
    generate = 'GENERATE'
class Result():
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

class RunMissionInterface():
    
    @staticmethod
    def handle_mission_request(json_data, generate_requests_queue, run_requests_queue):
        #validate recieved data and return 416 error code if something is invalid
        result = validate_request_data(json_data)
        if result.status >= 300:
            return result

        #check if generation of scenario is needed
        gen_mission = None
        result = create_generate_mission(json_data) if int(json_data['is_generated']) == 1 else None
        if result:
            if result.status >=300:
                return result
            gen_mission = result.data

        #check if run mission is needed
        run_mission = None
        result = create_run_mission(json_data) if json_data['request_type'] == ReuqestTypes.RUN else None
        if result:
            if result.status >=300:
                return result
            run_mission = result.data

        #create request
        gen_mission_id = gen_mission.id if gen_mission else None
        run_mission_id = run_mission.id if run_mission else None
        if int(json_data['is_generated']) == 1:
            result = create_gen_request(json_data, gen_mission_id, run_mission_id)
            if result.status >=300:
                return result
            gen_request = result.data
            generate_requests_queue.put_nowait(gen_request)
        else:
            result = create_run_request(json_data, gen_mission_id, run_mission_id)
            if result.status >=300:
                return result
            run_request = result.data
            run_requests_queue.put_nowait(run_request)
        return Result(200,'Mission created', {"gen_mission_id":gen_mission_id,"run_mission_id":run_mission_id})
def create_gen_request(json_data, gen_mission_id, run_mission_id):
    try:
        
        gen_request = {
                        "gen_mission_id":gen_mission_id,
                        "run_mission_id":run_mission_id,
                        "request_type":json_data['request_type']
                      }
        return Result(200, None, gen_request)
    except:
        return Result(500, 'error creating the generation request', None)

def create_run_request(json_data, gen_mission_id, run_mission_id):
    try:
      
        run_request = {
                        "gen_mission_id":gen_mission_id,
                        "run_mission_id":run_mission_id,
                        "request_type":json_data['request_type']
                      }
        return Result(200, None, run_request)
    except:
        return Result(500, 'error creating the run request', None)
            
def create_generate_mission(json_data):
    project_id = session['current_project_id']
    user_id = User.query.filter_by(name=session['username']).first().id
    stage_name = json_data['stage_name']
    stage = StageRunMani.query.filter_by(name=stage_name, project_id=project_id).first()
    
    try:
        #log a generate_mission in OctopusDb
        gen_mission = GenerateMission(
                                    source_scenario=stage.scenario_file,
                                    ext_events_folder=json_data['events_folder'],
                                    is_generate_subfolders = json_data['is_generate_subfolders'],
                                    created_by=user_id,
                                    created_time=datetime.utcnow(),
                                    project_id=project_id,
                                    run_stages=[]
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
    stage_name = json_data['stage_name']
    user_id = User.query.filter_by(name=session['username']).first().id
    stage = StageRunMani.query.filter_by(name=stage_name, project_id=project_id).first()

    try:
        #log a generate_mission in OctopusDb
        run_mission = RunMission(
                    name = stage_name+session['username'],
                    created_by=user_id,
                    project_id=project_id,
                    run_stages = [],
                    priority = json_data['priority'],
                    created_time = datetime.utcnow()
                    )
        db.session.add(run_mission)
        db.session.commit()
        return Result(200, None, run_mission)
    except:
        db.session.rollback()
        return Result(500, 'error creating the RunMission object', None)
    
def validate_request_data(json_data):
    try:
        #check that all fields exist in the recieved data
        expected_keys = ['request_type', 'stage_name', 'is_generated', 'events_folder', 'is_generate_subfolders', 'priority']
        missing_keys = list(filter(lambda x: x not in json_data.keys(), expected_keys))
        if missing_keys:
            return Result(
                        412,
                        "The keys: "+','.join(missing_keys) + " are missing",
                        None
                        )
        #check that the request type is valid
        request_type = json_data['request_type']
        if request_type not in ['RUN', 'GENERATE']:
            return Result(
                        412,
                        "request type must be 'RUN' or 'GENERATE'",
                        None
                        )
        
        #check that the requested stage exists
        project_id = session['current_project_id']
        stage_name = json_data['stage_name']
        stage = StageRunMani.query.filter_by(name=stage_name, project_id=project_id).first()
        if not stage:
            return Result(
                        404,
                        "Stage with the name "+ stage_name + " was not found",
                        None
                        )
        #return 200 if all is validated
        return Result(
                    200,
                    None,
                    None
                    )
    except Exception as error:
        return Result(
                    500, 
                    'Server error while validating request data',
                    None
                    )