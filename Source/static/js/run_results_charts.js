var ctx = document.getElementById('results_statistics_chart');
var colors = {
    nodata: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    info: '#17a2b8',
    warning: '#ffc107',
    fail: '#dc3545',
    light: '#f8f9fa',
    error: '#343a40'
};
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Success', 'Warning', 'Fail', 'Error', 'No Data', 'Unknown', 'In process'],
        datasets: [{
            label: ['Success', 'Warning', 'Fail', 'Error', 'No Data', 'Unknown', 'In process'],
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
                colors.success,
                colors.warning,
                colors.fail,
                colors.error,
                colors.nodata,
                colors.info,
                colors.secondary
            ],
            borderColor: [
                colors.success,
                colors.warning,
                colors.fail,
                colors.error,
                colors.nodata,
                colors.info,
                colors.secondary
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsiveAnimationDuration: 1500
            // scales: {
            //     yAxes: [{
            //         ticks: {
            //             beginAtZero: true
            //         }
            //     }]
            // }
    }
});