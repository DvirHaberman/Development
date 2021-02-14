from . import api2, jsonify, request
from Source.python.Model.GenerateMission import GenerateMissionStatus, db

@api2.route('/GenerateMissionStatus/delete/<int:id>', methods=["DELETE"])
def delete_gen_mission_status(id):
    try:
        m = GenerateMissionStatus.query.get(id)
        if m is None:
            return jsonify(message='mission with this id does not exist'), 404
        db.session.delete(m)
        db.session.commit()
        return jsonify(message='Success! Gen Mission '+ str(id) + ' was deleted'), 200
    except:
        return jsonify(message='Error! Gen Mission '+ str(id) + ' was not deleted'), 500
    finally:
        db.session.close()

@api2.route('/GenerateMissionStatus/delete/batch', methods=["DELETE"])
def delete_batch_gen_mission_status():
    try:
        to_remove_str = request.args.get('array')
        to_remove_list = to_remove_str.split(',')
        problems = []
        for r in to_remove_list:
            m = GenerateMissionStatus.query.get(r)
            if m is None:
                problems.append(r)
            else:
                db.session.delete(m)

        db.session.commit()
        if len(problems) > 0:
            return jsonify(message='Partial Success!\n attempted to remove Gen Missions '+ to_remove_str + ' and did not find ' + ','.join(problems)), 206
        else:
            return jsonify(message='Success! Gen Missions '+ to_remove_str + ' were deleted'), 200
    except:
        db.session.rollback()
        return jsonify(message='Error! Gen Missions '+ to_remove_str + ' were not deleted'), 500
    finally:
        db.session.close()
