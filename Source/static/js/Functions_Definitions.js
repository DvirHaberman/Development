// getting all form controls into one object
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
  changed_date: $("input[name='changed_date']")[0]
};

function clear_object(obj) {
  if (obj.type === "select-one") {
    var num_of_options = obj.options.length;
    for (i = 0; i < num_of_options; i++) {
      obj.remove(0);
    }
  } else {
    obj.value = "";
  }
}

function fill_object(obj, value) {
  if (obj.type === "select-one") {
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
          fill_object(this.form_controls[key], value);
        }
      }
    });
  };
}
form_handler = new form_controls_handler();
// form_handler.clear_form();

$("a[name='new_function_button']")[0].addEventListener("click", function() {
  form_handler.clear_form(["function_select"]);
});

form_controls.function_select.addEventListener("change", function() {
  form_handler.fill_form(this.selectedIndex, ["function_select"]);
});

var functions = [];

$.ajax({
  url: "/api/OctopusFunction/return_all",
  success: function(result) {
    functions = result;
    form_handler.fill_form(0, [""]);
  }
});
