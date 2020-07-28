var runs_tab = $('#runs_tab')[0];
var runs_table_div = $('#runs_table_div')[0];

var functions_tab = $('#functions_tab')[0];
var functions_table_div = $('#functions_table_div')[0];

var groups_tab = $('#groups_tab')[0];
var groups_table_div = $('#groups_table_div')[0];

var lists_tab = $('#lists_tab')[0];
var lists_table_div = $('#lists_table_div')[0];

var setup_toggle = $('#setup_toggle')[0];
var database_select = $('#database_select')[0];
var collapse_setup_button = $('#collapse_setup_button')[0];

var connections = null;
var dbs_list = {};
var selected_run_ids = {};
var selected_lists = {};
var selected_functions = {};
var selected_groups = {};

var chosen_functions_select = $('#chosen_functions_select')[0];
var chosen_runs_select = $('#chosen_runs_select')[0];
var database_select = $('#database_select')[0];

function load_run_ids(db_name) {
    runs_table.ajax.async = false;
    runs_table.ajax.url("/api/DbConnector/get_run_ids_json/" + db_name).load();
    selected_runs = Object.keys(selected_run_ids[db_name]);
    $('#runs_table').find('tr').each((index) => {
        row = $('#runs_table').find('tr')[index];
        if (selected_runs.includes(row.cells[0].innerHTML)) {
            row.hidden = true;
        }
    });
}

function get_db_names() {
    var num_of_options = database_select.options.length;
    for (i = 0; i < num_of_options; i++) {
        database_select.remove(0);
    }
    $.ajax({
        url: "/api/DbConnections/get_names",
        async: false,
        success: function(conn_names) {
            connections = conn_names;
            var num_of_conns = conn_names.length;
            for (i = 0; i < num_of_conns; i++) {
                var option = document.createElement("option");
                option.text = conn_names[i];
                database_select.add(option);

                dbs_list[conn_names[i]] = {};
                selected_run_ids[conn_names[i]] = {};

                // load_run_ids(database_select.options[0].text);
                // get_all_functions();
            }
        }
    });
}

//getting all initial data - functions, dbs list+run_ids
function load_init_data() {
    get_db_names();
    setTimeout(200);
    load_run_ids(connections[0]);
    // get_all_functions();
}

function assign_event_listeners() {
    database_select.addEventListener('change', () => { load_run_ids(database_select.options[database_select.selectedIndex].text) });
    $('#collapse_setup_button').click(() => {
        $('#collapse_setup_button i').toggleClass("fa-minus-square");
        $('#collapse_setup_button i').toggleClass("fa-plus-square");
    });

    $('#collapse_analyse_button').click(() => {
        $('#collapse_analyse_button i').toggleClass("fa-minus-square");
        $('#collapse_analyse_button i').toggleClass("fa-plus-square");
    });

    runs_tab.addEventListener('click', () => {
        functions_tab.classList.remove('active')
        functions_table_div.hidden = true;

        runs_tab.classList.add('active')
        runs_table_div.hidden = false;

        groups_tab.classList.remove('active');
        groups_table_div.hidden = true;

        lists_tab.classList.remove('active');
        lists_table_div.hidden = true;
    });

    functions_tab.addEventListener('click', () => {
        functions_tab.classList.add('active');
        functions_table_div.hidden = false;

        runs_tab.classList.remove('active');
        runs_table_div.hidden = true;

        groups_tab.classList.remove('active');
        groups_table_div.hidden = true;

        lists_tab.classList.remove('active');
        lists_table_div.hidden = true;
    });

    groups_tab.addEventListener('click', () => {
        functions_tab.classList.remove('active');
        functions_table_div.hidden = true;

        runs_tab.classList.remove('active');
        runs_table_div.hidden = true;

        groups_tab.classList.add('active');
        groups_table_div.hidden = false;

        lists_tab.classList.remove('active');
        lists_table_div.hidden = true;
    });

    lists_tab.addEventListener('click', () => {
        functions_tab.classList.remove('active');
        functions_table_div.hidden = true;

        runs_tab.classList.remove('active');
        runs_table_div.hidden = true;

        groups_tab.classList.remove('active');
        groups_table_div.hidden = true;

        lists_tab.classList.add('active');
        lists_table_div.hidden = false;
    });

    $('#select_all_button').click(() => {
        if ($('#functions_tab').hasClass('active')) {
            $("#functions_table").selectable().find('tr').each((index) => {
                if ($("#functions_table").selectable().find('tr')[index].hidden == false && index > 0) {
                    $("#functions_table").selectable().find('tr')[index].classList.add('selected');
                }
            });
        }
        if ($('#groups_tab').hasClass('active')) {
            $("#groups_table").selectable().find('tr').each((index) => {
                if ($("#groups_table").selectable().find('tr')[index].hidden == false && index > 0) {
                    $("#groups_table").selectable().find('tr')[index].classList.add('selected');
                }
            });
        }
        if ($('#runs_tab').hasClass('active')) {
            $("#runs_table").selectable().find('tr.selected').addClass('selected');
            $("#runs_table").selectable().find('tr').each((index) => {
                if ($("#runs_table").selectable().find('tr')[index].hidden == false && index > 0) {
                    $("#runs_table").selectable().find('tr')[index].classList.add('selected');
                }
            });
        }
    });

    $('#remove_selection_button').click(() => {
        if ($('#functions_tab').hasClass('active')) {
            $("#functions_table").selectable().find('tr.selected').removeClass('selected');
        }
        if ($('#groups_tab').hasClass('active')) {
            $("#groups_table").selectable().find('tr.selected').removeClass('selected');
        }
        if ($('#runs_tab').hasClass('active')) {
            $("#runs_table").selectable().find('tr.selected').removeClass('selected');
        }
    });
    $('#add_selected_button').click(() => {
        if ($('#functions_tab').hasClass('active')) {
            $("#functions_table").find('tr.selected').each((index) => {
                row = $("#functions_table").find('tr.selected')[index];
                row_index = $("#functions_table").find('tr.selected')[index].rowIndex
                row.hidden = true;
                option = document.createElement('option');
                option.text = row.cells[0].innerHTML;
                selected_functions[option.text] = { "index": row_index, "isFunctions": true };
                chosen_functions_select.add(option);
            });
            $("#functions_table").find('tr.selected').removeClass('selected');
        }
        if ($('#groups_tab').hasClass('active')) {
            $("#groups_table").find('tr.selected').each((index) => {
                row = $("#groups_table").find('tr.selected')[index];
                row_index = $("#groups_table").find('tr.selected')[index].rowIndex
                row.hidden = true;
                option = document.createElement('option');
                option.text = row.cells[0].innerHTML + '(group)';
                selected_functions[option.text] = { "index": row_index, "isFunctions": false };
                chosen_functions_select.add(option);
            });
            $("#groups_table").find('tr.selected').removeClass('selected');
        }
        if ($('#runs_tab').hasClass('active')) {
            db_name = database_select.options[database_select.options.selectedIndex].text;
            $("#runs_table").find('tr.selected').each((index) => {
                row = $("#runs_table").find('tr.selected')[index];
                row_index = $("#runs_table").find('tr.selected')[index].rowIndex
                row.hidden = true;
                option = document.createElement('option');
                option.text = row.cells[0].innerHTML + ' - ' + db_name;
                selected_run_ids[db_name][row.cells[0].innerHTML] = { "index": row_index, "isRunId": true };
                chosen_runs_select.add(option);
            });
            $("#runs_table").find('tr.selected').removeClass('selected');
        }
        if ($('#lists_tab').hasClass('active')) {
            $("#lists_table").find('tr.selected').each((index) => {
                row = $("#lists_table").find('tr.selected')[index];
                row_index = $("#lists_table").find('tr.selected')[index].rowIndex
                row.hidden = true;
                option = document.createElement('option');
                option.text = row.cells[0].innerHTML + '(list)';
                selected_lists[row.cells[0].innerHTML] = { "index": row_index, "is_RunId": false };
                chosen_runs_select.add(option);
            });
            $("#lists_table").find('tr.selected').removeClass('selected');
        }
    });

    $('#remove_function_button').click(() => {
        selected_options = chosen_functions_select.selectedOptions;
        numOfEle = selected_options.length;
        for (index = 0; index < numOfEle; index++) {
            option_name = selected_options[0].text;
            option_index = selected_options[0].index
            is_functions = selected_functions[option_name].isFunctions;
            row_index = selected_functions[option_name].index;
            chosen_functions_select.remove(option_index);
            if (is_functions) {
                $("#functions_table").find('tr')[row_index].hidden = false;
            } else {
                $("#groups_table").find('tr')[row_index].hidden = false;
            }
            delete selected_functions[option_name]
        }
    });

    $('#remove_run_button').click(() => {
        selected_options = chosen_runs_select.selectedOptions;
        numOfEle = selected_options.length;

        db_name = database_select.options[database_select.options.selectedIndex].text;
        for (index = 0; index < numOfEle; index++) {
            if (selected_options[0].text.search('(list)') > -1) {
                option_list = selected_options[0].text;
                option_index = selected_options[0].index
                row_index = selected_lists[option_list].index;
                chosen_runs_select.remove(option_index);
                if ($('#lists_tab').hasClass('active')) {
                    $("#lists_table").find('tr')[row_index].hidden = false;
                }
                delete selected_lists[option_list]
            } else {
                option_run_id = selected_options[0].text.split(' - ')[0];
                option_db = selected_options[0].text.split(' - ')[1];
                option_index = selected_options[0].index
                row_index = selected_run_ids[option_db][option_run_id].index;
                chosen_runs_select.remove(option_index);
                if ($('#runs_tab').hasClass('active')) {
                    if (db_name == option_db) {
                        $("#runs_table").find('tr')[row_index].hidden = false;
                    }
                }
                delete selected_run_ids[option_db][option_run_id]
            }
        }
    });
}

//Start from here
$(document).ready(() => {
    load_init_data();
    assign_event_listeners();
});