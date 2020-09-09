var skeleton = {};

var curr_net = {};

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

    //looping inner elements
    component.elements.forEach((element, ele_index) => {
        //for each element add it a number of times specified in element.amount
        skeleton[comp_index]['elements'][ele_index]['selected_indices'] = []
        for (let index = 0; index < element.amount; index++) {

            //creating the containing div
            form_div = document.createElement('div');
            //creating and editing the label
            label_ele = document.createElement('label');
            label_ele.innerHTML = element.labels[index];

            //check if cb or select element
            if (element.type == "select") {
                skeleton[comp_index]['elements'][ele_index]['selected_indices'].push(0);
                form_div.classList.add('form-inline');
                select_ele = document.createElement('select');
                element.options.forEach(option => {
                    opt_ele = document.createElement('option');
                    opt_ele.text = option;
                    select_ele.add(opt_ele);
                    select_ele.classList.add('form-control');
                });
                //append in the desired order - label first and then select
                form_div.appendChild(label_ele);
                form_div.appendChild(select_ele);
            } else {
                skeleton[comp_index]['elements'][ele_index]['selected_indices'].push(false);
                form_div.classList.add('form-check-inline');
                cb_ele = document.createElement('input');
                cb_ele.setAttribute('type', 'checkbox');
                //append in the desired order - cb first and then label
                form_div.appendChild(cb_ele);
                form_div.appendChild(label_ele);
                // cb_ele.addEventListener('change',()=>)
            }


            card_body.appendChild(form_div);

        }
    })
}

window.onload = () => {
    $.get('/api/ComplexNet/get_skeleton', (resp) => {
        if (resp.status) {
            skeleton = resp.skeleton;
            console.log(skeleton);
            sensors_div = $('.sensors_div_line1')[0];
            skeleton.forEach((component, comp_index) => {
                addComponents(component, comp_index);
            });
        } else {
            alert('bad response');
        }
    }).fail(() => {
        alert('fatal error - cannot load Complex Net skeleton');
    });
};