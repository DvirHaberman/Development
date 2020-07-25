var results_tab = $('#results_tab')[0];
var statistics_tab = $('#statistics_tab')[0];
var results_div = $('#results_div')[0];
var statistics_table_div = $('#statistics_table_div')[0];

var collapse_analyse_button = $('#collapse_analyse_button')[0];

$('#collapse_analyse_button').click(function() {
    $('#collapse_analyse_button i').toggleClass("fa-minus-square");
    $('#collapse_analyse_button i').toggleClass("fa-plus-square");
});

results_tab.addEventListener('click', () => {
    statistics_tab.classList.remove('active')
    statistics_table_div.hidden = true;
    results_tab.classList.add('active')
    results_div.hidden = false;
});

statistics_tab.addEventListener('click', () => {
    results_tab.classList.remove('active');
    results_div.hidden = true;
    statistics_tab.classList.add('active');
    statistics_table_div.hidden = false;
});

function get_mission_ids() {
    var mission_datalist = $('#mission_id_datalist')[0];
    $.ajax({
        url: "/api/Mission/get_ids",
        success: function(result) {
            var num_of_missions = result.length;
            var num_of_curr_missions = mission_datalist.options.length;
            for (i = 0; i < num_of_curr_missions; i++) {
                mission_datalist.remove(0);
            }
            for (i = 0; i < num_of_missions; i++) {
                opt = document.createElement('option');
                opt.text = result[i]
                mission_datalist.appendChild(opt);
            }
            // sleep(500).then(() => {
            //     load_results();
            // });

            // clear_drill_down();
        }
    });
}