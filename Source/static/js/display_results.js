var current_results = null;
var results_table_div = $('#results_table_div')[0];
var results_table = $('#results_table')[0];
var results_header = document.createElement('h1');
var drill_down_result = null;
var drill_down_table_div = $('#drill_down_table_div')[0];
var drill_down_table = $('#drill_down_table')[0];
var drill_down_div = $('#drill_down_div')[0];
var drill_down_header = $('#drill_down_header')[0];
var drill_down_run_id = $('#drill_down_run_id')[0];
var drill_down_function_name = $('#drill_down_function_name')[0];
var drill_down_db_name = $('#drill_down_db_name')[0];
var result_status = $('#result_status')[0];
var result_text = $('#result_text')[0];
var statistics = {
    success: 0,
    warning: 0,
    fail: 0,
    error: 0,
    nodata: 0
};
results_table_div.appendChild(results_header);


function clear_drill_down() {
    drill_down_header.innerHTML = null;
    drill_down_function_name.innerHTML = null;
    drill_down_run_id.innerHTML = null;
    drill_down_db_name.innerHTML = null;
    result_status.innerHTML = null;
    result_text.innerHTML = null;
    drill_down_table_div.removeChild(drill_down_table)
    drill_down_table = document.createElement('table');
    drill_down_table.id = 'drill_down_table';
    drill_down_table.classList.add(["table"]);
    drill_down_table.classList.add(["table-hover"]);
    drill_down_table.classList.add(["col-10"]);
    drill_down_table.classList.add(["m-auto"]);
    drill_down_table_div.appendChild(drill_down_table);
}
// drill_down_div.appendChild(drill_down_header);
// drill_down_div.appendChild(drill_down_function_name);
// drill_down_div.appendChild(drill_down_run_id);
// drill_down_div.appendChild(drill_down_db_name);
// drill_down_div.appendChild(drill_down_table);
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function get_mission_ids() {
    var select_obj = $('#mission_id_select')[0];
    $.ajax({
        url: "/api/Mission/get_ids",
        success: function(result) {
            var num_of_missions = result.length;
            var num_of_curr_missions = select_obj.options.length;
            for (i = 0; i < num_of_curr_missions; i++) {
                select_obj.remove(0);
            }
            for (i = 0; i < num_of_missions; i++) {
                opt = document.createElement('option');
                opt.text = result[i]
                select_obj.appendChild(opt);
            }
            sleep(2000);
            load_results();
            // clear_drill_down();
        }
    });
}

function drill_down() {
    run_id = current_results.schema.fields[this.cellIndex].name;
    function_name = current_results.data[this.parentElement.rowIndex - 2].function_name;
    result_id = current_results.data[this.parentElement.rowIndex - 2][run_id].result_id;
    $.ajax({
        url: "/api/AnalyseResult/jsonify_by_ids/" + result_id,
        success: function(result) {
            drill_down_result = result;

            drill_down_header.innerHTML = 'Result array for result id: ' + result_id;

            drill_down_function_name.innerHTML = 'Function name: ' + function_name;
            drill_down_run_id.innerHTML = 'Run id: ' + run_id;
            drill_down_db_name.innerHTML = 'DB name: ' + drill_down_result[0].db_conn;
            result_status.innerHTML = 'Result Status: ' + drill_down_result[0].result_status;
            result_text.innerHTML = 'Result Text: ' + drill_down_result[0].result_text;
            drill_down_table_div.removeChild(drill_down_table)
            drill_down_table = document.createElement('table');
            drill_down_table.id = 'drill_down_table';
            drill_down_table.classList.add(["table"]);
            drill_down_table.classList.add(["table-hover"]);
            drill_down_table.classList.add(["col-10"]);
            drill_down_table.classList.add(["m-auto"]);
            drill_down_table_div.appendChild(drill_down_table);
            num_of_cols = result[0].result_array.schema.fields.length;
            num_of_rows = result[0].result_array.data.length;
            newRow = drill_down_table.insertRow(-1);

            // newRow.appendChild(th);
            // th.colspan = num_of_cols; 
            newRow = drill_down_table.insertRow(-1);
            // newRow.insertCell(0);
            for (i = 0; i < num_of_cols - 1; i++) {
                th = document.createElement('th');
                th.innerHTML = result[0].result_array.schema.fields[i].name;
                th.bgColor = 'gray';
                newRow.appendChild(th);
            }
            for (i = 0; i < num_of_rows; i++) {
                newRow = drill_down_table.insertRow(-1);
                for (j = 0; j < num_of_cols - 1; j++) {
                    td = document.createElement('td');
                    var status = result[0].result_array.data[i][result[0].result_array.schema.fields[j].name];

                    td.innerHTML = status;
                    newRow.appendChild(td);
                }
            }
        },
        error() {
            clear_drill_down();
        }
    });
}

function load_results() {
    var select_obj = $('#mission_id_select')[0];
    mission_id = select_obj.options[select_obj.selectedIndex].text;
    $.ajax({
        url: "/api/AnalyseResult/jsonify_by_mission_id/" + mission_id,
        success: function(result) {
            current_results = result;
            results_header.innerHTML = 'Results for mission ' + mission_id;
            results_table_div.removeChild(results_table)
            results_table = document.createElement('table');
            results_table.id = 'results_table';
            results_table.classList.add(["table"]);
            results_table.classList.add(["table-hover"]);
            results_table.classList.add(["col-10"]);
            results_table.classList.add(["m-auto"]);
            results_table_div.appendChild(results_table);
            if (result === null) {
                ctx.hidden = true;
                // myChart.data.datasets[0].data = [statistics.success, statistics.warning, statistics.fail, statistics.error, statistics.nodata];
                myChart.update();
                clear_drill_down();
                alert('no data');
            }
            num_of_cols = result.schema.fields.length;
            num_of_rows = result.data.length;
            newRow = results_table.insertRow(-1);

            // newRow.appendChild(th);
            // th.colspan = num_of_cols; 
            newRow = results_table.insertRow(-1);
            // newRow.insertCell(0);
            for (i = 0; i < num_of_cols; i++) {
                th = document.createElement('th');
                th.innerHTML = result.schema.fields[i].name;
                newRow.appendChild(th);
            }
            statistics.success = 0;
            statistics.warning = 0;
            statistics.fail = 0;
            statistics.error = 0;
            statistics.nodata = 0;
            for (i = 0; i < num_of_rows; i++) {
                newRow = results_table.insertRow(-1);
                for (j = 0; j < num_of_cols; j++) {
                    td = document.createElement('td');
                    td.addEventListener("click", drill_down);
                    if (j == 0) {
                        var status = result.data[i][result.schema.fields[j].name];
                    } else {
                        var status = result.data[i][result.schema.fields[j].name].status;
                        // var status_text = '';


                        if (j > 0) {
                            switch (status) {
                                case 0:
                                    status = 'No Data';
                                    td.bgColor = 'blue';
                                    statistics.nodata += 1;
                                    break;
                                case 1:
                                    status = 'Error';
                                    td.bgColor = 'gray';
                                    statistics.error += 1;
                                    break;
                                case 2:
                                    status = 'Fail';
                                    td.bgColor = 'red';
                                    statistics.fail += 1;
                                    break;
                                case 3:
                                    status = 'Warning';
                                    td.bgColor = 'orange';
                                    statistics.warning += 1;
                                    break;
                                case 4:
                                    status = 'Success';
                                    td.bgColor = 'green';
                                    statistics.success += 1;
                                    break;
                                default:
                                    status = 'in process';
                                    // td.bgColor = 'green';
                                    break;
                            }
                        }
                    }
                    td.innerHTML = status;
                    newRow.appendChild(td);
                }
            }
            ctx.hidden = false;
            myChart.data.datasets[0].data = [statistics.success, statistics.warning, statistics.fail, statistics.error, statistics.nodata];

            myChart.update();
            clear_drill_down();
        }
    });
}

$('#display_button')[0].addEventListener('click', load_results);



get_mission_ids();