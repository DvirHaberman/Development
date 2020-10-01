import pandas as pd

class Calc:

    @staticmethod
    def plus_func(conn, run_id, a,b):
        return {'result_status':3, 'result_arr':pd.DataFrame({'head1':[1,2,3,4],'head2':['wow '+str(run_id),'wowz', 'weee', 'blaa']}), 'result_text':'just success'}

    @staticmethod
    def multi_func(conn, run_id, a, b):
        data = pd.read_sql('select * from run_ids',con=conn)
        return {'result_status':4, 'result_arr':data, 'result_text':'just success'}

class ReturnNums:
    @staticmethod
    def return_one():
        return 1
    
    def return_zero():
        return 0