var results_tab = $('#results_tab')[0];
var statistics_tab = $('#statistics_tab')[0];
var results_div = $('#results_div')[0];
var statistics_table_div = $('#statistics_table_div')[0];
var mission_names = []
var mission_name = $('#mission_name')[0];
var collapse_analyse_button = $('#collapse_analyse_button')[0];

var myWorker = null;

$('#collapse_analyse_button').click(function() {
    $('#collapse_analyse_button i').toggleClass("fa-minus-square");
    $('#collapse_analyse_button i').toggleClass("fa-plus-square");
});

results_tab.addEventListener('click', () => {
    statistics_tab.classList.remove('active')
    statistics_table_div.hidden = true;
    results_tab.classList.add('active')
    results_div.hidden = false;
});

statistics_tab.addEventListener('click', () => {
    results_tab.classList.remove('active');
    results_div.hidden = true;
    statistics_tab.classList.add('active');
    statistics_table_div.hidden = false;
});

function get_mission_names() {


    $.ajax({
        url: '/api/Mission/get_names',
        async: false,
        success: (data) => {
            mission_names = data;
        }
    });
    var mission_datalist = $('#mission_names_datalist')[0];

    mission_name.value = mission_names[0];
    numOfEle = mission_datalist.options.length;
    for (i = 0; i < numOfEle; i++) {
        mission_datalist.removeChild(mission_datalist.options[0]);
    }
    numOfEle = mission_names.length;

    for (i = 0; i < numOfEle; i++) {
        option = document.createElement('option');
        option.text = mission_names[i];
        mission_datalist.appendChild(option);
    }



}

function set_progressbar(percents) {

}

function set_header(percents) {
    set_progressbar(percents);
    // set_statistics();
    toggle_running(true)
}

// function set_content() {
//     set_tabs('Results');
//     hide_table();
//     show_loader();
// }

function init_widgets() {
    set_header(0);
    toggle_analyse_collapse(false);
    set_content();
}

function load_mission(mission_name) {
    // init_widgets();
    // myWorker = init_worker(mission_name);
    init_worker()
    $('#drill_down_div')[0].hidden = true;
    post_data = { "origin": window.location.origin, "analyse_mission_name": mission_name }
    myWorker.postMessage(post_data)
}



function load_init_analyse_data() {
    get_mission_names();
    load_mission(mission_names[0]);
}

function assign_event_analyse_listeners() {
    $('#mission_name')[0].addEventListener('change', () => {
        init_worker();
        post_data = { "origin": window.location.origin, "analyse_mission_name": $('#mission_name')[0].value };
        myWorker.postMessage(post_data);
    });
    // $('#results_table tbody').on('click', 'tr', function() {
    //     var data = table.row(this).data();
    //     alert('You clicked on ' + data[0] + '\'s row');
    // });
}

$(document).ready(() => {
    load_init_analyse_data();
    assign_event_analyse_listeners();
});

function toggle_running(bool) {
    if (bool) {
        // $('#run_status span')[0].classList.add("spinner-border");
        // $('#run_status span')[0].hidden = false;
        $('#run_status')[0].innerHTML = '&nbsp; Running...';
    } else {
        // $('#run_status span')[0].classList.remove("spinner-border")
        // $('#run_status span')[0].hidden = true;
        $('#run_status')[0].innerHTML = 'DONE!'
    }
}

function update_statistics(data) {
    myctx.hidden = false;
    $('#statistics_chart')[0].setAttribute('style', "display:block;height:500px;width:800px;")
    new_analyse_chart.data.datasets[0].data = data;
    new_analyse_chart.update();
}

function get_state_string(index) {
    switch (index) {
        case 0:
            return 'Needed';
        case 1:
            return "InDev";
        case 2:
            return "Completed";
    }
}

function convert_status(data) {
    converted_data = data;
    numOfEle = converted_data.table_data.length;
    ignore_keys = ["function name", "function state", "owner", "requirement"];
    for (i = 0; i < numOfEle; i++) {
        converted_data.table_data[i]["function state"] = get_state_string(converted_data.table_data[i]["function state"])
        keys = Object.keys(converted_data.table_data[i]);
        numOfKeys = keys.length;
        for (k = 0; k < numOfKeys; k++) {
            if (!ignore_keys.includes(keys[k]) && typeof(converted_data.table_data[i][keys[k]]) !== "string") {
                converted_data.table_data[i][keys[k]] = status_icons[String(converted_data.table_data[i][keys[k]])];
            }
        }
    }
    return converted_data;
}

function get_task_id(run_data, function_name) {
    var task_id = null;
    recieved_data.table_data.forEach((x) => { if (x['function name'] == function_name) { task_id = x[run_data + '-task id']; } });
    return task_id;
}

function update_meta_data(data) {

    //test data
    $('#test_status')[0].innerHTML = status_icons[String(data["test_result"]["status"])];
    time_elapsed = Math.round(data["test_result"]["time_elapsed"] * 1000).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + 'msec';
    $('#time_elapsed')[0].innerHTML = time_elapsed;

    //function data
    $('#function_name')[0].innerHTML = data["function_data"]["function name"];
    $('#function_state')[0].innerHTML = get_state_string(data["function_data"]["function state"]);
    $('#function_owner')[0].innerHTML = data["function_data"]["function owner"];

    //run data
    $('#db_name')[0].innerHTML = data["run_data"]["db"];
    $('#run_id')[0].innerHTML = data["run_data"]["run_id"];
    $('#scenario_name')[0].innerHTML = data["run_data"]["scenario"];

}

function init_res_workers(task_id) {
    //res array worker
    myResArrayWorker = new Worker(URL.createObjectURL(new Blob(["(" + results_array_worker_function.toString() + ")()"], { type: 'text/javascript' })));
    myResArrayWorker.onmessage = (e) => {
        if (myResArrayWorker) {
            myResArrayWorker.terminate();
            myResArrayWorker = null;
        }
        if (e.data.results_array) {
            update_drill_down_table(e.data.results_array)
            $('#drill_down_table_div')[0].hidden = false;
            $('#drill_down_div')[0].hidden = false;
        } else {
            $('#drill_down_table_div')[0].hidden = true;
        }
        // set_loading(false)
    }

    //res meta worker

    myResMetaWorker = new Worker(URL.createObjectURL(new Blob(["(" + results_meta_worker_function.toString() + ")()"], { type: 'text/javascript' })));
    myResMetaWorker.onmessage = (e) => {
        if (myResMetaWorker) {
            myResMetaWorker.terminate();
            myResMetaWorker = null;
        }
        if (e.data.function_data && e.data.run_data && e.data.test_result) {
            // update_drill_down_table(e.data.results_array)
            console.log(e.data);
            $('#drill_down_meta')[0].hidden = false;
            update_meta_data(e.data);
        } else {
            $('#drill_down_meta')[0].hidden = true;
        }
        // set_loading(false)
    }

    post_data = { "origin": window.location.origin, "task_id": task_id };

    myResArrayWorker.postMessage(post_data);
    myResMetaWorker.postMessage(post_data);
}

function init_worker() {
    if (myWorker) {
        myWorker.terminate();
        myWorker = null;
    }
    myWorker = new Worker(URL.createObjectURL(new Blob(["(" + analyse_worker_function.toString() + ")()"], { type: 'text/javascript' })));
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

function s2ab(s) {
    var buf = new ArrayBuffer(s.length);
    var view = new Uint8Array(buf);
    for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
    return buf;
}

$("#export_to_excel_button")[0].addEventListener('click', () => {
    var wb = XLSX.utils.table_to_book(document.getElementById('results_table'), { sheet: "Sheet JS" });
    var wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'binary' });
    saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), 'test.xlsx');
});