from threading import Thread
from multiprocessing import Process
# from multiprocessing import Process, Queue
# from multiprocessing import Queue as process_queue
from queue import Queue
from model import ErrorLog, Task, AnalyseTask, AnalyseResult

run_queue_flag = True

num_of_analyser_workers = 10

threads_dict = {}

tasks_queue = Queue()
error_queue = Queue()
updates_queue = Queue()
to_do_queue = Queue()
done_queue = Queue()

def init_threads():
    global num_of_analyser_workers
    global threads_dict

    error_logger = Thread(target=Worker.error_logger_worker)
    error_logger.start()
    threads_dict['error_logger'] = error_logger

    threads_dict['analyser_workers'] = []
    for _ in range(num_of_analyser_workers):
        p = Thread(target=Worker.analyser_worker)
        p.start()
        threads_dict['analyser_workers'].append(p)
    
    task_logger = Thread(target=Worker.task_logger_worker)
    task_logger.start()
    threads_dict['task_logger'] = task_logger

    results_logger_worker = Thread(target=Worker.results_logger_worker)
    results_logger_worker.start()
    threads_dict['results_logger_worker'] = results_logger_worker


class Worker:

    # def __init__(self, worker_type='analyser'):
    #     self.worker_type = worker_type
    #     if worker_type == 'analyser':
    #         self.thread = Thread(target=Worker.analyser_worker)
    #         self.thread.start()
    
    @staticmethod
    def error_logger_worker():
        global error_queue
        global run_queue_flag
        while run_queue_flag:
            if not error_queue.empty():
                error_log = error_queue.get_nowait()
                error_log.log()
                error_queue.task_done()


    @staticmethod
    def analyser_worker(db):
        global to_do_queue
        global done_queue
        global run_queue_flag
        global updates_queue
        while run_queue_flag:
            if not to_do_queue.empty():
                task = to_do_queue.get_nowait()
                try:
                    results = task.function_obj.run(task.db_conn_obj, task.run_id)
                    status=4
                    message=''
                except Exception as error:
                    status=3
                    message='technical error with running the function'
                    results = None
                    updates_queue.put_nowait((task.id,results,status,message))
                    to_do_queue.task_done()
                    error_log = ErrorLog(task_id = task.id, stage='performing the task', error_string=message)
                    error_log.push()
                    continue
                try:
                    done_queue.put_nowait((task.id,results,status,message))
                    to_do_queue.task_done()
                except Exception as error:
                    status=5
                    message='failed pushing to done_queue'
                    results = None
                    updates_queue.put_nowait((task.id,results,status,message))
                    to_do_queue.task_done()
                    error_log = ErrorLog(task_id = task.id, stage='pushing the task to done_queue', error_string=message)
                    error_log.push()
                    continue

                

    def task_logger_worker(db):
        global tasks_queue
        global to_do_queue
        global updates_queue
        flag = True
        if flag:
            flag = False
            while run_queue_flag:
                if not tasks_queue.empty():
                    task = tasks_queue.get_nowait()
                    try:
                        task.log()
                    except Exception as error:
                        message='failed logging the task'
                        tasks_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='logging the task', error_string=message)
                        error_log.push()
                        continue
                    try:
                        to_do_queue.put_nowait(task)
                        tasks_queue.task_done()
                    except Exception as error:
                        status=1
                        message='failed pushing to tasks queue'
                        results = None
                        updates_queue.put_nowait((task.id, results, status, message))
                        tasks_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='pushing to tasks queue', error_string=message)
                        error_log.push()
        else:
            flag = True
            while run_queue_flag:
                if not updates_queue.empty():
                    task_id, results, status, message = updates_queue.get_nowait()
                    try:
                        task = AnalyseTask.query.filter_by(id=task_id).first()
                        task.status = status
                        task.message = message
                        db.session.commit()
                        updates_queue.task_done()
                    except Exception as error:
                        message='failed updating the task'
                        updates_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='updating the task', error_string=message)
                        error_log.push()
                    
    @staticmethod
    def results_logger_worker(db):
        global done_queue
        global run_queue_flag
        global updates_queue
        while run_queue_flag:
            if not done_queue.empty():
                task_id, results, status, message = done_queue.get_nowait()
                try:
                    # results = task.function_obj.run(task.db_conn_obj, task.run_id)
                    analyse_result = AnalyseResult(overview_id=self.id, run_id=results['run_id'], db_conn='db_conn',
                                           result_status=results['result_status'], 
                                           result_text=results['result_text'],
                                           result_array=results['result_arr'])
                    
                except Exception as error:
                    status=5
                    message='error logging results'
                    results = None
                    updates_queue.put_nowait((task.id,results,status,message))
                    to_do_queue.task_done()
                    error_log = ErrorLog(task_id = task.id, stage='logging results', error_string=message)
                    error_log.push()