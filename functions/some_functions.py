def return_success(conn, run_id):
    return {'result_status':4, 'results_arr':None, 'result_text':'just success'}

def return_warning(conn, run_id):
    return {'result_status':3, 'results_arr':None, 'result_text':'just warning'}

def return_fail(conn, run_id):
    return {'result_status':2, 'results_arr':None, 'result_text':'just fail'}

def return_error(conn, run_id):
    return {'result_status':1, 'results_arr':None, 'result_text':'just error'}

def return_nodata(conn, run_id):
    return {'result_status':0, 'results_arr':None, 'result_text':'just nothing'}