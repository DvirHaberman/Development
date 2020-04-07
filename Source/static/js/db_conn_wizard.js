var connections = [];

var form_controls = {
    db_type : $('#db_type')[0],
    user : $('#user')[0],
    password : $('#password')[0],
    hostname : $('#hostname')[0],
    port : $('#port')[0],
    schema : $('#schema')[0],
    name : $('#name')[0],
    save_button : $('#save_button')[0]
}

var display_controls = {
    disp_connections : $('#current_connections')[0],
    disp_db_type : $('#disp_db_type')[0],
    disp_user : $('#disp_user')[0],
    disp_password : $('#disp_password')[0],
    disp_hostname : $('#disp_hostname')[0],
    disp_port : $('#disp_port')[0],
    disp_schema : $('#disp_schema')[0],
    disp_name : $('#disp_name')[0]
}

function display_conn(selected_index){
    display_controls.disp_db_type.innerText = connections[selected_index].db_type;
    display_controls.disp_user.innerText = connections[selected_index].user;
    display_controls.disp_password.innerText = connections[selected_index].password;
    display_controls.disp_hostname.innerText = connections[selected_index].hostname;
    display_controls.disp_port.innerText = connections[selected_index].port;
    display_controls.disp_schema.innerText = connections[selected_index].schema;
    display_controls.disp_name.innerText = connections[selected_index].name;
}

function clear_display(){
    display_controls.disp_db_type.innerText = ''
    display_controls.disp_user.innerText = ''
    display_controls.disp_password.innerTextvalue = ''
    display_controls.disp_hostname.innerText = ''
    display_controls.disp_port.innerText = ''
    display_controls.disp_schema.innerText = ''
    display_controls.disp_name.innerText = ''
}

function update_conn_display(){
    
    //getting current conn name to choose after update
    select_control = display_controls.disp_connections;
    num_of_options = select_control.options.length;
    if(num_of_options>0){
        curr_name = select_control.options[select_control.selectedIndex].text;
    }else{
        curr_name = '';
    }

    //remove old connecitons
    for(k=0;k<num_of_options;k++){
        select_control.remove(0);
    }

    //insert new names
    num_of_connection = connections.length;
    selected_index = 0;
    for(k=0;k<num_of_connection;k++){
        option = document.createElement('option');
        option.text = connections[k].name;
        if (option.text === curr_name){
            option.selected = true;
        }else{
            option.selected = false;
        }
        select_control.add(option);
    }

    //assign curr connection data to display controls
    if(num_of_connection > 0){
        display_conn(selected_index)
    }else{
        clear_display();
    }

}

function get_conn_data(){
    $.ajax({
        url: '/api/get_conn_data',
        success:function(conn_data){
            connections = conn_data;
            update_conn_display();
        }
    });
}

display_controls.disp_connections.addEventListener('change', function (){
    var selected_index = display_controls.disp_connections.selectedIndex;
    display_conn(selected_index);
})

form_controls.save_button.addEventListener('click',function (){
    form_controls.save_button.disabled=true;
    var data = {
        db_type : form_controls.db_type.options[form_controls.db_type.selectedIndex].text,
        user : form_controls.user.value,
        password : form_controls.password.value,
        hostname : form_controls.hostname.value,
        port : form_controls.port.value,
        schema : form_controls.schema.value,
        name : form_controls.name.value
    }
    $.ajax({
        type: "POST",
        url: "/api/save_connection",
        dataType: "json",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(result) {
          alert(result.message);
          get_conn_data();
          form_controls.save_button.disabled=false;
        }
      });
})

get_conn_data();