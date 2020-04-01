class Calc:

    @staticmethod
    def plus_func(conn, run_id, a,b):
        return {'result_status':(a+b)%5, 'results_arr':None, 'result_text':'just success'}

    @staticmethod
    def muilti_func(conn, run_id, a, b):
        return {'result_status':(a*b)%5, 'results_arr':None, 'result_text':'just success'}