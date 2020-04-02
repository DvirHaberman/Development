class Calc:

    @staticmethod
    def plus_func(conn, run_id, a,b):
        return {'result_status':int(run_id)%5, 'results_arr':a+b, 'result_text':'just success'}

    @staticmethod
    def multi_func(conn, run_id, a, b):
        return {'result_status':4, 'results_arr':a*b, 'result_text':'just success'}