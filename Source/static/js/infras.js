var Project_form_controls = {
    project_name: $('#project_select')[0],
    project_output_dir: $('#output-dir')[0],
}
var project_data = {
    name: null,
    output_dir: null
};

const get_select_value = (select_ele) => select_ele.options[select_ele.selectedIndex].text;

var Site_form_controls = {
    site_name: $('#site_select')[0],
    is_site_active: $('#is_site_active_cb')[0],
    Site_Conn: $('#Site_Conn')[0],
    exercise_Conn: $('#exercise_Conn')[0],
    Octopus_Conn: $('#Octopus_Conn')[0],
    recording_db: $('#recording_db')[0],
    excercise_db: $('#excercise_db')[0],
    octopus_db: $('#octopus_db')[0],
    nets: $('#nets')[0],
    stations: $('#stations')[0],
    version_input: $('#version_input')[0],
    ext_scenario_filer: $('#ext_scenario_filer')[0],
    auto_dir: $('#auto_dir')[0]
}

const reset_connections = () => {
    setSchemaNames(Site_form_controls.Site_Conn, SchemaNames, 0); // Site Schema
    SetRecordingDB(0);

    setSchemaNames(Site_form_controls.exercise_Conn, SchemaNames, 0); // exercise Schema
    SetExersiceDB(0);

    setSchemaNames(Site_form_controls.Octopus_Conn, SchemaNames, 0); // auto data Schema
    SetOctopusDB(0);
}

const set_conn = (obj, names, value) => {
    if (names.includes(value)) {
        index = names.indexOf(value);
    } else {
        alert(`site connection : ${value} was not found. Please select another`)
        index = 0;
    }
    setSchemaNames(obj, names, index);
}

const set_schema = (obj, conn_name, value) => {
    var connData = get_by_name(conn_name)
    if (connData.is_valid) {
        if (connData.schemas.includes(value)) {
            index = connData.schemas.indexOf(value);
        } else {
            alert(`site recording db schema : ${value} was not found. Please select another`)
            index = 0;
        }
    } else {
        connData = get_by_name(SchemaNames[0]);
        index = 0;
    }
    setSchemaNames(obj, connData.schemas, index);
}

const set_connections = (data) => {
    //setting site connection
    set_conn(Site_form_controls.Site_Conn, SchemaNames, data.site_conn);
    //setting site schema
    set_schema(Site_form_controls.recording_db, data.site_conn, data.recording_db);

    //setting exercise connection
    set_conn(Site_form_controls.exercise_Conn, SchemaNames, data.execrsice_conn);
    //setting exercise schema
    set_schema(Site_form_controls.excercise_db, data.execrsice_conn, data.execrsice_db);

    //setting octopus connection
    set_conn(Site_form_controls.Octopus_Conn, SchemaNames, data.octopus_conn);
    //setting octopus schema
    set_schema(Site_form_controls.octopus_db, data.octopus_conn, data.octopus_db);
}

function fill_form_Project_Infras(data) {
    Project_form_controls.project_output_dir.value = data.output_dir;
}

function fill_form_Site_Infras(data) {
    if (data) {
        Site_form_controls.is_site_active.checked = data.is_active;
        Site_form_controls.nets.value = data.nets;
        Site_form_controls.stations.value = data.stations;
        Site_form_controls.version_input.value = data.version;
        Site_form_controls.ext_scenario_filer.value = data.ext_scenario_filer;
        Site_form_controls.auto_dir.value = data.auto_dir;
    }
    set_connections(data);
}

function get_form(formType) {
    var data = {};
    if (formType == "Project") {
        data.name = Project_form_controls.project_name.value;
        data.output_dir = Project_form_controls.project_output_dir.value;
    }

    if (formType == "Site") {
        data.project_name = Project_form_controls.project_name.value;
        data.name = Site_form_controls.site_name.value;
        data.version = Site_form_controls.version_input.value;
        data.is_active = Site_form_controls.is_site_active.checked;
        data.site_conn = get_select_value(Site_form_controls.Site_Conn);
        data.recording_db = get_select_value(Site_form_controls.recording_db);
        data.exercise_conn = get_select_value(Site_form_controls.exercise_Conn);
        data.excercise_db = get_select_value(Site_form_controls.excercise_db);
        data.octopus_conn = get_select_value(Site_form_controls.Octopus_Conn);
        data.octopus_db = get_select_value(Site_form_controls.octopus_db);
        data.nets = Site_form_controls.nets.value;
        data.stations = Site_form_controls.stations.value;
        data.ext_scenario_filer = Site_form_controls.ext_scenario_filer.value;
        data.auto_dir = Site_form_controls.auto_dir.value;
    }
    return data
}

function siteFormDisable(trueFalse) {
    Site_form_controls.site_name.disabled = trueFalse;
    Site_form_controls.is_site_active.disabled = trueFalse;
    Site_form_controls.Site_Conn.disabled = trueFalse;
    Site_form_controls.exercise_Conn.disabled = trueFalse;
    Site_form_controls.Octopus_Conn.disabled = trueFalse;
    Site_form_controls.nets.disabled = trueFalse;
    Site_form_controls.stations.disabled = trueFalse;
    Site_form_controls.version_input.disabled = trueFalse;
    Site_form_controls.recording_db.disabled = trueFalse;
    Site_form_controls.excercise_db.disabled = trueFalse;
    Site_form_controls.octopus_db.disabled = trueFalse;
    Site_form_controls.ext_scenario_filer.disabled = trueFalse;
    Site_form_controls.auto_dir.disabled = trueFalse;
    $('#site_toggle')[0].disabled = trueFalse;
    $('#Duplicate_Site')[0].disabled = trueFalse;
    $('#Save_Site')[0].disabled = trueFalse;
    $('#Delete_Site')[0].disabled = trueFalse;
}

function AddSiteEventListener() {
    document.getElementById("site_select").addEventListener("change", function() {
        var selectedSiteName = Site_form_controls.site_name.options[Site_form_controls.site_name.selectedIndex].text;
        fill_form("SiteInfras", "Site", "get_by_name", selectedSiteName)
    });
}

function getSchemaNames() {
    var SchemaNames = "";
    $.ajax({
        url: "/api/DbConnector/get_names",
        async: false,
        success: function(result) {
                if (result.status === 1) {
                    SchemaNames = result.data;
                } //if
            } // function
    });
    return SchemaNames;
}


function CreateSelectElement(SellectArray, currValueIndex) {
    let newElement = document.createElement('select');

    for (m = 0; m < SellectArray.length; m++) {
        var currValue = SellectArray[m];
        var option = document.createElement("option");
        option.value = currValue;
        option.text = currValue;
        option.classList.add("form-control");
        option.classList.add("medium-margin");

        newElement.add(option);
    }

    newElement.classList.add("form-control");
    // newElement.classList.add("table-select");
    newElement.selectedIndex = currValueIndex;

    return newElement
}

function get_by_name(conn_name) {

    var connData = "";
    $.ajax({
        url: "/api/DbConnector/get_by_name/" + conn_name,
        async: false,
        success: function(result) {
                if (result.status === 1) {
                    connData = result.data;
                } //if
            } // function
    });
    return connData;
}


function setSchemaNames(obj, SchemaNames, index) {

    var num_of_children = obj.children.length;
    for (i = 0; i < num_of_children; i++) {
        obj.remove(0);
    }

    var num_of_children = SchemaNames.length;
    for (i = 0; i < num_of_children; i++) {
        option = document.createElement('option');
        option.text = SchemaNames[i];
        option.classList.add("form-control");
        option.classList.add("medium-margin");
        obj.add(option);
    }
    obj.selectedIndex = index;
    // obj.appendChild(CreateSelectElement(SchemaNames, 0)); // Select

}

function SetOctopusDB(index) {
    var relevantConnName = Site_form_controls.Octopus_Conn.options[Site_form_controls.Octopus_Conn.selectedIndex].text;
    var connData = get_by_name(relevantConnName)
    setSchemaNames(Site_form_controls.octopus_db, connData.schemas, index)
}

function SetExersiceDB(index) {
    var relevantConnName = Site_form_controls.exercise_Conn.options[Site_form_controls.exercise_Conn.selectedIndex].text;
    var connData = get_by_name(relevantConnName)
    setSchemaNames(Site_form_controls.excercise_db, connData.schemas, 0)
}

function SetRecordingDB(index) {
    var relevantConnName = Site_form_controls.Site_Conn.options[Site_form_controls.Site_Conn.selectedIndex].text;
    var connData = get_by_name(relevantConnName)
    setSchemaNames(Site_form_controls.recording_db, connData.schemas, 0)
}

/////// 

// projects = new Project_form_controls();

// New/Existing Project
$('#project_toggle').change(function() {
    if ($('#project_toggle')[0].checked) { //new
        // alert("New Project");
        infras.new(Project_form_controls, "project_name");
        // infras.new(Site_form_controls, "site_name");
        setToggle("site_toggle", "on");
        siteFormDisable(true);

    } else {

        infras.exist(Project_form_controls, "project_name", "select", "select-one");
        // select Site
        document.getElementById("project_select").addEventListener("change", function() {
            var selectedProjectName = Project_form_controls.project_name.options[Project_form_controls.project_name.selectedIndex].text;
            fill_form("ProjectInfras", "Project", "get_by_name", selectedProjectName);
            siteFormDisable(false);
            setToggle("site_toggle", "off");
        });
        siteFormDisable(false);
        get_names("ProjectInfras", "Project", "get_names", Project_form_controls.project_name)
        setToggle("site_toggle", "off");
    }

});

// Save Project
document.getElementById("Save_Project").addEventListener("click", function() {
    var data = {};
    data = get_form('Project');

    if ($('#project_toggle')[0].checked) {
        msg = save('Project', data, []);
        saved_name = Project_form_controls.project_name.value;
        if (msg.status === 1) {
            setToggle("project_toggle", "off");
            for (k = 0; k < Project_form_controls.project_name.options.length; k++) {
                if (Project_form_controls.project_name.options[k].text === saved_name) {
                    Project_form_controls.project_name.options.selectedIndex = k;
                    break;
                }
            }
            siteFormDisable(false);
            fill_form("ProjectInfras", "Project", "get_by_name", saved_name);
            setToggle("site_toggle", "on");
        }
    } else {
        msg = update('Project', data, []);
    }
    alert(msg.message);


});

// delete Project
document.getElementById("Delete_Project").addEventListener("click", function() {
    if (!$('#project_toggle')[0].checked) {
        project_name = Project_form_controls.project_name.value;
        msg = item_delete('Project', project_name);
        if (msg.status === 1) {
            setToggle("project_toggle", "off");
        }
        alert(msg.message);
    }
});

// New/Existing Site


$('#site_toggle').change(function() {
    if ($('#site_toggle')[0].checked) { //new
        infras.new(Site_form_controls, "site_name");
        siteFormDisable(false);
        reset_connections();
    } else { //exist
        infras.exist(Site_form_controls, "site_name", "select", "select-one");
        // select Site
        AddSiteEventListener();
        var Selected_Project = Project_form_controls.project_name.options[Project_form_controls.project_name.selectedIndex].text;
        get_names_with_args("SiteInfras", "Site", "get_names_by_project_name", Selected_Project, Site_form_controls.site_name)
            // infras.exist(Site_form_controls, "site_name");
        if (Site_form_controls.site_name.options.length === 0) {
            setToggle("site_toggle", "on");
        }
    }

});
// ask for all site get_names
//     --> ask for data of the first site
// ask for data of the site X

// Save Site
document.getElementById("Save_Site").addEventListener("click", function() {
    var data = {};
    data = get_form('Site');

    if ($('#site_toggle')[0].checked) {
        var saved_name = data.name;
        msg = save('Site', data, []);
        if (msg.status === 1) {
            setToggle("site_toggle", "off");
            for (k = 0; k < Site_form_controls.site_name.options.length; k++) {
                if (Site_form_controls.site_name.options[k].text === saved_name) {
                    Site_form_controls.site_name.options.selectedIndex = k;
                    break;
                }
            }
            fill_form("SiteInfras", "Site", "get_by_name", saved_name);
        }
    } else {
        msg = update('Site', data, []);
    }

    alert(msg.message);


});

// Duplicate Site
document.getElementById("Duplicate_Site").addEventListener("click", function() {
    // alert("Duplicate Site");
    data = get_form('Site');
    setToggle("site_toggle", "on");
    fill_form_Site_Infras(data);

});

// delete Site
document.getElementById("Delete_Site").addEventListener("click", function() {
    if (!$('#site_toggle')[0].checked) {
        site_name = Site_form_controls.site_name.value;
        msg = item_delete('Site', site_name);
        if (msg.status === 1) {
            setToggle("site_toggle", "off");
        }
        alert(msg.message);
    }
});
//  Check Recording
document.getElementById("check_Recording_DB").addEventListener("click", function() {
    alert("checking Recording DB");
});

//  Check Excersice_DB_IP
document.getElementById("check_excersice_db").addEventListener("click", function() {
    alert("checking Excersice DB");
});

// check check_Auto_Run_DB_IP
document.getElementById("check_Octopus_DB").addEventListener("click", function() {
    alert("checking Auto_Run DB IP");
});


$('#Site_Conn').change(function() {
    SetRecordingDB(0);
});

$('#exercise_Conn').change(function() {
    SetExersiceDB(0);
});

$('#octopus_Conn').change(function() {
    SetOctopusDB(0);
});

var SchemaNames = getSchemaNames();

reset_connections();

var newele = null;
infras = new form_controls_handler();
// AddSiteEventListener();
// setToggle("project_toggle", "on");