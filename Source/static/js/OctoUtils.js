// form control handler can do the following functions:
// New(class)
// Save(api, data) -> return id
// delete(api, id)
// duplicate(id, class)
// clear_form(form_field)
// fill_form(form_field, Data) - i'm not shore may be should be specific
// get_form_data  - i'm not sure may be should be specific
// get_names(class)
//

function setToggle(toggleID, state) {
    $('#' + toggleID).bootstrapToggle(state)
}

function changeInputType(oldObject, eType, oType) {
    var newObject = document.createElement(eType);
    newObject.type = oType;
    // if(oldObject.size) newObject.size = oldObject.size;
    if (oldObject.value) newObject.value = oldObject.value;
    if (oldObject.name) newObject.name = oldObject.name;
    if (oldObject.id) newObject.id = oldObject.id;
    if (oldObject.classList) newObject.classList = oldObject.classList;
    if (oldObject.className) newObject.className = oldObject.className;
    oldObject.parentNode.replaceChild(newObject, oldObject);
    return newObject;
}



function clear_object(obj) {

    if (obj.type === "select-one") {
        var num_of_options = obj.options.length;
        for (i = 0; i < num_of_options; i++) {
            obj.remove(0);
        }
    } else if (obj.type === "checkbox") {
        obj.checked = 0;

    } else {
        obj.value = "";
    }
}

function fill_object2(obj, values) {
    if (obj.type === "select-one") {
      for (i = 0; i < values.length; i++) {
        var option = document.createElement("option");
        option.text = values[i];
        obj.add(option);
      }

    } else if (obj.type === "checkbox") {
      obj.checked = values;

    } else {
      obj.value = values;
    }
}



// data list example should be added to fill object
// <input list='some_datalist' type="text" class="input" placeholder="Add items in your list"/>
// <span class="add"><input class="btn btn-sm btn-primary" type="button" value="add"></span>
// <datalist id='some_datalist'>
//     <option value="data1"></option>
//     <option value="data3"></option>
//     <option value="data4"></option>
//     <option value="data2"></option>
// </datalist>

//
// } else if (obj.type === "Input") && (obj.hasOwnProperty("list"))  {
//   for (i = 0; i < values.length; i++) {
//     var option = document.createElement("option");
//     option.value = values[i];
//     obj.appendChild(option);
//   }

function form_controls_handler() {

    this.clear_form = function(form_controls, exclude) {
            Object.keys(form_controls).forEach(function(key, index) {
                if (!exclude.includes(key)) {
                    clear_object(form_controls[key]);
                }
            });
        },

        this.new = function(form_controls, field_name_key) {
            if (field_name_key !== "noChange") form_controls[field_name_key] = changeInputType(form_controls[field_name_key], "input", "text");
            // clear
            this.clear_form(form_controls, []);
        },

        this.exist = function(form_controls, field_name_key, elementType, objectType) {
            form_controls[field_name_key] = changeInputType(form_controls[field_name_key], elementType, objectType);
            this.clear_form(form_controls, []);
        }
}

function save(Class_Name, obj, exclude) {
    if (!is_containing_null(obj, exclude)) {
        var server_msg = { status: 0, message: 'server error' }
        $.ajax({
            type: "POST",
            url: "/api/" + Class_Name + "/save",
            dataType: "json",
            data: JSON.stringify(obj),
            contentType: 'application/json',
            async: false,
            success: function(msg) {
                server_msg = msg;
            },
            error: function() {
                server_msg = { status: 0, message: 'server error' };
            }
        });
        return server_msg;
    }
}

function update(Class_Name, obj, exclude) {
    if (!is_containing_null(obj, exclude)) {
        var server_msg = { status: 0, message: 'server error' }
        $.ajax({
            type: "POST",
            url: "/api/" + Class_Name + "/update_by_name/" + obj.name,
            dataType: "json",
            data: JSON.stringify(obj),
            contentType: 'application/json',
            async: false,
            success: function(msg) {
                server_msg = msg;
            },
            error: function() {
                server_msg = { status: 0, message: 'server error' };
            }
        });
        return server_msg;
    }
}

function item_delete(Class_Name, item_name) {
    var server_msg = { status: 0, message: 'server error' }
    $.ajax({
        url: "/api/" + Class_Name + "/delete_by_name/" + item_name,
        async: false,
        success: function(msg) {
            server_msg = msg;
        },
        error: function() {
            server_msg = { status: 0, message: 'server error' };
        }
    });
    return server_msg;
}

function get_names(form_name, Class_Name, Method, obj) {
    $.ajax({
        url: "/api/" + Class_Name + "/" + Method,
        async: false,
        success: function(msg) {
            // alert(msg.message)
            clear_object(obj);
            fill_object2(obj, msg.data);
            fill_form(form_name, Class_Name, "get_by_name", msg.data[0])

        }
    });
}

// function extract_content(obj, exclude){
//   var data = {};
//   Object.keys(obj).forEach(function(key, index) {
//     if (!exclude.includes(key)) {
//       data[key];
//     }
//   });
// }

function get_names_with_args(form_name, Class_Name, Method, arg, obj) {
    $.ajax({
        url: "/api/" + Class_Name + "/" + Method + "/" + arg,
        async: false,
        success: function(msg) {
            // alert(msg.message)
            clear_object(obj);
            fill_object2(obj, msg.data);
            fill_form(form_name, Class_Name, "get_by_name", msg.data[0])

        }
    });
}

function is_containing_null(obj, exclude) {
    Object.keys(obj).forEach(function(key, index) {
        if (!exclude.includes(key) && obj[key] === null) {
            return true;
        }
    });
    return false;
}
// 127.0.0.1:5000/api/Site/get_by_name/siteA

function fill_form(form_name, Class_Name, Method, SelectedName) {
    $.ajax({
        url: "/api/" + Class_Name + "/" + Method + "/" + SelectedName,
        async: false,
        success: function(msg) {
            // alert(msg.message)
            if (form_name == "SiteInfras") {
                fill_form_Site_Infras(msg.data);
            }

            if (form_name == "ProjectInfras") {
                fill_form_Project_Infras(msg.data);
            }

            if (form_name == "ComplexNet") {
                fill_form_ComplexNet(msg.data);
            }
        }
    });
}