// getting all form controls into one object
var current_user = 'ami';
var current_version = 1;
var parmasHeader = ["ID", "kind", "value", "type", "remove"];
var functionArray = ["incValue", "byValue", "placeRemoveImg"];
var paramsTblHeader = ["ID", "kind", "value", "type", "remove"];
var paramsTblFunctionArray = [IncValue, "byValue", "byValue", "byValue", PlaceRemoveImg];
var paramsTblIsByValue = [0, 1, 1, 1, 0];
var paramsTblKinds = ["Sys Params", "Tests Params", "text"];
var paramsTblType = ["DataFrame", "String", "Number"];
var functions = [];
var selected_Groups = [];
var optionList = ["Seattle", "Las Vegas", "New York", "Salt lake City"];
var Stage = "update";
var funciton_kinds = ["Python", "Matlab", "SQL"];
var Flag_toggle = 0;
var action = "update";
var group_permissions = {};
var sep = null;

var form_controls = {
    function_select: $('#meta_function_name')[0],
    owner: $('#meta_owner')[0],
    status: $("select[name='meta_status']")[0],
    changed_date: $("input[name='changed_date']")[0],
    feature: $("input[name='feature']")[0],
    requirement: $("input[name='requirement']")[0],
    tags: $("input[name='tags']")[0],
    callback: $("input[name='callback']")[0],
    kind: $("select[name='kind']")[0],
    location: $("input[name='Location']")[0],
    description: $('#function_description')[0],
    is_class_method: $("input[name='isOutputIsAClass']")[0],
    class_name: $("input[name='outputClassName']")[0],
    function_parameters: $("table[name='function_parameters']")[0],
    groups: $("ul[name='GroupsListNames']")[0],
    changed_by: $("#function_last_changed_by")[0],
    add_param: $("button[name='plus_param_row_button']")[0],
    oper_line: $('#oper_line')[0]
};

function FindSelectFuncIndex() {
    selectedIndex = -1;
    numOfEle = $('#meta_name_datalist')[0].children.length;
    for (i = 0; i < numOfEle; i++) {
        if ($('#meta_name_datalist')[0].options[i].innerHTML === form_controls.function_select.value) selectedIndex = i;
    }
    return selectedIndex;
}

function functionFormDisable(trueFalse) {
    // form_controls.function_select.disabled = trueFalse;
    form_controls.owner.disabled = trueFalse;
    form_controls.status.disabled = trueFalse;
    form_controls.feature.disabled = trueFalse;
    form_controls.requirement.disabled = trueFalse;
    form_controls.tags.disabled = trueFalse;
    form_controls.callback.disabled = trueFalse;
    form_controls.kind.disabled = trueFalse;
    form_controls.location.disabled = trueFalse;
    form_controls.description.disabled = trueFalse;

    form_controls.is_class_method.disabled = trueFalse;
    form_controls.class_name.disabled = trueFalse;

    form_controls.function_parameters.disabled = trueFalse;
    $("table[name='function_parameters']").find('td').each((index) => {
        elem = $("table[name='function_parameters']").find('td')[index];
        if (elem.children.length) { elem.children[0].disabled = trueFalse; }
    });

    $('#addGroupButton')[0].disabled = trueFalse;
    $('#newGroupButton')[0].disabled = trueFalse;
    $('#GroupsList').find('li').each((index) => {
        elem = $('#GroupsList').find('li')[index];
        if (elem.children.length) { elem.children[0].children[1].disabled = trueFalse; }
    });


    form_controls.groups.disabled = trueFalse;

    $('#meta_save')[0].disabled = trueFalse;
    $('#meta_delete')[0].disabled = trueFalse;
    $("button[name='plus_param_row_button']")[0].disabled = trueFalse;


}



var Group_Modal_form_controls = {
    Group_name: $('#Modal_Select_Group_Name')[0],
    Group_List: $('#chosen_list')[0]
}


function fillDataList(container, optionList) {
    i = 0,
        len = optionList.length,
        dl = document.createElement('datalist');

    dl.id = 'dlCities';
    for (; i < len; i += 1) {
        var option = document.createElement('option');
        option.value = optionList[i];
        dl.appendChild(option);
    }
    container.appendChild(dl);
}

function is_permitted(group_name, action) {
    var premission = {};
    if ($('#Group_toggle')[0].checked) {
        premission = { "status": 1, "message": '', "permission": 1 };
    } else {
        $.ajax({
            url: '/api/FunctionsGroup/is_permitted/' + group_name + ',' + action,
            async: false,
            success: (response) => {
                premission = response;
            },
            error: () => {
                premission = { "status": 0, "message": 'server error', "permission": 0 };
            }
        });
    }
    return premission;
}

function add_group() {
    value = $('#group_input')[0].value;
    premission = is_permitted(value, 'add');
    if (premission.status > 0 && premission.permission > 0) {
        if (!selected_Groups.includes(value) && AllGroups.includes(value)) {
            var GroupsList = document.getElementsByName("GroupsListNames")[0];
            GroupsList.appendChild(create_li_element(value, 'group'));
            selected_Groups.push(value);
            $('#group_input')[0].value = null;
        }
    } else {
        $('#main_dissmisable_alert_text')[0].innerHTML = premission.message;
        $('#main_alert')[0].hidden = false;
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

function remove_li_element() {

    var curr_li_ele = this.parentElement.parentElement;
    var li_type = curr_li_ele.classList[1];
    var value = this.parentElement.children[0].innerHTML;
    permission = is_permitted(value, 'remove');
    if (permission.status > 0 && permission.permission > 0) {

        curr_li_ele.parentElement.removeChild(curr_li_ele);
        if (li_type === 'function') {
            selected_functions = selected_functions.filter(function(filter_val, index, arr) { return filter_val !== value; });
        }
        if (li_type === 'group') {
            selected_Groups = selected_Groups.filter(function(filter_val, index, arr) { return filter_val !== value; });
        }
        if (li_type === 'run_id') {
            selected_run_ids = selected_run_ids.filter(function(filter_val, index, arr) { return filter_val !== value; });
        }
    } else {
        $('#main_dissmisable_alert_text')[0].innerHTML = permission.message;
        $('#main_alert')[0].hidden = false;
    }

}

// document.querySelector('.custom-file-input').addEventListener('change',function(e){
//   var fileName = document.getElementById("functionLocation").files[0].name;
//   var nextSibling = e.target.nextElementSibling
//   nextSibling.innerText = $('#functionLocation').val()
// })

function CreateOperLineString() {
    var fileName = document.getElementById("functionCallback").value;
    // var filename = "ilanFun";
    var OperLineString = fileName + "(conn, RunID";
    var tableRowsLength = $("table[name='function_parameters']")[0].rows.length;
    tableData = [];
    if (tableRowsLength == 1) {
        OperLineString = OperLineString + ")";
    } else {
        for (i = 1; i < tableRowsLength; i++) {
            var currParam = ""
            var currRow = $("table[name='function_parameters']")[0].rows[i]

            // kind
            var selectObj = currRow.cells[1].children[0];
            var kind = selectObj.options[selectObj.selectedIndex].text;
            if (kind == "text") {
                // value
                if (currRow.cells[2].childElementCount > 0) {
                    currParam = currRow.cells[2].children[0].value;
                } else {
                    currParam = currRow.cells[2].innerHTML;
                }
            } else {
                currParam = kind;
            }

            if (i == tableRowsLength - 1) {
                OperLineString = OperLineString + ", " + currParam + ")";
            } else {
                OperLineString = OperLineString + ", " + currParam;
            }
        }
    }
    return OperLineString;
}

function setOperLineString() {
    var OperString = CreateOperLineString();
    var objOperLine = document.getElementsByName("funcOperLine");
    objOperLine[0].innerHTML = OperString;
}



function calc() {
    var className = document.getElementById('className');

    if (document.getElementById('isOutputIsAClass').checked) {
        className.disabled = false;

    } else {
        className.disabled = true
        className.value = "";
    }
}


// Definition and Assignment TableHeaderNodes //

function IncValue(value) {
    return value + 1;
}

function PlaceRemoveImg() {
    return '<i class="far fa-trash-alt"></i>';
}

function RemoveTblRow() {
    var table = document.getElementsByName("function_parameters")[0];
    var rowIndex = this.parentElement.parentElement.rowIndex;
    table.deleteRow(rowIndex);
    for (i = 1; i < table.rows.length; i++) {
        table.rows[i].cells[0].innerHTML = i;
    }
    setOperLineString();
}

function GetTypeArray(funKind, paramKind) {
    if (paramKind == "text") {
        return ["String", "Number"];

    }

    if (funKind == "Matlab") {
        return ["Struct"];
    }

    return ["DataFrame"];


}


function setParamTblTypeKind() {
    // case funKind is "sql" - Clean ParamTbl
    // case funKind is "Matlab" Change Type in ParamTbl for Sysparams And Test Params to struct 
    // case funKind is "Python"  Change Type in ParamTbl for Sysparams And Test Params to DataFrame
    // case funKind is "Undefiend"  - Do nothing
    funKind = this.value;
    if (funKind == "Sql") {

    } else if (funKind == "Matlab" || funKind == "Python") {

        $("table[name='function_parameters']").find('tr').each((index) => {
            if (index > 0) {
                curr_row = $("table[name='function_parameters']").find('tr')[index];
                paramKind = curr_row.cells[1].children[0].options[curr_row.cells[1].children[0].options.selectedIndex].text;
                typecell = curr_row.cells[3];
                TypeArray = GetTypeArray(funKind, paramKind);
                typecell.removeChild(typecell.children[0]);
                typecell.appendChild(CreateParamSelectElement(TypeArray, 0));
            }
        });

    }

}

function setParamTblValueField() {
    var currCell = this.parentElement.parentElement.cells[2];
    var TypeCell = this.parentElement.parentElement.cells[3];
    var num_of_children = TypeCell.children.length;
    for (i = 0; i < num_of_children; i++) {
        TypeCell.removeChild(TypeCell.children[0]);
    }

    var selectedParamKind = this.options[this.selectedIndex].text;
    if (selectedParamKind == "text") {
        currCell.innerHTML = [];
        let newElement = document.createElement('input');
        newElement.classList.add("form-control");
        currCell.appendChild(newElement);

    } else {
        setOperLineString();
        currCell.innerHTML = "--";

    }

    TypeCell.appendChild(CreateParamSelectElement(GetTypeArray(form_controls.kind.options[form_controls.kind.selectedIndex].text, selectedParamKind), 0)); // SelectTypeCell

}

function TableHeaderNodes(key, handleFunction, isByValue) {
    this.Header = key;
    this.handle = handleFunction;
    this.isByValue = isByValue;
}


function FillHeaderNodes(parmasHeader, functionArray, isByValue) {

    var TableHeaderNodesArray = [];
    for (i = 0; i < parmasHeader.length; i++) {
        // var node = new TableHeaderNodes(parmasHeader[i], functionArray[i], isByValue[i])
        TableHeaderNodesArray.push(new TableHeaderNodes(parmasHeader[i], functionArray[i], isByValue[i]));
    }
    return TableHeaderNodesArray;
}

var ParamTableArrayNodes = FillHeaderNodes(paramsTblHeader, paramsTblFunctionArray, paramsTblIsByValue);
//  //


function FindParamsTblKindsIndex(paramsTblKinds, name) {
    var index = paramsTblKinds.indexOf(name);
    return index
}

function FindParamsTblTypeIndex(paramsTblType, name) {
    var index = paramsTblType.indexOf(name);
    return index
}

function CreateParamEmptyBottunElement(PlaceRemoveImg) {
    let newElement = document.createElement('bottun');
    newElement = PlaceRemoveImg;
    return newElement;
}

function CreateParamSelectElement(paramsTblArray, currValueIndex) {
    let newElement = document.createElement('select');

    for (m = 0; m < paramsTblArray.length; m++) {
        var currKind = paramsTblArray[m];
        // newElement.setAttribute("id", "MykindsDown");
        var option = document.createElement("option");
        option.value = m;
        option.text = currKind;
        option.classList.add("table-option");
        newElement.add(option);
    }

    newElement.classList.add("form-control");
    newElement.classList.add("table-select");
    newElement.selectedIndex = currValueIndex;

    return newElement
}


function Create_New_Tbl_Row(table, rowNum) {
    var newRow = table.insertRow(rowNum);
    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1); //kind
    var cell3 = newRow.insertCell(2); //value
    var cell4 = newRow.insertCell(3); //type
    var cell5 = newRow.insertCell(4); // remove Img

    cell1.innerHTML = rowNum;
    let newElement = CreateParamSelectElement(paramsTblKinds, 0)
    newElement.addEventListener('change', setParamTblValueField);
    cell2.appendChild(newElement); // SelectKindCell

    cell3.innerHTML = "--";
    cell3.addEventListener('change', setOperLineString);
    // cell4.appendChild(CreateParamSelectElement(paramsTblType, 0)); 
    var selectedParamKind = cell2.children[0].options[cell2.children[0].options.selectedIndex].text;
    // SelectTypeCell
    cell4.appendChild(CreateParamSelectElement(GetTypeArray(form_controls.kind.options[form_controls.kind.selectedIndex].text, selectedParamKind), 0));

    newElement = document.createElement('button');
    newElement.innerHTML = PlaceRemoveImg();
    newElement.addEventListener('click', RemoveTblRow);

    cell5.appendChild(newElement);
}

function fill_row_data(row_obj, values, header) {
    var num_of_values = header.length;

    for (k = 0; k < num_of_values; k++) {
        if (k === 1) { // kind
            var currKindValueIndex = FindParamsTblKindsIndex(paramsTblKinds, values.kind);
            row_obj.cells[1].children[0].selectedIndex = currKindValueIndex;

        } else if (k === 2 && currKindValueIndex === 2) { // value
            currCell = row_obj.cells[2]
            currCell.innerHTML = [];
            let newElement = document.createElement('input');
            newElement.classList.add("form-control");
            newElement.value = values.value;
            currCell.appendChild(newElement);
        } else if (k === 3) { // type
            var paramKind = row_obj.cells[1].children[0].options[row_obj.cells[1].children[0].options.selectedIndex].text;

            if (paramKind == "text") {
                TypeCell = row_obj.cells[3];
                funKind = form_controls.kind.value;
                TypesArray = GetTypeArray(funKind, paramKind)
                var currValueIndex = FindParamsTblTypeIndex(TypesArray, values.type);
                TypeCell.removeChild(TypeCell.children[0]);
                TypeCell.appendChild(CreateParamSelectElement(TypesArray, currValueIndex)); // SelectTypeCell
                //                 row_obj.cells[3].children[0].selectedIndex = currValueIndex;
            }
        }
    }
}


function clear_object(obj) {
    if (obj.tagName === 'TABLE') {
        var num_of_rows = obj.rows.length;
        for (i = 0; i < num_of_rows - 1; i++) {
            obj.deleteRow(1);
        }
    } else if (obj.tagName === 'P') {
        obj.innerHTML = "";

    } else if (obj.type === "select-one") {
        var num_of_options = obj.options.length;
        for (i = 0; i < num_of_options; i++) {
            obj.remove(0);
        }
    } else if (obj.tagName === "UL") {
        var GroupsList = document.getElementsByName("GroupsListNames")[0];
        num_of_li = GroupsList.children.length;
        for (i = 0; i < num_of_li; i++) {
            GroupsList.removeChild(GroupsList.children[0]);
        }
        selected_Groups = [];
    } else if (obj.type === "checkbox") {
        obj.checked = 0;
        calc();

    } else {
        obj.value = "";
    }
}

function fill_object(obj, value, header) {
    if (obj.tagName === 'TABLE') {
        var num_of_rows = value.length;
        if (num_of_rows > 0) {
            // var table = document.getElementsByName("function_parameters")[0];
            var param_keys = Object.keys(value[0]);
            for (i = 0; i < num_of_rows; i++) {
                Create_New_Tbl_Row(obj, i + 1);
                var currRow = $("table[name='function_parameters']")[0].rows[i + 1]
                fill_row_data(currRow, value[i], header);
            }
        }
    } else if (obj.type === "select-one") {
        // var num_of_options = value.options.length;
        // for (i = 0; i < num_of_functions; i++) {
        var option = document.createElement("option");
        option.text = value;
        obj.add(option);
        //   }
    } else if (obj.type === "checkbox") {
        obj.checked = value;
        calc();
        // } else if (obj.tagName==="DATALIST"){
        //
    } else if (obj.tagName === "UL") {
        // Add_Group(obj, value, obj.children.length+1);
        var GroupsList = document.getElementsByName("GroupsListNames")[0];
        var num_of_ele = value.length;
        for (i = 0; i < num_of_ele; i++) {
            GroupsList.appendChild(create_li_element(value[i], 'group'));
            selected_Groups.push(value[i]);
        }
    } else if (obj.tagName === "P") {
        obj.innerHTML = value;

    } else {
        obj.value = value;
    }
}

function get_data_from_control(obj) {
    if (obj.tagName === 'TABLE') {
        // fill later
        return null;
    } else if (obj.type === "select-one") {
        //nothing to do here
        return null;
    } else {
        return obj.value;
    }
}


// /////////////////////////////////////////////////////////////////////////
// Declaring the
//
// /////////////////////////////////////////////////////////////////////////

function GetParameterDataTbl(id, kind, val, type) {
    var parameterData = {
        index: id,
        kind: kind,
        value: val,
        type: type
    }
}
////////////////////////////////////////////////////////////////////////////
// Declaring the form handler class.                                      //
// this class is holding all the form object controls and is in charge of //
// clearing and filling the form                                          //
////////////////////////////////////////////////////////////////////////////
function getAllUsers() {
    var Users = "";
    $.ajax({
        url: "/api/User/get_names",
        async: false,
        success: function(result) {
                if (result.status === 1) {
                    Users = result.data;
                } //if
            } // function
    });
    return Users;
}

function SetAllUsers() {
    Users = getAllUsers()
    var num_of_Users = Users.length;

    owner_data_list = $('#meta_owner_datalist')[0]
    for (i = 0; i < num_of_Users; i++) {
        var option = document.createElement("option");
        option.text = Users[i];
        owner_data_list.appendChild(option);
    }

}

function getAllGroups(groupListID) {
    var groups = "";
    $.ajax({
        url: "/api/FunctionsGroup/get_names",
        async: false,
        success: function(result) {

                if (result.status === 1) {
                    groups = result.data;
                    var datalistObj = $('#' + groupListID)[0]
                    var numOfEle = datalistObj.children.length;
                    for (i = 0; i < numOfEle; i++) {
                        datalistObj.removeChild(datalistObj.options[0]);
                    }
                    for (i = 0; i < groups.length; i++) {
                        // insert
                        var option = document.createElement("option");
                        option.value = groups[i];
                        datalistObj.appendChild(option);
                    }

                } //if
            } // function
    });
    return groups;
}


function Add_Group(ul, li_Name, numOfRows) {
    // var ul = document.getElementById("list");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(li_Name));
    li.innerHTML = li_Name + CreateParamEmptyBottunElement(PlaceRemoveImg());
    li.setAttribute("id", ["element" + numOfRows]); // added line
    ul.appendChild(li);
    // ul.push(li);
}

const validate_name = (name, field_name) => {
    let result = {
        status: 1,
        message: null,
        data: null
    };
    name = name.trim();
    if (name.replace(' ', '').length == 0) {
        result.status = 0;
        result.message = field_name + ' : name cannot be empty';
    }
    if (/[^a-z_\-A-Z0-9]/.test(name.replace(' ', ''))) {
        result.status = 0;
        result.message += '\n' + field_name + `: name can only contain letters, numbers and the - , _ characters`;
    }
    result.data = name;
    return result;
};

const not_in_datalist = (datalist, lookup_value) => {
    let numOfEle = datalist.children.length;
    for (let index = 0; index < numOfEle; index++) {
        if (lookup_value == datalist.children[index].value) {
            return 0;
        }

    }

    return 1;
}

function Function_Definition_form_controls_handler() {
    this.form_controls = form_controls;
    this.clear_form = function(exclude) {

            $('#group_input')[0].value = '';
            // clear function select DL Control
            function_datalist_object = $('#meta_name_datalist')[0]
            var num_of_options = function_datalist_object.options.length;
            for (i = 0; i < num_of_options; i++) {
                function_datalist_object.removeChild(function_datalist_object.children[0]);
            }

            // clear owner DL Control
            owner_datalist_object = $('#meta_owner_datalist')[0]
            var num_of_options = owner_datalist_object.options.length;
            for (i = 0; i < num_of_options; i++) {
                owner_datalist_object.removeChild(owner_datalist_object.children[0]);
            }

            // clear all other Form_controls
            Object.keys(this.form_controls).forEach(function(key, index) {
                if (!exclude.includes(key)) {
                    if (!["status", "kind"].includes(key)) {
                        clear_object(this.form_controls[key]);
                    }
                }
            });
        },

        this.fill_form = function(index, exclude) {
            var funcSelectedIndex = index;

            this.clear_form(exclude);

            curr_function = functions[index];
            Object.keys(this.form_controls).forEach(function(key, index) {
                if (!exclude.includes(key)) {
                    value = curr_function[key];
                    if (key === "status") {
                        this.form_controls[key].selectedIndex = value;
                    } else if (key === "kind") {
                        selected_index = funciton_kinds.indexOf(value);
                        if (selected_index === -1) {
                            selected_index = 3;
                        }
                        this.form_controls[key].selectedIndex = selected_index;
                    } else if (key === "function_select") {
                        function_data_list = $('#meta_name_datalist')[0]
                        var num_of_functions = functions.length;
                        for (i = 0; i < num_of_functions; i++) {
                            var option = document.createElement("option");
                            option.text = functions[i].name;
                            function_data_list.appendChild(option);
                        }

                        this.form_controls.function_select.value = function_data_list.children[funcSelectedIndex].innerHTML;
                    } else if (value) {
                        fill_object(this.form_controls[key], value, ParamTableArrayNodes);
                    }
                }
            });
            setOperLineString();
        },
        this.get_form_data = function() {
            let final_result = {
                status: 1,
                message: null,
                data: null
            };

            var tableRowsLength = $("table[name='function_parameters']")[0].rows.length;
            tableData = [];
            for (i = 1; i < tableRowsLength; i++) {
                let currRow = $("table[name='function_parameters']")[0].rows[i]

                // index
                let index = currRow.cells[0].innerHTML;

                // kind
                let selectObj = currRow.cells[1].children[0];
                let kind = selectObj.options[selectObj.selectedIndex].text;

                // value
                if (currRow.cells[2].childElementCount > 0) {
                    var value = currRow.cells[2].children[0].value;
                } else {
                    var value = currRow.cells[2].innerHTML;
                }


                // type
                selectObj = currRow.cells[3].children[0];
                var type = selectObj.options[selectObj.selectedIndex].text;

                var paramRowData = {
                    index: index,
                    kind: kind,
                    value: value,
                    type: type
                }

                tableData.push(paramRowData)
            }

            //--------------- validation -------------------------
            //validate manual/needed - only name
            //validate indev/completed//
            // 1. not empty or space only.
            // 2. legal characters
            // 3. trim spaces.
            let name_result = validate_name($('#meta_function_name')[0].value, 'function name')
            if (name_result.status) {
                name = name_result.data;
            } else {
                final_result.status = 0;
                final_result.message = final_result.message ? final_result.message + '\n' + name_result.message : name_result.message;
            }

            // owner - backend validation

            // status - closed list does not need validation

            // feature - future validation needed when TFS or other managment tool is integrated
            // requirement - future validation needed when TFS or other managment tool is integrated
            // tags - no need
            //-----------------------------------------------------
            // File Full Path
            // in list
            if (not_in_datalist($('#location_datalist')[0], $("input[name='Location']")[0].value)) {
                final_result.status = 0;
                let message = 'file not in given path';
                final_result.message = final_result.message ? final_result.message + '\n' + message : message;
            }
            // description - no need 
            // callback - 
            //1. if matlab and sql-> not empty
            //2. if python -> not empty in list
            let kind = $("select[name='kind']")[0].options[$("select[name='kind']")[0].selectedIndex].text;
            let callback_result = validate_name($("input[name='callback']")[0].value, 'callback');
            if (callback_result.status) {
                callback = callback_result.data;
            } else {
                final_result.status = 0;
                final_result.message = final_result.message ? final_result.message + '\n' + callback_result.message : callback_result.message;
            }
            if (kind.toLowerCase() == 'python') { // will be commented
                if (not_in_datalist($('#callback_datalist')[0], callback_result.data)) {
                    final_result.status = 0;
                    let message = 'callback not found in given python file';
                    final_result.message = final_result.message ? final_result.message + '\n' + message : message;
                }
            }
            // is_class_method - no need
            let is_class_method = $("input[name='isOutputIsAClass']")[0].checked;
            let class_name = $("input[name='outputClassName']")[0].value;
            if (is_class_method) {
                // class_name - if class method is checked - check for this class in file
                if (not_in_datalist($('#classname_datalist')[0], class_name)) {
                    final_result.status = 0;
                    let message = 'class name not found in given python file';
                    final_result.message = final_result.message ? final_result.message + '\n' + message : message;
                }
            }


            // groups - backend validation
            // function_parameters - no need
            if (final_result.status) {
                let function_data = {

                    name: name,
                    owner: $('#meta_owner')[0].value,
                    status: $("select[name='meta_status']")[0].selectedIndex,
                    // changed_date: $("input[name='changed_date']")[0],

                    feature: $("input[name='feature']")[0].value,
                    requirement: $("input[name='requirement']")[0].value,
                    tags: $("input[name='tags']")[0].value,
                    callback: $("input[name='callback']")[0].value,

                    kind: kind,
                    location: $("input[name='Location']")[0].value,
                    description: $('#function_description')[0].value,
                    is_class_method: is_class_method,
                    class_name: class_name,

                    groups: selected_Groups,
                    function_parameters: tableData
                };
                final_result.data = function_data;
            }

            return final_result;
        },
        this.get_all_functions = function(mode) {
            $.ajax({
                url: "/api/OctopusFunction/jsonify_all",
                async: false,
                success: function(result) {
                    functions = result;
                    if (mode === 'onReset') {
                        functoinIndex = 0;
                    } else if (mode === 'save') {
                        functoinIndex = result.length - 1;
                    } else {
                        functoinIndex = FindSelectFuncIndex()
                    }
                    form_handler.fill_form(functoinIndex, []);
                }
            });
        }
}


form_handler = new Function_Definition_form_controls_handler();
modal_form_controls_handler = new form_controls_handler();

function manual_clear() {
    //clear callback
    //clear class name and checkbox
    //clear full path
    clear_callback_data()
    form_controls.oper_line.innerHTML = '';
    let new_thead = document.createElement('thead');
    let old_thead = form_controls.function_parameters.children[0];
    form_controls.function_parameters.replaceChild(new_thead, old_thead);
    //clear table
    //clear oper line
}

function clear_callback_data() {
    //clear callback
    //clear class name and checkbox
    //clear full path
}

function manual_disable() {
    //disable callback
    //disable class name and checkbox
    //disable full path
    //diable table add
}

function manual_disable() {
    form_controls.callback.disabled = true;
    form_controls.location.disabled = true;
    form_controls.is_class_method.disabled = true;
    form_controls.class_name.disabled = true;
    form_controls.add_param.disabled = true;
    form_controls.function_parameters.disabled = true;
}

function clear_callback_data() {
    form_controls.callback.value = '';
    clear_datalist('callback_datalist');
    form_controls.class_name.value = '';
    clear_datalist('classname_datalist');
    form_controls.is_class_method.checked = false;
}

function clear_datalist(dl_id) {
    let dl = document.getElementById(dl_id);
    let numOfEle = dl.children.length;
    for (let index = 0; index < numOfEle; index++) {
        dl.removeChild(dl.children[0]);
    }
}

function set_new_valid_file() {
    form_controls.callback.disabled = false;
    form_controls.location.disabled = false;
    form_controls.is_class_method.disabled = false;
    form_controls.class_name.disabled = true;
    form_controls.add_param.disabled = false;
    form_controls.function_parameters.disabled = false;
    clear_callback_data();
}

function set_new_invalid_file() {
    form_controls.callback.disabled = true;
    form_controls.location.disabled = false;
    form_controls.is_class_method.disabled = true;
    form_controls.class_name.disabled = true;
    form_controls.add_param.disabled = false;
    form_controls.function_parameters.disabled = false;
    clear_callback_data();
}

function get_seperator() {
    // let seperator = null;
    fetch('api/OctopusUtils/get_seperator')
        .then(resp => resp.json()).then(result => { sep = result.data; })
        // return seperator;
}

function get_files_in_dir() {
    let kind = $("select[name='kind']")[0].options[$("select[name='kind']")[0].selectedIndex].text;
    if (kind == "Manual") {
        manual_clear();
        manual_disable();
    } else {

        $.ajax({
            type: "POST",
            async: false,
            url: "/api/OctopusUtils/get_files_in_dir",
            dataType: "json",
            data: JSON.stringify({ "path": form_controls.location.value, "kind": kind }),
            contentType: 'application/json',
            success: function(result) {
                var datalistObj = $('#location_datalist')[0]
                var numOfEle = datalistObj.children.length;
                for (i = 0; i < numOfEle; i++) {
                    datalistObj.removeChild(datalistObj.options[0]);
                }
                if (result.status) {
                    for (i = 0; i < result.all.length; i++) {
                        // insert
                        var option = document.createElement("option");
                        option.value = result.all[i];
                        datalistObj.appendChild(option);
                    }
                }
            }
        });
        //if file is full valid enable is class checkbox and callback
        //if not, disable
        let file = form_controls.location.value;
        if (not_in_datalist($('#location_datalist')[0], file)) {
            set_new_invalid_file();
        } else {
            set_new_valid_file();
            let splitted_location = file.split(sep)
            if (kind == 'Python') {
                // 1. get callbacks
                set_callbacks();
            } else {
                // 1. is class = false and disabled
                form_controls.is_class_method.checked = false;
                form_controls.is_class_method.disabled = true;
                form_controls.callback.value = splitted_location[splitted_location.length - 1]
            }
        }

    }
}

// form_handler.clear_form();
form_controls.location.addEventListener("input", get_files_in_dir);
form_controls.kind.addEventListener("change", get_files_in_dir);
$('#NewExist_toggle').change(function() {
    $('.alert')[0].hidden = true;
    if (action === "saveNewFunction") {
        action = '';
        return;
    } else {

        if ($('#NewExist_toggle')[0].checked) { //new
            Stage = "new";
            form_handler.clear_form([]);
            form_controls.function_select.setAttribute("list", null) // change function select to text
            form_controls.kind.selectedIndex = 0;
            form_controls.status.selectedIndex = 0;
            functionFormDisable(false);
            $.ajax({
                url: "/api/OctopusUtils/get_functions_basedir",
                success: function(result) {
                    form_controls.location.value = result.dir;
                }
            });

            SetAllUsers();

        } else { //exist
            Stage = "update";
            form_controls.function_select.setAttribute("list", "meta_name_datalist") // change function select to DL
            form_handler.fill_form(0, []);
            functionFormDisable(true);

        }

    }

});

function fill_datalist(dl_id, values) {
    obj = document.getElementById(dl_id);
    numOfEle = values.length;
    for (let index = 0; index < numOfEle; index++) {
        option = document.createElement('option');
        option.text = values[index];
        obj.appendChild(option);
    }
}

async function get_classes(file_full_path) {
    let classes = [];
    await fetch('api/OctopusUtils/get_classes_from_file', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "path": file_full_path })
    }).then(resp => resp.json()).then(result => {
        if (result.status) {
            classes = result.data;
        }
    })
    return classes;
}

async function get_callbacks(file_full_path) {
    let callbacks = [];
    await fetch('api/OctopusUtils/get_callbacks_from_file', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "path": file_full_path })
    }).then(resp => resp.json()).then(result => {
        if (result.status) {
            callbacks = result.data;
        }
    })
    return callbacks;
}

async function get_callbacks_from_class(file_full_path, class_name) {
    let callbacks = [];
    await fetch('api/OctopusUtils/get_callbacks_from_class', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "path": file_full_path, "class_name": class_name })
    }).then(resp => resp.json()).then(result => {
        if (result.status) {
            callbacks = result.data;
        }
    })
    return callbacks;
}

async function set_callbacks() {
    //get file name
    let file = form_controls.location.value;
    let is_checked = form_controls.is_class_method.checked;

    //if checked:
    if (is_checked) {
        //--------callback-----------

        //clear and disable callback
        form_controls.callback.value = '';
        form_controls.callback.disabled = true;

        //clear callback dl
        clear_datalist('callback_datalist');

        //--------class name-------------

        //clear and enable class
        form_controls.class_name.value = '';
        form_controls.class_name.disabled = false;

        //clear class dl
        clear_datalist('classname_datalist');

        //get classes form the file
        let classes = await get_classes(file);

        fill_datalist('classname_datalist', classes);
    } else {
        //--------class name-----------

        //clear and disable class
        form_controls.class_name.value = '';
        form_controls.class_name.disabled = true;

        //clear class dl
        clear_datalist('classname_datalist');

        //--------callback-------------

        //clear and enable callback
        form_controls.callback.value = '';
        form_controls.callback.disabled = false;

        //clear callback dl
        clear_datalist('callback_datalist');

        //get callbacks form the file
        let callbacks = await get_callbacks(file);

        //fill callback dl
        fill_datalist('callback_datalist', callbacks);
    }
}

form_controls.is_class_method.addEventListener('change', set_callbacks);

form_controls.class_name.addEventListener('change', async() => {
    file = form_controls.location.value;
    class_name = form_controls.class_name.value;
    if (!not_in_datalist($('#location_datalist')[0], file) &&
        !not_in_datalist($('#classname_datalist')[0], class_name)) {
        clear_datalist('callback_datalist');
        form_controls.callback.disabled = false;
        let callbacks = await get_callbacks_from_class(file, class_name);
        fill_datalist('callback_datalist', callbacks);
    } else {
        clear_datalist('callback_datalist');
        form_controls.callback.value = '';
        form_controls.callback.disabled = true;
    }

});

$('#meta_duplicate')[0].addEventListener("click", function() {
    $('.alert')[0].hidden = true;
    var functoinIndex = FindSelectFuncIndex()
    setToggle("NewExist_toggle", "on"); //(new)
    form_handler.fill_form(functoinIndex, []);
    form_controls.function_select.value = "";
});



$('#meta_edit')[0].addEventListener("click", function() {
    $('.alert')[0].hidden = true;
    functionFormDisable(false);
    SetAllUsers();

});
//

//
//

$('#meta_delete')[0].addEventListener("click", function() {
    $('.alert')[0].hidden = true;
    var function_name = form_controls.function_select.value;
    $.ajax({
        type: "POST",
        url: "/api/OctopusFunction/delete_by_name/" + function_name,
        success: function(msg) {
            $('#main_dissmisable_alert_text')[0].innerHTML = msg;
            $('#main_alert')[0].hidden = false;

            form_handler.get_all_functions('onReset');
            Stage === "update";
            functionFormDisable(true);
        }
    });

});
//
//
$('#meta_save')[0].addEventListener("click", function() {
    $('.alert')[0].hidden = true;
    let result = form_handler.get_form_data();
    if (result.status) {
        if (Stage === "new") {
            $.ajax({
                type: "POST",
                url: "/api/OctopusFunction/save_function",
                dataType: "json",
                data: JSON.stringify(result.data),
                contentType: 'application/json',
                success: function(resp) {

                    $('#main_dissmisable_alert_text')[0].innerHTML = resp.message;
                    $('#main_alert')[0].hidden = false;
                    if (resp.status) {
                        action = "saveNewFunction";
                        setToggle("NewExist_toggle", "off");
                        $('#main_alert')[0].hidden = false;
                        form_handler.get_all_functions('save');
                        Stage = "update";
                        functionFormDisable(true);
                    }
                }
            });

        }
        if (Stage === "update") {
            $.ajax({
                type: "POST",
                url: "/api/OctopusFunction/update",
                dataType: "json",
                data: JSON.stringify(result.data),
                contentType: 'application/json',
                success: function(msg) {
                    $('#main_dissmisable_alert_text')[0].innerHTML = msg;
                    $('#main_alert')[0].hidden = false;
                    // alert(msg)
                    form_handler.get_all_functions('current');
                    functionFormDisable(true);
                    var temp = 1;
                }
            });
        }
    } else {
        // $('#main_dissmisable_alert_text')[0].innerHTML = result.message;
        // $('#main_alert')[0].hidden = false;
        alert(result.message);
    }

});




$('.alert button')[0].addEventListener('click', function() { $('.alert')[0].hidden = true; });

form_controls.function_select.addEventListener("change", function() {
    $('.alert')[0].hidden = true;
    var functoinIndex = FindSelectFuncIndex()
    if (Stage == "update" && functoinIndex !== -1) {
        form_handler.fill_form(functoinIndex, []);
        functionFormDisable(true);
    } else return;
});

// kind Function 


$("#function_kind")[0].addEventListener("change", setParamTblTypeKind);

//
$("#addGroupButton")[0].addEventListener("click", add_group);
//
//
$("button[name='plus_param_row_button']")[0].addEventListener("click", function() {
    var table = document.getElementsByName("function_parameters")[0];
    var numOfRows = table.rows.length;
    Create_New_Tbl_Row(table, numOfRows);
    setOperLineString();
});
//
$("input[name='callback']")[0].addEventListener("change", function() {
    setOperLineString();
});

var AllGroups = getAllGroups("groups_datalist");
form_handler.get_all_functions('onReset');
setToggle("NewExist_toggle", "off");

get_seperator();
// getAllGroups("Group_Function_Name"); // modal
// getAllGroups("some_datalist");  // modal