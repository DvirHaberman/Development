from threading import Thread
from multiprocessing import Process, Pipe
from queue import Queue
from .Interfaces import *
from datetime import datetime


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
                 tasks_queue,error_queue,updates_queue,to_do_queue,done_queue,
                 generate_requests_queue, run_requests_queue, generated_queue ,pipes_dict):

    error_logger = Process(target=Worker.error_logger_worker, args=([error_queue,run_or_stop_flag]))
    error_logger.start()
    processes_dict['error_logger'] = error_logger

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

    # system_runner_worker = Process(target=Worker.system_runner_worker, args=([error_queue,run_or_stop_flag, run_requests_queue]))
    # system_runner_worker.start()
    # processes_dict['system_runner_worker'] = system_runner_worker

    # scenario_generator_worker = Process(target=Worker.scenario_generator_worker, args=([error_queue,run_or_stop_flag, generate_requests_queue, generated_queue]))
    # system_runner_worker.start()
    # processes_dict['scenario_generator_worker'] = scenario_generator_worker

    error_logger = Process(target=Worker.error_logger_worker, args=([error_queue,run_or_stop_flag]))
    error_logger.start()
    processes_dict['error_logger'] = error_logger

    return processes_dict

class Worker:

    @staticmethod
    def error_logger_worker(error_queue, run_or_stop_flag):
        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not error_queue.empty():
                    try:
                        error_log = error_queue.get_nowait()
                        error_log.log()
                    except:
                        print('error logger failure')
                    finally:
                        db.session.close()


    @staticmethod
    def analyser_worker(tasks_queue,error_queue,updates_queue,
                        to_do_queue,done_queue,run_or_stop_flag,pipe_conn):
        process_app = create_process_app(db)
        tests_params = None
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                try:
                    try:
                        update_flag, new_tests_params = check_tests_params_update(pipe_conn)
                        if update_flag:
                            tests_params = new_tests_params
                    except:
                        message='failed reading Tests_Params from pipe'
                        error_log = ErrorLog(task_id = 0, stage='reading Tests_Params from pipe', error_string=message)
                        error_log.push(error_queue)
                        sleep(5)
                    if not to_do_queue.empty():
                        try:
                            task = to_do_queue.get_nowait()
                        except:
                            continue
                        try:
                            if task.run_status > 0:
                                function_obj = OctopusFunction.query.get(task.function_id)
                                results = function_obj.run(task.db_conn_obj, task.run_id, tests_params)
                                status=results['result_status']
                                message=''
                            else:
                                status = task.run_status
                                results = {}
                                if status == -1:
                                    message = 'db conn is invalid'
                                else:
                                    message = 'run not in db'
                            print(f'done with preforming task {task.id} in {datetime.utcnow()}')
                        except Exception as error:
                            status=3
                            message='technical error with running the function'
                            results = None
                            updates_queue.put_nowait((task.id,status,message))
                            error_log = ErrorLog(task_id = task.id, stage='performing the task', error_string=message)
                            error_log.push(error_queue)
                            continue
                        try:
                            done_queue.put_nowait((task,results,status,message))
                            print(f'done with pushing result for task {task.id} in {datetime.utcnow()}')
                        except Exception as error:
                            status=5
                            message='failed pushing to done_queue'
                            updates_queue.put_nowait((task.id,status,message))
                            error_log = ErrorLog(task_id = task.id, stage='pushing the task to done_queue', error_string=message)
                            error_log.push(error_queue)
                            continue
                except:
                    print('analyse worker failure')
                finally:
                    db.session.close()

    def task_logger_worker(tasks_queue, error_queue,updates_queue,to_do_queue,run_or_stop_flag):

        process_app = create_process_app(db)
        flag = True

        with process_app.app_context():

            while run_or_stop_flag.is_set():
                if flag:
                    flag = False
                    if not tasks_queue.empty():
                        try:
                            task = tasks_queue.get_nowait()
                            try:
                                task.log(task.status)
                                print(f'done with logging task {task.id} in {datetime.utcnow()}')
                            except Exception as error:
                                message='failed logging the task'
                                error_log = ErrorLog(task_id = task.id, stage='logging the task', error_string=message)
                                error_log.push(error_queue)
                                continue
                            try:
                                if(task.status == -3):
                                    to_do_queue.put_nowait(task)
                            except Exception as error:
                                status=-4
                                message='failed pushing to tasks queue'
                                updates_queue.put_nowait((task.id, status, message))
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
                            task_id, status, time_elapsed,message = updates_queue.get_nowait()
                            try:
                                task = AnalyseTask.query.filter_by(id=task_id).first()
                                task.status = status
                                task.message = message
                                task.time_elapsed = time_elapsed
                                db.session.add(task)
                                db.session.commit()
                                print(f'done with updating task {task.id} in {datetime.utcnow()}')
                            except Exception as error:
                                message='failed updating the task'
                                error_log = ErrorLog(task_id = task.id, stage='updating the task', error_string=message)
                                error_log.push(error_queue)
                        except:
                            print("task logger failure")
                        finally:
                            db.session.close()
    @staticmethod
    def results_logger_worker(done_queue,updates_queue,error_queue,run_or_stop_flag):

        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not done_queue.empty():
                    try:
                        task, results, status, message = done_queue.get_nowait()
                        try:
                            sleep(0.1)
                            if status > -1:
                                keys = ['run_id', 'result_status', 'result_text', 'time_elapsed', 'results_arr']
                                final_result = {'run_id':'Unknown', 'result_status':1, 'result_text':'Missing', 'time_elapsed':0, 'results_arr':None}
                                missing = [key for key in keys if key not in results]
                                for key, value in results.items():
                                    if key not in missing:
                                        final_result[key] = value
                                if missing:
                                    # status = 5
                                    message = 'fields' + ', '.join(missing) + 'are missing in the returned result'
                                    final_result = {'run_id':final_result['run_id'], 'result_status':1, 'result_text':message, 'time_elapsed':0, 'results_arr':None}
                                status = final_result['result_status']
                            else:
                                final_result = {'run_id':task.run_id, 'result_status':status, 'result_text':'Missing', 'time_elapsed':0, 'results_arr':None}

                            analyse_result = AnalyseResult(mission_id=task.mission_id,
                                                task_id=task.id, 
                                                run_id=final_result['run_id'],
                                                scenario_name=task.scenario_name,
                                                run_status=task.run_status,
                                                function_id=task.function_id, 
                                                db_conn_string=task.db_conn_obj.name,
                                                result_status=final_result['result_status'],
                                                result_text=final_result['result_text'],
                                                time_elapsed = final_result['time_elapsed'])

                            message = analyse_result.log(final_result['results_arr'], error_queue)
                            updates_queue.put_nowait((task.id,status,final_result['time_elapsed'],message))
                            print(f'done with logging result {task.id} in {datetime.utcnow()}')
                        except Exception as error:
                            status=-5
                            message='error logging results'
                            updates_queue.put_nowait((task.id,status,message))
                            error_log = ErrorLog(task_id = task.id, stage='logging results', error_string=message)
                            error_log.push(error_queue)
                    except:
                            print("result logger failure")
                    finally:
                        db.session.close()

    # @staticmethod
    # def system_runner_worker(error_queue, run_or_stop_flag, run_requests_queue):
    #     process_app = create_process_app(db)
    #     with process_app.app_context():
    #         while run_or_stop_flag.is_set():
    #             if not run_requests_queue.empty():
    #                 try:
    #                     run_request = error_queue.get_nowait()
    #                     # create a run mission row in octopus db
    #                     result = RunMissionInterface.create_run_mission(run_request=run_request)
    #                     # log error if somthing failed
    #                     if result.status >= 300:
    #                         error = ErrorLog(
    #                                          error_string=result.message,
    #                                          stage='making a run request'
    #                                         )
    #                         error.log()
    #                         continue
    #                     # if run mission row was created - create the mission for run script 
    #                     # AutoRunData, ComplexNet etc.
    #                 except:
    #                     print('exeption in system runner failure')
    #                     try:
    #                         pass
    #                     except expression as identifier:
    #                         pass
    #                 finally:
    #                     db.session.close()
