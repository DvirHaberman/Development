from . import api2, g, session, request,jsonify
from Source.python.Model.GenerateMission import Project, User, SystemMission, db, StageRunMani

@api2.route('/SystemMission', methods=['GET', 'POST'])
def get_sys_missions():
    
    project_id = g.project_id 
    sys_missions = SystemMission.query.filter_by(project_id=project_id).all()
    response_data = [{"id":m.id, "user": m.created_by, "time": m.created_time,
                "name": m.name,
                "run_mission":m.run_mission.id if m.run_mission else None,
                "gen_mission":m.gen_mission.id if m.gen_mission else None}
                for m in sys_missions]
    return jsonify(data=response_data)

@api2.route('/SystemMission/<int:id>')
def get_sys_mission(id):
    sys_mission = SystemMission.query.get(id)
    gen_missions = sys_mission.gen_mission.gen_stages.all()
    run_missions = sys_mission.run_mission.run_stages.all()
    num_of_gen_missions = len(gen_missions)
    num_of_run_missions = len(run_missions)
    gen_missions_data=[]
    run_missions_data = []
    def get_status(failed,succeeded):
        if failed > 0 and succeeded ==0:
            status = "2"
        if failed ==0:
            status = "1"
        if failed > 0 and succeeded > 0:
            status = "3"
        return status
    if num_of_gen_missions > 0:
        gen_missions_data = [{
                            "id":gen_mission.id,
                            "stage_name":StageRunMani.query.get(gen_mission.stage_id).name,
                            "ext_events_folder":gen_mission.ext_events_folder,
                            "is_generate_subfolders":gen_mission.is_generate_subfolders,
                            "generate_mission_id":gen_mission.generate_mission_id,
                            "run_mission_id":gen_mission.run_mission_id,
                            "is_validated":gen_mission.is_validated,
                            "is_in_db":gen_mission.is_in_db,
                            "is_generated":gen_mission.is_generated,
                            "delete_after":gen_mission.delete_after,
                            "updated_time":gen_mission.updated_time,
                            "priority":gen_mission.priority,
                            "statistics":
                                [{
                                    "succeeded":s.succeeded, 
                                    "failed": s.failed,
                                    "stage_type":s.stage_type,
                                    "status": get_status(s.failed,s.succeeded)
                                 } for s in gen_mission.statistics]
                            
                            } for gen_mission in gen_missions]
    if num_of_run_missions > 0:
        run_missions_data = [{
                            "id": run_mission.id,
                            "stage_id":run_mission.stage_id,
                            "generate_status_id":run_mission.generate_status_id,
                            "delete_after":run_mission.delete_after,
                            "updated_time":run_mission.updated_time,
                            "run_id":run_mission.run_id,
                            "priority":run_mission.priority
                            } for run_mission in run_missions]
    response_data = {
        "header":{
            "id":sys_mission.id,
            "name":sys_mission.name,
            "gen_missions":str(num_of_gen_missions),
            "run_missions":str(num_of_run_missions),
        },
        "details":{
            "gen_missions_data":gen_missions_data,
            "run_missions_data":run_missions_data
        }
    }
    db.session.close()
    return jsonify(data=response_data)

@api2.route('/SystemMission/Delete/<int:id>', methods=['DELETE'])
def delete_sys_mission(id):
    try:
        sys_mission = SystemMission.query.get(id)
        if sys_mission is None:
            return jsonify(message='mission with this id does not exist'), 404
        mission_name = sys_mission.name
        db.session.delete(sys_mission)
        db.session.commit()
        return jsonify(message='Success! Mission '+ str(mission_name) + ' was deleted'), 200
    except:
        return jsonify(message='Error! Mission '+ str(mission_name) + ' was not deleted'), 500
    finally:
        db.session.close()