var save_button = document.querySelector('#meta_save');
var delete_button = document.getElementById('meta_delete');
var toggle_button = document.getElementById('NewExist_toggle');
var selected_net = document.getElementById('selected_net');
var net_names = [];
var meta_controls = {
    net_name: document.querySelector('#meta_name'),
    owner: document.querySelector('#meta_owner'),
    owner_datalist: document.querySelector('#meta_owner_datalist'),
    net_versions: document.querySelector('#net_versions'),
    net_versions_datalist: document.querySelector('#net_versions_datalist'),
    tags: document.querySelector('#meta_tags'),
    description: document.querySelector('#meta_description'),
    changed_date: document.querySelector('#meta_date'),
    changed_by: document.getElementById('meta_changed_by')
}

var skeleton = {};

var curr_net = {};

function updateSkeleton(e) {
    skeletonKey = this.parentElement.parentElement.parentElement.children[0].innerHTML;
    comp_index = Number(this.parentElement.parentElement.parentElement.getAttribute('name'));
    indices = this.getAttribute('name').split(',');
    if (this.tagName == 'SELECT') {
        value = this.selectedIndex;
    } else {
        value = this.checked;
    }
    skeleton.data[comp_index]['elements'][indices[0]]['indices'][indices[1]] = value;
}

function validate_net_data(net_data) {
    return 0;
}

function save_net() {
    net_data = {
        name: meta_controls.net_name.value,
        owner: meta_controls.owner.value,
        tags: meta_controls.tags.value,
        description: meta_controls.description.value,
        skeleton: skeleton
    }
    validate_net_data(net_data);
    $.ajax({
        url: '/api/ComplexNet/save',
        contentType: 'application/json',
        type: 'POST',
        data: JSON.stringify(net_data),
        success: resp => {
            if (resp.status == 1) {
                alert('net saved!');
            } else {
                alert(resp.message);
            }
        },
        error: () => alert('server error')
    });
    $('#NewExist_toggle').bootstrapToggle('off')
}

function update_net() {
    net_data = {
        name: meta_controls.net_name.value,
        owner: meta_controls.owner.value,
        tags: meta_controls.tags.value,
        description: meta_controls.description.value,
        skeleton: skeleton
    }
    validate_net_data(net_data);
    $.ajax({
        url: '/api/ComplexNet/update_by_name/' + selected_net.innerHTML,
        contentType: 'application/json',
        async: false,
        type: 'POST',
        data: JSON.stringify(net_data),
        success: resp => alert(resp.message),
        error: () => alert('server error')
    });
    get_names_by_version(meta_controls.net_versions.value);
    load_net(meta_controls.net_name.value);
}

function addComponents(component, comp_index) {
    //getting parent div
    parent_div = $("." + component.location)[0];

    //creating the wrapper and setting it's width
    div_element = document.createElement('div');
    div_element.classList.add('col-' + component.width);

    //creating the card div
    card = document.createElement('div');
    card.classList.add('card');

    //creating the card header
    card_header = document.createElement('div');
    card_header.classList.add('card-header');
    card_header.innerHTML = component.name;

    //creating the card header
    card_body = document.createElement('div');
    card_body.classList.add('card-body');
    //center if needed
    if (component.isCentered == 'yes') {
        card_body.classList.add('flex-centered');
    }

    //appending in desired structure
    parent_div.appendChild(div_element);
    div_element.appendChild(card);
    card.appendChild(card_header);
    card.appendChild(card_body);
    card.setAttribute('name', comp_index);
    //looping inner elements
    component.elements.forEach((element, ele_index) => {
        //for each element add it a number of times specified in element.amount
        // skeleton[comp_index]['elements'][ele_index]['selected_indices'] = []
        for (let index = 0; index < element.amount; index++) {

            //creating the containing div
            form_div = document.createElement('div');
            //creating and editing the label
            label_ele = document.createElement('label');
            label_ele.innerHTML = element.labels[index];

            //check if cb or select element
            if (element.type == "select") {
                // skeleton[comp_index]['elements'][ele_index]['selected_indices'].push(0);
                form_div.classList.add('form-inline');
                select_ele = document.createElement('select');
                select_ele.addEventListener('change', updateSkeleton);
                select_ele.setAttribute('name', String(ele_index) + ',' + String(index));
                element.options.forEach(option => {
                    opt_ele = document.createElement('option');
                    opt_ele.text = option;
                    select_ele.add(opt_ele);
                    select_ele.classList.add('form-control');
                });
                select_ele.selectedIndex = element.indices[index];
                //append in the desired order - label first and then select
                form_div.appendChild(label_ele);
                form_div.appendChild(select_ele);
            } else {
                // skeleton[comp_index]['elements'][ele_index]['selected_indices'].push(false);
                form_div.classList.add('form-check-inline');
                cb_ele = document.createElement('input');
                cb_ele.setAttribute('type', 'checkbox');
                //append in the desired order - cb first and then label
                form_div.appendChild(cb_ele);
                form_div.appendChild(label_ele);
                cb_ele.setAttribute('name', String(ele_index) + ',' + String(index));
                cb_ele.addEventListener('change', updateSkeleton);
                cb_ele.checked = element.indices[index] == 1 ? true : false;
            }


            card_body.appendChild(form_div);

        }
    })
}

function delete_net() {
    $.ajax({
        url: 'api/ComplexNet/delete_by_name/' + meta_controls.net_name.value,
        async: false,
        success: resp => alert(resp.message)
    });
    get_names_by_version(meta_controls.net_versions.value);
    load_net(meta_controls.net_name.value);
}

function addEventListeners() {
    save_button.addEventListener('click', () => toggle_button.checked ? save_net() : update_net());
    delete_button.addEventListener('click', delete_net);
    meta_controls.net_versions.addEventListener('change', update_skeleton);
    meta_controls.net_name.addEventListener('change', () => {
        if (!toggle_button.checked) { //not new
            load_net(meta_controls.net_name.value);
        }
    })
    $('#NewExist_toggle').change(set_form)
}

function update_datalist(datalist_id, values_array, input_id, selected_value) {
    const input = document.querySelector('#' + input_id);
    input.value = selected_value;

    const datalist = document.querySelector('#' + datalist_id);
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

function get_names_by_version(version) {
    $.ajax({
        url: 'api/ComplexNet/get_names_by_version/' + version,
        async: false,
        success: resp => {
            names = resp.data;
            update_datalist('meta_name_datalist', resp.data, 'meta_name', resp.data.length > 0 ? resp.data[0] : '')
        }
    })

}

function load_net(net_name) {
    if (!names.includes(net_name)) {
        return 0;
    }
    clear_skeleton();
    $.get('/api/ComplexNet/get_by_name/' + net_name, resp => {
        if (resp.status) {
            skeleton = resp.data.skeleton;
            console.log(skeleton);
            sensors_div = $('.sensors_div_line1')[0];
            skeleton.data.forEach((component, comp_index) => {
                addComponents(component, comp_index);
            });
            let net_data = resp.data.net;
            meta_controls.owner.value = net_data.owner;
            meta_controls.tags.value = net_data.tags;
            meta_controls.description.value = net_data.description;
            meta_controls.changed_date.innerHTML = "changed date: " + net_data.changed_date;
            meta_controls.changed_by.innerHTML = "changed by: " + net_data.changed_by;
            selected_net.innerHTML = meta_controls.net_name.value;
        } else {
            alert('bad response');
        }
    }).fail(() => {
        alert('fatal error - cannot load Complex Net skeleton');
    });
    return 1;
}

function set_form() {
    if (toggle_button.checked) { //new
        meta_controls.net_name.setAttribute('list', null);
        update_skeleton();
        selected_net.innerHTML = '';
        meta_controls.changed_by.innerHTML = '';
        meta_controls.changed_date.innerHTML = '';
        meta_controls.description.value = '';
        meta_controls.net_name.value = '';
        meta_controls.owner.value = '';
        meta_controls.tags.value = '';
    } else { //exist
        meta_controls.net_name.setAttribute('list', 'meta_name_datalist');
        get_names_by_version(meta_controls.net_versions.value);
        load_net(meta_controls.net_name.value);
    }
}

function update_skeleton() {
    if (toggle_button.checked) { //new
        version = meta_controls.net_versions.value;
        clear_skeleton();
        get_skeleton(version);
    } else { //existing
        get_names_by_version(meta_controls.net_versions.value);
        load_net(meta_controls.net_name.value);
    }
}

async function get_skeleton(version) {
    // let skeleton = {};
    await $.get('/api/ComplexNet/get_skeleton/' + version, resp => {
        if (resp.status) {
            skeleton = resp.skeleton;
            console.log(skeleton);
            sensors_div = $('.sensors_div_line1')[0];
            skeleton.data.forEach((component, comp_index) => {
                addComponents(component, comp_index);
            });
        } else {
            alert('bad response');
        }
    }).fail(() => {
        alert('fatal error - cannot load Complex Net skeleton');
    });
    // return skeleton;
}

function get_users() {
    let users = [];
    $.get('api/User/get_names', resp =>
        resp.status ? update_datalist('meta_owner_datalist', resp.data, 'meta_owner', resp.data[0]) : alert('server error')
    );
    // return users;
}

function update_versions(versions, latest) {
    const datalist = meta_controls.net_versions_datalist;
    const numOfEle = datalist.childElementCount;
    for (let index = 0; index < numOfEle; index++) {
        datalist.removeChild(datalist.children[0]);
    }

    for (let index = 0; index < versions.length; index++) {
        let option = document.createElement('option');
        option.text = versions[index];
        datalist.appendChild(option);
    }

    meta_controls.net_versions.value = latest;

}

function clear_skeleton() {
    external_simulators_div = document.querySelector('.external_simulators_div');
    numOfEle = external_simulators_div.children.length;
    for (let index = 0; index < numOfEle; index++) {
        external_simulators_div.removeChild(external_simulators_div.children[0]);
    }

    sensors_div_line1 = document.querySelector('.sensors_div_line1');
    numOfEle = sensors_div_line1.children.length;
    for (let index = 0; index < numOfEle; index++) {
        sensors_div_line1.removeChild(sensors_div_line1.children[0]);
    }
}

function get_skeleton_versions() {
    let version = []
    $.ajax({
        url: 'api/ComplexNet/get_skeleton_versions',
        async: false,
        success: resp => {
            if (resp.status == 1) {
                update_datalist('net_versions_datalist', resp.versions, 'net_versions', resp.latest)
            } else {
                alert('cannot load versions')
            }
        }
    })
}

function update_users(users, index) {
    let datalist = meta_controls.owner_datalist;
    numOfEle = datalist.children.length;
    for (let index = 0; index < numOfEle; index++) {
        datalist.removeChild(datalist.children[index]);
    }
    for (user of users.values()) {
        option = document.createElement('option');
        option.text = user;
        datalist.appendChild(option);
    }
    meta_controls.owner.value = users[index];
}

async function load_setup() {
    get_skeleton_versions();
    get_skeleton(meta_controls.net_versions.value);
    get_users();
}

window.onload = () => {
    load_setup();
    addEventListeners();
};