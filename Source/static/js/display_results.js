function get_mission_ids(){
    var select_obj = $('#mission_id_select')[0];
    $.ajax({
        url: "/api/Mission/jsonify_all",
        success: function(result)  {
          var num_of_missions = result.length;
          var num_of_curr_missions = select_obj.options.length;
          for(i=0;i<num_of_curr_missions;i++){
              select_obj.remove(0);
          }
          for(i=0;i<num_of_missions;i++){
              opt= document.createElement('option');
              opt.text = result[i].id
              select_obj.appendChild(opt);
          }
        }
      });
}

function load_results(){
    var select_obj = $('#mission_id_select')[0];
    mission_id = select_obj.options[select_obj.selectedIndex].text;
    $.ajax({
        url: "/api/AnalyseResult/jsonify_by_mission_id/" + mission_id,
        success: function(result) {
          var results_table_div = $('#results_table_div')[0];
          var results_table = $('#results_table')[0];
          results_table_div.removeChild(results_table)
          results_table = document.createElement('table');
          results_table.id = 'results_table';
          results_table.classList.add(["table"]);
          results_table.classList.add(["table-hover"]);
          results_table.classList.add(["col-10"]);
          results_table.classList.add(["m-auto"]);
          results_table_div.appendChild(results_table);
          num_of_cols = result.schema.fields.length;
          num_of_rows = result.data.length;
          newRow = results_table.insertRow(-1);
          th = document.createElement('th');
          th.innerHTML = 'Results for mission '+ mission_id;
          newRow.appendChild(th);
          th.colspan = num_of_cols; 
          newRow = results_table.insertRow(-1);
          // newRow.insertCell(0);
          for(i=0;i<num_of_cols;i++){
            th = document.createElement('th');
            th.innerHTML = result.schema.fields[i].name;
            newRow.appendChild(th);
          }
          for(i=0;i<num_of_rows;i++){
            newRow = results_table.insertRow(-1);
            for (j=0; j<num_of_cols; j++){
              td = document.createElement('td');
              var status = result.data[i][result.schema.fields[j].name];
              // var status_text = '';
              if(j>0){
                switch (status) {
                  case 0:
                    status = 'No Data';
                    td.bgColor = 'blue';
                    break;
                  case 1:
                    status = 'Error';
                    td.bgColor = 'gray';
                    break;
                  case 2:
                    status = 'Fail';
                    td.bgColor = 'red';
                    break;
                  case 3:
                    status = 'Warning';
                    td.bgColor = 'orange';
                    break;
                  case 4:
                    status = 'Success';
                    td.bgColor = 'green';
                    break;
                  default:
                    status = 'in process';
                    // td.bgColor = 'green';
                    break;
                }
              }
              td.innerHTML = status;
              newRow.appendChild(td);
            }
          }
          
        }
      });
}

$('#display_button')[0].addEventListener('click',load_results);

get_mission_ids();