var myctx = document.getElementById('statistics_chart');
var colors = {
    nodata: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    info: '#17a2b8',
    warning: '#ffc107',
    fail: '#dc3545',
    light: '#f8f9fa',
    error: '#343a40',
    invalid_conn: "#8675a9",
    run_not_in_db: "#cffffe",
    failed_to_log_results: "#411f1f"
};
var new_analyse_chart = new Chart(myctx, {
    type: 'doughnut',
    data: {
        labels: ['No Data', 'Error', 'Fail', 'Warning', 'Success', 'Failed to log results', 'Failed to push to queue', 'InProcess', 'Run Not in DB', 'Invalid Conn'],
        datasets: [{
            label: ['No Data', 'Error', 'Fail', 'Warning', 'Success', 'Run Not in DB', 'Invalid Conn', 'InProcess', 'Failed to push to queue', 'Failed to log results'],
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                colors.nodata,
                colors.error,
                colors.fail,
                colors.warning,
                colors.success,
                colors.secondary,
                colors.secondary,
                colors.invalid_conn,
                colors.run_not_in_db,
                colors.failed_to_log_results
            ],
            borderColor: [
                colors.nodata,
                colors.error,
                colors.fail,
                colors.warning,
                colors.success,
                colors.secondary,
                colors.secondary,
                colors.invalid_conn,
                colors.run_not_in_db,
                colors.failed_to_log_results
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        responsiveAnimationDuration: 500
            // scales: {
            //     yAxes: [{
            //         ticks: {
            //             beginAtZero: true
            //         }
            //     }]
            // }
    }
});