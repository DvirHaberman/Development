//-----------GLOBAL VARIABLES----------
const toggle_button = document.getElementById('NewExist_toggle');
var current_site = {};
// var scenario_paths = {};
var sep = null;
var curr_stage = {};
var stages = [];
var state = null;
//-----------GLOBAL CONTROLS----------
const meta_controls = {
    meta_save: document.getElementById('meta_save'),
    meta_duplicate: document.getElementById('meta_duplicate'),
    meta_delete: document.getElementById('meta_delete'),
    meta_name: document.querySelector('#meta_name'),
    meta_name_datalist: document.querySelector('#meta_name_datalist'),
    selected_stage: document.getElementById('selected_stage'),
    owner: document.querySelector('#meta_owner'),
    owner_datalist: document.querySelector('#meta_owner_datalist'),
    description: document.querySelector('#meta_description'),
    tags: document.querySelector('#meta_tags'),
    concequences: document.querySelector('#meta_concequences'),
    changed_by: document.getElementById('meta_changed_by'),
    changed_date: document.getElementById('meta_date'),
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
    ovr_file: document.querySelector('#ovr_file'),
    ovr_file_datalist: document.querySelector('#ovr_file_dl'),
    is_run_all: document.querySelector('#run_all_cb'),
    run_time: document.querySelector('#run_time'),
    btn_run_stage: document.querySelector('#run_stage')

};

const generate_stage_controls = {
    is_generate_scenario: document.querySelector('#generate_external'),
    is_2_delete_scenario_after_run: document.querySelector('#delete_secnario'),
    is_generate_all_sub_folder: document.querySelector('#generate_all_sub_folders'),
    generate_scenario_folder: document.querySelector('#generate_scenario_folder'),
    btn_generate: document.querySelector('#btn_generate'),
};

const generate_stage_labels = {

    generate_scenario_folder_label: document.querySelector('#generate_scenario_folder_label'),
    scenario_generated_label: document.querySelector('#scenario_generated_at'),
    delete_secnario_label_1: document.querySelector('#delete_secnario_label_1'),
    delete_secnario_label: document.querySelector('#delete_secnario_label'),
    generate_all_sub_folders_label: document.querySelector('#generate_all_sub_folders_label')
};

const analyse_stage_controls = {

};

const set_generate_state = is_checked => {
        // generate_stage_controls.is_generate_scenario.checked = is_checked;
        if (is_checked) {
            run_stage_controls.btn_run_stage.innerHTML = '<i class="fas fa-chevron-circle-right"></i>  Generate & Run';
            // <i class="fas fa-chevron-circle-right"></i> &nbsp;Generate & Run

            generate_stage_controls.is_2_delete_scenario_after_run.disabled = false;
            generate_stage_controls.is_generate_all_sub_folder.disabled = false;

            generate_stage_controls.generate_scenario_folder.disabled = false;
            generate_stage_controls.btn_generate.disabled = false;

            generate_stage_labels.generate_scenario_folder_label.classList.remove("color-gray");
            generate_stage_labels.scenario_generated_label.classList.remove("color-gray");

            generate_stage_labels.delete_secnario_label_1.classList.remove("color-gray");
            generate_stage_labels.delete_secnario_label.classList.remove("color-gray");
            generate_stage_labels.generate_all_sub_folders_label.classList.remove("color-gray");


        } else {
            run_stage_controls.btn_run_stage.innerHTML = '<i class="fas fa-chevron-circle-right"></i>  Run';
            // <i class="fas fa-chevron-circle-right"></i> &nbsp; Run

            generate_stage_controls.is_2_delete_scenario_after_run.checked = false;
            generate_stage_controls.is_2_delete_scenario_after_run.disabled = true;

            generate_stage_controls.is_generate_all_sub_folder.checked = false;
            generate_stage_controls.is_generate_all_sub_folder.disabled = true;

            generate_stage_controls.generate_scenario_folder.disabled = true;
            generate_stage_controls.generate_scenario_folder.value = '';
            generate_stage_controls.btn_generate.disabled = true;

            generate_stage_labels.generate_scenario_folder_label.classList.add("color-gray");
            generate_stage_labels.scenario_generated_label.classList.add("color-gray");

            generate_stage_labels.delete_secnario_label_1.classList.add("color-gray");
            generate_stage_labels.delete_secnario_label.classList.add("color-gray");
            generate_stage_labels.generate_all_sub_folders_label.classList.add("color-gray");


        }
    }
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
async function get_owners() {
    let owners = [];
    await fetch('api/User/get_names')
        .then(resp => resp.json()).then(result => { owners = result.data; });
    // .catch(alert('error - could not get sites'));
    return owners;
}

async function get_stage_names() {
    let names = [];
    await fetch('api/StageRunMani/get_names')
        .then(resp => resp.json()).then(result => { names = result.data; });
    return names
}

async function get_stage(stage_name) {
    let stage = {};
    await fetch('api/StageRunMani/get_by_name/' + stage_name)
        .then(resp => resp.json()).then(result => { stage = result.data; });
    // .catch(alert('error - could not get sites'));
    return stage;
}

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
    await fetch('api/Site/get_scenario_folder/' + site_name, {
            method: 'POST',
            body: JSON.stringify({ path: run_stage_controls.scenario_folder.value }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(resp => resp.json()).then(result => { folders = result.data; });
    // .catch(alert('error - could not get sites'));
    return folders;
}

async function get_ovr_files(site_name) {
    let files = [];
    await fetch('api/Site/get_ovr_files/' + site_name)
        .then(resp => resp.json()).then(result => { files = result.data; });
    // .catch(alert('error - could not get sites'));
    return files;
}

async function get_dps_folder(site_name) { // needs update! currently as same as get_scenarios_folder
    let folders = [];
    await fetch('api/Site/get_scenario_folder/' + site_name, {
            method: 'POST',
            body: JSON.stringify({ path: run_stage_controls.dp_folder.value }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(resp => resp.json()).then(result => { folders = result.data; });
    // .catch(alert('error - could not get sites'));
    return folders;
}
const get_meta_data = () => {
    let meta_data = {
        stage_name: meta_controls.meta_name.value.trim(),
        orig_stage_name: meta_controls.selected_stage.innerHTML,
        concequences: meta_controls.concequences.options[meta_controls.concequences.selectedIndex].text,
        owner: meta_controls.owner.value,
        tags: meta_controls.tags.value,
        description: meta_controls.description.value
    };

    return meta_data
};

const get_stage_data = () => {
    let stage_data = {
        site: run_stage_controls.sites.options[run_stage_controls.sites.selectedIndex].text,
        net: run_stage_controls.nets.options[run_stage_controls.nets.selectedIndex].text,
        config: run_stage_controls.configs.options[run_stage_controls.configs.selectedIndex].text,
        scenario_folder: run_stage_controls.scenario_folder.value,
        scenario_file: run_stage_controls.scenario_file.value,
        dp_folder: run_stage_controls.dp_folder.value,
        dp_file: run_stage_controls.dp_file.value,
        ovr_file: run_stage_controls.ovr_file.value,
        run_time: String(run_stage_controls.run_time.value).trim(),
        is_run_all: run_stage_controls.is_run_all.checked
    };

    return stage_data
};
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
    run_stage_controls.ovr_file.value = '';
    // run_stage_controls.ovr_file.setAttribute('list', null);
    run_stage_controls.run_time.value = '20';

    generate_stage_controls.is_generate_scenario.checked = false;
    generate_stage_controls.is_2_delete_scenario_after_run.checked = false;
    generate_stage_controls.is_generate_all_sub_folder.checked = false;
    generate_stage_controls.generate_scenario_folder.value = '';
    generate_stage_labels.scenario_generated_label.innerHTML = "Generated at: &nbsp root/Octopus_Scenario/";

}

const clear_meta_controls = () => {
    meta_controls.meta_name.value = '';
    meta_controls.meta_name.setAttribute('list', null);
    meta_controls.selected_stage.innerHTML = '';
    meta_controls.owner.value = '';
    meta_controls.concequences.selectedIndex = 0;
    meta_controls.description.value = '';
    meta_controls.tags.value = '';
    meta_controls.changed_by.innerHTML = '';
    meta_controls.changed_date.innerHTML = '';
}



const update_meta = stage => {
    clear_meta_controls();
    if (stage) {
        //stage names
        meta_controls.meta_name.setAttribute('list', meta_controls.meta_name_datalist.id);
        meta_controls.selected_stage.innerHTML = stage.name;
        update_datalist(meta_controls.meta_name_datalist, stages, meta_controls.meta_name, stage.name);
        update_select(meta_controls.concequences.id, ['Critical', 'Warning', 'Light', 'None'], stage.concequences);
        meta_controls.owner.value = stage.owner;
        meta_controls.tags.value = stage.tags;
        meta_controls.description.value = stage.description;
        meta_controls.changed_by.innerHTML = 'Changed by: ' + stage.changed_by;
        meta_controls.changed_date.innerHTML = 'Change time: ' + stage.changed_date;
    }
}

async function update_stage(stage) {
    update_meta(stage);
    update_site(stage);
}

async function update_site(stage) {
    // clear all stage form controls
    clear_run_stage_controls();
    let errors = '';
    //----------setting select controls----------------------------
    // get all sites for current project
    let sites = await get_sites();
    let value, error;
    ({ value, error } = validate_value(stage, 'site_name', sites));
    let site = value;
    if (error.length > 0) {
        errors = errors + error;
    }
    if (!stage) {
        site = sites[run_stage_controls.sites.selectedIndex];
    }
    update_select(run_stage_controls.sites.id, sites, site);
    // from first site get the first net
    let nets = await get_nets(site)
    nets.unshift('any');
    result = validate_value(stage, 'net', nets);
    let net = result.value;
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }

    update_select(run_stage_controls.nets.id, nets, net);

    // get all configurations for this current project
    let configs = await get_configs(site);

    result = validate_value(stage, 'complex_net_name', configs);
    let config = result.value;
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }
    update_select(run_stage_controls.configs.id, configs, config);

    //---------------setting text controls and datalists------------------
    // getting scenario paths
    let scenario_paths = await get_scenarios_folder(site);
    // let scenario_folders = Object.keys(scenario_paths);

    result = validate_value(stage, 'scenario_folder', scenario_paths['folders']);
    let scenario_folder = result.value;
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }
    result = validate_value(stage, 'scenario_file', scenario_paths['exercises']);
    if (stage) {
        scenario_file = result.value;
    } else {
        scenario_file = '';
    }
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }
    //updating scenario folders
    update_datalist(
        run_stage_controls.scenario_folder_datalist,
        scenario_paths['folders'],
        run_stage_controls.scenario_folder,
        scenario_folder
    );
    //updating scenario files
    update_datalist(
        run_stage_controls.scenario_file_datalist,
        scenario_paths['exercises'],
        run_stage_controls.scenario_file,
        scenario_file
    );

    // let dp_paths = await get_dps_folder(site);
    // // let dp_folders = Object.keys(scenario_paths);

    // result = validate_value(stage, 'dp_folder', dp_paths['folders']);
    // dp_folder = result.value;
    // if (result.error.length > 0) {
    //     errors = errors + '\n' + result.error;
    // }
    // result = validate_value(stage, 'dp_file', dp_paths['exercises']);
    // if (stage) {
    //     dp_file = result.value;
    // } else {
    //     dp_file = '';
    // }
    // if (result.error.length > 0) {
    //     errors = errors + '\n' + result.error;
    // }
    // //updating dp folders
    // update_datalist(
    //     run_stage_controls.dp_folder_datalist,
    //     dp_paths['folders'],
    //     run_stage_controls.dp_folder,
    //     dp_folder
    // );
    // //updating dp files
    // update_datalist(
    //     run_stage_controls.dp_file_datalist,
    //     dp_paths['exercises'],
    //     run_stage_controls.dp_file,
    //     dp_file
    // );


    //update is run all secnarios
    result = validate_value(stage, 'is_run_all_scenarios', [false, true]);
    is_run_all = result.value;
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }
    run_stage_controls.is_run_all.checked = is_run_all;

    let ovr_files = await get_ovr_files(site);

    // update ovr files
    result = validate_value(stage, 'ovr_file', ovr_files);
    if (stage) {
        ovr_file = result.value;
    } else {
        ovr_file = '';
    }
    if (result.error.length > 0) {
        errors = errors + '\n' + result.error;
    }
    update_datalist(
        run_stage_controls.ovr_file_datalist,
        ovr_files,
        run_stage_controls.ovr_file,
        ovr_file
    );

    //update run time
    if (stage) {
        run_stage_controls.run_time.value = stage.run_time;
    } else {
        run_stage_controls.run_time.value = '';
    }

    if (errors.length > 0 && !toggle_button.checked) {
        if (stage) {
            if (stage['site_name'] == site) {
                alert(errors);
            }
        }
    }
}

async function update_paths(path) {

}

async function new_run_stage() {
    // disable generate scenario panel
    set_generate_state(false);

    // run div hidden to false
    document.querySelector('#run_stage_div').hidden = false;

    // analyse div hidden to true
    document.querySelector('#analyse_stage_div').hidden = true;

    // clear all meta controls
    clear_meta_controls();

    // unlink names datalist
    meta_controls.meta_name.setAttribute('list', null);

    //updating site to first on the list
    update_stage(null);
}

//---------ACTIONS---------
//save
const save_stage = () => {

    let result = {
        status: 0,
        message: ''
    }

    meta_data = get_meta_data();
    site_data = get_stage_data();

    let meta_validator = validate_meta(meta_data);
    let data_validator = validate_data(site_data);

    result.message = data_validator.error + '\n' + meta_validator.error;
    result.status = data_validator.status * meta_validator.status;
    if (!result.status) {
        return result;
    }
    let stage_data = {
            meta: meta_data,
            site: site_data
        }
        //actual save
    $.ajax({
        url: 'api/StageRunMani/save',
        data: JSON.stringify(stage_data),
        type: 'POST',
        dataType: "json",
        async: false,
        contentType: 'application/json',
        success: (resp) => {
            if (resp.status) {
                result.status = 1;
            } else {
                result.status = 0;
            }
            result.message = resp.message;
        },
        error: (resp) => {
            result.status = 0;
            result.message = 'server error';
        }
    })

    return result;
}

const save_updates = () => {

    let result = {
        status: 0,
        message: ''
    }

    meta_data = get_meta_data();
    site_data = get_stage_data();

    let meta_validator = validate_meta(meta_data);
    let data_validator = validate_data(site_data);

    result.message = data_validator.error + '\n' + meta_validator.error;
    result.status = data_validator.status * meta_validator.status;
    if (!result.status) {
        return result;
    }
    let stage_data = {
            meta: meta_data,
            site: site_data
        }
        //actual save
    $.ajax({
        url: 'api/StageRunMani/update',
        data: JSON.stringify(stage_data),
        type: 'POST',
        dataType: "json",
        async: false,
        contentType: 'application/json',
        success: (resp) => {
            if (resp.status) {
                result.status = 1;
            } else {
                result.status = 0;
            }
            result.message = resp.message;
        },
        error: (resp) => {
            result.status = 0;
            result.message = 'server error';
        }
    })

    return result;
}

//delete
const delete_stage = stage_name => {
    let result = {
        status: 0,
        message: ''
    }
    if (stages.includes(stage_name)) {
        $.ajax({
            url: 'api/StageRunMani/delete_by_name/' + stage_name,
            async: false,
            success: resp => {
                result.status = resp.status
                result.message = resp.message
            },
            error: () => {
                result.status = 0
                result.message = 'server error'
            }
        });
    } else {
        result.status = 0
        result.message = 'no stage with this name'
    }
    return result;
}

//-------VALIDATORS-----------

const validate_meta = (data) => {
    const result = {
        status: 1,
        error: ''
    };

    if (data.stage_name.replace(' ', '').length == 0) {
        result.status = 0;
        result.error = 'name cannot be empty';
    }

    if (/[^a-z_\-A-Z0-9]/.test(data.stage_name.replace(' ', ''))) {
        result.status = 0;
        result.error += '\n' + `name can only contain letters, numbers and the - , _ characters`;
    }
    data.stage_name;
    return result;
};

const not_in_datalist = (datalist, lookup_value) => {
    let numOfEle = datalist.options.length;
    for (let index = 0; index < numOfEle; index++) {
        if (lookup_value == datalist.options[index].text) {
            return 0;
        }

    }

    return 1;
}

const validate_data = (data) => {
    const result = {
        status: 1,
        error: '',
        data: {}
    };

    //scenario folder
    if (not_in_datalist(run_stage_controls.scenario_folder_datalist, data.scenario_folder)) {
        result.status = 0;
        result.error = `${data.scenario_folder} is not a valid folder name`;
    }
    //scenario file
    if (not_in_datalist(run_stage_controls.scenario_file_datalist, data.scenario_file)) {
        result.status = 0;
        result.error = result.error + '\n' + `${data.scenario_file} is not a valid file name`;
    }
    // //dp folder
    // if (not_in_datalist(run_stage_controls.dp_folder_datalist, data.dp_folder)) {
    //     result.status = 0;
    //     result.error = result.error + '\n' + `${data.dp_folder} is not a valid folder name`;
    // }
    // //dp file
    // if (not_in_datalist(run_stage_controls.dp_file_datalist, data.dp_file)) {
    //     result.status = 0;
    //     result.error = result.error + '\n' + `${data.dp_file} is not a valid file name`;
    // }
    // ovr file
    if (not_in_datalist(run_stage_controls.ovr_file_datalist, data.ovr_file)) {
        result.status = 0;
        result.error = result.error + '\n' + `${data.ovr_file} is not a valid ovr file name`;
    }
    //run time
    if (/[^0-9]/.test(data.run_time)) {
        result.status = 0;
        result.error = result.error + '\n' + `run time must be a number`;
    }

    return result;
};

const validate_value = (stage, prop_name, values_array) => {
    const result = {
        value: values_array[0],
        error: ''
    };

    if (!stage) {
        result.value = values_array[0];
    } else {
        if (stage[prop_name] !== null) {
            if (typeof(stage[prop_name]) === "number") {
                stage[prop_name] = String(stage[prop_name]);
            }
            if (values_array.includes(stage[prop_name])) {
                result.value = stage[prop_name];
            } else {
                result.value = values_array[0];
                result.error = `Couldn't find ${prop_name} : ${stage[prop_name]}, defaulting to first ${prop_name} : ${values_array[0]}`;
            }
        } else {
            result.value = values_array[0];
            result.error = `Stage without a ${prop_name}, defaulting to first ${prop_name} : ${values_array[0]}`;
        }
    }
    return result;
}


const addEventListeners = () => {
    //----------Meta controls------------
    // name - only in exisiting stage load stage by name
    $('#NewExist_toggle').change(async() => {
        if (toggle_button.checked) { // new

            if (state !== 'duplicate') {
                new_run_stage()
            } else {
                set_generate_state(false);
                meta_controls.meta_name.setAttribute('list', null);
                meta_controls.meta_name.value = '';
                meta_controls.selected_stage.innerHTML = '';
                meta_controls.description.value = '';
                meta_controls.tags.value = '';
                meta_controls.changed_by.innerHTML = '';
                meta_controls.changed_date.innerHTML = '';
            }
            state = null;
        } else { // exist
            run_stage_controls.btn_run_stage.disabled = false;
            stages = await get_stage_names();
            let stage_name;
            if (state == 'save' || state == 'update') {
                stage_name = meta_controls.meta_name.value;
            } else {
                stage_name = stages[0];
            }
            let stage = await get_stage(stage_name);
            update_stage(stage);
            state = null;
        }
    })

    meta_controls.meta_save.addEventListener('click', () => {
        let result;
        if (toggle_button.checked) {
            result = save_stage();
            state = 'save';
        } else {
            result = save_updates();
            state = 'update'
        }
        alert(result.message);
        if (result.status == 0) {
            return 0;
        }
        $('#NewExist_toggle').bootstrapToggle('off')
    });

    meta_controls.meta_duplicate.addEventListener('click', () => {
        state = 'duplicate';
        $('#NewExist_toggle').bootstrapToggle('on')
    });

    meta_controls.meta_delete.addEventListener('click', () => {
        result = delete_stage(meta_controls.meta_name.value);
        if (result.status) {
            state = 'delete';
            $('#NewExist_toggle').bootstrapToggle('off');
        }
        alert(result.message);
    });

    meta_controls.meta_name.addEventListener('change', async() => {
        if (!toggle_button.checked) { // exist
            if (stages.includes(meta_controls.meta_name.value)) {
                let stage = await get_stage(meta_controls.meta_name.value);
                update_stage(stage);
                curr_stage = stage;
            }
        }
    });
    //----------stage controls-----------
    // site
    run_stage_controls.sites.addEventListener('change', () => {
        if (toggle_button.checked) { //new
            update_site(null);
        } else { //exist
            if (curr_stage.site_id == current_site.id) {
                update_site(curr_stage);
            } else {
                update_site(null);
            }
        }
    });

    //scenario folder
    run_stage_controls.scenario_folder.addEventListener('input', async() => {
        // folders = Object.keys(scenario_paths);
        // chosen_folder = run_stage_controls.scenario_folder.value;
        // if (!folders.includes(chosen_folder)) {
        //     return 0;
        // }
        // files = scenario_paths[chosen_folder];
        // update_datalist(
        //     run_stage_controls.scenario_file_datalist,
        //     files,
        //     run_stage_controls.scenario_file,
        //     ''
        // );
        let site_obj = run_stage_controls.sites;
        let site = site_obj.options[site_obj.selectedIndex].text;
        let scenario_paths = await get_scenarios_folder(site);
        scenario_paths['folders'] = scenario_paths['folders'].map(ele => ele + sep)
            //updating scenario folders
        update_datalist(
            run_stage_controls.scenario_folder_datalist,
            scenario_paths['folders'],
            run_stage_controls.scenario_folder,
            run_stage_controls.scenario_folder.value
        );
        //updating scenario files
        update_datalist(
            run_stage_controls.scenario_file_datalist,
            scenario_paths['exercises'],
            run_stage_controls.scenario_file,
            run_stage_controls.scenario_file.value
        );

    });

    // run_stage_controls.dp_folder.addEventListener('input', () => {
    //     folders = Object.keys(scenario_paths);
    //     chosen_folder = run_stage_controls.dp_folder.value;
    //     if (!folders.includes(chosen_folder)) {
    //         return 0;
    //     }
    //     files = scenario_paths[chosen_folder];
    //     update_datalist(
    //         run_stage_controls.dp_file_datalist,
    //         files,
    //         run_stage_controls.dp_file,
    //         ''
    //     );

    // });
    run_stage_controls.is_run_all.addEventListener('change', () => {
        if (run_stage_controls.is_run_all.checked) {
            run_stage_controls.scenario_file.value = '';
            run_stage_controls.scenario_file.disabled = true;
        } else {
            run_stage_controls.scenario_file.disabled = false;
        }
    })


    generate_stage_controls.is_generate_scenario.addEventListener('change', () => { set_generate_state(generate_stage_controls.is_generate_scenario.checked); });

    generate_stage_controls.generate_scenario_folder.addEventListener('change', () => {
        generate_stage_labels.scenario_generated_label.innerHTML = "Generated at: &nbsp root/Octopus_Scenario/" + generate_stage_controls.generate_scenario_folder.value

    })

}

// --------------BUTTONS -------------------
$('#btn_generate').click(() => {

    flagGenerateAllSubFolder = generate_stage_controls.is_generate_all_sub_folder.checked;
    folder2Generate = generate_stage_labels.scenario_generated_label.innerHTML;

    if (flagGenerateAllSubFolder) { //Generate all Sub Folder

        $.ajax({
            url: 'api/run_stage/' + curr_setup_name,
            success: (response) => {

            }

        });

    } else { //Generate Selected Folder

        $.ajax({
            url: 'api/run_stage/' + curr_setup_name,
            success: (response) => {

            }

        });
    }

});

$('#run_stage').click(() => {
    // if "new" - > save first.   
    if (generate_stage_controls.is_generate_scenario.checked) { // Generate & Run 
        // execute Generate ... 
        // Run:
        $.ajax({
            url: 'api/run_stage/' + curr_setup_name,
            success: (response) => {

            }
        });
    } else { // Run Stage
        $.ajax({
            url: 'api/run_stage/' + curr_setup_name,
            success: (response) => {

            }
        });
    }
});



async function update_owners() {
    let owners = await get_owners();
    user_name = document.querySelector('.user-name').innerHTML;
    update_datalist(meta_controls.owner_datalist, owners, meta_controls.owner, user_name);
}

function get_seperator() {
    // let seperator = null;
    fetch('api/OctopusUtils/get_seperator')
        .then(resp => resp.json()).then(result => { sep = result.data; })
        // return seperator;
}

window.onload = () => {
    get_seperator();
    update_owners();
    new_run_stage();
    addEventListeners();
}