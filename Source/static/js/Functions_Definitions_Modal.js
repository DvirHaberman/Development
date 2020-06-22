
    //   var GroupsList = document.getElementsByName("GroupsListNames")[0];
    //   var numOfRows = GroupsList.children.length;
    //   var selectedGroupName = $('#group_input')[0].value;
    //   if (AllGroups.includes(selectedGroupName)){
    //     found = false;
    //     $("#GroupsList li").each((id, elem) => {
    //     if (elem.innerText == selectedGroupName) {
    //       found = true;
    //     }
    //     });
    //     if (!found) Add_Group(GroupsList,selectedGroupName , numOfRows+1);
    //   } else {
    //     alert("not such Group Name!")
    //   }
    //   // setOperLineString();
    // });

$('#Group_toggle').change(function() {
    if ($('#Group_toggle')[0].checked) { //new
        // infras.new(Site_form_controls, "site_name");
        alert('new group');
        modal_form_controls_handler.new(Group_Modal_form_controls, "Group_name");

    } else { //exist
        getAllGroups("Modal_Select_Group_Name")
        setToggle("Group_funciton_toggle", "on"); //select Function
    }

});

$('#Group_funciton_toggle').change(function() {
    if ($('#Group_funciton_toggle')[0].checked) { //new
        // getAllFunctionNames("Modal_Select_Group_Name");  // or use get names Method
    } else { //exist
        getAllGroups("Modal_Select_Group_Name");
    }

});

$('#Duplicate_Group').change(function() { //duplicate
    alert("duplicate group");
});

$('#Save_Group').change(function() { //save
    alert("save group")
});

$('#Delete_Group').change(function() { //delete
    alert("delete group")
});

$('#Modal_Select_Group_Name').change(function() { //Select
    // get group
});
