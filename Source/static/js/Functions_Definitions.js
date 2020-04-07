// getting all form controls into one object
var current_user = 'ami';
var current_version = 1;
var parmasHeader  =  ["ID", "kind", "value", "type", "remove"];
var functionArray = ["incValue", "byValue",  "placeRemoveImg"];
var paramsTblHeader  =  ["ID", "kind", "value", "type", "remove"];
var paramsTblFunctionArray = [IncValue, "byValue",  "byValue","byValue", PlaceRemoveImg];
var paramsTblIsByValue = [0, 1, 1, 1, 0];
var paramsTblKinds = ["Sys Params",  "Octopus Params",  "text"];
var paramsTblType = ["DataFrame", "String", "Number"];
var functions = [];


var form_controls = {
  function_select: $("select[name='function_select']")[0],
  owner: $("select[name='owner']")[0],
  version: $("select[name='version']")[0],
  function_checksum: $("input[name='function_checksum']")[0],
  version_comments: $("textarea[name='version_comments']")[0],
  name: $("input[name='name']")[0],
  kind: $("input[name='kind']")[0],
  tags: $("input[name='tags']")[0],
  callback: $("input[name='callback']")[0],
  location: $("input[name='location']")[0],
  description: $("input[name='description']")[0],
  changed_date: $("input[name='changed_date']")[0],
  function_parameters: $("table[name='function_parameters']")[0]
};

// Definition and Assignment TableHeaderNodes //

function IncValue(value){
  return value+1;
}

function PlaceRemoveImg(){
  return '<i class="far fa-trash-alt"></i>';
}

function TableHeaderNodes(key, handleFunction, isByValue){
  this.Header = key;
  this.handle = handleFunction;
  this.isByValue = isByValue;
}


function FillHeaderNodes(parmasHeader,functionArray, isByValue ){

  var TableHeaderNodesArray = [];
  for  (i=0; i<parmasHeader.length; i++){
    // var node = new TableHeaderNodes(parmasHeader[i], functionArray[i], isByValue[i])
    TableHeaderNodesArray.push(new TableHeaderNodes(parmasHeader[i], functionArray[i], isByValue[i]));
  }
  return TableHeaderNodesArray;
}

var ParamTableArrayNodes = FillHeaderNodes(paramsTblHeader,paramsTblFunctionArray, paramsTblIsByValue );
//  //


function FindParamsTblKindsIndex (paramsTblKinds, name){
  var index = paramsTblKinds.indexOf( name);
  return index
}

function FindParamsTblTypeIndex (paramsTblType, name){
  var index = paramsTblKinds.indexOf( name);
  return index
}

function fill_row(row_obj, values, header){
  // header === ParamTableArrayNodes

    var num_of_values = header.length;
    var value_to_put = '';
    var currField = '';
    var rowNums = form_controls.function_parameters.rows.length;

    for(k=0;k<num_of_values;k++){
      newCell = row_obj.insertCell(-1);

      if (header[k].isByValue){
        if (header[k].Header === 'value') {
          var currKindValue =  values[rowNums-2][header[1].Header];
          if (currKindValue === 'text') {
            let newElement = document.createElement('input');
            newElement.value = values[rowNums-2][header[k].Header];
            newElement.classList.add("form-control");
            newCell.appendChild(newElement);
            // <td><select name="" id="" class="form-control table-select">
            //     <option selected class="table-option">BM-Params</option>

          } else {
            let newElement = document.createElement('text');
            newCell.appendChild(newElement);
          }

        } else {
          var currValue = values[rowNums-2][header[k].Header];

          if (k===1){ // kind
            var textArray = paramsTblKinds;
            var currValueIndex = FindParamsTblKindsIndex (textArray, currValue);
            let newElement = document.createElement('select');

              for (m = 0; m < paramsTblKinds.length; m++) {
                  var currKind =  paramsTblKinds[m];
                  // newElement.setAttribute("id", "MykindsDown");
                  var option = document.createElement("option");
                  option.value = m;
                  option.text = currKind;
                  option.classList.add("table-option");
                  newElement.add(option);
              }

              newElement.classList.add("form-control");
              newElement.classList.add("table-select");
              newElement.selectedIndex =  currValueIndex;
              newCell.appendChild(newElement)

          }
          else if (k===3){  // Type
            var textArray = paramsTblType;
            var currValueIndex = FindParamsTblTypeIndex (textArray, currValue);
          }

          // let newElement = document.createElement('select');
          // newElement.setAttribute("id", "MykindsDown");
          // var clownElement = Object.assign($("#MykindsDown")[0]);
          // clownElement.selectedIndex =  currValueIndex;
          //
          // // var option = document.createElement("option");
          // // option.value =  currValueIndex;
          // // option.text = textArray;
          // // option.classList.add("table-option");
          // // newElement.add(option);
          // // newElement.classList.add("form-control");
          // // newElement.classList.add("table-select");
          //
          // newCell.appendChild(clownElement);
        }
      } else if(header[k].Header === 'ID') {
       let newText = document.createTextNode('');
       newText.data = rowNums - 1;
       newCell.appendChild(newText);
      } else{
        newCell.innerHTML = header[k].handle();
      }



  }
}

function clear_object(obj) {
  if (obj.tagName === 'TABLE'){
    var num_of_rows = obj.rows.length;
    for (i = 0; i < num_of_rows-1; i++) {
      obj.deleteRow(1);
    }
  }
  else if (obj.type === "select-one") {
    var num_of_options = obj.options.length;
    for (i = 0; i < num_of_options; i++) {
      obj.remove(0);
    }
  } else {
    obj.value = "";
  }
}

function fill_object(obj, value, header) {
  if (obj.tagName === 'TABLE'){
    var num_of_rows = value.length;
    var param_keys = Object.keys(value[0]);
    for (i = 0; i < num_of_rows; i++) {
      newRow = obj.insertRow(-1);
      fill_row(newRow, value, header);
    }
  }
  else if (obj.type === "select-one") {
    // var num_of_options = value.options.length;
    // for (i = 0; i < num_of_functions; i++) {
    var option = document.createElement("option");
    option.text = value;
    obj.add(option);
    //   }
  } else {
    obj.value = value;
  }
}

function get_data_from_control(obj){
  if (obj.tagName === 'TABLE'){
// fill later
    return null;
  }
  else if (obj.type === "select-one") {
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
////////////////////////////////////////////////////////////////////////////
// Declaring the form handler class.                                      //
// this class is holding all the form object controls and is in charge of //
// clearing and filling the form                                          //
////////////////////////////////////////////////////////////////////////////



function form_controls_handler() {
  this.form_controls = form_controls;
  this.clear_form = function(exclude) {
    Object.keys(this.form_controls).forEach(function(key, index) {
      if (!exclude.includes(key)) {
        clear_object(this.form_controls[key]);
      }
    });
  };

  this.fill_form = function(index, exclude) {
    this.clear_form(exclude);

    curr_function = functions[index];
    Object.keys(this.form_controls).forEach(function(key, index) {
      if (!exclude.includes(key)) {
        value = curr_function[key];
        if (key === "function_select") {
          var num_of_functions = functions.length;
          for (i = 0; i < num_of_functions; i++) {
            var option = document.createElement("option");
            option.text = functions[i].name;
            this.form_controls.function_select.add(option);
          }
        } else if (value) {
          fill_object(this.form_controls[key], value, ParamTableArrayNodes);
        }
      }
    });
  },
  this.get_form_data = function() {
    var function_data = {
      owner: current_user,
      version: current_version,
      version_comments: $("textarea[name='version_comments']")[0].value,
      name: $("input[name='name']")[0].value,
      kind: $("input[name='kind']")[0].value,
      tags: $("input[name='tags']")[0].value,
      callback: $("input[name='callback']")[0].value,
      location: $("input[name='location']")[0].value,
      description: $("input[name='description']")[0].value,
      // changed_date: $("input[name='changed_date']")[0],
      // function_parameters: $("table[name='function_parameters']")[0]
    };
    return function_data;
  },
  this.get_all_functions = function() {
    $.ajax({
      url: "/api/OctopusFunction/jsonify_all",
      success: function(result) {
        functions = result;
        form_handler.fill_form(0, [""]);
      }
    });
  }
}
form_handler = new form_controls_handler();
// form_handler.clear_form();

$("a[name='new_function_button']")[0].addEventListener("click", function() {
  form_handler.clear_form(["function_select", "owner" , "version" , "function_checksum", "version_comments", "changed_date" ]);
});

$("a[name='save_function_button']")[0].addEventListener("click", function() {
  data = form_handler.get_form_data();
  $.ajax({
    type: "POST",
    url: "/api/OctopusFunction/save_function",
    dataType: "json",
    data: JSON.stringify(data),
    contentType: 'application/json',
    success: function(result) {
<<<<<<< HEAD
      alert("Function '"  + data.name + "' was successfuly saved!")
      form_handler.get_all_functions();
    }
  });
  
=======
      var dd = result;
      form_handler.get_all_functions();
    }
  });
>>>>>>> 66acceedf5f2e3a9ab41221d39a3c4d3a3c501dd
});

form_controls.function_select.addEventListener("change", function() {
  form_handler.fill_form(this.selectedIndex, ["function_select"]);
});


form_handler.get_all_functions();