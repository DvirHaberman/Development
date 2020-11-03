from .model import *

class RunMissionInterface:
    def __init__(
                self, 
                name,
                created_by,
                project_id,
                created_date = datetime.utcnow(),
                run_stages = [],
                priority = 10
                ):
        self.name = name
        self.created_by = created_by
        self.created_date = created_date
        self.project_id = project_id
        self.run_stages = run_stages
        self.priority = priority

class RunStageStatusInterface:
    def __init__(
                self,
                stage_id,
                is_validated,
                is_db_updated,
                is_generated,
                delete_after,
                updated_time = datetime.utcnow(),
                run_mission = None
                ):
        self.stage_id = stage_id
        self.is_validated = is_validated
        self.is_db_updated = is_db_updated
        self.is_generated = is_generated
        self.delete_after = delete_after
        self.updated_time = updated_time
        self.run_mission = run_mission
