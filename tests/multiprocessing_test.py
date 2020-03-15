import pandas as pd
from time import time
from threading import Thread
from queue import Queue

def write_reports_list(reports_list, index):
    global data
    file_name = 'Reports' + str(index) + '.xlsx'
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    for name in reports_list:
        data.to_excel(writer, sheet_name=name)
    writer.save()


def worker_write_report():
    global q
    while True:
        if q.empty():
            break
        num, name = q.get()
        write_reports_list([name], num)
        q.task_done()

def write_report_async(reports_list):
    threads = []

    for num, report in enumerate(reports_list):
        t = Thread(target=write_reports_list, args=([report], num))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def write_report_async_with_queue():
    workers = []
    num_of_workers = 30
    for _ in range(num_of_workers):
        worker = Thread(target=worker_write_report)
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    ###################################
    #####       SETUP          ########
    ###################################
    num_of_rows = 10000
    num_of_cols = 10
    num_of_reports = 30
    q = Queue()
    dict_data = {'col' + str(num):range(num_of_rows) for num in range(num_of_cols)}
    data = pd.DataFrame(dict_data)


    ###################################
    ####  CREATING LIST AND QUEUE  ####
    ###################################
    reports_list = ['report_' + str(num) for num in range(num_of_reports)]
    [q.put_nowait((num+30,name)) for num, name in enumerate(reports_list)]

    ###################################
    ####    TESTING EACH METHOD    ####
    ###################################
    t1 = time()
    write_report_async(reports_list)
    print(f'syncronic writing took {time() - t1} seconds')

    t1 = time()
    write_report_async_with_queue()
    print(f'syncronic writing with queue took {time() - t1} seconds')

    t1 = time()
    write_reports_list(reports_list, 60)
    print(f'syncronic writing took {time() - t1} seconds')