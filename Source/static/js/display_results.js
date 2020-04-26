function get_mission_ids(){
    var select_obj = $('#mission_id_select')[0];
    $.ajax({
        url: "/api/Mission/jsonify_all",
        success: function(result) {
          functions = result;
          alert('got it!');
        }
      });
}

function load_results(){
    var select_obj = $('#mission_id_select')[0];
    mission_id = select_obj.options[select_obj.selectedIndex].text;
    $.ajax({
        url: "/api/AnalyseResult/jsonify_by_mission_id/" + mission_id,
        success: function(result) {
          functions = result;
          alert('got it!');
        }
      });
}


$('#display_button')[0].addEventListener('click',load_results);

get_mission_ids();