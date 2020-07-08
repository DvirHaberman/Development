import pandas as pd
from time import sleep
def return_success(conn, run_id):
    data = pd.read_sql('select * from run_ids',con=conn)
    return {'result_status':4, 'results_arr':None, 'result_text':'just success'}

def return_warning(conn, run_id):
    return {'result_status':3, 'results_arr':pd.DataFrame({'head1':[1,2,3,4,5,6,7,8,9,10],
                                                          'head2':[1,2,3,4,5,6,7,8,9,10],
                                                          'head3':[1,2,3,4,5,6,7,8,9,10],
                                                          'head4':[1,2,3,4,5,6,7,8,9,10],
                                                          'head5':[1,2,3,4,5,6,7,8,9,10],
                                                          'head6':[1,2,3,4,5,6,7,8,9,10],
                                                          'head7':[1,2,3,4,5,6,7,8,9,10],
                                                          'head8':[1,2,3,4,5,6,7,8,9,10]
                                                          }), 'result_text':'just warning'}

def return_fail(conn, run_id):
    return {'result_status':2, 'results_arr':None, 'result_text':'just fail'}

def return_error(conn, run_id):
    return {'result_status':1, 'results_arr':None, 'result_text':'just error'}

def return_nodata(conn, run_id):
    return {'result_status':0, 'results_arr':None, 'result_text':'just nothing'}

def return_unknown(conn, run_id):
    return {'result_statu':0, 'result_arr':None, 'result_text':'just nothing'}