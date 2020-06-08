var form_controls = {
  project_name: $("select[id='project_select']")[0],
  project_output_dir: $("input[id='output-dir']")[0],
  site_name: $("select[id='site_select']")[0],
  is_site_active: $("input[id='is_site_active_cb']")[0],
  site_IP: $("input[name='site_ip']")[0],
  excersice_site_ip: $("input[name='excersice_site_ip']")[0],
  auto_data_IP: $("input[name='auto_data_IP']")[0],
  nets: $("input[name='nets']")[0],
  stations: $("input[name='stations']")[0],
  version_input: $("input[name='version_input']")[0],
  recording_db_ip: $("input[name='recording_db_ip']")[0],
  excersice_db_ip: $("input[name='excersice_db_ip']")[0],
  auto_run_DB_IP: $("input[name='auto_run_DB_IP']")[0],
};

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
  } else if (obj.type==="checkbox"){
    obj.checked = 0;
    calc ();

  } else {
    obj.value = "";
  }
}


function form_controls_handler() {
  this.form_controls = form_controls;
  this.clear_form = function(exclude) {
    Object.keys(this.form_controls).forEach(function(key, index) {
      if (!exclude.includes(key)) {
        clear_object(this.form_controls[key]);
      }
    });
  },
  //
  // this.fill_form = function(index, exclude) {
  //   var funcSelectedIndex  = index;
  //
  //   this.clear_form(exclude);
  //
  //   curr_function = functions[index];
  //   Object.keys(this.form_controls).forEach(function(key, index) {
  //     if (!exclude.includes(key)) {
  //       value = curr_function[key];
  //       if (key === "function_select") {
  //         var num_of_functions = functions.length;
  //         for (i = 0; i < num_of_functions; i++) {
  //           var option = document.createElement("option");
  //           option.text = functions[i].name;
  //           this.form_controls.function_select.add(option);
  //         }
  //         this.form_controls.function_select.selectedIndex = funcSelectedIndex;
  //       } else if (value) {
  //         fill_object(this.form_controls[key], value, ParamTableArrayNodes);
  //       }
  //     }
  //   });
  //   setOperLineString();
  // },
  // this.get_form_data = function() {
  //
  //   var function_data = {
  //     owner: current_user,
  //     version: current_version,
  //     version_comments: $("textarea[name='version_comments']")[0].value,
  //     name: $("input[name='name']")[0].value,
  //     kind: $("input[name='kind']")[0].value,
  //     tags: $("input[name='tags']")[0].value,
  //     callback: $("input[name='callback']")[0].value,
  //     location: $("input[name='Location']")[0].value,
  //     description: $("input[name='description']")[0].value,
  //     is_class_method: $("input[name='isOutputIsAClass']")[0].checked,
  //     class_name: $("input[name='outputClassName']")[0].value,
  //     // changed_date: $("input[name='changed_date']")[0],
  //
  //     function_parameters: tableData
  //   }
  //
  //   return function_data;
  // },
  // this.get_all_functions = function(mode) {
  //   $.ajax({
  //     url: "/api/OctopusFunction/jsonify_all",
  //     success: function(result) {
  //       functions = result;
  //       if (mode==='onReset') {
  //         functoinIndex = 0;
  //       } else {
  //         functoinIndex = result.length-1;
  //       }
  //       form_handler.fill_form(functoinIndex, [""]);
  //     }
  //   });
  // }
}


$("button[id='project_toggle']")[0].addEventListener(function() {
  form_handler.clear_form(["site_ip"])
});
