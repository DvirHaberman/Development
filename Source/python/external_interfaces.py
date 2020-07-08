import pandas as pd

def params_to_dict(params):
    return {'&BBBB':'repBBBB', '&ZZZ':'repZZZ'}

def run_sql(conn, run_id, query, params):
    try:
        translator = params_to_dict(params)
    except:
        return {
                    'result_status':1,
                    'result_text':"Error! parameters extaction error!",
                    'results_arr' : None
                }

    try:
        for key, value in translator.items():
            query = query.replace(key,value)
    except:
        return {
                    'result_status':1,
                    'result_text':"Error! parameters replacement error!",
                    'results_arr' : None
                }
    try:
        result = pd.read_sql(query,con=conn)
    except Exception as error:
        return {
                        'result_status':1,
                        'result_text':"Error! SQL didn't run properly!",
                        'results_arr' : None
                    }
    if len(result) == 0:
        return {
                        'result_status':1,
                        'result_text':'Error! SQL returned a empty result',
                        'results_arr' : None
                    }
    try:
        if len(result) == 1:
            return {
                            'result_status':result['Status'],
                            'result_text':result['Text'],
                            'results_arr' : None
                        }
    except Exception as error:
        return {
                    'result_status':1,
                    'result_text':"Error! something went wrong while extracting the result Text and Status",
                    'results_arr' : None
                }

    try:
        if len(result) > 1:
            result_first_line = result.head(1)
            result_arr = result.drop(result.head(1), inplace=True)
            return {
                            'result_status':result_first_line['Status'],
                            'result_text':result_first_line['Text'],
                            'results_arr' : result_arr
                        }
    except Exception as error:
        return {
                    'result_status':1,
                    'result_text':"Error! something went wrong while extracting the result Text, Status and array",
                    'results_arr' : None
                }
    

def run_matlab(conn, run_id, params):
    return {
        'result_status':4,
        'result_text':"Well you just did nothing",
        'results_arr' : None
    }

if __name__ == "__main__":
    query = 'how about some &BBBB and some a lot of &ZZZ'
    print(run_sql('','',query, 'params'))