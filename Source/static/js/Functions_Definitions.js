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
  description: $("input[name='description']")[0],
  is_class_method: $("input[name='isOutputIsAClass']")[0],
  class_name: $("input[name='outputClassName']")[0],
  function_parameters: $("table[name='function_parameters']")[0]

};

document.querySelector('.custom-file-input').addEventListener('change',function(e){
  var fileName = document.getElementById("functionLocation").files[0].name;
  var nextSibling = e.target.nextElementSibling
  nextSibling.innerText = $('#functionLocation').val()
})

function CreateOperLineString(){
  var fileName = document.getElementById("functionCallback").value;
  // var filename = "ilanFun";
  var OperLineString = fileName + "(conn, RunID";
  var tableRowsLength = $("table[name='function_parameters']")[0].rows.length;
  tableData = [];
  if (tableRowsLength==1){
    OperLineString = OperLineString + ")";
  } else {
      for (i=1 ; i<tableRowsLength  ; i++) {
        var currParam = ""
        var currRow = $("table[name='function_parameters']")[0].rows[i]

        // kind
        var selectObj = currRow.cells[1].children[0];
        var kind = selectObj.options[selectObj.selectedIndex].text;
        if (kind=="text"){
          // value
          if (currRow.cells[2].childElementCount >0){
            currParam = currRow.cells[2].children[0].value;
          }else{
            currParam = currRow.cells[2].innerHTML;
          }
        } else {
            currParam = kind;
        }

        if (i==tableRowsLength - 1){
          OperLineString = OperLineString + ", " + currParam + ")";
        } else {
          OperLineString = OperLineString + ", " + currParam ;
        }
    }
}
return OperLineString;
}

function setOperLineString(){
  var OperString = CreateOperLineString();
  var objOperLine = document.getElementsByName("funcOperLine");
  objOperLine[0].innerHTML = OperString;
}



function calc (){
var className = document.getElementById('className') ;

  if (document.getElementById('isOutputIsAClass').checked)
  {
    className.disabled = false;

  } else {
    className.disabled = true
    className.value ="";
  }
}


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
  setOperLineString()
}

function setParamTblValueField(){
  var currCell = this.parentElement.parentElement.cells[2];
  var selectedParamKind = this.options[this.selectedIndex].text;
   if (selectedParamKind=="text"){
     currCell.innerHTML = [];
     let newElement = document.createElement('input');
     newElement.classList.add("form-control");
     currCell.appendChild(newElement);
   } else {
     setOperLineString();
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


function Create_New_Tbl_Row(table, rowNum){
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
  cell4.appendChild(CreateParamSelectElement(paramsTblType, 0)); // SelectTypeCell

  newElement = document.createElement('button');
  newElement.innerHTML = PlaceRemoveImg();
  newElement.addEventListener('click', RemoveTblRow);

  cell5.appendChild(newElement);
}

function fill_row_data(row_obj, values, header){
  var num_of_values = header.length;

  for(k=0;k<num_of_values;k++){
    if (k===1){ // kind
      var currKindValueIndex = FindParamsTblKindsIndex (paramsTblKinds, values.kind);
      row_obj.cells[1].children[0].selectedIndex = currKindValueIndex;

    }
      else if (k===2 && currKindValueIndex===2){ // value
        currCell = row_obj.cells[2]
        currCell.innerHTML = [];
        let newElement = document.createElement('input');
        newElement.classList.add("form-control");
        newElement.value = values.value;
        currCell.appendChild(newElement);
    }
      else if (k===3){ // type
        var currValueIndex = FindParamsTblTypeIndex (paramsTblType, values.type);
        row_obj.cells[3].children[0].selectedIndex = currValueIndex;
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
  } else if (obj.type === "file") {
    $("#functionLocationLabel")[0].innerHTML = "";

  } else if (obj.type==="checkbox"){
    obj.checked = 0;
    calc ();

  } else {
    obj.value = "";
  }
}

function fill_object(obj, value, header) {
  if (obj.tagName === 'TABLE'){
    var num_of_rows = value.length;
        if (num_of_rows>0){
          // var table = document.getElementsByName("function_parameters")[0];
          var param_keys = Object.keys(value[0]);
          for (i = 0; i < num_of_rows; i++) {
            Create_New_Tbl_Row(obj, i+1);
            var currRow = $("table[name='function_parameters']")[0].rows[i+1]
            fill_row_data(currRow, value[i], header);
          }
        }
  }
  else if (obj.type === "select-one") {
    // var num_of_options = value.options.length;
    // for (i = 0; i < num_of_functions; i++) {
    var option = document.createElement("option");
    option.text = value;
    obj.add(option);
    //   }
  } else if (obj.type==="checkbox"){
    obj.checked = value;
    calc ();

  } else if ( (obj.type==="file")){
    // obj.value = value;
    $("#functionLocationLabel")[0].innerHTML = value;

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
    var funcSelectedIndex  = index;

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
          this.form_controls.function_select.selectedIndex = funcSelectedIndex;
        } else if (value) {
          fill_object(this.form_controls[key], value, ParamTableArrayNodes);
        }
      }
    });
    setOperLineString();
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
      is_class_method: $("input[name='isOutputIsAClass']")[0].checked,
      class_name: $("input[name='outputClassName']")[0].value,
      // changed_date: $("input[name='changed_date']")[0],

      function_parameters: tableData
    }

    return function_data;
  },
  this.get_all_functions = function(mode) {
    $.ajax({
      url: "/api/OctopusFunction/jsonify_all",
      success: function(result) {
        functions = result;
        if (mode==='onReset') {
          functoinIndex = 0;
        } else {
          functoinIndex = result.length-1;
        }
        form_handler.fill_form(functoinIndex, [""]);
      }
    });
  }
}
form_handler = new form_controls_handler();
// form_handler.clear_form();




$("button[name='plus_param_row_button']")[0].addEventListener("click", function() {
  var table = document.getElementsByName("function_parameters")[0];
  var numOfRows = table.rows.length;
  Create_New_Tbl_Row(table, numOfRows);
  setOperLineString();
});

$("input[name='callback']")[0].addEventListener("change", function() {
  setOperLineString();
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
    success: function(msg) {
      alert(msg)
      form_handler.get_all_functions('save');
    }
  });

});

form_controls.function_select.addEventListener("change", function() {
  form_handler.fill_form(this.selectedIndex, ["function_select"]);

});


form_handler.get_all_functions('onReset');
