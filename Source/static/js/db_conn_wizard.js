var connections = [];

var form_controls = {
    db_type: $('#db_type')[0],
    user: $('#user')[0],
    password: $('#password')[0],
    hostname: $('#hostname')[0],
    port: $('#port')[0],
    schema: $('#schema')[0],
    schema_select: $('#schema_select')[0],
    name: $('#name')[0],
    is_dbrf: $('#is_dbrf')[0],
    is_hidden: $('#is_hidden')[0],
    save_button: $('#save_button')[0]
}

var display_controls = {
    disp_connections: $('#current_connections')[0],
    disp_db_type: $('#disp_db_type')[0],
    disp_user: $('#disp_user')[0],
    disp_password: $('#disp_password')[0],
    disp_hostname: $('#disp_hostname')[0],
    disp_port: $('#disp_port')[0],
    disp_schema: $('#disp_schema')[0],
    disp_schema_select: $('#disp_schema_select')[0],
    disp_name: $('#disp_name')[0],
    disp_is_dbrf: $('#disp_is_dbrf')[0],
    disp_is_hidden: $('#disp_is_hidden')[0],
    delete_connection_button: $('#delete_connection_button')[0],
    update_connection_button: $('#update_connection_button')[0],
    confirm_delete_button: $('#confirm_delete_button')[0]
}

function display_conn(selected_index) {
    display_controls.disp_db_type.innerText = connections[selected_index].db_type;
    display_controls.disp_user.innerText = connections[selected_index].user;
    display_controls.disp_password.innerText = connections[selected_index].password;
    display_controls.disp_hostname.innerText = connections[selected_index].hostname;
    display_controls.disp_port.innerText = connections[selected_index].port;
    display_controls.disp_schema.value = connections[selected_index].schema;
    display_controls.disp_name.innerText = connections[selected_index].name;
    display_controls.disp_is_dbrf.checked = connections[selected_index].is_dbrf;
    display_controls.disp_is_hidden.checked = connections[selected_index].is_hidden;
    response = get_schemas('existing');
    if (response.status > 0) {
        update_schemas(response.schemas, 'existing');
    } else {
        show_invalid_conn('existing');
    }

}

function clear_disp_schemas() {
    select_obj = $('#disp_schema_select')[0];
    numOfEle = select_obj.options.length;
    for (let index = 0; index < numOfEle; index++) {
        select_obj.remove(0);
    }
}

// function fill_disp_schemas(schemas, selected_index) {

// }

function clear_new_schemas() {
    select_obj = $('#schema_select')[0];
    numOfEle = select_obj.options.length;
    for (let index = 0; index < numOfEle; index++) {
        select_obj.remove(0);
    }
}

// function fill_new_schemas(schemas, selected_index) {

// }

function get_schemas(type) {
    if (type == 'new') {
        json_data = {
            "user": form_controls.user.value,
            "password": form_controls.password.value,
            "hostname": form_controls.hostname.value,
            "port": form_controls.port.value,
            "schema": form_controls.schema.value,
            "db_type": form_controls.db_type.options[form_controls.db_type.selectedIndex].text
        }
    } else {
        json_data = {
            "user": display_controls.disp_user.innerText,
            "password": display_controls.disp_password.innerText,
            "hostname": display_controls.disp_hostname.innerText,
            "port": display_controls.disp_port.innerText,
            "schema": display_controls.disp_schema.value,
            "db_type": display_controls.disp_db_type.innerText
        }
    }
    var resp = [];
    $.ajax({
        type: "POST",
        url: "/api/DbConnector/get_schemas_names",
        dataType: "json",
        async: false,
        data: JSON.stringify(json_data),
        contentType: 'application/json',
        success: function(response) {
            resp = response;
        }
    });

    return resp;
}

function update_schemas(schemas, type) {
    if (type == "new") {
        clear_new_schemas();
        select_obj = $('#schema_select')[0];
    } else {
        clear_disp_schemas();
        select_obj = $('#disp_schema_select')[0];
    }
    numOfEle = schemas.length;
    for (let index = 0; index < numOfEle; index++) {
        option = document.createElement('option');
        option.text = schemas[index];
        select_obj.add(option);
    }
    show_valid_conn(type);
}

function show_valid_conn(type) {
    if (type == "new") {
        $('#conn_status')[0].innerHTML = '<i class="valid-conn fas fa-check-circle"></i><h6 class="valid-conn">Connected</h6>';
    } else {
        $('#disp_conn_status')[0].innerHTML = '<i class="valid-conn fas fa-check-circle"></i><h6 class="valid-conn">Connected</h6>';
    }
};

function show_invalid_conn(type) {
    if (type == "new") {
        $('#conn_status')[0].innerHTML = '<i class="invalid-conn fas fa-times-circle"></i><h6 class="invalid-conn">No Connection</h6>';
        clear_new_schemas();
    } else {
        $('#disp_conn_status')[0].innerHTML = '<i class="invalid-conn fas fa-times-circle"></i><h6 class="invalid-conn">No Connection</h6>';
        clear_disp_schemas();
    }
}

function clear_display() {
    display_controls.disp_db_type.innerText = ''
    display_controls.disp_user.innerText = ''
    display_controls.disp_password.innerTextvalue = ''
    display_controls.disp_hostname.innerText = ''
    display_controls.disp_port.innerText = ''
    display_controls.disp_schema.innerText = ''
    display_controls.disp_name.innerText = ''
    numOfEle = display_controls.disp_schema.options.length;
    for (let index = 0; index < numOfEle; index++) {
        display_controls.disp_schema.remove(0);
    }
}

function update_conn_display() {

    //getting current conn name to choose after update
    select_control = display_controls.disp_connections;
    num_of_options = select_control.options.length;
    if (num_of_options > 0) {
        curr_name = select_control.options[select_control.selectedIndex].text;
    } else {
        curr_name = '';
    }

    //remove old connecitons
    for (k = 0; k < num_of_options; k++) {
        select_control.remove(0);
    }

    //insert new names
    num_of_connection = connections.length;
    selected_index = 0;
    for (k = 0; k < num_of_connection; k++) {
        option = document.createElement('option');
        option.text = connections[k].name;
        if (option.text === curr_name) {
            option.selected = true;
        } else {
            option.selected = false;
        }
        select_control.add(option);
    }

    //assign curr connection data to display controls
    if (num_of_connection > 0) {
        display_conn(selected_index)
    } else {
        clear_display();
    }

}

function get_conn_data() {
    $.ajax({
        url: '/api/get_conn_data',
        async: false,
        success: function(conn_data) {
            connections = conn_data;
            update_conn_display();
        }
    });
}

display_controls.disp_connections.addEventListener('change', function() {
    var selected_index = display_controls.disp_connections.selectedIndex;
    display_conn(selected_index);
})

form_controls.save_button.addEventListener('click', function() {
    form_controls.save_button.disabled = true;

    if (form_controls.schema_select.selectedIndex > -1) {
        schema = form_controls.schema_select.options[form_controls.schema_select.selectedIndex].text
    } else {
        schema = ''
    }
    var data = {
        db_type: form_controls.db_type.options[form_controls.db_type.selectedIndex].text,
        user: form_controls.user.value,
        password: form_controls.password.value,
        hostname: form_controls.hostname.value,
        port: form_controls.port.value,
        schema: schema,
        name: form_controls.name.value,
        is_dbrf: form_controls.is_dbrf.checked,
        is_hidden: form_controls.is_hidden.checked
    }
    keys = Object.keys(data);
    keys = keys.filter(function(value, index, arr) { return value !== 'is_dbrf' && value !== "is_hidden"; })
    all_filled_flag = 1;
    for (let index = 0; index < keys.length; index++) {
        if (data[keys[index]].replace(/\s/g, '').length == 0) {
            all_filled_flag = 0;
        }
    }
    if (all_filled_flag) {
        $.ajax({
            type: "POST",
            url: "/api/save_connection",
            dataType: "json",
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(message) {
                $('#dissmisable_alert_text')[0].innerHTML = message.msg;
                $('.alert')[0].hidden = false;
                get_conn_data();
                form_controls.save_button.disabled = false;
            }
        });
    } else {
        $('#dissmisable_alert_text')[0].innerHTML = "some fields are missing";
        $('.alert')[0].hidden = false;
        form_controls.save_button.disabled = false;
    }
})

function delete_conn() {
    $.ajax({
        type: "POST",
        url: "/api/DbConnector/delete_conn_by_name/" + display_controls.disp_connections[display_controls.disp_connections.selectedIndex].text,
        success: function(message) {
            $('#dissmisable_alert_text')[0].innerHTML = message.msg;
            $('.alert')[0].hidden = false;
            if (message.status == 1) {
                get_conn_data();
            }
        }
    });
}
display_controls.confirm_delete_button.addEventListener('click', delete_conn);

function update_modal_text() {
    if (display_controls.disp_connections.options.length) {
        conn_name = display_controls.disp_connections.options[display_controls.disp_connections.selectedIndex].text;
        $('#delete_connection_modal_body')[0].innerHTML = 'Delete ' + conn_name + '?';
    } else {
        $('#delete_connection_modal_body')[0].innerHTML = 'Nothing to delete';
    }
}

display_controls.delete_connection_button.addEventListener('click', update_modal_text);
$('.alert button')[0].addEventListener('click', function() { $('.alert')[0].hidden = true; })

$('.db-check-required').change(() => {
    response = get_schemas('new');
    if (response.status > 0) {
        update_schemas(response.schemas, 'new');
    } else {
        show_invalid_conn('new');
    }
});

$('.disp-db-check-required').change(() => {
    response = get_schemas('existing');
    if (response.status > 0) {
        update_schemas(response.schemas, 'existing');
    } else {
        show_invalid_conn('existing');
    }
});

$('#update_connection_button').click(() => {
    if (display_controls.disp_schema_select.selectedIndex > -1) {
        schema = display_controls.disp_schema_select.options[display_controls.disp_schema_select.selectedIndex].text
    } else {
        schema = ''
    }
    var data = {
        name: display_controls.disp_name.innerText,
        schema: schema,
        is_dbrf: display_controls.disp_is_dbrf.checked,
        is_hidden: display_controls.disp_is_hidden.checked,
    }
    keys = Object.keys(data);
    keys = keys.filter(function(value, index, arr) { return value !== 'is_dbrf' && value !== "is_hidden"; })
    all_filled_flag = 1;
    for (let index = 0; index < keys.length; index++) {
        if (data[keys[index]].replace(/\s/g, '').length == 0) {
            all_filled_flag = 0;
        }
    }
    if (all_filled_flag) {
        $.ajax({
            type: "POST",
            url: "/api/DbConnector/update_connection",
            dataType: "json",
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(message) {
                $('#dissmisable_alert_text')[0].innerHTML = message.msg;
                $('.alert')[0].hidden = false;
                get_conn_data();
                display_conn(display_controls.disp_connections.selectedIndex);
            }
        });
    } else {
        $('#dissmisable_alert_text')[0].innerHTML = "some fields are missing";
        $('.alert')[0].hidden = false;
        // form_controls.save_button.disabled = false;
    }
});

get_conn_data();