var add_function_button = $('#add_function_button')[0];
var selected_modal_groups = []
var selected_modal_functions = []
var functions_modal_select = $('#functions_modal_select')[0];
var function_select_state = 'functions'
var selected_ul = $('#modal_ul')[0];
var functions_names = [];
var groups_names = [];
var modal_datalist = $('#modal_datalist')[0];
var functions_option = $('#functions_option')[0];
var functions_select_label = $('#functions_select_label')[0];
var Description_functions_Group_label = $('#Description_functions_Group_label')[0];
var groups_option = $('#groups_option')[0];
var modal_group_name = $('#Modal_Select_Group_Name')[0];
var modal_group_names_datalist = $('#Group_Function_Name')[0];
var modal_filter_Tags = $('#modal_filter_Tags')[0];
var modal_filter_owner = $('#modal_filter_owner')[0];
var action = 'new';

var modal_form_controls = {
    Group_Name_select: $('#Modal_Select_Group_Name')[0],
    owner: $('#modal_owner')[0],
    description: $('#Modal_Group_Description')[0],
    changed_date: $("#modal_changed_date")[0],
    changed_by: $("#modal_changed_by")[0],
    function_select: $("#functions_modal_select")[0],
    GroupFunction_Description: $("#Modal_GroupFunction_Description")[0],
    ul: $("#modal_ul")[0]
};

function clear_Modal_form() {
    modal_form_controls.Group_Name_select.value = null;
    modal_form_controls.description.value = "";
    modal_form_controls.changed_by.innerHTML = "";
    modal_form_controls.changed_date.innerHTML = "";
    modal_form_controls.GroupFunction_Description.innerHTML = "";
    modal_filter_Tags.value = "";
    modal_filter_owner.value = "";
    SetModalAllUsers();
}


function ModalFormDisable(trueFalse) {
    // form_controls.function_select.disabled = trueFalse;
    modal_form_controls.owner.disabled = trueFalse;
    modal_form_controls.description.disabled = trueFalse;
    modal_form_controls.function_select.disabled = trueFalse;
    modal_form_controls.GroupFunction_Description.disabled = trueFalse;
    modal_filter_Tags.disabled = trueFalse;
    modal_filter_owner.disabled = trueFalse;
    add_function_button.disabled = trueFalse;
    function_group_dropdown_menu.disabled = trueFalse;
    $('#Save_Group')[0].disabled = trueFalse;
    $('#Delete_Group')[0].disabled = trueFalse;

    $('#modal_ul').find('li').each((index) => {
        elem = $('#modal_ul').find('li')[index];
        if (elem.children.length) { elem.children[0].children[1].disabled = trueFalse; }
    });

}
//   GroupsListNames

function SetModalFuctionsOrGroups(FuctionsOrGroupsNames) {
    var num_of_Records = FuctionsOrGroupsNames.length;

    FuctionsOrGroup_list = $('#modal_datalist')[0];
    // clear owner DL Control
    var num_of_options = FuctionsOrGroup_list.options.length;
    for (i = 0; i < num_of_options; i++) {
        FuctionsOrGroup_list.removeChild(FuctionsOrGroup_list.children[0]);
    }

    //insert data
    for (i = 0; i < num_of_Records; i++) {
        var option = document.createElement("option");
        option.text = FuctionsOrGroupsNames[i];
        FuctionsOrGroup_list.appendChild(option);
    }

}




function SetModalAllUsers() {
    Users = getAllUsers()
    var num_of_Users = Users.length;
    var owner_datalists = ["modal_owner_datalist", "modal_filter_owner_datalist"];

    for (x = 0; x < owner_datalists.length; x++) {

        owner_data_list = $('#' + owner_datalists[x])[0];
        // clear owner DL Control
        var num_of_options = owner_data_list.options.length;
        for (i = 0; i < num_of_options; i++) {
            owner_data_list.removeChild(owner_data_list.children[0]);
        }

        //insert data
        for (i = 0; i < num_of_Users; i++) {
            var option = document.createElement("option");
            option.text = Users[i];
            owner_data_list.appendChild(option);
        }

    }


}

function add_modal_group() {
    var value = functions_modal_select.value;
    if (!selected_modal_groups.includes(value) && groups_names.includes(value)) {
        var GroupsList = document.getElementsByName("GroupsListNames")[0];
        selected_ul.appendChild(create_modal_li_element(value, 'modal_group'));
        selected_modal_groups.push(value);
        functions_modal_select.value = null;
    }
}

function add_modal_function() {
    value = functions_modal_select.value;
    if (!selected_modal_functions.includes(value) && functions_names.includes(value)) {
        selected_ul.appendChild(create_modal_li_element(value, 'modal_function'));
        selected_modal_functions.push(value);
        functions_modal_select.value = null;
    }
}

function load_group(group_name) {
    $.ajax({
        url: "/api/FunctionsGroup/get_by_name/" + group_name,
        async: false,
        success: function(result) {
            if (result.status === 1) {
                clear_chosen_list();
                numOfEle = result.data.functions.length;
                for (i = 0; i < numOfEle; i++) {
                    selected_ul.appendChild(create_modal_li_element(result.data.functions[i], 'modal_function'));
                    selected_modal_functions.push(result.data.functions[i]);
                }
                functions_modal_select.value = null;
            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = result.message;
                $('#modal_alert')[0].hidden = false;
                // alert(result.message);
            }
        }

    });
}


function save_group(group_name) {
    chosen_functions = selected_modal_functions;
    numOfEle = selected_modal_groups.length;
    for (i = 0; i < numOfEle; i++) {
        $.ajax({
            url: "/api/FunctionsGroup/get_by_name/" + selected_modal_groups[i],
            async: false,
            success: function(result) {
                if (result.status === 1) {
                    numOffunctions = result.data.functions.length;
                    for (k = 0; k < numOffunctions; k++) {
                        chosen_functions.push(result.data.functions[k]);
                    }
                }
            }
        });
    }
    data = {
        name: group_name,
        // owner:
        // description: 
        // changed_date: 
        // changed_by: 
        functions: chosen_functions

    };
    $.ajax({
        type: "POST",
        url: "/api/FunctionsGroup/save",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        async: false,
        success: function(result) {
            if (result.status === 1) {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = 'group ' + group_name + ' was successfuly saved!';
                $('#modal_alert')[0].hidden = false;
                // alert('group ' + group_name + ' was successfuly saved!');
            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = 'something went wrong';
                $('#modal_alert')[0].hidden = false;
                // alert('something went wrong')
            }
        }

    });
}

function update_group(group_name) {
    chosen_functions = selected_modal_functions;
    numOfEle = selected_modal_groups.length;
    for (i = 0; i < numOfEle; i++) {
        $.ajax({
            url: "/api/FunctionsGroup/get_by_name/" + selected_modal_groups[i],
            async: false,
            success: function(result) {
                if (result.status === 1) {
                    numOffunctions = result.data.functions.length;
                    for (k = 0; k < numOffunctions; k++) {
                        chosen_functions.push(result.data.functions[k]);
                    }
                }
            }
        });
    }
    data = {
        name: group_name,
        functions: chosen_functions
    };
    $.ajax({
        type: "POST",
        url: "/api/FunctionsGroup/update_by_name/" + group_name,
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        async: false,
        success: function(result) {
            if (result.status === 1) {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = 'group ' + group_name + ' was successfuly updated!';
                $('#modal_alert')[0].hidden = false;
                // alert('group ' + group_name + ' was successfuly updated!');
            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = 'something went wrong';
                $('#modal_alert')[0].hidden = false;
                // alert('something went wrong')
            }
        }

    });
}

function delete_group(group_name) {
    // group_name = modal_group_names_datalist.options[index].value;
    $.ajax({
        url: "/api/FunctionsGroup/delete_by_name/" + group_name,
        async: false,
        success: function(result) {
            if (result.status === 1) {
                clear_chosen_list();
                numOfEle = result.data.functions.length;
                for (i = 0; i < numOfEle; i++) {
                    selected_ul.appendChild(create_modal_li_element(result.data.functions[i], 'modal_function'));
                    selected_modal_functions.push(result.data.functions[i]);
                }
                functions_modal_select.value = null;
            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = result.message;
                $('#modal_alert')[0].hidden = false;
                // alert(result.message);
            }
        }

    });
}

function remove_modal_li_element() {
    var curr_li_ele = this.parentElement.parentElement;
    var li_type = curr_li_ele.classList[1];
    var value = this.parentElement.children[0].innerHTML;
    curr_li_ele.parentElement.removeChild(curr_li_ele);
    if (li_type === 'modal_function') {
        selected_modal_functions = selected_modal_functions.filter(function(filter_val, index, arr) { return filter_val !== value; });
    }
    if (li_type === 'modal_group') {
        selected_modal_groups = selected_modal_groups.filter(function(filter_val, index, arr) { return filter_val !== value; });
    }

}

function create_modal_li_element(value, type) {
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
    button_ele.addEventListener('click', remove_modal_li_element);
    i_ele.classList.add('far')
    i_ele.classList.add('fa-trash-alt')

    return li_ele;
}

function getModalFilterData() {

    data = {
        owner: modal_filter_owner.value,
        tags: modal_filter_Tags.value
    };
    return data;
}

function Filter_function_names(json_data) {

    $.ajax({
        async: false,
        type: "POST",
        url: "/api/OctopusFunction/get_names_by_filter",
        dataType: "json",
        data: JSON.stringify(json_data),
        contentType: 'application/json',
        success: function(result) {
            FilterFunction = result;
        }

    });
    return FilterFunction.data;
}



add_function_button.addEventListener('click', function() {
    if (function_select_state === 'functions') {
        add_modal_function();
    } else {
        add_modal_group();
    }
});

$('#modal_filter_owner')[0].addEventListener('input', function() {
    if ($('#groups_option').hasClass('dropdown-selected')) { // Group Case
        json_data = getModalFilterData();
        delete json_data['tags'];

        FilerNames = get_names_by_filter(json_data);

    } else { // Function Case
        json_data = getModalFilterData();
        FilerNames = Filter_function_names(json_data);
        SetModalFuctionsOrGroups(FilerNames);
    }

});

$('#modal_filter_Tags')[0].addEventListener('input', function() {

    if ($('#groups_option').hasClass('dropdown-selected')) { // Group Case
        json_data = getModalFilterData();
        delete json_data['tags'];

        FilerNames = get_names_by_filter(json_data);

    } else { // Function Case
        json_data = getModalFilterData();
        FilerNames = Filter_function_names(json_data);
        SetModalFuctionsOrGroups(FilerNames);
    }





});

$('#Group_toggle').change(function() {
    if ($('#Group_toggle')[0].checked) { //new

        modal_group_name.setAttribute("list", null);
        if (action !== "duplicate") {
            clear_Modal_form();
            clear_chosen_list();
        }

        get_groups_names();
        get_functions_names();
        // $('#function_group_dropdown_menu').dropdown() - need to be added
        ModalFormDisable(false)
        action = 'new';

    } else { //exist

        modal_group_name.setAttribute("list", "Group_Function_Name");
        get_groups_names();
        get_functions_names();
        if (action !== 'save' && action !== 'update') {
            modal_group_name.value = groups_names[0];
        }
        // if (action !== 'update') {
        load_group(modal_group_name.value);
        // }
        ModalFormDisable(true)
        action = 'existing';
    }


});

$('#Duplicate_Group').click(function() { //duplicate
    if ($('#Group_toggle')[0].checked === false) {
        action = 'duplicate';
        setToggle('Group_toggle', 'on')
    }
});


$('#Edit_Group').click(function() { //duplicate
    ModalFormDisable(false)
});


$('#Save_Group').click(function() { //save
    if ($('#Group_toggle')[0].checked) { //new
        group_name = modal_group_name.value;
        save_group(group_name);
        action = 'save';
        reload_functions();
        setToggle('Group_toggle', 'off')
    } else { //existing
        group_name = modal_group_name.value;
        update_group(group_name);
        action = 'update';
        reload_functions();
        setToggle('Group_toggle', 'off')
    }
});

$('#Delete_Group').click(function() { //delete
    if ($('#Group_toggle')[0].checked === false) {
        group_name = modal_group_name.value;
        if (groups_names.includes(group_name)) {
            delete_group(group_name);
            get_groups_names();
            get_functions_names();
            modal_group_name.value = groups_names[0];
            load_group(groups_names[0]);
            reload_functions();
        }
    }
});

function reload_functions() {
    $.ajax({
        url: "/api/OctopusFunction/jsonify_all",
        async: false,
        success: function(result) {
            functions = result;
            functoinIndex = form_controls.function_select.selectedIndex;
            form_handler.fill_form(functoinIndex, []);
        }

    });
}


$('#Modal_Select_Group_Name').on('keyup', function(e) {
    if (e.keyCode === 13) {
        if (groups_names.includes(modal_group_name.value)) {
            load_group(modal_group_name.value);
        }
    }
});

function clear_chosen_list() {
    var numOfEle = selected_ul.children.length;
    for (i = 0; i < numOfEle; i++) {
        selected_ul.removeChild(selected_ul.children[0]);
    }
    selected_modal_groups = [];
    selected_modal_functions = [];
}

function get_functions_names() {
    $.ajax({
        url: "/api/OctopusFunction/get_names",
        async: false,
        success: function(result) {
            if (result.status) {
                functions_names = result.data;
                var numOfEle = modal_datalist.children.length;
                for (i = 0; i < numOfEle; i++) {
                    modal_datalist.removeChild(modal_datalist.options[0]);
                }
                for (i = 0; i < functions_names.length; i++) {
                    // insert
                    var option = document.createElement("option");
                    option.value = functions_names[i];
                    modal_datalist.appendChild(option);
                }
            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = result.message;
                $('#modal_alert')[0].hidden = false;
                // alert(result.message);
            }
            functions_select_label.innerHTML = '<h5>Select a function to the list</h5>'
            modal_filter_Tags.hidden = false;
            Description_functions_Group_label.innerHTML = '<h6>Function Description</h6>'
            functions_option.classList.add('dropdown-selected');
            groups_option.classList.remove('dropdown-selected')
            function_select_state = 'functions';
            functions_modal_select.value = null;
        }
    });
}

function get_groups_names() {
    $.ajax({
        url: "/api/FunctionsGroup/get_names",
        async: false,
        success: function(result) {

            if (result.status === 1) {
                groups_names = result.data;
                var numOfEle = modal_datalist.children.length;
                for (i = 0; i < numOfEle; i++) {
                    modal_datalist.removeChild(modal_datalist.options[0]);
                }

                var numOfEle = modal_group_names_datalist.children.length;
                for (i = 0; i < numOfEle; i++) {
                    modal_group_names_datalist.removeChild(modal_group_names_datalist.options[0]);
                }

                for (i = 0; i < groups_names.length; i++) {
                    // insert
                    var option = document.createElement("option");
                    option.value = groups_names[i];
                    modal_datalist.appendChild(option);
                    var option = document.createElement("option");
                    option.value = groups_names[i];
                    modal_group_names_datalist.appendChild(option);
                }

            } else {
                $('#main_dissmisable_modal_alert_text')[0].innerHTML = result.message;
                $('#modal_alert')[0].hidden = false;
                // alert(result.message);
            }
            functions_select_label.innerHTML = '<h5>Select a group to the list</h5>'
            modal_filter_Tags.hidden = true;

            Description_functions_Group_label.innerHTML = '<h6>Group Description</h6>'
            groups_option.classList.add('dropdown-selected');
            functions_option.classList.remove('dropdown-selected')
            function_select_state = 'groups';
            functions_modal_select.value = null;

        }

    });
}

$('#modal_alert button')[0].addEventListener('click', function() { $('#modal_alert')[0].hidden = true; });
functions_option.addEventListener('click', get_functions_names);
groups_option.addEventListener('click', get_groups_names);

get_groups_names();
get_functions_names();

modal_group_name.setAttribute("list", null);