var Project_form_controls = {
    project_name: $('#project_select')[0],
    project_output_dir: $('#output-dir')[0],
}
var project_data = {
  name: null,
  output_dir: null
};
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
}

function fill_form_Project_Infras(data){
  Project_form_controls.project_output_dir.value = data.output_dir;
}

function fill_form_Site_Infras(data) {
  if(data){
    Site_form_controls.is_site_active.checked = data.is_active;
    Site_form_controls.site_IP.value = data.site_ip;
    Site_form_controls.excersice_site_ip.value = data.execrsice_site_ip;
    Site_form_controls.auto_data_IP.value = data.auto_data_site_ip;
    Site_form_controls.nets.value = data.nets;
    Site_form_controls.stations.value = data.stations;
    Site_form_controls.version_input.value = data.version;
    Site_form_controls.recording_db_ip.value = data.recording_db_ip;
    Site_form_controls.excersice_db_ip.value = data.execrsice_db_ip;
    Site_form_controls.auto_run_DB_IP.value = data.auto_data_db_ip;
  }
}

function AddSiteEventListener(){
  document.getElementById("site_select").addEventListener("change", function() {
     var selectedSiteName = Site_form_controls.site_name.options[Site_form_controls.site_name.selectedIndex].text;
     fill_form("SiteInfras", "Site", "get_by_name" ,selectedSiteName)
  });
}

var newele = null;
infras = new form_controls_handler();
// projects = new Project_form_controls();

// New/Existing Project
$('#project_toggle').change(function() {
  if ($('#project_toggle')[0].checked){ //new
    // alert("New Project");
    infras.new(Project_form_controls, "project_name");
    // infras.new(Site_form_controls, "site_name");
    setToggle("site_toggle", "on");

  } else {
    // alert("Exist");
    infras.exist(Project_form_controls, "project_name","select", "select-one");
    // select Site
    document.getElementById("project_select").addEventListener("change", function() {
      var selectedProjectName = Project_form_controls.project_name.options[Project_form_controls.project_name.selectedIndex].text;
      fill_form("ProjectInfras", "Project", "get_by_name" ,selectedProjectName);
      setToggle("site_toggle", "off");
    });

    get_names("ProjectInfras", "Project", "get_names", Project_form_controls.project_name)
    setToggle("site_toggle", "off");
  }

});

// Save Project
document.getElementById("Save_Project").addEventListener("click", function() {
  var data = {};
  data.name = Project_form_controls.project_name.value;
  data.output_dir = Project_form_controls.project_output_dir.value;
  if ($('#project_toggle')[0].checked) {
    msg = save('Project', data, []);
    if (msg.status === 1){
      setToggle("project_toggle", "off");
    }
  }else{
    msg = update('Project', data, []);
  }
  alert(msg.message);


});

// delete Project
document.getElementById("Delete_Project").addEventListener("click", function() {
  if (!$('#project_toggle')[0].checked) {
    project_name = Project_form_controls.project_name.value;
    msg = item_delete('Project', project_name);
    if (msg.status === 1){
      setToggle("project_toggle", "off");
    }
    alert(msg.message);
  }
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
    // select Site
    AddSiteEventListener();
    var Selected_Project = Project_form_controls.project_name.options[Project_form_controls.project_name.selectedIndex].text;
    get_names_with_args("SiteInfras", "Site", "get_names_by_project_name",Selected_Project,  Site_form_controls.site_name)
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

// select Project
document.getElementById("project_select").addEventListener("change", function() {
   alert("Seleted project");
});

// select Site
// document.getElementById("site_select").addEventListener("change", function() {
//    var selectedSiteName = Site_form_controls.site_name.options[Site_form_controls.site_name.selectedIndex].text;
//    fill_form(form_name, "Site", "get_by_name" ,selectedSiteName)
// });
AddSiteEventListener();

function setToggle(toggleID, state) {
  $('#'+ toggleID).bootstrapToggle(state)
}
