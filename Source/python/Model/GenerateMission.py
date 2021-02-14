from ..model import *

class GenerateMission(db.Model):
    __tablename__ = "generatemission"
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer)
    created_time = db.Column(db.DateTime)
    project_id = db.Column(db.Integer)
    parent_mission = db.Column(db.Integer, db.ForeignKey('systemmission.id'))
    gen_stages = db.relationship('GenerateMissionStatus', backref='GenerateMission', 
                                cascade="all,delete", lazy='dynamic', uselist=True)

    def __init__(
                self,
                created_by,
                created_time,
                project_id,
                gen_stages,
                parent_mission
                ):

        self.created_by = created_by
        self.created_time = created_time
        self.project_id = project_id
        self.gen_stages = gen_stages
        self.parent_mission = parent_mission


class GenerateMissionStatus(db.Model):
    __tablename__ = 'generatemissionstatus'
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer)
    ext_events_folder = db.Column(db.Text)
    is_generate_subfolders = db.Column(db.Boolean)
    generate_mission_id = db.Column(db.Integer, db.ForeignKey('generatemission.id'))
    run_mission_id = db.Column(db.Integer)
    is_validated = db.Column(db.Integer)
    is_in_db = db.Column(db.Integer)
    is_generated = db.Column(db.Integer)
    statistics = db.relationship('GenerateStatistics', backref='GenerateMissionStatus', 
                                  cascade="all,delete", lazy=True, uselist=True)
    delete_after = db.Column(db.Boolean)
    updated_time = db.Column(db.DateTime)
    priority = db.Column(db.Integer)

    def __init__(
                self,
                stage_id,
                ext_events_folder,
                is_generate_subfolders,
                generate_mission_id,
                run_mission_id,
                is_validated,
                is_in_db,
                is_generated,
                statistics,
                delete_after,
                updated_time,
                priority
                ):
        self.stage_id = stage_id
        self.ext_events_folder = ext_events_folder
        self.is_generate_subfolders = is_generate_subfolders
        self.generate_mission_id = generate_mission_id
        self.run_mission_id = run_mission_id
        self.is_validated = is_validated
        self.is_in_db = is_in_db
        self.is_generated = is_generated
        self.statistics = statistics
        self.delete_after = delete_after
        self.updated_time = updated_time
        self.priority = priority

class GenerateStatistics(db.Model):
    __tablename__ = 'generatestatistics'
    id = db.Column(db.Integer, primary_key=True)
    generate_status_id = db.Column(db.Integer, db.ForeignKey('generatemissionstatus.id'))
    generate_mission_id = db.Column(db.Integer)
    succeeded = db.Column(db.Integer)
    failed = db.Column(db.Integer)
    total = db.Column(db.Integer)
    stage_type = db.Column(db.Integer)

    def __init__(
                self,
                generate_status_id,
                generate_mission_id,
                succeeded,
                failed,
                total,
                stage_type
                ):

        self.generate_status_id = generate_status_id
        self.generate_mission_id = generate_mission_id
        self.succeeded = succeeded
        self.failed = failed
        self.total = total
        self.stage_type = stage_type


class RunMission(db.Model):
    __tablename__ = 'runmission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    created_by = db.Column(db.Integer)
    created_time = db.Column(db.DateTime)
    project_id = db.Column(db.Integer)
    parent_mission = db.Column(db.Integer, db.ForeignKey('systemmission.id'))
    run_stages = db.relationship('RunMissionStatus', backref='RunMission', lazy='dynamic', uselist=True)

    def __init__(
                self, 
                name,
                created_by,
                project_id,
                run_stages,
                created_time,
                parent_mission
                ):
        self.name = name
        self.created_by = created_by
        self.created_time = created_time
        self.project_id = project_id
        self.run_stages = run_stages
        self.parent_mission = parent_mission

        
class RunMissionStatus(db.Model):
    __tablename__ = 'runmissionstatus'
    id = db.Column(db.Integer, primary_key=True)
    stage_id = db.Column(db.Integer)
    generate_mission_id = db.Column(db.Integer)
    generate_status_id = db.Column(db.Integer)
    delete_after = db.Column(db.Boolean)
    updated_time = db.Column(db.DateTime)
    run_mission_id = db.Column(db.Integer, db.ForeignKey('runmission.id'))
    run_id = db.Column(db.Integer)
    priority = db.Column(db.Integer)

    def __init__(
                self,
                stage_id,
                generate_mission_id,
                generate_status_id,
                delete_after,
                updated_time,
                run_mission_id,
                priority
                ):
        self.stage_id = stage_id
        self.generate_mission_id = generate_mission_id
        self.generate_status_id = generate_status_id
        self.delete_after = delete_after
        self.updated_time = updated_time
        self.run_mission_id = run_mission_id
        self.priority = priority


class SystemMission(db.Model):
    __tablename__ = 'systemmission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    gen_mission = db.relationship('GenerateMission', backref='SystemMission',  cascade="all,delete",
                                  lazy=True, uselist=False)
    run_mission = db.relationship('RunMission', backref='SystemMission', cascade="all,delete",
                                  lazy=True, uselist=False)
    created_by = db.Column(db.Integer)
    created_time = db.Column(db.DateTime)
    project_id = db.Column(db.Integer)

    def __init__(
                self,
                name,
                created_by,
                project_id,
                created_time=datetime.utcnow(),
                gen_mission_id = None,
                run_mission_id = None,
                ):
        self.name = name
        self.gen_mission_id = gen_mission_id
        self.run_mission_id = run_mission_id
        self.created_by = created_by
        self.created_time = created_time
        self.project_id = project_id