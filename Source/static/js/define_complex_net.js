var Metadata_form_controls = {
    Name: $('#meta_name')[0],
    Id: $('#meta_id')[0],
    Owner: $('#meta_owner')[0],
    Tags: $('#meta_tags')[0],
    Description: $('#meta_description')[0],
    MetaDate: $('#meta_date')[0],
}

var Config_form_controls = {
    Link_System: $('#Link_System')[0],
    Link_Ext_Simulation: $('#Link_Ext_Simulation')[0],
    Simulation_Watch: $('#Simulation_Watch')[0],
    Simulation_DIS: $('#Simulation_DIS')[0],
    Simulation_Ext_Sim_Flag: $('#ext_sim_cb')[0],
    Backup_Env: $('#Backup_Env')[0],
    Backup_env_sim_Flag: $('#ext_env_sim_cb')[0],
}


var Complex_Net_form_controls = {
    Sensors: {
        Sensors1: $('#Sensors1')[0],
        Sensors2: $('#Sensors2')[0],
        Sensors3: $('#Sensors3')[0],
        Sensors4: $('#Sensors4')[0]
    },
    Sords: {
        Sord1: $('#Sord1')[0],
        Sord2: $('#Sord2')[0],
        Sord3: $('#Sord3')[0],
        Sord4: $('#Sord4')[0],
        Sord5: $('#Sord5')[0],
        Sord6: $('#Sord6')[0],
        Sord7: $('#Sord7')[0],
        Sord8: $('#Sord8')[0]
    },
    Looks: {
        look1: $('#look1')[0],
        look2: $('#look2')[0],
        look3: $('#look3')[0],
        look4: $('#look4')[0]
    },
    Hears: {
        Hear1: $('#Hear1')[0],
        Hear2: $('#Hear2')[0],
        Hear3: $('#Hear3')[0],
        Hear4: $('#Hear4')[0],
        Hear5: $('#Hear5')[0],
        Hear6: $('#Hear6')[0],
        Hear7: $('#Hear7')[0],
        Hear8: $('#Hear8')[0],
        Hear9: $('#Hear9')[0],
        Hear10: $('#Hear10')[0]
    },
    Glasses: {
        Glasses1: $('#Glasses1')[0]
    }
}




function fill_form_ComplexNet(data) {
    if (data) {
        //  Metadata
        Metadata_form_controls.Name.value = data.is_active;
        Metadata_form_controls.Id.value = data.site_ip;
        Metadata_form_controls.Owner.value = data.execrsice_site_ip;
        Metadata_form_controls.Tags.value = data.auto_data_site_ip;
        Metadata_form_controls.Description.value = data.nets;
        Metadata_form_controls.Date.value = data.stations;

        // //  Config
        // var Config_Obj_Names = Metadata_form_controls
        // for (i=0; i<Config_Obj_Names.Length; i++){
        //   fill_object(Config_form_controls.(Config_Obj_Names[i]), data.Config_Obj_Names[i])
        // }
        //
        // //  ComplexNet
        // for (i=0; i<Config_Obj_Names.Length; i++){
        //   fill_object(Config_form_controls.(Config_Obj_Names[i]), data.Config_Obj_Names[i])
        // }

    }
}

// function get_form (){
//   var data = {};
//     data.name = Project_form_controls.project_name.value;
//     data.output_dir = Project_form_controls.project_output_dir.value;
//     data.project_name = Project_form_controls.project_name.value;
//     data.name = Site_form_controls.site_name.value;
//     data.version = Site_form_controls.version_input.value;
//     data.is_active = Site_form_controls.is_site_active.checked;
//     data.site_ip = Site_form_controls.site_IP.value;
//     data.recording_db_ip = Site_form_controls.recording_db_ip.value;
//     data.execrsice_site_ip = Site_form_controls.excersice_site_ip.value;
//     data.execrsice_db_ip = Site_form_controls.excersice_db_ip.value;
//     data.auto_data_site_ip = Site_form_controls.auto_data_IP.value;
//     data.auto_data_db_ip = Site_form_controls.auto_run_DB_IP.value;
//     data.nets = Site_form_controls.nets.value;
//     data.stations = Site_form_controls.stations.value;
//   return data
// }



var newele = null;
complexNet = new form_controls_handler();
// projects = new Project_form_controls();

// New/Existing ComplexNet
$('#NewExist_toggle').change(function() {
    if ($('#NewExist_toggle')[0].checked) { //new
        alert("New ComplexNet");
        complexNet.new(Metadata_form_controls, "noChange");
        Metadata_form_controls.Name.setAttribute("list", null);
        fillComplexNetDefaultCT();
        // Should Be added: ComplexNetDefult.
    } else {
        complexNet.exist(Metadata_form_controls, "meta_name", "select", "select-one"); //todo: to change to dataList
        // select Site
        Metadata_form_controls.Name.setAttribute("list", "meta_name_datalist");
        document.getElementById("meta_name").addEventListener("change", function() {
            var selectedComplexNetName = Metadata_form_controls.Name.text;
            fill_form("ComplexNet", "ComplexNet", "get_by_name", selectedComplexNetName);
        });
        get_names("ComplexNet", "ComplexNet", "get_names", Metadata_form_controls.Name)
    }

});
//
// // Save  ComplexNet
// document.getElementById("Save_Project").addEventListener("click", function() {
//   var data = {};
//   data = get_form('Project');
//
//   if ($('#project_toggle')[0].checked) {
//     msg = save('Project', data, []);
//     saved_name = Project_form_controls.project_name.value;
//     if (msg.status === 1){
//       setToggle("project_toggle", "off");
//       for(k=0;k<Project_form_controls.project_name.options.length;k++){
//           if(Project_form_controls.project_name.options[k].text === saved_name){
//             Project_form_controls.project_name.options.selectedIndex = k;
//             break;
//           }
//       }
//       siteFormDisable(false);
//       fill_form("ProjectInfras", "Project", "get_by_name" ,saved_name);
//       setToggle("site_toggle", "on");
//     }
//   }else{
//     msg = update('Project', data, []);
//   }
//   alert(msg.message);
//
//
// });
//
// // delete Project
// document.getElementById("Delete_Project").addEventListener("click", function() {
//   if (!$('#project_toggle')[0].checked) {
//     project_name = Project_form_controls.project_name.value;
//     msg = item_delete('Project', project_name);
//     if (msg.status === 1){
//       setToggle("project_toggle", "off");
//     }
//     alert(msg.message);
//   }
// });
//
// // New/Existing Site
//
//
// $('#site_toggle').change(function() {
//   if ($('#site_toggle')[0].checked){ //new
//     infras.new(Site_form_controls, "site_name");
//     siteFormDisable(false);
//
//   } else { //exist
//     infras.exist(Site_form_controls, "site_name","select", "select-one");
//     // select Site
//     AddSiteEventListener();
//     var Selected_Project = Project_form_controls.project_name.options[Project_form_controls.project_name.selectedIndex].text;
//     get_names_with_args("SiteInfras", "Site", "get_names_by_project_name",Selected_Project,  Site_form_controls.site_name)
//     // infras.exist(Site_form_controls, "site_name");
//     if (Site_form_controls.site_name.options.length === 0){
//       setToggle("site_toggle", "on");
//     }
//   }
//
// });
// // ask for all site get_names
// //     --> ask for data of the first site
// // ask for data of the site X
//
// // Save Site
// document.getElementById("Save_Site").addEventListener("click", function() {
//   var data = {};
//   data = get_form('Site');
//
//   if ($('#site_toggle')[0].checked) {
//     var saved_name = data.name;
//     msg = save('Site', data, []);
//     if (msg.status === 1){
//       setToggle("site_toggle", "off");
//       for(k=0;k<Site_form_controls.site_name.options.length;k++){
//         if(Site_form_controls.site_name.options[k].text === saved_name){
//           Site_form_controls.site_name.options.selectedIndex = k;
//           break;
//         }
//       }
//       fill_form("SiteInfras", "Site", "get_by_name" ,saved_name);
//     }
//   }else{
//     msg = update('Site', data, []);
//   }
//
//   alert(msg.message);
//
//
// });
//
// // Duplicate Site
// document.getElementById("Duplicate_Site").addEventListener("click", function() {
//   // alert("Duplicate Site");
//   data = get_form('Site');
//   setToggle("site_toggle", "on");
//   fill_form_Site_Infras(data);
//
// });
//
// // delete Site
// document.getElementById("Delete_Site").addEventListener("click", function() {
//   if (!$('#site_toggle')[0].checked) {
//     site_name = Site_form_controls.site_name.value;
//     msg = item_delete('Site', site_name);
//     if (msg.status === 1){
//       setToggle("site_toggle", "off");
//     }
//     alert(msg.message);
//   }
// });
// //  Check Recording
// document.getElementById("check_Recording_DB_IP").addEventListener("click", function() {
//    alert("checking Recording DB IP");
// });
//
// //  Check Excersice_DB_IP
// document.getElementById("check_excersice_db_ip").addEventListener("click", function() {
//    alert("checking Excersice DB IP");
// });
//
// // check check_Auto_Run_DB_IP
// document.getElementById("check_Auto_Run_DB_IP").addEventListener("click", function() {
//    alert("checking Auto_Run DB IP");
// });
//
// // select Site
// // document.getElementById("site_select").addEventListener("change", function() {
// //    var selectedSiteName = Site_form_controls.site_name.options[Site_form_controls.site_name.selectedIndex].text;
// //    fill_form(form_name, "Site", "get_by_name" ,selectedSiteName)
// // });
// AddSiteEventListener();
//
// function setToggle(toggleID, state) {
//   $('#'+ toggleID).bootstrapToggle(state)
// }
//
// setToggle("project_toggle", "on");
fillComplexNetDefaultCT();
ChangeComplexNetHeaders();