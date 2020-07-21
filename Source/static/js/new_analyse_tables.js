var status_icons = {
    "InProcess": "<div class='spinner-border' role='status'><span class='sr-only'>Loading...</span>  </div>",
    "Success": '<div class="status"><i class="fas fa-check-circle text-success"></i></div>',
    "Warning": '<div class="status"><i class="fas fa-exclamation-triangle text-warning"></i></div>',
    "Fail": '<div class="status"><i class="fas fa-times-circle text-danger"></i></div>',
    "Error": '<div class="status"><i class="fas fa-skull-crossbones text-secondary"></i></div>',
    "NoData": '<div class="status"><i class="far fa-circle text-primary"></i></div>'
}
var dataSet = [
    ['func1', 'needed', 'dvir', '1234'],
    ['func2', 'InDev', 'dvir', '1234'],
    ['func3', 'Completed', 'dvir', '1234']
]

var dataSet2 = [
    ['func1', 'needed', 'dvir', '1234', status_icons.Success, status_icons.Fail, status_icons.Error, status_icons.Warning, status_icons.InProcess, status_icons.Error],
    ['func2', 'InDev', 'dvir', '1234', status_icons.NoData, status_icons.InProcess, status_icons.Success, status_icons.Success, status_icons.InProcess, status_icons.Warning],
    ['func3', 'Completed', 'dvir', '1234', status_icons.Error, status_icons.NoData, status_icons.Fail, status_icons.Fail, status_icons.InProcess, status_icons.InProcess]
]
var dataSet3 = [
    ['1111', 'bla1', 'nana', 'nana', 'banana'],
    ['2222', 'blabla', 'damdam', 'damdam', 'damndam'],
    ['3333', 'papapa', 'zzzz', 'aaa', 'pumpum']
]
$(document).ready(function() {
    $('#functions_table').DataTable({
        data: dataSet,
        columns: [
            { title: "Function" },
            { title: "State" },
            { title: "Owner" },
            { title: "Feature" }
        ]
    });
    $('#runs_table').DataTable({
        data: dataSet3,
        columns: [
            { title: "Run ID" },
            { title: "Scenario Name" },
            { title: "stuff1" },
            { title: "stuff2" },
            { title: "stuff3" }
        ]
    });
});

$(document).ready(function() {
    $('#results_table').DataTable({
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