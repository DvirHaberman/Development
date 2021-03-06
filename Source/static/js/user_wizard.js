var team_names = [];
var role_names = [];
var project_names = [];
var users_names = [];
var users_ids = [];
var user_data = null;
var selected_user_index = 0;

var first_name = $('#first_name')[0];
var last_name = $('#last_name')[0];
var team_select = $('#team')[0];
var role_select = $('#role')[0];
var project_ul = $('#project')[0];
var max_priority = $('#max_priority')[0];
var user_select = $('#user_select')[0];

// var disp_nick_name = $('#disp_nick_name')[0];
var disp_first_name = $('#disp_first_name')[0];
var disp_last_name = $('#disp_last_name')[0];
var disp_team_select = $('#disp_team')[0];
var disp_role_select = $('#disp_role')[0];
var disp_project_ul = $('#disp_project')[0];
var disp_max_priority = $('#disp_max_priority')[0];
var save_button = $('#save_button')[0];
var save_changes_button = $('#save_changes_button')[0];
var reset_password_button = $('#reset_password_button')[0];
var delete_user_button = $('#delete_user_button')[0];

function update_select_obj(select_obj, data_array, selected_index) {
    var data_array_length = data_array.length;
    var obj_curr_length = select_obj.options.length;
    for (i = 0; i < obj_curr_length; i++) {
        select_obj.remove(0);
    }
    for (i = 0; i < data_array_length; i++) {
        var option = document.createElement("option");
        option.text = data_array[i];
        select_obj.add(option);
    }
    select_obj.selectedIndex = selected_index;
}

function update_ul_obj(ul_obj, data_array, selected_projects) {
    var data_array_length = data_array.length;
    var obj_curr_length = ul_obj.children.length;
    for (i = 0; i < obj_curr_length; i++) {
        ul_obj.removeChild(ul_obj.children[0]);
    }
    for (i = 0; i < data_array_length; i++) {
        ul_obj.appendChild(create_li_element(data_array[i]));
        if (selected_projects.includes(data_array[i])) {
            ul_obj.children[i].children[0].classList.remove('unselected_project');
            ul_obj.children[i].children[0].classList.add('selected_project');
        }
    }
}

function update_team_names() {
    $.ajax({
        url: '/api/Team/get_names',
        success: function(names) {
            team_names = names;
            update_select_obj(team_select, team_names, 0);
            update_select_obj(disp_team_select, team_names, team_names.indexOf(user_data.team));
        }
    });
}

function update_role_names() {
    $.ajax({
        url: '/api/Role/get_names',
        success: function(names) {
            role_names = names;
            update_select_obj(role_select, role_names, 0);
            update_select_obj(disp_role_select, role_names, role_names.indexOf(user_data.role));
        }
    });
}

function update_project_names() {
    $.ajax({
        url: '/api/Project/get_names',
        success: function(result) {
            project_names = result.data;
            update_ul_obj(project_ul, project_names, []);
            update_ul_obj(disp_project_ul, project_names, user_data.projects);
        }
    });
}

function update_user_names(index) {
    $.ajax({
        url: '/api/User/get_names_and_ids',
        success: function(users) {
            user_names = users.names;
            users_ids = users.ids;
            if (index == -1) {
                index = user_names.length - 1;
            }
            update_select_obj(user_select, user_names, index);
            update_all(index);
        }
    });
}

function update_all(index) {
    $.ajax({
        url: "/api/User/get_user_by_id/" + String(users_ids[index]),
        success: function(user) {
            user_data = user;
            // disp_nick_name.innerHTML = user_data.name;
            disp_first_name.innerHTML = user_data.first_name;
            disp_last_name.innerHTML = user_data.last_name;
            disp_max_priority.value = user_data.max_priority;
            update_team_names();
            update_role_names();
            update_project_names();
        }
    });
}

function update_user_data(index) {
    $.ajax({
        url: "/api/User/get_user_by_id/" + String(users_ids[index]),
        success: function(user) {
            user_data = user;
            // disp_nick_name.innerHTML = user_data.name;
            disp_first_name.innerHTML = user_data.first_name;
            disp_last_name.innerHTML = user_data.last_name;
            disp_max_priority.value = user_data.max_priority;
            update_select_obj(disp_team_select, team_names, team_names.indexOf(user_data.team));
            update_select_obj(disp_role_select, role_names, role_names.indexOf(user_data.role));
            update_ul_obj(disp_project_ul, project_names, user_data.projects);
        }
    });
}

function save_user() {
    var send_first_name = first_name.value;
    var send_last_name = last_name.value;
    var send_team = team_select.options[team_select.selectedIndex].text;
    var send_role = role_select.options[role_select.selectedIndex].text;
    var send_projects = [];
    numOfEle = project_ul.children.length;
    for (let i = 0; i < numOfEle; i++) {
        if (project_ul.children[i].children[0].classList[1] === 'selected_project') {
            send_projects.push(project_ul.children[i].children[0].children[0].innerText);
        }
    }
    var send_max_priority = max_priority.value;

    var data = {
        first_name: send_first_name,
        last_name: send_last_name,
        team: send_team,
        role: send_role,
        projects: send_projects,
        max_priority: send_max_priority
    };
    $.ajax({
        type: "POST",
        url: "/api/User/save_user",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(message) {
            $('#dissmisable_alert_text')[0].innerHTML = message.msg;
            $('.alert')[0].hidden = false;
            if (message.status == 1) {
                update_user_names(-1);
            }
        }
    });
}

function create_li_element(value) {
    var li_ele = document.createElement('li');
    var div_ele = document.createElement('div');
    var label_ele = document.createElement('label');
    li_ele.classList.add('project_li');
    li_ele.appendChild(div_ele);
    div_ele.classList.add('row');
    div_ele.classList.add('unselected_project');
    div_ele.appendChild(label_ele);
    label_ele.classList.add('mx-auto');
    label_ele.innerHTML = value;
    li_ele.addEventListener('click', toggle_select);

    return li_ele;
}

function toggle_select() {
    is_selected_flag = 0;
    div_child = this.children[0];
    for (i = 1; i < div_child.classList.length; i++) {
        if (div_child.classList[i] === 'selected_project') {
            is_selected_flag = 1;
        }
    }
    if (is_selected_flag) {
        div_child.classList.remove('selected_project');
        div_child.classList.add('unselected_project');
    } else {
        div_child.classList.remove('unselected_project');
        div_child.classList.add('selected_project');
    }
}

function update_user() {
    var send_team = disp_team_select.options[disp_team_select.selectedIndex].text;
    var send_role = disp_role_select.options[disp_role_select.selectedIndex].text;
    // var send_project = disp_project_ul.options[disp_project_ul.selectedIndex].text;
    var send_max_priority = disp_max_priority.value;
    send_projects = [];
    numOfEle = disp_project_ul.children.length;
    for (let i = 0; i < numOfEle; i++) {
        if (disp_project_ul.children[i].children[0].classList[1] === 'selected_project') {
            send_projects.push(disp_project_ul.children[i].children[0].children[0].innerText);
        }
    }
    var data = {
        id: users_ids[user_select.selectedIndex],
        team: send_team,
        role: send_role,
        projects: send_projects,
        max_priority: send_max_priority
    };
    $.ajax({
        type: "POST",
        url: "/api/User/update_user",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(message) {
            $('#dissmisable_alert_text')[0].innerHTML = message.msg;
            $('.alert')[0].hidden = false;
            if (message.status == 1) {
                update_user_names(selected_user_index);
            }
        }
    });
}

function reset_password() {
    $.ajax({
        type: "POST",
        url: "/api/User/reset_password_by_id/" + users_ids[user_select.selectedIndex],
        success: function(message) {
            $('#dissmisable_alert_text')[0].innerHTML = message.msg;
            $('.alert')[0].hidden = false;
            if (message.status == 1) {
                update_user_names(-1);
            }
        }
    });
}

function delete_user() {
    $.ajax({
        type: "POST",
        url: "/api/User/delete_user_by_id/" + users_ids[user_select.selectedIndex],
        success: function(message) {
            $('#dissmisable_alert_text')[0].innerHTML = message.msg;
            $('.alert')[0].hidden = false;
            if (message.status == 1) {
                update_user_names(-1);
            }
        }
    });
}

function update_modal_text() {
    user_name = user_select.options[user_select.selectedIndex].text;
    $('#delete_user_modal_body')[0].innerHTML = 'Delete ' + user_name + ' user?';
}

save_button.addEventListener('click', save_user);
save_changes_button.addEventListener('click', update_user);
reset_password_button.addEventListener('click', reset_password);
delete_user_button.addEventListener('click', update_modal_text);
$('#confirm_delete_button')[0].addEventListener('click', delete_user);
$('.alert button')[0].addEventListener('click', function() { $('.alert')[0].hidden = true; })
user_select.addEventListener('change', function() {
    selected_user_index = this.selectedIndex;
    update_user_data(this.selectedIndex);
});

update_user_names(0);