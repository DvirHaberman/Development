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




def init_processes(num_of_analyser_workers,run_or_stop_flag,
            tasks_queue,error_queue,updates_queue,to_do_queue,done_queue, 
            generate_requests_queue, run_requests_queue, to_generate_queue ,pipes_dict):

    processes_dict = {}

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

    system_runner_worker = Process(target=Worker.system_runner_worker, args=([error_queue,run_or_stop_flag, run_requests_queue]))
    system_runner_worker.start()
    processes_dict['system_runner_worker'] = system_runner_worker

    scenario_generator_worker = Process(target=Worker.scenario_generator_worker, args=([error_queue,run_or_stop_flag, to_generate_queue, run_requests_queue]))
    scenario_generator_worker.start()
    processes_dict['scenario_generator_worker'] = scenario_generator_worker

    generate_requests_logger = Process(target=Worker.generate_requests_logger, args=([error_queue,run_or_stop_flag, generate_requests_queue, to_generate_queue]))
    generate_requests_logger.start()
    processes_dict['generate_requests_logger'] = generate_requests_logger

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
                    
    @staticmethod
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

    @staticmethod
    def system_runner_worker(error_queue,run_or_stop_flag, run_requests_queue):
        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not run_requests_queue.empty():
                    try:
                        run_request = run_requests_queue.get_nowait()
                        #logging the request
                        result = RunMissionInterface.log_request(run_request=run_request)
                        # log error if somthing failed
                        if result.status >= 300:
                            error = ErrorLog(
                                             task_id = run_request['run_mission_id'],
                                             error_string=result.message,
                                             stage='logging a run request'
                                            )
                            error.log()
                            continue
                        run_status = result.data
                        db.session.add(run_status)
                        db.session.commit()
                        # execute the run request
                        result = RunMissionInterface.execute_request(run_status=run_status)
                        # log error if somthing failed
                        if result.status >= 300:
                            error = ErrorLog(
                                             task_id = run_request['run_mission_id'],
                                             error_string=result.message,
                                             stage='executing a run request'
                                            )
                            error.log()
                            continue
                        # if run mission row was created - create the mission for run script 
                        # AutoRunData, ComplexNet etc.
                    except:
                        print('exception in system runner')
                    finally:
                        db.session.close()

    @staticmethod
    def generate_requests_logger(error_queue,run_or_stop_flag, generate_requests_queue, to_generate_queue):
        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not generate_requests_queue.empty():
                    try:
                        gen_request = generate_requests_queue.get_nowait()
                        #getting task_id for the error log
                        if "gen_mission_id" in gen_request:
                            task_id = int(gen_request['gen_mission_id'])
                        else:
                            task_id = None
                        # execute the generate request
                        result = GenerateMissionInterface.log_request(gen_request=gen_request)
                        # log error if somthing failed
                        if result.status >= 300:
                            db.session.rollback()
                            error = ErrorLog(
                                             task_id = task_id,
                                             error_string=result.message,
                                             stage='logging a generate requests'
                                            )
                            error.log()
                            continue
                        
                        # log the statistics
                        statistics = result.data['statistics']
                        gen_statistics = GenerateStatistics(
                                            generate_status_id=None,
                                            generate_mission_id=gen_request['gen_mission_id'],
                                            succeeded=statistics['succeeded'],
                                            failed=statistics['failed'],
                                            total=statistics['failed']+statistics['succeeded'],
                                            stage_type=GenerateStageTypes.LOGGING
                                                            )
                        db.session.add(gen_statistics)

                        #complete the db trasaction
                        db.session.commit()

                        # loop requests logging results
                        results = result.data['results']
                        for res in results:
                            if res.status < 300:
                                gen_status = res.data
                                # if gen_request['to_run']:
                                #     run_request = {
                                #             "stage_id":gen_request['stage_id'],
                                #             "generate_mission_id":gen_request['gen_mission_id'],
                                #             "generate_status_id":gen_status.id,
                                #             "delete_after":gen_request['run_delete_after'],
                                #             "run_mission_id":gen_request['run_mission_id'],
                                #             "priority":gen_request['priority']
                                #         }
                                print(f"logged and pushed gen status id {gen_status.id}")
                                to_generate_queue.put_nowait((gen_status.id, gen_request))
                                # gen_result = GenerateMissionInterface.execute_request(gen_status)
                                # if gen_result.status < 300:
                                #     statistics = gen_result.data['gen_process']
                                #     generate_status_id = gen_result.data['generate_status_id']
                                #     for key, stat in statistics.items():
                                #         gen_statistics = GenerateStatistics(
                                #             generate_status_id=generate_status_id,
                                #             generate_mission_id=gen_request['gen_mission_id'],
                                #             succeeded=stat['succeeded'],
                                #             failed=stat['failed'],
                                #             total=stat['total'],
                                #             stage_type=stat['stage_type']
                                #                             )
                                #         db.session.add(gen_statistics)
                                #     db.session.commit()
                                    
                                # else:
                                #     error = ErrorLog(
                                #             task_id=task_id,
                                #             error_string=res.message,
                                #             stage='executing a generate request'
                                #         )
                                #     error.log()
                            else:
                                error = ErrorLog(
                                            task_id=task_id,
                                            error_string=res.message,
                                            stage='logging a generate request'
                                        )
                                error.log()
                    except:
                        db.session.rollback()
                        print('exception in generate requests logger')
                        try:
                            pass
                        except Exception as e:
                            pass
                    finally:
                        db.session.close()    

    @staticmethod
    def scenario_generator_worker(error_queue,run_or_stop_flag, to_generate_queue, run_requests_queue):
        process_app = create_process_app(db)
        with process_app.app_context():
            while run_or_stop_flag.is_set():
                if not to_generate_queue.empty():
                    try:
                        gen_status_id, gen_request = to_generate_queue.get_nowait()
                        gen_status = GenerateMissionStatus.query.get(gen_status_id)
                        gen_result = GenerateMissionInterface.execute_request(gen_status=gen_status)
                        if gen_result.status < 300:
                            statistics = gen_result.data['gen_process']

                            for key, stat in statistics.items():
                                gen_statistics = GenerateStatistics(
                                    generate_status_id=gen_status_id,
                                    generate_mission_id=gen_status.generate_mission_id,
                                    succeeded=stat['succeeded'],
                                    failed=stat['failed'],
                                    total=stat['total'],
                                    stage_type=stat['stage_type']
                                                    )
                                db.session.add(gen_statistics)
                                setattr(gen_status, key, stat['status'])
                            
                            db.session.commit()
                            print(f"generated gen status id {gen_status_id}")
                            if gen_request['to_run']:
                                run_request = {
                                            "stage_id":gen_request['stage_id'],
                                            "gen_mission_id":gen_request['gen_mission_id'],
                                            "generate_status_id":gen_status_id,
                                            "run_delete_after":gen_request['run_delete_after'],
                                            "gen_delete_after":gen_request['gen_delete_after'],
                                            "run_mission_id":gen_request['run_mission_id'],
                                            "priority":gen_request['priority']
                                        }
                                print(f"pushed run request with gen status id {gen_status_id}")
                                run_requests_queue.put_nowait(run_request)
                                
                        else:
                            error = ErrorLog(
                                    task_id=gen_status,
                                    error_string=res.message,
                                    stage='executing a generate request'
                                )
                            error.log()
                        
                        
                    except Exception as error:
                        db.session.rollback()
                        print('exception in scenario generator')
                        try:
                            pass
                        except Exception as e:
                            pass
                    finally:
                        db.session.close()
    
