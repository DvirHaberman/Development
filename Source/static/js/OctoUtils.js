// form control hanndler can do the following functions:
// New(class)
// Save(api, data) -> return id
// delete(api, id)
// duplicate(id, class)
// clear_form(form_field)
// fill_form(form_field, Data) - i'm not shore may be should be specific
// get_form_data  - i'm not shore may be should be specific
// get_names(class)
//

function changeInputType(oldObject, eType, oType) {
  var newObject = document.createElement(eType);
  newObject.type = oType;
  // if(oldObject.size) newObject.size = oldObject.size;
  if(oldObject.value) newObject.value = oldObject.value;
  if(oldObject.name) newObject.name = oldObject.name;
  if(oldObject.id) newObject.id = oldObject.id;
  if(oldObject.classList) newObject.classList = oldObject.classList;
  if(oldObject.className) newObject.className = oldObject.className;
  oldObject.parentNode.replaceChild(newObject,oldObject);
  return newObject;
}



function clear_object(obj) {

if (obj.type === "select-one") {
    var num_of_options = obj.options.length;
    for (i = 0; i < num_of_options; i++) {
      obj.remove(0);
    }
  } else if (obj.type==="checkbox"){
    obj.checked = 0;

  } else {
    obj.value = "";
  }
}

function fill_object(obj, values) {
    if (obj.type === "select-one") {
      for (i = 0; i < values.length; i++) {
        var option = document.createElement("option");
        option.text = values[i];
        obj.add(option);
      }

    } else if (obj.type === "checkbox") {
      obj.checked = value;

    } else {
      obj.value = value;
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

  this.new = function(form_controls, field_name_key){

    // name - > text
    form_controls[field_name_key] = changeInputType(form_controls[field_name_key], "input", "text");
    // clear
    this.clear_form(form_controls, []);
  },

  this.exist = function(form_controls, field_name_key, elementType, objectType){
    form_controls[field_name_key] = changeInputType(form_controls[field_name_key], elementType, objectType);
    this.clear_form(form_controls, []);
  },

  this.save = function(){
  }
}


function get_names(form_name, Class_Name, Method, obj){
  $.ajax({
    url: "/api/" + Class_Name + "/" + Method,
    async: false,
    success: function(msg) {
      // alert(msg.message)
      clear_object(obj);
      fill_object(obj, msg.data);
      fill_form(form_name, Class_Name, "get_by_name" ,msg.data[0])

    }
  });
}

function get_names_with_args(form_name, Class_Name, Method, arg, obj){
  $.ajax({
    url: "/api/" + Class_Name + "/" + Method + "/" + arg,
    async: false,
    success: function(msg) {
      // alert(msg.message)
      clear_object(obj);
      fill_object(obj, msg.data);
      fill_form(form_name, Class_Name, "get_by_name" ,msg.data[0])

    }
  });
}


// 127.0.0.1:5000/api/Site/get_by_name/siteA

function fill_form(form_name, Class_Name, Method,  SelectedName){
  $.ajax({
    url: "/api/" + Class_Name + "/" + Method + "/" + SelectedName,
    success: function(msg) {
      // alert(msg.message)
      if (form_name=="SiteInfras"){
        fill_form_Site_Infras(msg.data);
      }

      if (form_name=="ProjectInfras"){
        fill_form_Project_Infras(msg.data);
      }
    }
  });
}


// function form_controls_handler() {
//   this.form_controls = form_controls;
//   this.clear_form = function(exclude) {
//     Object.keys(this.form_controls).forEach(function(key, index) {
//       if (!exclude.includes(key)) {
//         clear_object(this.form_controls[key]);
//       }
//     });
//   },
//
//   this.fill_form = function(index, exclude) {
//     var funcSelectedIndex  = index;
//
//     this.clear_form(exclude);
//
//     curr_function = functions[index];
//     Object.keys(this.form_controls).forEach(function(key, index) {
//       if (!exclude.includes(key)) {
//         value = curr_function[key];
//         if (key === "function_select") {
//           var num_of_functions = functions.length;
//           for (i = 0; i < num_of_functions; i++) {
//             var option = document.createElement("option");
//             option.text = functions[i].name;
//             this.form_controls.function_select.add(option);
//           }
//           this.form_controls.function_select.selectedIndex = funcSelectedIndex;
//         } else if (value) {
//           fill_object(this.form_controls[key], value, ParamTableArrayNodes);
//         }
//       }
//     });
//     setOperLineString();
//   },
//   this.get_form_data = function() {
//
//     var tableRowsLength = $("table[name='function_parameters']")[0].rows.length;
//     tableData = [];
//     for (i=1 ; i<tableRowsLength  ; i++) {
//       var currRow = $("table[name='function_parameters']")[0].rows[i]
//
//         // index
//         var index = currRow.cells[0].innerHTML;
//
//         // kind
//         var selectObj = currRow.cells[1].children[0];
//         var kind = selectObj.options[selectObj.selectedIndex].text;
//
//         // value
//         if (currRow.cells[2].childElementCount >0){
//           var value = currRow.cells[2].children[0].value;
//         }else{
//           var value = currRow.cells[2].innerHTML;
//         }
//
//
//         // type
//         var selectObj = currRow.cells[3].children[0];
//         var type = selectObj.options[selectObj.selectedIndex].text;
//
//         var paramRowData = {
//           index: index,
//           kind: kind,
//           value: value,
//           type: type
//         }
//
//         tableData.push(paramRowData)
//     }
