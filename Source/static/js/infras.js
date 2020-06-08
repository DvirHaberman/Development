var Project_form_controls = {
    project_name: $('#project_select')[0],
    project_output_dir: $('#output-dir')[0],

}

var Site_form_controls = {
  site_name: $('#site_select')[0],
  is_site_active: $('#is_site_active_cb')[0],
  site_IP: $('#site_ip')[0],
  excersice_site_ip: $('#excersice_site_ip')[0],
  auto_data_IP: $('#auto_data_IP')[0],
  nets: $('#nets')[0],
  stations: $('#stations')[0],
  version_input: $('#version_input')[0],
  recording_db_ip: $('#recording_db_ip')[0],
  excersice_db_ip: $('#excersice_db_ip')[0],
  auto_run_DB_IP: $('#auto_run_DB_IP')[0],

};

fill_form_Site_Infras(data) {
  Site_form_controls.is_site_active.value = data
  Site_form_controls.site_IP.value = data
  Site_form_controls.excersice_site_ip.value = data
  Site_form_controls.auto_data_IP.value = data
  Site_form_controls.nets.value = data
  Site_form_controls.stations.value = data
  Site_form_controls.version_input.value = data
  Site_form_controls.recording_db_ip.value = data
  Site_form_controls.excersice_db_ip.value = data
  Site_form_controls.auto_run_DB_IP.value = data
}



var newele = null;
infras = new form_controls_handler();
// projects = new Project_form_controls();

// New/Existing Project
$('#project_toggle').change(function() {
  if ($('#project_toggle')[0].checked){ //new
    // alert("New Project");
    infras.new(Project_form_controls, "project_name");
    infras.new(Site_form_controls, "site_name");

  } else {
    // alert("Exist");
    infras.exist(Project_form_controls, "project_name","select", "select-one");
    // projects.get_names();   // get project_names from DB
    // // Show Project1 Database
    // // exist Site



  }

});

// Save Project
document.getElementById("Save_Project").addEventListener("click", function() {
  alert("Save Project");
  // var id = form_controls_handler.create_id();
  // alert('your id is ' + id);
});

// delete Project
document.getElementById("Delete_Project").addEventListener("click", function() {
   alert("Delete Project");
});

// New/Existing Site
document.getElementById("site_toggle").addEventListener("click", function() {
  alert("New/Existing Site");
});

$('#site_toggle').change(function() {
  if ($('#site_toggle')[0].checked){ //new
    infras.new(Site_form_controls, "site_name");

  } else {
    infras.exist(Site_form_controls, "site_name","select", "select-one");
    get_names("SiteInfras", "Site", "get_names", Site_form_controls.site_name)
    // infras.exist(Site_form_controls, "site_name");
  }

});
// ask for all site get_names
//     --> ask for data of the first site
// ask for data of the site X

// Save Site
document.getElementById("Save_Site").addEventListener("click", function() {
  alert("Save Site");
  // var id = form_controls_handler.create_id();
  // alert('your id is ' + id);
});

// Duplicate Site
document.getElementById("Duplicate_Site").addEventListener("click", function() {
  alert("Duplicate Site");
  // var id = form_controls_handler.create_id();
  // alert('your id is ' + id);
});

// delete Site
document.getElementById("Delete_Site").addEventListener("click", function() {
   alert("Delete Site");
});

//  Check Recording
document.getElementById("check_Recording_DB_IP").addEventListener("click", function() {
   alert("checking Recording DB IP");
});

//  Check Excersice_DB_IP
document.getElementById("check_excersice_db_ip").addEventListener("click", function() {
   alert("checking Excersice DB IP");
});

// check check_Auto_Run_DB_IP
document.getElementById("check_Auto_Run_DB_IP").addEventListener("click", function() {
   alert("checking Auto_Run DB IP");
});
