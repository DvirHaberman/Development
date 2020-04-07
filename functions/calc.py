import pandas as pd
class Calc:

    @staticmethod
    def plus_func(conn, run_id, a,b):
        return {'result_status':int(run_id)%5, 'result_arr':a+b, 'result_text':'just success'}

    @staticmethod
    def multi_func(conn, run_id, a, b):
        data = pd.read_sql('select * from run_ids_data',con=conn.connection)
        return {'result_status':4, 'result_arr':data, 'result_text':'just success'}