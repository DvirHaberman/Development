// getting all form controls into one object
var current_user = 'ami';
var current_version = 1;
var parmasHeader  =  ["ID", "kind", "value", "type", "remove"];
var functionArray = ["incValue", "byValue",  "placeRemoveImg"];
var paramsTblHeader  =  ["ID", "kind", "value", "type", "remove"];
var paramsTblFunctionArray = [IncValue, "byValue",  "byValue","byValue", PlaceRemoveImg];
var paramsTblIsByValue = [0, 1, 1, 1, 0];
var paramsTblKinds = ["Sys Params",  "Tests Params",  "text"];
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

function RemoveTblRow(){
  var table = document.getElementsByName("function_parameters")[0];
  var rowIndex = this.parentElement.parentElement.rowIndex;
  table.deleteRow(rowIndex);
  for (i=1 ; i< table.rows.length; i++){
      table.rows[i].cells[0].innerHTML = i;
  }
}

function setParamTblValueField(){
  var currCell = this.parentElement.parentElement.cells[2];
  var selectedParamKind = this.options[this.selectedIndex].text;
   if (selectedParamKind=="text"){
     currCell.innerHTML = [];
     let newElement = document.createElement('input');
     newElement.classList.add("form-control");
     currCell.appendChild(newElement);
   }
   else {
     currCell.innerHTML = "--";
   }

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
  var index = paramsTblType.indexOf( name);
  return index
}

function CreateParamEmptyBottunElement(PlaceRemoveImg){
  let newElement = document.createElement('bottun');
  newElement = PlaceRemoveImg;
  return newElement;
}

function CreateParamSelectElement(paramsTblArray, currValueIndex) {
    let newElement = document.createElement('select');

      for (m = 0; m < paramsTblArray.length; m++) {
          var currKind =  paramsTblArray[m];
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

      return newElement
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
            newElement.innerHTML = '--';
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
            let newElement = document.createElement('select');

              for (m = 0; m < paramsTblType.length; m++) {
                  var currType =  paramsTblType[m];
                  // newElement.setAttribute("id", "MykindsDown");
                  var option = document.createElement("option");
                  option.value = m;
                  option.text = currType;
                  option.classList.add("table-option");
                  newElement.add(option);
              }

              newElement.classList.add("form-control");
              newElement.classList.add("table-select");
              newElement.selectedIndex =  currValueIndex;
              newCell.appendChild(newElement)
          }

        }
      } else if(header[k].Header === 'ID') {
       let newText = document.createTextNode('');
       newText.data = rowNums - 1;
       newCell.appendChild(newText);
      } else{
        newElement = document.createElement('button');
        newElement.innerHTML = PlaceRemoveImg();
        newElement.addEventListener('click', RemoveTblRow);
        // newCell.innerHTML = header[k].handle();
        newCell.appendChild(newElement);
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
  },

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

    var tableRowsLength = $("table[name='function_parameters']")[0].rows.length;
    tableData = [];
    for (i=1 ; i<tableRowsLength  ; i++) {
      var currRow = $("table[name='function_parameters']")[0].rows[i]

        // index
        var index = currRow.cells[0].innerHTML;

        // kind
        var selectObj = currRow.cells[1].children[0];
        var kind = selectObj.options[selectObj.selectedIndex].text;

        // value
        if (currRow.cells[2].childElementCount >0){
          var value = currRow.cells[2].children[0].value;
        }else{
          var value = currRow.cells[2].innerHTML;
        }
        

        // type
        var selectObj = currRow.cells[3].children[0];
        var type = selectObj.options[selectObj.selectedIndex].text;

        var paramRowData = {
          index: index,
          kind: kind,
          value: value,
          type: type
        }

        tableData.push(paramRowData)
    }

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
      function_parameters: tableData
    }

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




$("button[name='plus_param_row_button']")[0].addEventListener("click", function() {
  var table = document.getElementsByName("function_parameters")[0];
  var numOfRows = table.rows.length;
  var newRow = table.insertRow(numOfRows);
  // fill_row(newRow, [], ParamTableArrayNodes)
  var cell1 = newRow.insertCell(0);
  var cell2 = newRow.insertCell(1); //kind
  var cell3 = newRow.insertCell(2); //value
  var cell4 = newRow.insertCell(3); //type
  var cell5 = newRow.insertCell(4); // remove Img

  cell1.innerHTML = numOfRows;
  let newElement = CreateParamSelectElement(paramsTblKinds, 0)
  newElement.addEventListener('change', setParamTblValueField);
  cell2.appendChild(newElement); // SelectKindCell

  cell3.innerHTML = "--";
  cell4.appendChild(CreateParamSelectElement(paramsTblType, 0)); // SelectTypeCell

  newElement = document.createElement('button');
  newElement.innerHTML = PlaceRemoveImg();
  newElement.addEventListener('click', RemoveTblRow);

  cell5.appendChild(newElement);


});

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
      alert("Function '"  + data.name + "' was successfuly saved!")
      form_handler.get_all_functions();
    }
  });

});

form_controls.function_select.addEventListener("change", function() {
  form_handler.fill_form(this.selectedIndex, ["function_select"]);
});


form_handler.get_all_functions();
