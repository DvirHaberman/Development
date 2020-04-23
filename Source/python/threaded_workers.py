from threading import Thread
from multiprocessing import Process
# from multiprocessing import Process, Queue
# from multiprocessing import Queue as process_queue
from queue import Queue
from python.model import *
from datetime import datetime
# from model import ErrorLog, Task, AnalyseTask, AnalyseResult




def init_threads(threads_dict,num_of_analyser_workers,run_queue_flag,
                 tasks_queue,error_queue,updates_queue,to_do_queue,done_queue):
    # global num_of_analyser_workers
    # global threads_dict
    # global run_queue_flag
    # global error_queue
    error_logger = Process(target=Worker.error_logger_worker, args=([error_queue,run_queue_flag]))
    error_logger.start()
    threads_dict['error_logger'] = error_logger

    threads_dict['analyser_workers'] = []
    for _ in range(num_of_analyser_workers):
        p = Process(target=Worker.analyser_worker, args=([tasks_queue,error_queue,updates_queue,to_do_queue,done_queue,run_queue_flag]))
        p.start()
        threads_dict['analyser_workers'].append(p)
    
    task_logger = Process(target=Worker.task_logger_worker, args=([tasks_queue,error_queue,updates_queue,to_do_queue,run_queue_flag]))
    task_logger.start()
    threads_dict['task_logger'] = task_logger

    results_logger_worker = Process(target=Worker.results_logger_worker, args=([done_queue,updates_queue,error_queue,run_queue_flag]))
    results_logger_worker.start()
    threads_dict['results_logger_worker'] = results_logger_worker


class Worker:

    # def __init__(self, worker_type='analyser'):
    #     self.worker_type = worker_type
    #     if worker_type == 'analyser':
    #         self.thread = Thread(target=Worker.analyser_worker)
    #         self.thread.start()
    
    @staticmethod
    def error_logger_worker(error_queue, run_queue_flag):
        # global error_queue
        # global run_queue_flag
        threaded_app = create_threaded_app(db)
        # scoped_session = db.create_scoped_session()
        with threaded_app.app_context():
            while run_queue_flag:
                if not error_queue.empty():
                    error_log = error_queue.get_nowait()
                    error_log.log()
                    # error_queue.task_done()


    @staticmethod
    def analyser_worker(tasks_queue,error_queue,updates_queue,
                        to_do_queue,done_queue,run_queue_flag):
        # global to_do_queue
        # global done_queue
        # global run_queue_flag
        # global updates_queue
        threaded_app = create_threaded_app(db)
        # scoped_session = db.create_scoped_session()
        with threaded_app.app_context():
            while run_queue_flag:
                if not to_do_queue.empty():
                    try:
                        task = to_do_queue.get_nowait()
                    except:
                        continue
                    try:
                        function_obj = OctopusFunction.query.get(task.function_id)
                        results = function_obj.run(task.db_conn_obj, task.run_id)
                        status=4
                        message=''
                        print(f'done with preforming task {task.id} in {datetime.utcnow()}')
                    except Exception as error:
                        status=3
                        message='technical error with running the function'
                        results = None
                        updates_queue.put_nowait((task.id,status,message))
                        # to_do_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='performing the task', error_string=message)
                        error_log.push(error_queue)
                        continue
                    try:
                        done_queue.put_nowait((task,results,status,message))
                        print(f'done with pushing result for task {task.id} in {datetime.utcnow()}')
                        # to_do_queue.task_done()
                    except Exception as error:
                        status=5
                        message='failed pushing to done_queue'
                        updates_queue.put_nowait((task.id,status,message))
                        # to_do_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='pushing the task to done_queue', error_string=message)
                        error_log.push(error_queue)
                        continue

                

    def task_logger_worker(tasks_queue,error_queue,updates_queue,to_do_queue,run_queue_flag):
        # global tasks_queue
        # global to_do_queue
        # global updates_queue

        threaded_app = create_threaded_app(db)
        flag = True

        with threaded_app.app_context():
                
            while run_queue_flag:
                if flag:
                    flag = False
                    if not tasks_queue.empty():
                        task = tasks_queue.get_nowait()
                        try:
                            task.log()
                            print(f'done with logging task {task.id} in {datetime.utcnow()}')
                        except Exception as error:
                            message='failed logging the task'
                            # tasks_queue.task_done()
                            error_log = ErrorLog(task_id = task.id, stage='logging the task', error_string=message)
                            error_log.push(error_queue)
                            continue
                        try:
                            to_do_queue.put_nowait(task)
                            # tasks_queue.task_done()
                        except Exception as error:
                            status=1
                            message='failed pushing to tasks queue'
                            updates_queue.put_nowait((task.id, status, message))
                            # tasks_queue.task_done()
                            error_log = ErrorLog(task_id = task.id, stage='pushing to tasks queue', error_string=message)
                            error_log.push(error_queue)
                else:
                    flag = True
                    if not updates_queue.empty():
                        task_id, status, message = updates_queue.get_nowait()
                        try:
                            task = AnalyseTask.query.filter_by(id=task_id).first()
                            task.status = status
                            task.message = message
                            db.session.add(task)
                            db.session.commit()
                            print(f'done with updating task {task.id} in {datetime.utcnow()}')
                            # updates_queue.task_done()
                        except Exception as error:
                            message='failed updating the task'
                            # updates_queue.task_done()
                            error_log = ErrorLog(task_id = task.id, stage='updating the task', error_string=message)
                            error_log.push(error_queue)
                    
    @staticmethod
    def results_logger_worker(done_queue,updates_queue,error_queue,run_queue_flag):
        # global done_queue
        # global run_queue_flag
        # global updates_queue

        threaded_app = create_threaded_app(db)
        with threaded_app.app_context():
            while run_queue_flag:
                if not done_queue.empty():
                    task, results, status, message = done_queue.get_nowait()
                    try:
                        # results = task.function_obj.run(task.db_conn_obj, task.run_id)
                        analyse_result = AnalyseResult(task_id=task.id,run_id=results['run_id'],
                                            db_conn_string=task.db_conn_obj.name,
                                            result_status=results['result_status'], 
                                            result_text=results['result_text'])
                        # db.session.add(analyse_result)
                        # db.session.commit()
                        # done_queue.task_done()
                        message = analyse_result.log(results['result_arr'], error_queue)
                        updates_queue.put_nowait((task.id,status,message))
                        print(f'done with logging result {task.id} in {datetime.utcnow()}')
                    except Exception as error:
                        status=5
                        message='error logging results'
                        updates_queue.put_nowait((task.id,status,message))
                        # done_queue.task_done()
                        error_log = ErrorLog(task_id = task.id, stage='logging results', error_string=message)
                        error_log.push(error_queue)