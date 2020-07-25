var runs_tab = $('#runs_tab')[0];
var functions_tab = $('#functions_tab')[0];
var functions_table_div = $('#functions_table_div')[0];
var runs_table_div = $('#runs_table_div')[0];
var setup_toggle = $('#setup_toggle')[0];
var database_select = $('#database_select')[0];
var collapse_setup_button = $('#collapse_setup_button')[0];

var connections = null;
var dbs_list = {};
var selected_run_ids = {};


function load_run_ids(db_name) {
    runs_table.ajax.url("/api/DbConnector/get_run_ids_json/" + db_name).load();
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

    runs_tab.addEventListener('click', () => {
        functions_tab.classList.remove('active')
        functions_table_div.hidden = true;
        runs_tab.classList.add('active')
        runs_table_div.hidden = false;
    });

    functions_tab.addEventListener('click', () => {
        runs_tab.classList.remove('active');
        runs_table_div.hidden = true;
        functions_tab.classList.add('active');
        functions_table_div.hidden = false;
    });
}

//Start from here
$(document).ready(() => {
    load_init_data();
    assign_event_listeners();
});