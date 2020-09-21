//-----------GLOBAL CONTROLS----------
const meta_controls = {
    meta_name: document.querySelector('#meta_name'),
    meta_name_datalist: document.querySelector('#meta_name_datalist'),
    owner: document.querySelector('#meta_owner'),
    owner_datalist: document.querySelector('#meta_owner_datalist'),
    description: document.querySelector('#meta_description'),
    tags: document.querySelector('#meta_tags'),
    concequences: document.querySelector('#meta_concequences')
};

const run_stage_controls = {
    sites: document.querySelector('#site_select'),
    nets: document.querySelector('#site_net'),
    configs: document.querySelector('#site_config'),
    scenario_folder: document.querySelector('#scenario_folder'),
    scenario_folder_datalist: document.querySelector('#scenario_folder_dl'),
    scenario_file: document.querySelector('#scenario_file_name'),
    scenario_file_datalist: document.querySelector('#scenario_file_dl'),
    dp_folder: document.querySelector('#dp_folder'),
    dp_folder_datalist: document.querySelector('#dp_folder_dl'),
    dp_file: document.querySelector('#dp_file'),
    dp_file_datalist: document.querySelector('#dp_file_dl'),
    over_file: document.querySelector('#ovr_file'),
    over_file_datalist: document.querySelector('#ovr_file_dl'),
    is_run_all: document.querySelector('#run_all_cb'),
    run_time: document.querySelector('#run_time')

};

const analyse_stage_controls = {

};

var current_site = {};
var scenario_paths = {};
//---------UPDATE FUNCTIONS--------------
function update_datalist(datalist, values_array, input, selected_value) {
    // const input = document.querySelector('#' + input_id);
    input.value = selected_value;

    // const datalist = document.querySelector('#' + datalist_id);
    const numOfEle = datalist.childElementCount;
    for (let index = 0; index < numOfEle; index++) {
        datalist.removeChild(datalist.children[0]);
    }

    for (let index = 0; index < values_array.length; index++) {
        let option = document.createElement('option');
        option.text = values_array[index];
        datalist.appendChild(option);
    }

}

function update_select(select_id, values_array, selected_value) {
    let select_obj = document.querySelector('#' + select_id);
    let numOfEle = select_obj.options.length;
    for (let index = 0; index < numOfEle; index++) {
        select_obj.remove(0);
    }

    for (let index = 0; index < values_array.length; index++) {
        let option = document.createElement('option');
        option.text = values_array[index];
        select_obj.add(option);
    }

    select_obj.selectedIndex = values_array.indexOf(selected_value);

}

//---------------GETTERS-------------
async function get_sites() {
    let sites = [];
    await fetch('api/Site/get_names_current_project')
        .then(resp => resp.json()).then(result => { sites = result.data; });
    // .catch(alert('error - could not get sites'));
    return sites;
}

async function get_curr_site(site_name) {
    // let sites = [];
    await fetch('api/Site/get_by_name/' + site_name)
        .then(resp => resp.json()).then(result => { current_site = result.data; });
    // .catch(alert('error - could not get sites'));
    // return sites;
}

async function get_nets(site_name) {
    let nets = [];
    await fetch('api/Site/get_by_name/' + site_name)
        .then(resp => resp.json()).then(result => { nets = result.data.nets.split(','); });
    // .catch(alert('error - could not get sites'));
    return nets;
}

async function get_configs(site_name) {
    let configs = [];
    await get_curr_site(site_name);
    await fetch('api/ComplexNet/get_names_by_version/' + current_site.version)
        .then(resp => resp.json()).then(result => { configs = result.data; });
    // .catch(alert('error - could not get sites'));
    return configs;
}

async function get_scenarios_folder(site_name) {
    let folders = [];
    await fetch('api/Site/get_scenario_folder/' + site_name)
        .then(resp => resp.json()).then(result => { folders = result.data; });
    // .catch(alert('error - could not get sites'));
    return folders;
}

//---------------SETTERS-------------

const clear_run_stage_controls = () => {
    run_stage_controls.scenario_folder.value = '';
    // run_stage_controls.scenario_folder.setAttribute('list', null);
    run_stage_controls.scenario_file.value = '';
    // run_stage_controls.scenario_file.setAttribute('list', null);
    run_stage_controls.dp_folder.value = '';
    // run_stage_controls.dp_folder.setAttribute('list', null);
    run_stage_controls.dp_file.value = '';
    // run_stage_controls.dp_file.setAttribute('list', null);
    run_stage_controls.is_run_all.checked = false;
    run_stage_controls.over_file.value = '';
    // run_stage_controls.over_file.setAttribute('list', null);
    run_stage_controls.run_time.value = '';
}

const clear_meta_controls = () => {
    meta_controls.meta_name.value = '';
    meta_controls.meta_name.setAttribute('list', null);
    meta_controls.owner.value = '';
    meta_controls.concequences.selectedIndex = 0;
    meta_controls.description.value = '';
    meta_controls.tags.value = '';
}

async function update_site(index) {
    // clear all stage form controls
    clear_run_stage_controls();

    //----------setting select controls----------------------------
    // get all sites for current project
    let sites = await get_sites();
    update_select(run_stage_controls.sites.id, sites, sites[index]);

    // from first site get the first net
    let nets = await get_nets(sites[index])
    nets.unshift('any');
    update_select(run_stage_controls.nets.id, nets, nets[index]);

    // get all configurations for this current project
    let configs = await get_configs(sites[index]);
    update_select(run_stage_controls.configs.id, configs, configs[index]);

    //---------------setting text controls and datalists------------------
    scenario_paths = await get_scenarios_folder(sites[index]);
    let scenario_folders = Object.keys(scenario_paths);
    update_datalist(
        run_stage_controls.scenario_folder_datalist,
        scenario_folders,
        run_stage_controls.scenario_folder,
        scenario_folders[0]
    );
    update_datalist(
        run_stage_controls.scenario_file_datalist,
        scenario_paths[scenario_folders[0]],
        run_stage_controls.scenario_file,
        scenario_paths[scenario_folders[0]][0]
    );
    run_stage_controls.is_run_all.checked = false;
    run_stage_controls.over_file.value = false;
    run_stage_controls.run_time.value = '';
}

async function update_paths(path) {

}

async function new_run_stage() {
    // run div hidden to false
    document.querySelector('#run_stage_div').hidden = false;

    // analyse div hidden to true
    document.querySelector('#analyse_stage_div').hidden = true;

    // clear all meta controls
    clear_meta_controls();

    // unlink names datalist
    meta_controls.meta_name.setAttribute('list', null);

    //updating site to first on the list
    update_site(0);
}

const addEventListeners = () => {
    //----------Meta controls------------
    // name - only in exisiting stage load stage by name
    meta_controls.stage_name.addEventListener('change', load_stage(index));
    //----------stage controls-----------
    // site
    run_stage_controls.site_name.addEventListener('change', load_nets(run_stage_controls.site.value));
}

window.onload = () => {
    new_run_stage();
    addEventListeners();
}