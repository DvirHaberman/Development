var select_all_button = $('#select_all_button');
var remove_selection_button = $('#remove_selection_button');
var add_selected_button = $('#add_selected_button');

var status_icons = {
    "-3": "<div class='spinner-border center-spinner' role='status' data-toggle='tooltip' data-placement='top' title='In Process'><span class='sr-only'>Loading...</span>  </div>",
    "4": '<div class="status" data-toggle="tooltip" data-placement="top" title="Success"><i class="fas fa-check-circle text-success"></i></div>',
    "3": '<div class="status" data-toggle="tooltip" data-placement="top" title="Warning"><i class="fas fa-exclamation-triangle text-warning"></i></div>',
    "2": '<div class="status" data-toggle="tooltip" data-placement="top" title="Fail"><i class="fas fa-times-circle text-danger"></i></div>',
    "1": '<div class="status" data-toggle="tooltip" data-placement="top" title="Error"><i class="fas fa-skull-crossbones text-secondary"></i></div>',
    "0": '<div class="status" data-toggle="tooltip" data-placement="top" title="No Data"><i class="fab fa-creative-commons-zero text-primary"></i></div>',
    "-1": '<div class="status" data-toggle="tooltip" data-placement="top" title="DB conn invalid"><i class="fas fa-unlink  text-secondary"></i></i></div>',
    "-2": '<div class="status" data-toggle="tooltip" data-placement="top" title="Run not in DB"><i class="fas fa-database text-secondary"></i></div>',
    "-4": '<div class="status" data-toggle="tooltip" data-placement="top" title="Failed to push task"><i class="fas fa-database text-secondary"></i></div>',
    "-5": '<div class="status" data-toggle="tooltip" data-placement="top" title="Failed to log results"><i class="fas fa-database text-secondary"></i></div>'
}

// var dataSet2 = [
//     ['func1', 'needed', 'dvir', '1234', status_icons.Success, status_icons.Fail, status_icons.Error, status_icons.Warning, status_icons.InProcess, status_icons.Error],
//     ['func2', 'InDev', 'dvir', '1234', status_icons.NoData, status_icons.InProcess, status_icons.Success, status_icons.Success, status_icons.InProcess, status_icons.Warning],
//     ['func3', 'Completed', 'dvir', '1234', status_icons.Error, status_icons.NoData, status_icons.Fail, status_icons.Fail, status_icons.InProcess, status_icons.InProcess]
// ]

function update_table(data) {
    if ($.fn.DataTable.isDataTable('#results_table')) {
        $('#results_table').DataTable().destroy();
        $('#results_table').empty();
    }
    $('#results_table').DataTable({
        data: data.table_data,
        select: true,
        columns: data.table_columns
    });
}

$(document).ready(function() {
    functions_table = $('#functions_table').DataTable({
        ajax: { url: "/api/OctopusFunction/get_names_json", async: false },
        columns: [
            { title: "Function", "data": "name" },
            { title: "Status", "data": "status" },
            { title: "Owner", "data": "owner" },
            { title: "Feature", "data": "feature" }
        ]
    });
    groups_table = $('#groups_table').DataTable({
        select: true,
        ajax: { url: "/api/FunctionsGroup/get_names_json", async: false },
        columns: [
            { title: "Group Name", "data": "name" }
        ]
    });

    lists_table = $('#lists_table').DataTable({
        select: true,
        ajax: { url: "/api/RunList/get_names_json", async: false },
        columns: [
            { title: "List Name", "data": "name" }
        ]
    });

    runs_table = $('#runs_table').DataTable({
        ajax: { url: 'api/DbConnector/get_empty', async: false },
        select: true,
        columns: [
            { title: "Run ID", "data": "run_id" },
            { title: "Scenario", "data": "scenario_name" }
        ]

    });
    // results_table = $('#results_table').DataTable({
    //     data: dataSet2,
    //     select: true,
    //     columns: [
    //         { title: "Function" },
    //         { title: "State" },
    //         { title: "Owner" },
    //         { title: "Feature" },
    //         { title: "db1 - 1223" },
    //         { title: "db2 - 2222" },
    //         { title: "db2 - 334" },
    //         { title: "db2 - 1223" },
    //         { title: "db1 - 111" },
    //         { title: "db1 - 333" },
    //     ]
    // });
    //event listeners makes tables row highliht on click
    $('#functions_table tbody').on('click', 'tr', function() {
        $(this).toggleClass('selected');
    });
    $('#runs_table tbody').on('click', 'tr', function() {
        $(this).toggleClass('selected');
    });
    $('#groups_table tbody').on('click', 'tr', function() {
        $(this).toggleClass('selected');
    });

    $('#lists_table tbody').on('click', 'tr', function() {
        $(this).toggleClass('selected');
    });
    // $('#results_table tbody').on('click', 'tr', function() {
    //     $(this).toggleClass('selected');
    // });

    $("#functions_table").selectable({
        distance: 10,
        stop: enable_drag_select
    });

    $("#groups_table").selectable({
        distance: 10,
        stop: enable_drag_select
    });

    $("#runs_table").selectable({
        distance: 10,
        stop: enable_drag_select
    });

    $("#lists_table").selectable({
        distance: 10,
        stop: enable_drag_select
    });

    function enable_drag_select() {
        $(this).find("tr.ui-selected").each(
            function() {
                if ($(this).hasClass('ui-selectee'))
                    $(this).toggleClass('selected');
                // else
                //     $(this).removeClass('selected');
            });
    }

});