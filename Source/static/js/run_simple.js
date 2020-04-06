var functions;
var function_select = $('#functions_select')[0];
var run_ids_select_button = $('#run_ids_select_button')[0];
var run_ids_text_button = $('#run_ids_text_button')[0];
var res_table = $('#res_table')[0];
var database_select = $('#database_select')[0];

function fill_table(data){
    var num_of_rows = res_table.rows.length;
    
    for (i = 0; i < num_of_rows; i++) {
      res_table.deleteRow(0);
    }
    var num_of_rows = data.function_names.length;
    var num_of_cols = data.runs.length;
    var curr_result = 0;
    newRow = res_table.insertRow(-1);
    // newCell = newRow.insertCell(0);
    let new_th = document.createElement("th");
    new_th.innerHTML = 'functions/run_ids';
    newRow.appendChild(new_th);
    for(i=0;i<num_of_cols;i++){
        // newCell = newRow.insertCell(-1);
        let new_th = document.createElement("th");
        new_th.innerHTML = data.runs[i];
        newRow.appendChild(new_th);
    }
    for (i = 0; i < num_of_rows; i++) {
        newRow = res_table.insertRow(-1);
        newCell = newRow.insertCell(0);
        let newText = document.createTextNode('');
        newText.data = data.function_names[i];
        newCell.appendChild(newText);
        for(k=0; k < num_of_cols;k++){
            newCell = newRow.insertCell(-1);
            let newText = document.createTextNode('');
            curr_result = data.results[k+(i*num_of_cols)].result.result_status;
            switch(curr_result){
                case 0:
                    newText.data = 'no data';
                    newCell.bgColor = 'white';
                    break;
                case 1:
                    newText.data = 'error';
                    newCell.bgColor = 'gray';
                    break;
                case 2:
                    newText.data = 'fail';
                    newCell.bgColor = 'red';
                    break;
                case 3:
                    newText.data = 'warning';
                    newCell.bgColor = 'orange'
                    break;
                case 4:
                    newText.data = 'success';
                    newCell.bgColor = 'green'
            }
            
            newCell.appendChild(newText);
        }
    }
}

$.ajax({
    url: "/api/OctopusFunction/jsonify_all",
    success: function(result) {
      functions = result;
      var num_of_functions = functions.length;
      for (i = 0; i < num_of_functions; i++) {
        var option = document.createElement("option");
        option.text = functions[i].name;
        function_select.add(option);
      }    }
  });

  run_ids_select_button.addEventListener('click', function(){
    run_id = run_ids_select.options[run_ids_select.selectedIndex].innerHTML;
    // function_ids=functions.filter(obj=>{return [1,3].includes(obj.id)})
    name = function_select.options[function_select.selectedIndex].innerHTML;
    function_id=functions.filter(obj=>{return obj.name === name})[0].id;
    database = database_select.options[database_select.selectedIndex].value
    var data = {
        functions:function_id,
        runs: run_id,
        db_name: database
    };
    $.ajax({
        type: "POST",
        url: "/api/run_functions",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(result) {
          fill_table(result);
        }
      });
  });

  run_ids_text_button.addEventListener('click', function(){
    run_ids = run_ids_text.value.split(',');
    // function_ids=functions.filter(obj=>{return [1,3].includes(obj.id)})
    name = function_select.options[function_select.selectedIndex].innerHTML;
    function_id=functions.filter(obj=>{return obj.name === name})[0].id;
    database = database_select.options[database_select.selectedIndex].text
    var data = {
        functions:function_id,
        runs: run_ids,
        db_name: database
    };
    $.ajax({
        type: "POST",
        url: "/api/run_functions",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(result) {
          fill_table(result);
        }
      });
  });