var functions;
var groups;
var selected_functions = [];
var selected_groups = [];
var selected_run_ids = [];
var functions_list = [];
var run_ids_list = [];
var groups_list = [];
var functions_option = $('#functions_option')[0];
var functions_select_label = $('#functions_select_label')[0];
var groups_option = $('#groups_option')[0];
var function_select = $('#functions_select')[0];
var function_datalist = $('#function_datalist')[0];
var add_run_id_button = $('#add_run_id_button')[0];
var add_function_button = $('#add_function_button')[0];
var res_table = $('#res_table')[0];
var functions_ul = $('#functions_list')[0];
var run_ids_ul = $('#run_ids_list')[0];
var database_select = $('#database_select')[0];
var run_ids_select = $('#run_ids_select')[0];
var go_button = $('#go_button')[0];
var run_ids_datalist = $('#run_ids_datalist')[0];
var function_select_state = 'functions';

function remove_li_element() {
    var curr_li_ele = this.parentElement.parentElement;
    var li_type = curr_li_ele.classList[1];
    var value = this.parentElement.children[0].innerHTML;
    curr_li_ele.parentElement.removeChild(curr_li_ele);
    if (li_type === 'function') {
        selected_functions = selected_functions.filter(function(filter_val, index, arr) { return filter_val !== value; });
    }
    if (li_type === 'group') {
        selected_groups = selected_groups.filter(function(filter_val, index, arr) { return filter_val !== value; });
    }
    if (li_type === 'run_id') {
        selected_run_ids = selected_run_ids.filter(function(filter_val, index, arr) { return filter_val !== value; });
    }

}

function create_li_element(value, type) {
    var li_ele = document.createElement('li');
    var div_ele = document.createElement('div');
    var label_ele = document.createElement('label');
    var button_ele = document.createElement('button');
    var i_ele = document.createElement('i')
    li_ele.classList.add('draggable');
    li_ele.classList.add(type);
    li_ele.appendChild(div_ele);
    div_ele.classList.add('row');
    div_ele.appendChild(label_ele);
    div_ele.appendChild(button_ele);
    label_ele.classList.add('mr-auto');
    button_ele.classList.add('ml-auto');
    label_ele.innerHTML = value;
    button_ele.appendChild(i_ele);
    button_ele.addEventListener('click', remove_li_element);
    i_ele.classList.add('far')
    i_ele.classList.add('fa-trash-alt')

    return li_ele;
}

function add_function() {
    value = function_select.value;
    if (!selected_functions.includes(value) && functions_list.includes(value)) {
        functions_ul.appendChild(create_li_element(value, 'function'));
        selected_functions.push(value);
        function_select.value = null;
    }
}

function add_group() {
    value = function_select.value;
    if (!selected_groups.includes(value) && groups_list.includes(value)) {
        functions_ul.appendChild(create_li_element(value, 'group'));
        selected_groups.push(value);
        function_select.value = null;
    }
}

function add_run_id() {
    value = run_ids_select.value;
    if (!selected_run_ids.includes(value) && run_ids_list.includes(Number(value))) {
        run_ids_ul.appendChild(create_li_element(value, 'run_id'));
        selected_run_ids.push(value);
        run_ids_select.value = null;
    }
}

function get_all_functions() {
    $.ajax({
        url: "/api/OctopusFunction/get_names",
        success: function(result) {
            functions = result.data;
            var num_of_current_items = function_datalist.options.length;
            for (i = 0; i < num_of_current_items; i++) {
                function_datalist.removeChild(function_datalist.options[0]);
            }
            var num_of_functions = functions.length;
            functions_list = [];
            for (i = 0; i < num_of_functions; i++) {
                var name = functions[i];
                var option = document.createElement("option");
                option.text = name;
                function_datalist.appendChild(option);
                functions_list.push(name);
            }
            functions_select_label.innerHTML = '<h5>Select a function</h5>'
            functions_option.classList.add('dropdown-selected');
            groups_option.classList.remove('dropdown-selected')
            function_select_state = 'functions';
            function_select.value = null;
        }
    });
}

function get_all_groups() {
    $.ajax({
        url: "/api/FunctionsGroup/get_names",
        success: function(result) {
            groups_list = result.data;
            var num_of_current_items = function_datalist.options.length;
            for (i = 0; i < num_of_current_items; i++) {
                function_datalist.removeChild(function_datalist.options[0]);
            }
            var num_of_groups = groups_list.length;
            for (i = 0; i < num_of_groups; i++) {
                var option = document.createElement("option");
                option.text = groups_list[i];
                function_datalist.appendChild(option);
            }
            functions_select_label.innerHTML = '<h5>Select a group</h5>'
            groups_option.classList.add('dropdown-selected');
            functions_option.classList.remove('dropdown-selected')
            function_select_state = 'groups';
            function_select.value = null;
        }
    });
}

function load_run_ids(db_name) {
    $.ajax({
        url: "/api/DbConnector/get_run_ids/" + db_name,
        success: function(result) {
            run_ids_list = result;
            var num_of_runs = run_ids_list.length;
            // var num_of_current_runs = run_ids_select.options.length;
            // for (i = 0; i < num_of_current_runs; i++) {
            //   run_ids_select.remove(0);
            // }
            var num_of_current_runs = run_ids_datalist.options.length;
            for (i = 0; i < num_of_current_runs; i++) {
                run_ids_datalist.removeChild(run_ids_datalist.options[0]);
            }

            for (i = 0; i < num_of_runs; i++) {
                // var option = document.createElement("option");
                // option.text = run_ids_list[i];
                // run_ids_select.add(option);
                var option = document.createElement("option");
                option.text = run_ids_list[i];
                run_ids_datalist.appendChild(option);
            }
            run_ids_select.value = null;
        }
    });
}

function run_setup() {
    // run_ids = run_ids_list.value;
    // function_ids=functions.filter(obj=>{return [1,3].includes(obj.id)})
    // name = function_select.options[function_select.selectedIndex].innerHTML;
    // function_names = selected_functions;
    database_name = database_select.options[database_select.selectedIndex].value
    var data = {
        functions: selected_functions,
        groups: selected_groups,
        runs: selected_run_ids,
        db_name: database_name
    };
    $.ajax({
        type: "POST",
        url: "/api/run_functions",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(result) {
            $('#dissmisable_alert_text')[0].innerHTML = 'your mission id is: ' + result;
            $('.alert')[0].hidden = false;
            // alert('your mission id is: ' + result);
            get_mission_ids();
        }
    });
}

$('.alert button')[0].addEventListener('click', function() { $('.alert')[0].hidden = true; });
functions_option.addEventListener('click', get_all_functions);
groups_option.addEventListener('click', get_all_groups);
add_run_id_button.addEventListener('click', add_run_id);
add_function_button.addEventListener('click', function() {
    if (function_select_state === 'functions') {
        add_function();
    } else {
        add_group();
    }
});
database_select.addEventListener('change', function() { load_run_ids(database_select.options[database_select.selectedIndex].text) });
go_button.addEventListener('click', run_setup);

function get_db_names() {
    var num_of_options = database_select.options.length;
    for (i = 0; i < num_of_options; i++) {
        database_select.remove(0);
    }
    $.ajax({
        url: "/api/DbConnections/get_names",
        success: function(conn_names) {
            var num_of_conns = conn_names.length;
            for (i = 0; i < num_of_conns; i++) {
                var option = document.createElement("option");
                option.text = conn_names[i];
                database_select.add(option);
                load_run_ids(database_select.options[0].text);
                get_all_functions();
            }
        }
    });
}

get_all_functions();
get_db_names();