var functions;
var groups;
var selected_functions = [];
var selected_groups = [];
var connections = [];
var selected_run_ids = {
    // toJSON() {
    //     var json_string = '';
    //     for (entry in connections) {
    //         // if (entry in selected_run_ids) {
    //         //     selected_run_ids[entry];
    //         // }
    //         json_string = json_string + this[connections[entry]]['111111'];
    //     }
    //     return json_string;
    // }
};
var functions_list = [];
var run_ids_list = [];
var scenarios_list = [];
var groups_list = [];
var dbs_list = {};
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
        db = database_select.value
        delete selected_run_ids[db][value];
    }

}

function create_li_element(value, type) {
    var li_ele = document.createElement('li');
    var div_ele = document.createElement('div');
    if (type == 'run_id') {
        var run_label_ele = document.createElement('label');
        var db_label_ele = document.createElement('label');
        var scenario_label_ele = document.createElement('label');

        run_label_ele.innerHTML = value[0];
        db_label_ele.innerHTML = value[1];
        scenario_label_ele.innerHTML = value[2];

        run_label_ele.classList.add('col-6')
        run_label_ele.classList.add('mr-auto')
        db_label_ele.classList.add('col-6')
        db_label_ele.classList.add('ml-auto')
        scenario_label_ele.classList.add('mr-auto')

        div_ele.appendChild(run_label_ele);
        div_ele.appendChild(db_label_ele);
        div_ele.appendChild(scenario_label_ele);
    } else {
        label_ele = document.createElement('label');
        label_ele.innerHTML = value;
        label_ele.classList.add('mr-auto')
        div_ele.appendChild(label_ele);
    }

    var button_ele = document.createElement('button');
    var i_ele = document.createElement('i')
    li_ele.classList.add('draggable');
    li_ele.classList.add(type);
    li_ele.appendChild(div_ele);
    div_ele.classList.add('row');

    div_ele.appendChild(button_ele);
    button_ele.classList.add('ml-auto');

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
    run_id = run_ids_select.value;
    db = database_select.value
    scenario = dbs_list[db][run_id];
    if (!run_ids_list.includes(Number(run_id))) {
        return
    }
    if (run_id in selected_run_ids[db]) {
        return
    } else {
        Object.defineProperty(selected_run_ids[db], run_id, {
            value: scenario,
            writable: true,
            configurable: true,
            enumerable: true
        });
    }
    run_ids_ul.appendChild(create_li_element([run_id, db, scenario], 'run_id'));
    // selected_run_ids.push({ 'run_id': run_id, 'db': db, 'scenario': scenario });
    run_ids_select.value = null;
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

        success: function(result) {;
            var num_of_current_runs = run_ids_datalist.options.length;
            for (i = 0; i < num_of_current_runs; i++) {
                run_ids_datalist.removeChild(run_ids_datalist.options[0]);
            }
            if (result.status) {
                scenarios_list = result.scenarios;
                run_ids_list = result.run_ids;
                var num_of_runs = run_ids_list.length;
                for (i = 0; i < num_of_runs; i++) {
                    var option = document.createElement("option");
                    option.value = run_ids_list[i];
                    option.text = scenarios_list[i];
                    run_ids_datalist.appendChild(option);
                    // dbs_list[db_name].push({ 'scenario': option.text, 'run_id':  });
                    Object.defineProperty(dbs_list[db_name], option.value, {
                        value: option.text,
                        writable: true,
                        configurable: true,
                        enumerable: true
                    });
                }
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
    if (selected_run_ids.length == 0 || (selected_functions.length == 0 && selected_groups.length == 0)) {
        $('#dissmisable_alert_text')[0].innerHTML = 'runs or functions cannot be empty';
        $('.alert')[0].hidden = false;
        return
    }
    // database_name = database_select.options[database_select.selectedIndex].value
    var data = {
        functions: selected_functions,
        groups: selected_groups,
        runs: selected_run_ids
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
            connections = conn_names;
            var num_of_conns = conn_names.length;
            for (i = 0; i < num_of_conns; i++) {
                var option = document.createElement("option");
                option.text = conn_names[i];
                database_select.add(option);
                Object.defineProperty(dbs_list, conn_names[i], {
                    value: {},
                    writable: true,
                    configurable: true,
                    enumerable: true
                });
                Object.defineProperty(selected_run_ids, conn_names[i], {
                    value: {},
                    writable: true,
                    configurable: true,
                    enumerable: true
                });
            }
            load_run_ids(database_select.options[0].text);
            get_all_functions();
        }
    });
}

get_all_functions();
get_db_names();