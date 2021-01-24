class GenerateStageTypes:
    LOGGING = 1
    VALIDATING = 2
    DB_INSERT = 3
    GENERATE = 4

class GenerateStatus:
    SUCCESS = 1
    FAILED = 2
    PARTIAL_SUCCESS = 3
    EXCEPTION = 4