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
        def validate_request_data(json_data):
            try:
                #check that all fields exist in the recieved data
                expected_keys = ['request_type', 'is_generated', 'request_content']
                content_keys  = ['stage_name', 'ext_events_folder', 'is_generate_subfolders', 'priority']
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
                        "request_type":json_data['request_type'],
                        'request_content': json_data['request_content'],
                        "project_id": session['current_project_id'],
                        "user_name": session['username']
                      }
        return Result(200, None, gen_request)
    except:
        return Result(500, 'error creating the generation request', None)

def create_run_request(json_data, gen_mission_id, run_mission_id, project_id, user_name):
    try:
      
        run_request = {
                        "gen_mission_id":gen_mission_id,
                        "run_mission_id":run_mission_id,
                        "request_type":json_data['request_type'],
                        'request_content': json_data['request_content'],
                        "project_id": project_id,
                        "user_name": user_name
                      }
        return Result(200, None, run_request)
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
        def validate_request_data(json_data):
            try:
                #check that all fields exist in the recieved data
                expected_keys = ['run_mission_id', 'gen_mission_id', 'request_content']
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
                            None,
                            None
                            )
            except Exception as error:
                return Result(
                            500, 
                            'Server error while validating request data',
                            None
                            )
        # validating the data             
        result = validate_request_data(gen_request)
        if result.status >=300:
            return result
        
        run_mission_id = int(gen_request['run_mission_id'])
        
        gen_mission_id = int(gen_request['gen_mission_id'])

        #get the gen mission from the db
        gen_mission = GenerateMission.query.get(gen_mission_id)
        
        if not gen_mission:
            return Result(404, 'No gen mission was found with id:' + str(gen_mission_id), None)
        project_id = gen_mission.project_id
        results = []
        statistics = {"failed": 0, "succeeded": 0}
        for request in gen_request['request_content']:
            stage_name = request['stage_name']
            stage = StageRunMani.query.filter_by(name=stage_name,project_id=project_id).first()
            if not stage:
                result=Result(
                            404, 
                            "stage with name " + stage_name + " was not found",
                            None
                            )
                statistics['failed'] += 1
                results.append(result)
                continue
            request.update({"stage_id":stage.id})
            if Path(request['ext_events_folder']).exists():
                if int(request['is_generate_subfolders']) > 0:
                    folders = list(set(get_subfolders(request['ext_events_folder'],'').split(',')))
                else:
                    folders = [gen_mission.ext_events_folder]
                for folder in folders:
                    result = GenerateMissionInterface.generate_mission_status(request, gen_mission_id, run_mission_id, project_id, folder)
                    results.append(result)
                    if result.status >= 300:
                        statistics['failed'] += 1
                    else:
                        statistics['succeeded'] += 1
            else:
                result = Result(416, f'external events folder: {request["ext_events_folder"]} was not found',None)
                statistics['failed'] += 1
                results.append(result)
        statistics.update({"total": statistics['failed']+statistics['succeeded']})
        return Result(200,None,{"results":results, "statistics":statistics})
    
    @staticmethod
    def execute_request(gen_status):
        stage_id = gen_status.stage_id
        stage = StageRunMani.query.get(stage_id)
        if not stage:
            return Result(
                        404, 
                        "stage with name " + stage_name + " was not found",
                        None
                        )
        return Result(200, None, {
                                "is_validated":{"failed":1, "succeeded":2, "total":3},
                                "is_in_db":{"failed":1, "succeeded":2, "total":3},
                                "is_generated":{"failed":1, "succeeded":2, "total":3}
                                }
                    )
    @staticmethod
    def generate_mission_status(request, gen_mission_id, run_mission_id, project_id, ext_events_folder):
        try:
            stage_id = request['stage_id']
            run_mission_id = run_mission_id
            priority = int(request['priority'])
            ext_events_folder = ext_events_folder
            is_generate_subfolders = int(request['is_generate_subfolders'])
            generate_id = gen_mission_id
            is_validated = None
            is_in_db = None
            is_generated = None
            delete_after = int(request['gen_delete_after'])
            updated_time = datetime.utcnow()
            generate_mission_id = gen_mission_id

            gen_status = GenerateMissionStatus(
                                        stage_id=stage_id,
                                        run_mission_id=run_mission_id,
                                        ext_events_folder=ext_events_folder,
                                        is_generate_subfolders=is_generate_subfolders,
                                        generate_mission_id=generate_mission_id,
                                        is_validated=is_validated,
                                        is_in_db=is_in_db,
                                        is_generated=is_generated,
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

def get_subfolders(basedir,folders):
    folders += ',' + basedir if len(folders) > 0 else basedir
    if not [f for f in listdir(basedir) if not isfile(basedir + sep + f)]:
        return folders
    return ','.join([get_subfolders(basedir+sep+f, folders) for f in listdir(basedir) if not isfile(basedir + sep + f)])

