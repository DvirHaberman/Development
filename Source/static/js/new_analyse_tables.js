var select_all_button = $('#select_all_button');
var remove_selection_button = $('#remove_selection_button');
var add_selected_button = $('#add_selected_button');

var status_icons = {
    "4": '<div class="status" data-toggle="tooltip" data-placement="top" title="Success"><i class="fas fa-check-circle text-success"></i></span><span hidden="hidden">Success</span></div>',
    "3": '<div class="status" data-toggle="tooltip" data-placement="top" title="Warning"><i class="fas fa-exclamation-triangle text-warning"></i><span hidden="hidden">Warning</span></div>',
    "2": '<div class="status" data-toggle="tooltip" data-placement="top" title="Fail"><i class="fas fa-times-circle text-danger"></i><span hidden="hidden">Fail</span></div>',
    "1": '<div class="status" data-toggle="tooltip" data-placement="top" title="Error"><i class="fas fa-skull-crossbones text-secondary"></i><span hidden="hidden">Error</span></div>',
    "0": '<div class="status" data-toggle="tooltip" data-placement="top" title="No Data"><i class="fab fa-creative-commons-zero text-primary"></i><span hidden="hidden">No Data</span></div>',
    "-1": '<div class="status" data-toggle="tooltip" data-placement="top" title="DB conn invalid"><i class="fas fa-unlink  text-secondary"></i></i><span hidden="hidden">DB conn Invalid</span></div>',
    "-2": '<div class="status" data-toggle="tooltip" data-placement="top" title="Run not in DB"><i class="fas fa-database text-secondary"></i><span hidden="hidden">Run Not In DB</span></div>',
    "-3": "<div class='spinner-border center-spinner' role='status' data-toggle='tooltip' data-placement='top' title='In Process'><span class='sr-only'>Loading...</span><span hidden='hidden'>In Process</span>  </div>",
    "-4": '<div class="status" data-toggle="tooltip" data-placement="top" title="Failed to push task"><i class="fas fa-database text-secondary"></i><span hidden="hidden">Failed Logging Task</span></div>',
    "-5": '<div class="status" data-toggle="tooltip" data-placement="top" title="Failed to log results"><i class="fas fa-database text-secondary"></i><span hidden="hidden">Failed Logging Results</span></div>'
}

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

function update_drill_down_table(data) {
    if ($.fn.DataTable.isDataTable('#drill_down_table')) {
        $('#drill_down_table').DataTable().destroy();
        $('#drill_down_table').empty();
    }
    $('#drill_down_table').DataTable({
        data: data.data,
        select: true,
        columns: data.column_names
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