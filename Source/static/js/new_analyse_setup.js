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
var run_setup_button = $('#run_setup_button')[0];

var connections = null;
var dbs_list = {};
var selected_run_ids = {};
var selected_lists = {};
var selected_functions = {};
var selected_groups = {};

var num_of_functions = 0;
var num_of_runs = 0;

var chosen_functions_select = $('#chosen_functions_select')[0];
var chosen_runs_select = $('#chosen_runs_select')[0];
var database_select = $('#database_select')[0];

var setup_names = [];
var curr_setup_name = '';
var action = '';

function save_list(list_name) {
    if (list_name.replace(' ', '').length == 0) {
        $('#save_list_dissmisable_text')[0].innerHTML = "list name cannot be empty";
        $('#save_list_alert')[0].hidden = false;
        // alert('list name cannot be empty')
        return 0;
    }
    dbs = Object.keys(selected_run_ids);
    num_of_dbs = dbs.length;
    var data = {};
    data['run_ids'] = [];
    var z = 0;
    for (i = 0; i < num_of_dbs; i++) {
        runs = Object.keys(selected_run_ids[dbs[i]]);
        numOfRuns = runs.length
        for (k = 0; k < numOfRuns; k++) {
            data['run_ids'][z] = {
                "db": dbs[i],
                "run_id": runs[k],
                "scenario": selected_run_ids[dbs[i]][runs[k]].scenario
            }
            z = z + 1;
        }
    }
    lists = Object.keys(selected_lists);
    numOfEle = lists.length;
    data['lists'] = []
    for (k = 0; k < numOfEle; k++) {
        lists[k] = lists[k].split('(')[0];
    }
    if (numOfEle > 0) {
        data['lists'] = lists;
    }
    if (data['lists'].length + data['run_ids'].length == 0) {
        $('#save_list_dissmisable_text')[0].innerHTML = "cannot save an empty list";
        $('#save_list_alert')[0].hidden = false;
        // alert('cannot save an empty list')
        return 0;
    }
    data['name'] = list_name;
    $.ajax({
            url: '/api/RunList/save',
            type: "POST",
            dataType: "json",
            async: false,
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: (response) => {
                lists_table.ajax.reload();
                lists = Object.keys(selected_lists);
                $('#lists_table').find('tr').each((index) => {
                    row = $('#lists_table').find('tr')[index];
                    if (lists.includes(row.cells[0].innerHTML + '(list)')) {
                        row.hidden = true;
                    }
                });
            },
            error: () => {
                $('#save_list_dissmisable_text')[0].innerHTML = "something went wrong";
                $('#save_list_alert')[0].hidden = false;
                // alert('something went wrong')
                return 0;
            }
        },

    );
    $('#save_list_dissmisable_text')[0].innerHTML = "list saved";
    $('#save_list_alert')[0].hidden = false;
    // alert('success')
    return 1;

}

function get_setup_data() {
    var data = {};
    data['status'] = 0;

    //getting and validating name
    data['name'] = $('#setup_name')[0].value;
    if (data['name'].replace(' ', '').length == 0) {
        $('#main_dissmisable_alert_text')[0].innerHTML = "name cannot be empty";
        $('#main_alert')[0].hidden = false;
        // alert('name cannot be empty');
        return data;
    }

    //getting runs
    dbs = Object.keys(selected_run_ids);
    num_of_dbs = dbs.length;


    data['runs'] = [];
    var z = 0;
    for (i = 0; i < num_of_dbs; i++) {
        runs = Object.keys(selected_run_ids[dbs[i]]);
        numOfRuns = runs.length
        for (k = 0; k < numOfRuns; k++) {
            data['runs'][z] = {
                "db_name": dbs[i],
                "run_id": runs[k],
                "scenario_name": selected_run_ids[dbs[i]][runs[k]].scenario
            }
            z = z + 1;
        }
    }

    //getting lists
    lists = Object.keys(selected_lists);
    numOfEle = lists.length;
    data['run_lists'] = [];
    for (k = 0; k < numOfEle; k++) {
        lists[k] = lists[k].split('(')[0];
    }
    if (numOfEle > 0) {
        data['run_lists'] = lists;
    }

    //validating we do not have 0 runs
    if (data['run_lists'].length + data['runs'].length == 0) {
        $('#main_dissmisable_alert_text')[0].innerHTML = "cannot save a setup with 0 runs";
        $('#main_alert')[0].hidden = false;
        // alert('cannot save a setup with 0 runs');
        return data;
    }

    //validating we do not have 0 functions
    keys = Object.keys(selected_functions);
    numOfEle = keys.length
    if (numOfEle == 0) {
        $('#main_dissmisable_alert_text')[0].innerHTML = "cannot save a setup with 0 functions";
        $('#main_alert')[0].hidden = false;
        // alert('cannot save a setup with 0 functions');
        return data;
    }

    data['functions'] = [];
    data['groups'] = [];
    var z = 0;
    var t = 0;
    for (k = 0; k < numOfEle; k++) {
        if (selected_functions[keys[k]]['isFunctions']) {
            data['functions'][z] = keys[k];
            z = z + 1;
        } else {
            data['groups'][t] = keys[k].split('(')[0];
            t = t + 1;
        }

    }


    data['status'] = 1;
    return data;
}

function save_setup(data) {
    var status = 0;
    $.ajax({
        url: '/api/AnalyseSetup/save',
        type: "POST",
        dataType: "json",
        async: false,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            status = response.status;
            if (response.status) {
                $('#main_dissmisable_alert_text')[0].innerHTML = "setup saved";
                $('#main_alert')[0].hidden = false;
                // alert('success');
            } else {
                $('#main_dissmisable_alert_text')[0].innerHTML = response.message;
                $('#main_alert')[0].hidden = false;
                // alert('something went wrong');
            }
        },
        error: () => {
            $('#main_dissmisable_alert_text')[0].innerHTML = "something went wrong";
            $('#main_alert')[0].hidden = false;
            // alert('something went wrong');
        }
    });
    return status;
}

function update_setup(data) {
    $.ajax({
        url: '/api/AnalyseSetup/update_by_name/' + current_setup.name,
        type: "POST",
        dataType: "json",
        async: false,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: (response) => {
            if (response.status) {
                $('#dissmisable_main_alert_text')[0].innerHTML = "setup updated";
                $('#main_alert')[0].hidden = false;
                // alert('success');
            } else {
                $('#main_dissmisable_alert_text')[0].innerHTML = response.message;
                $('#main_alert')[0].hidden = false;
                // alert('something went wrong');
            }
        },
        error: () => {
            $('#main_dissmisable_alert_text')[0].innerHTML = "something went wrong";
            $('#main_alert')[0].hidden = false;
            // alert('something went wrong');
        }
    });
}

function load_run_ids(db_name) {
    runs_table.ajax.async = false;
    runs_table.ajax.url("/api/DbConnector/get_run_ids_json/" + db_name).load();
    runs_table.draw();
    selected_runs = Object.keys(selected_run_ids[db_name]);
    $('#runs_table').find('tr').each((index) => {
        row = $('#runs_table').find('tr')[index];
        if (selected_runs.includes(row.cells[0].innerHTML)) {
            row.hidden = true;
            selected_run_ids[db_name][row.cells[0].innerHTML].index = index;
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

function calculate_group_num_of_functions(group_name) {
    $.ajax({
        url: '/api/FunctionsGroup/get_num_of_functions_by_name/' + group_name,
        async: false,
        success: (response) => {
            group_num_of_functions = response.data;
        },
        error: () => {
            group_num_of_functions = 0;
        }
    });
    return group_num_of_functions;
}

function calculate_list_num_of_runs(list_name) {
    $.ajax({
        url: '/api/RunList/get_num_of_runs_by_name/' + list_name,
        async: false,
        success: (response) => {
            list_num_of_runs = response.data;
        },
        error: () => {
            list_num_of_runs = 0;
        }
    });
    return list_num_of_runs;
}
//getting all initial data - functions, dbs list+run_ids
function load_init_setup_data() {
    get_db_names();
    setTimeout(200);
    load_run_ids(connections[0]);
    // get_all_functions();
}

function load_setup_names() {
    $.ajax({
        url: 'api/AnalyseSetup/get_names',
        async: false,
        success: (response) => {
            setup_names = response.data;
            datalist_obj = $('#setups_datalist')[0];
            numOfEle = datalist_obj.options.length;
            for (i = 0; i < numOfEle; i++) {
                datalist_obj.removeChild(datalist_obj.options[0]);
            }
            numOfEle = setup_names.length;
            for (i = 0; i < numOfEle; i++) {
                var option = document.createElement("option");
                option.value = setup_names[i];
                datalist_obj.appendChild(option);
            }
        }
    });
}

function clear_setup() {
    selected_functions = {};
    selected_groups = {};
    selected_lists = {};
    selected_dbs = Object.keys(selected_run_ids);
    numOfEle = selected_dbs.length;
    for (i = 0; i < numOfEle; i++) {
        selected_run_ids[selected_dbs[i]] = [];
    }
    $("#functions_table").find('tr').each((index) => {
        $("#functions_table").find('tr')[index].hidden = false;
    })
    $("#lists_table").find('tr').each((index) => {
        $("#lists_table").find('tr')[index].hidden = false;
    })
    $("#groups_table").find('tr').each((index) => {
        $("#groups_table").find('tr')[index].hidden = false;
    })
    $("#runs_table").find('tr').each((index) => {
        $("#runs_table").find('tr')[index].hidden = false;
    })

    numOfEle = chosen_functions_select.options.length;
    for (i = 1; i < numOfEle; i++) {
        chosen_functions_select.remove(numOfEle - i);
    }

    numOfEle = chosen_runs_select.options.length;
    for (i = 1; i < numOfEle; i++) {
        chosen_runs_select.remove(numOfEle - i);
    }

    num_of_functions = 0;
    num_of_runs = 0;
    $('#num_of_functions')[0].innerHTML = 'Total : 0 functions';
    $('#num_of_runs')[0].innerHTML = 'Total : 0 runs';
    $('#num_of_tests')[0].innerHTML = 'Total : 0 tests';
    $('#statistics_text')[0].innerHTML = String(num_of_functions) + ' functions on ' + String(num_of_runs) + ' runs : ' + String(num_of_runs * num_of_functions) + ' tests';
    $('#setup_name')[0].value = '';
    $('#curr_setup_name')[0].innerHTML = ''
    curr_setup_name = ''
}

function load_setup(setup_name) {
    $('#setup_name')[0].value = setup_name;
    curr_setup_name = setup_name;
    $('#curr_setup_name')[0].innerHTML = curr_setup_name;
    $.ajax({
        url: 'api/AnalyseSetup/get_by_name/' + setup_name,
        async: false,
        success: (response) => {
            current_setup = response.data;
            $('#setup_name')[0].value = current_setup.name;
            $("#functions_table").find('tr').each((index) => {
                //selecting fuctions
                if (current_setup.functions.includes($("#functions_table").find('tr')[index].cells[0].innerHTML)) {
                    $("#functions_table").find('tr')[index].classList.add('selected');
                }
            });
            add_selected_functions();

            $("#groups_table").find('tr').each((index) => {
                //selecting groups
                if (current_setup.groups.includes($("#groups_table").find('tr')[index].cells[0].innerHTML)) {
                    $("#groups_table").find('tr')[index].classList.add('selected');
                }
            });
            add_selected_groups();

            $("#lists_table").find('tr').each((index) => {
                //selecting lists
                if (current_setup.run_lists.includes($("#lists_table").find('tr')[index].cells[0].innerHTML)) {
                    $("#lists_table").find('tr')[index].classList.add('selected');
                }
            });
            add_selected_lists();

            $("#runs_table").find('tr').each((index) => {
                db_name = $('#database_select')[0].options[database_select.options.selectedIndex].text;
                if (Object.keys(current_setup.runs).includes(db_name)) {
                    runs = Object.keys(current_setup.runs[db_name]);
                    if (runs.includes($("#runs_table").find('tr')[index].cells[0].innerHTML)) {
                        $("#runs_table").find('tr')[index].classList.add('selected');
                    }
                }
            });
            add_selected_runs();


            setup_runs_keys = Object.keys(current_setup.runs);
            numOfEle = setup_runs_keys.length;
            selected_run_ids_keys = Object.keys(selected_run_ids);
            for (i = 0; i < numOfEle; i++) {
                key = setup_runs_keys[i];
                if (db_name !== key && selected_run_ids_keys.includes(key)) {
                    runs = Object.keys(current_setup.runs[key]);
                    setup_db_runs = runs.length;
                    for (k = 0; k < setup_db_runs; k++) {
                        selected_run_ids[key][runs[k]] = { "index": -1, "scenario": current_setup.runs[key][runs[k]], "isRunId": true };
                        option = document.createElement('option');
                        option.text = runs[k] + ' - ' + key;
                        chosen_runs_select.add(option);
                        num_of_runs = num_of_runs + 1;
                    }
                }
            }
            $('#num_of_runs')[0].innerHTML = 'Total : ' + String(num_of_runs) + ' runs';
            $('#num_of_tests')[0].innerHTML = 'Total : ' + String(num_of_runs * num_of_functions) + ' tests';
            $('#statistics_text')[0].innerHTML = String(num_of_functions) + ' functions on ' + String(num_of_runs) + ' runs : ' + String(num_of_runs * num_of_functions) + ' tests';
        }
    });
}

function add_selected_functions() {
    $("#functions_table").find('tr.selected').each((index) => {
        row_index = $("#functions_table").find('tr.selected')[index].rowIndex
        if (row_index > 0) {
            row = $("#functions_table").find('tr.selected')[index];
            row.hidden = true;
            option = document.createElement('option');
            option.text = row.cells[0].innerHTML;
            selected_functions[option.text] = { "index": row_index, "isFunctions": true };
            chosen_functions_select.add(option);
            //add one function to counter
            num_of_functions = num_of_functions + 1;
        }
    });
    $("#functions_table").find('tr.selected').removeClass('selected');
    $('#num_of_functions')[0].innerHTML = 'Total : ' + String(num_of_functions) + ' functions';
}

function add_selected_groups() {
    $("#groups_table").find('tr.selected').each((index) => {
        row_index = $("#groups_table").find('tr.selected')[index].rowIndex
        if (row_index > 0) {
            row = $("#groups_table").find('tr.selected')[index];
            row.hidden = true;
            option = document.createElement('option');
            option.text = row.cells[0].innerHTML + '(group)';
            selected_functions[option.text] = { "index": row_index, "isFunctions": false };
            chosen_functions_select.add(option);
            //add num of functions in group
            num_of_functions = num_of_functions + calculate_group_num_of_functions(row.cells[0].innerHTML);
        }
    });
    $("#groups_table").find('tr.selected').removeClass('selected');
    $('#num_of_functions')[0].innerHTML = 'Total : ' + String(num_of_functions) + ' functions';
}

function add_selected_runs() {
    db_name = database_select.options[database_select.options.selectedIndex].text;
    $("#runs_table").find('tr.selected').each((index) => {
        row_index = $("#runs_table").find('tr.selected')[index].rowIndex
        if (row_index > 0) {
            row = $("#runs_table").find('tr.selected')[index];
            row.hidden = true;
            option = document.createElement('option');
            option.text = row.cells[0].innerHTML + ' - ' + db_name;
            selected_run_ids[db_name][row.cells[0].innerHTML] = { "index": row_index, "scenario": row.cells[1].innerHTML, "isRunId": true };
            chosen_runs_select.add(option);
            //add 1 run to counter
            num_of_runs = num_of_runs + 1;
        }
    });
    $("#runs_table").find('tr.selected').removeClass('selected');
    $('#num_of_runs')[0].innerHTML = 'Total : ' + String(num_of_runs) + ' runs';
}

function add_selected_lists() {
    $("#lists_table").find('tr.selected').each((index) => {
        row_index = $("#lists_table").find('tr.selected')[index].rowIndex
        if (row_index > 0) {
            row = $("#lists_table").find('tr.selected')[index];
            row.hidden = true;
            option = document.createElement('option');
            option.text = row.cells[0].innerHTML + '(list)';
            selected_lists[row.cells[0].innerHTML + '(list)'] = { "index": row_index, "is_RunId": false };
            chosen_runs_select.add(option);
            //add list num of runs
            num_of_runs = num_of_runs + calculate_list_num_of_runs(row.cells[0].innerHTML);
        }
    });
    $("#lists_table").find('tr.selected').removeClass('selected');
    $('#num_of_runs')[0].innerHTML = 'Total : ' + String(num_of_runs) + ' runs';
}

function assign_event_setup_listeners() {
    $('#setup_name').change(() => {
        if (!$('#setup_toggle')[0].checked) {
            name = $('#setup_name')[0].value;
            if (setup_names.includes(name)) {
                clear_setup();
                load_setup(name);
            }
        }
    });

    $('#setup_toggle').change(() => {
        if (action !== "duplicate") {
            if ($('#setup_toggle')[0].checked) {
                $('#setup_name')[0].setAttribute('list', null);
                clear_setup();
            } else {
                $('#setup_name')[0].setAttribute('list', 'setups_datalist');
                load_setup_names();
                curr_setup_name = $('#setup_name')[0].value;
                $('#curr_setup_name')[0].innerHTML = curr_setup_name;
                if (action !== 'save') {
                    clear_setup();
                    load_setup(setup_names[0]);
                }
            }
        } else {
            $('#setup_name')[0].setAttribute('list', null);
            $('#setup_name')[0].value = '';
            $('#curr_setup_name')[0].innerHTML = ''
            curr_setup_name = '';
        }
        action = '';
    });

    $('#run_setup_button').click(() => {
        if (!$('#setup_toggle')[0].checked) {
            $.ajax({
                url: 'api/run_setup/' + curr_setup_name,
                success: (response) => {
                    $('#main_dissmisable_alert_text')[0].innerHTML = "running!";
                    $('#main_alert')[0].hidden = false;
                    // alert("running!");
                    get_mission_names();
                    load_mission(mission_names[0])
                }
            });
        } else {
            //save the setup as temp and run it
        }
    });


    $('#save_list_button').click(() => {
        save_list($('#list_name')[0].value);
    });

    $('#duplicate_setup').click(() => {
        if (!$('#setup_toggle')[0].checked) {
            action = "duplicate";
            $('#setup_toggle').bootstrapToggle('on')
        }
    });

    $('#save_setup').click(() => {
        setup_data = get_setup_data()
        if (setup_data['status']) {
            if ($('#setup_toggle')[0].checked) {
                status = save_setup(setup_data)
                if (status) {
                    action = 'save';
                    $('#setup_toggle').bootstrapToggle('off')
                }
            } else {
                setup_data['new_name'] = setup_data['name'];
                update_setup(setup_data)
            }
        }
    });

    $('#delete_setup').click(() => {
        if (!$('#setup_toggle')[0].checked) {
            name = $('#setup_name')[0].value;
            $.ajax({
                url: '/api/AnalyseSetup/delete_by_name/' + name,
                async: false,
                success: (response) => {
                    $('#main_dissmisable_alert_text')[0].innerHTML = 'setup ' + name + ' was deleted';
                    $('#main_alert')[0].hidden = false;
                    // alert('setup ' + name + ' was deleted')
                }
            });
            $('#setup_toggle').bootstrapToggle('off');
        }
    });

    database_select.addEventListener('change', () => { load_run_ids(database_select.options[database_select.selectedIndex].text) });
    // runs_tab.addEventListener('click', () => { load_run_ids(database_select.options[database_select.selectedIndex].text) });
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

        if ($('#lists_tab').hasClass('active')) {
            $("#lists_table").selectable().find('tr.selected').addClass('selected');
            $("#lists_table").selectable().find('tr').each((index) => {
                if ($("#lists_table").selectable().find('tr')[index].hidden == false && index > 0) {
                    $("#lists_table").selectable().find('tr')[index].classList.add('selected');
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
            add_selected_functions();
        }
        if ($('#groups_tab').hasClass('active')) {
            add_selected_groups();
        }
        if ($('#runs_tab').hasClass('active')) {
            add_selected_runs();
        }
        if ($('#lists_tab').hasClass('active')) {
            add_selected_lists();
        }
        $('#num_of_tests')[0].innerHTML = 'Total : ' + String(num_of_runs * num_of_functions) + ' tests';
        $('#statistics_text')[0].innerHTML = String(num_of_functions) + ' functions on ' + String(num_of_runs) + ' runs : ' + String(num_of_runs * num_of_functions) + ' tests';
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
                num_of_functions = num_of_functions - 1;
            } else {
                $("#groups_table").find('tr')[row_index].hidden = false;
                num_of_functions = num_of_functions - calculate_group_num_of_functions(option_name.split('(')[0]);
            }
            delete selected_functions[option_name]
        }
        $('#num_of_functions')[0].innerHTML = 'Total : ' + String(num_of_functions) + ' functions';
        $('#num_of_tests')[0].innerHTML = 'Total : ' + String(num_of_runs * num_of_functions) + ' tests';
        $('#statistics_text')[0].innerHTML = String(num_of_functions) + ' functions on ' + String(num_of_runs) + ' runs : ' + String(num_of_runs * num_of_functions) + ' tests';
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
                if (row_index > -1) {
                    $("#lists_table").find('tr')[row_index].hidden = false;
                }
                delete selected_lists[option_list]
                num_of_runs = num_of_runs - calculate_list_num_of_runs($("#lists_table").find('tr')[row_index].cells[0].innerHTML);
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
                num_of_runs = num_of_runs - 1;
            }
        }
        $('#num_of_runs')[0].innerHTML = 'Total : ' + String(num_of_runs) + ' runs';
        $('#num_of_tests')[0].innerHTML = 'Total : ' + String(num_of_runs * num_of_functions) + ' tests';
        $('#statistics_text')[0].innerHTML = String(num_of_functions) + ' functions on ' + String(num_of_runs) + ' runs : ' + String(num_of_runs * num_of_functions) + ' tests';
    });
}

//Start from here
$('#save_list_alert button')[0].addEventListener('click', function() { $('#save_list_alert')[0].hidden = true; });
$('#main_alert button')[0].addEventListener('click', function() { $('#main_alert')[0].hidden = true; });
$(document).ready(() => {
    load_init_setup_data();
    assign_event_setup_listeners();
});