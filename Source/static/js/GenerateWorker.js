function generate_worker_function() {
    // importScripts('../js/jquery_3_4_1_min.js')
    var data = 0;
    var run_flag = 0;

    function wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        origin = e.data.origin;
        mission_id = e.data.mission_id;
        while (true) {
            await wait(1000)
            await fetch(origin + "/dummyapi/GenerateMission/get_by_id/" + mission_id).then(response => response.json())
                .then((data) => postMessage(data));
        }
    }
}



function init_worker() {
    if (myWorker) {
        myWorker.terminate();
        myWorker = null;
    }
    myWorker = new Worker(URL.createObjectURL(new Blob(["(" + generate_worker_function.toString() + ")()"], { type: 'text/javascript' })));
    toggle_running(true);
    $('#progress_bar')[0].setAttribute('aria-valuenow', String(0));
    $('#progress_bar')[0].setAttribute('style', "width: " + String(0) + "%");
    $('#progress_text')[0].innerHTML = String(0) + "% Completed";
    $('#statistics_div')[0].innerHTML = ''
    myWorker.onmessage = (e) => {
        if (!e.data.status) {
            myWorker.terminate();
            //     show_error();
            myWorker = null;
            toggle_running(false);
            return false;
        }
        inprocess = e.data.data.statistics[7];
        all_tests = e.data.data.statistics.reduce(function(a, b) {
            return a + b;

        }, 0)
        functions_counter = e.data.data.table_data.length;
        if (functions_counter > 0) {
            runs_counter = all_tests / functions_counter
            if (e.data.data.is_done) {
                myWorker.terminate();
                myWorker = null;
                toggle_running(false);
                $('#progress_bar')[0].setAttribute('aria-valuenow', String(100));
                $('#progress_bar')[0].setAttribute('style', "width: " + String(100) + "%");
                $('#progress_text')[0].innerHTML = String(100) + "% Completed";
                $('#statistics_div')[0].innerHTML = String(functions_counter) + " functions on " + String(runs_counter) + " runs : " + String(all_tests) + "/" + String(all_tests) + " completed"
            } else {
                percents = Math.floor(100 - (inprocess / all_tests) * 100);
                // set_header(percents)
                $('#progress_bar')[0].setAttribute('aria-valuenow', String(percents));
                $('#progress_bar')[0].setAttribute('style', "width: " + String(percents) + "%");
                $('#progress_text')[0].innerHTML = String(percents) + "% Completed";
                $('#statistics_div')[0].innerHTML = String(functions_counter) + " functions on " + String(runs_counter) + " runs : " + String(all_tests - inprocess) + "/" + String(all_tests) + " completed"

            }
        } else {
            $('#statistics_div')[0].innerHTML = 'waiting for worker data'
        }
        recieved_data = e.data.data;
        converted_data = convert_status(e.data.data);
        update_statistics(converted_data.statistics);
        update_table(converted_data);
        $('#results_table td').on('click', (e) => {

            if (e.target.className == '') {
                td = e.target;
            }
            if (e.target.className.split(' ').includes('status')) {
                td = e.target.parentElement;
            }
            if (e.target.className.split(' ').includes('fas')) {
                td = e.target.parentElement.parentElement;
            }
            run_data = results_table.rows[0].children[td.cellIndex].innerHTML;
            function_name = results_table.rows[td.parentElement.rowIndex].children[0].innerHTML;
            task_id = get_task_id(run_data, function_name)
                // clear_drill_down()
                // set_loading(true)
            init_res_workers(task_id);
        });
    }
}




function toggle_running(bool) {
    if (bool) {
        $('#run_status')[0].innerHTML = '&nbsp; Running...';
    } else {
        $('#run_status')[0].innerHTML = 'DONE!'
    }
}