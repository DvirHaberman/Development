var functions;
var function_select = $('#functions_select')[0];
var function_datalist = $('#function_datalist')[0];
var add_run_id_button = $('#add_run_id_button')[0];
var add_function_button = $('#add_function_button')[0];
var res_table = $('#res_table')[0];
var functions_list = $('#functions_list')[0];
var run_ids_list = $('#run_ids_list')[0];
var database_select = $('#database_select')[0];
var run_ids_select = $('#run_ids_select')[0];
var go_button = $('#go_button')[0];
var run_ids_datalist = $('#run_ids_datalist')[0];

function add_function(){
  if (functions_list.value === ''){
    functions_list.value = function_select.value;//.options[function_select.selectedIndex].text;
  }else{
    functions_list.value = functions_list.value + ',' + function_select.value;//.options[function_select.selectedIndex].text;
  }
}

function add_run_id(){
  if (run_ids_list.value === ''){
    run_ids_list.value = run_ids_select.value;//options[run_ids_select.selectedIndex].text;
  }else{
    run_ids_list.value = run_ids_list.value + ',' + run_ids_select.value;//.options[run_ids_select.selectedIndex].text;
  }
  
}
function get_all_functions(){
  $.ajax({
      url: "/api/OctopusFunction/jsonify_all",
      success: function(result) {
        functions = result;
        var num_of_functions = functions.length;
        for (i = 0; i < num_of_functions; i++) {
          var option = document.createElement("option");
          option.text = functions[i].name;
          function_datalist.appendChild(option);
        }    
      }
  });
}

  function load_run_ids(db_name){
    $.ajax({
      url: "/api/DbConnector/get_run_ids/" + db_name,
      success: function(result) {
        var num_of_runs = result.length;
        // var num_of_current_runs = run_ids_select.options.length;
        // for (i = 0; i < num_of_current_runs; i++) {
        //   run_ids_select.remove(0);
        // }
        var num_of_current_runs = run_ids_datalist.options.length;
        for (i = 0; i < num_of_current_runs; i++) {
          run_ids_datalist.removeChild(run_ids_datalist.options[0]);
        }
        
        for (i = 0; i < num_of_runs; i++) {
          // var option = document.createElement("option");
          // option.text = result[i];
          // run_ids_select.add(option);
          var option = document.createElement("option");
          option.text = result[i];
          run_ids_datalist.appendChild(option);
          
        }    
      }
    });
  }
  function run_setup(){
    run_ids = run_ids_list.value;
    // function_ids=functions.filter(obj=>{return [1,3].includes(obj.id)})
    // name = function_select.options[function_select.selectedIndex].innerHTML;
    function_names=functions_list.value;
    database_name = database_select.options[database_select.selectedIndex].value
    var data = {
        functions:function_names,
        runs: run_ids,
        db_name: database_name
    };
    $.ajax({
        type: "POST",
        url: "/api/run_functions",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(result) {
          alert('your mission id is: ' + result);
          get_mission_ids();
        }
      });
  }

  
  add_run_id_button.addEventListener('click',add_run_id);
  add_function_button.addEventListener('click',add_function);
  database_select.addEventListener('change',function(){load_run_ids(database_select.options[database_select.selectedIndex].text)});
  go_button.addEventListener('click', run_setup);
  function get_db_names(){
    var num_of_options = database_select.options.length;
    for(i=0;i<num_of_options;i++)
    {
        database_select.remove(0);
    }
    $.ajax({
        url: "/api/DbConnections/get_names",
        success: function(conn_names) {
          var num_of_conns = conn_names.length;
          for (i = 0; i < num_of_conns; i++) {
            var option = document.createElement("option");
            option.text = conn_names[i];
            database_select.add(option);
            load_run_ids(database_select.options[0].text);
            get_all_functions();
          }    
        }
      });
  }

  get_db_names();