from threading import Thread
from multiprocessing import Process, Pipe
# from multiprocessing import Process, Queue
# from multiprocessing import Queue as process_queue
from queue import Queue
from python.model import *
from datetime import datetime
# from DataCollector import get_tests_params
# from model import ErrorLog, Task, AnalyseTask, AnalyseResult


def send_data_to_workers(data, pipes_dict, num_of_analyser_workers):
    for num in range(num_of_analyser_workers):
        pipes_dict[f'master_conn_{num}'].send(data)


def create_pipes(num_of_analyser_workers):
    pipes_dict = {}
    for num in range(num_of_analyser_workers):
        conn1, conn2 = Pipe()
        pipes_dict[f'analyser_worker_conn_{num}'] = conn1
        pipes_dict[f'master_conn_{num}'] = conn2
    return pipes_dict

def check_tests_params_update(pipe_conn):
    test_params = None
    update_flag = False
    while pipe_conn.poll():
        test_params = pipe_conn.recv()
        update_flag = True


    return (update_flag, test_params)




def init_processes(processes_dict,num_of_analyser_workers,run_or_stop_flag,
                 tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, pipes_dict):
    # global num_of_analyser_workers
    # global processes_dict
    # global run_or_stop_flag
    # global error_queue
    error_logger = Process(target=Worker.error_logger_worker, args=([error_queue,run_or_stop_flag]))
    error_logger.start()
    processes_dict['error_logger'] = error_logger

    # processes_dict['analyser_workers'] = []
    for num in range(num_of_analyser_workers):
        p = Process(target=Worker.analyser_worker, args=([tasks_queue,error_queue,
                                                        updates_queue,to_do_queue,
                                                        done_queue,run_or_stop_flag,
                                                        pipes_dict[f'analyser_worker_conn_{num}']]))
        p.start()
        processes_dict[f'analyser_workers_{num}'] = p

    task_logger = Process(target=Worker.task_logger_worker, args=([tasks_queue,error_queue,updates_queue,to_do_queue,run_or_stop_flag]))
    task_logger.start()
    processes_dict['task_logger'] = task_logger

    results_logger_worker = Process(target=Worker.results_logger_worker, args=([done_queue,updates_queue,error_queue,run_or_stop_flag]))
    results_logger_worker.start()
    processes_dict['results_logger_worker'] = results_logger_worker

    return processes_dict

class Worker:

    # def __init__(self, worker_type='analyser'):
    #     self.worker_type = worker_type
    #     if worker_type == 'analyser':
    #         self.thread = Thread(target=Worker.analyser_worker)
    #         self.thread.start()

    @staticmethod
    def error_logger_worker(error_queue, run_or_stop_flag):
        # global error_queue
        # global run_or_stop_flag
        process_app = create_process_app(db)
        # scoped_session = db.create_scoped_session()
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not error_queue.empty():
                    try:
                        #db.session.expire_all()
                        error_log = error_queue.get_nowait()
                        error_log.log()
                    except:
                        print('error logger failure')
                    finally:
                        db.session.close()
                    # error_queue.task_done()


    @staticmethod
    def analyser_worker(tasks_queue,error_queue,updates_queue,
                        to_do_queue,done_queue,run_or_stop_flag,pipe_conn):
        # global to_do_queue
        # global done_queue
        # global run_or_stop_flag
        # global updates_queue
        process_app = create_process_app(db)
        # scoped_session = db.create_scoped_session()
        tests_params = None
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                try:
                    #db.session.expire_all()
                    try:
                        update_flag, new_tests_params = check_tests_params_update(pipe_conn)
                        if update_flag:
                            tests_params = new_tests_params
                    except:
                        message='failed reading Tests_Params from pipe'
                        # updates_queue.put_nowait((task.id,status,message))
                        # to_do_queue.task_done()
                        error_log = ErrorLog(task_id = 0, stage='reading Tests_Params from pipe', error_string=message)
                        error_log.push(error_queue)
                        sleep(5)
                    if not to_do_queue.empty():
                        try:
                            task = to_do_queue.get_nowait()
                        except:
                            continue
                        try:
                            function_obj = OctopusFunction.query.get(task.function_id)
                            results = function_obj.run(task.db_conn_obj, task.run_id, tests_params)
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
                except:
                    print('analyse worker failure')
                finally:
                    db.session.close()

    def task_logger_worker(tasks_queue,error_queue,updates_queue,to_do_queue,run_or_stop_flag):
        # global tasks_queue
        # global to_do_queue
        # global updates_queue

        process_app = create_process_app(db)
        flag = True

        with process_app.app_context():

            while run_or_stop_flag.is_set():
                if flag:
                    flag = False
                    if not tasks_queue.empty():
                        try:
                            #db.session.expire_all()
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
                        except:
                            print("task logger failure")
                        finally:
                            db.session.close()
                else:
                    flag = True
                    if not updates_queue.empty():
                        try:
                            #db.session.expire_all()
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
                        except:
                            print("task logger failure")
                        finally:
                            db.session.close()
    @staticmethod
    def results_logger_worker(done_queue,updates_queue,error_queue,run_or_stop_flag):
        # global done_queue
        # global run_or_stop_flag
        # global updates_queue

        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not done_queue.empty():
                    try:
                        #db.session.expire_all()
                        task, results, status, message = done_queue.get_nowait()
                        try:
                            # results = task.function_obj.run(task.db_conn_obj, task.run_id)
                            analyse_result = AnalyseResult(task_id=task.id,run_id=results['run_id'],
                                                db_conn_string=task.db_conn_obj.name,
                                                result_status=results['result_status'],
                                                result_text=results['result_text'],
                                                time_elapsed = results['time_elapsed'])
                            # db.session.add(analyse_result)
                            # db.session.commit()
                            # done_queue.task_done()
                            message = analyse_result.log(results['results_arr'], error_queue)
                            updates_queue.put_nowait((task.id,status,message))
                            print(f'done with logging result {task.id} in {datetime.utcnow()}')
                        except Exception as error:
                            status=5
                            message='error logging results'
                            updates_queue.put_nowait((task.id,status,message))
                            # done_queue.task_done()
                            error_log = ErrorLog(task_id = task.id, stage='logging results', error_string=message)
                            error_log.push(error_queue)
                    except:
                            print("result logger failure")
                    finally:
                        db.session.close()