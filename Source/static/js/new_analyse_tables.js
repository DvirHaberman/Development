var select_all_button = $('#select_all_button');
var remove_selection_button = $('#remove_selection_button');
var add_selected_button = $('#add_selected_button');

var status_icons = {
    "InProcess": "<div class='spinner-border' role='status'><span class='sr-only'>Loading...</span>  </div>",
    "Success": '<div class="status"><i class="fas fa-check-circle text-success"></i></div>',
    "Warning": '<div class="status"><i class="fas fa-exclamation-triangle text-warning"></i></div>',
    "Fail": '<div class="status"><i class="fas fa-times-circle text-danger"></i></div>',
    "Error": '<div class="status"><i class="fas fa-skull-crossbones text-secondary"></i></div>',
    "NoData": '<div class="status"><i class="far fa-circle text-primary"></i></div>'
}

var dataSet2 = [
    ['func1', 'needed', 'dvir', '1234', status_icons.Success, status_icons.Fail, status_icons.Error, status_icons.Warning, status_icons.InProcess, status_icons.Error],
    ['func2', 'InDev', 'dvir', '1234', status_icons.NoData, status_icons.InProcess, status_icons.Success, status_icons.Success, status_icons.InProcess, status_icons.Warning],
    ['func3', 'Completed', 'dvir', '1234', status_icons.Error, status_icons.NoData, status_icons.Fail, status_icons.Fail, status_icons.InProcess, status_icons.InProcess]
]

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
    results_table = $('#results_table').DataTable({
        data: dataSet2,
        select: true,
        columns: [
            { title: "Function" },
            { title: "State" },
            { title: "Owner" },
            { title: "Feature" },
            { title: "db1 - 1223" },
            { title: "db2 - 2222" },
            { title: "db2 - 334" },
            { title: "db2 - 1223" },
            { title: "db1 - 111" },
            { title: "db1 - 333" },
        ]
    });
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