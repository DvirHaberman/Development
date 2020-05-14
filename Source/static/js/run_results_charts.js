var ctx = document.getElementById('results_statistics_chart');
var colors={
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
    type: 'bar',
    data: {
        labels: ['Success', 'Warning', 'Fail', 'Error', 'No Data'],
        datasets: [{
            label: 'Statistics',
            data: [12, 19, 3, 5, 2],
            backgroundColor: [
                colors.success,
                colors.warning,
                colors.fail,
                colors.error,
                colors.nodata
            ],
            borderColor: [
                colors.success,
                colors.warning,
                colors.fail,
                colors.error,
                colors.nodata
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsiveAnimationDuration: 2000
        // scales: {
        //     yAxes: [{
        //         ticks: {
        //             beginAtZero: true
        //         }
        //     }]
        // }
    }
});