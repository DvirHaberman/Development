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
        // data: dataSet,
        ajax: { url: "/api/OctopusFunction/get_names_json" },
        columns: [
            { title: "Function", "data": "name" },
            { title: "Status", "data": "status" },
            { title: "Owner", "data": "owner" },
            { title: "Feature", "data": "feature" }
        ]
    });
    runs_table = $('#runs_table').DataTable({
        // data: dataSet3,
        // dataSrc: "",
        columns: [
            { title: "Run ID", "data": "run_id" },
            { title: "Scenario", "data": "scenario_name" }
        ]

    });
});

$(document).ready(function() {
    results_table = $('#results_table').DataTable({
        data: dataSet2,
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
});