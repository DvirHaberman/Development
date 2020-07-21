var runs_tab = $('#runs_tab')[0];
var functions_tab = $('#functions_tab')[0];
var functions_table_div = $('#functions_table_div')[0];
var runs_table_div = $('#runs_table_div')[0];

var results_tab = $('#results_tab')[0];
var statistics_tab = $('#statistics_tab')[0];
var results_div = $('#results_div')[0];
var statistics_table_div = $('#statistics_table_div')[0];

var collapse_setup_button = $('#collapse_setup_button')[0];
// var functions_table = $('#functions_tab')[0];
// var functions_table = $('#functions_tab')[0];

$('#collapse_setup_button').click(function() {
    $('#collapse_setup_button i').toggleClass("fa-minus-square");
    $('#collapse_setup_button i').toggleClass("fa-plus-square");
});

runs_tab.addEventListener('click', () => {
    functions_tab.classList.remove('active')
    functions_table_div.hidden = true;
    runs_tab.classList.add('active')
    runs_table_div.hidden = false;
});

functions_tab.addEventListener('click', () => {
    runs_tab.classList.remove('active');
    runs_table_div.hidden = true;
    functions_tab.classList.add('active');
    functions_table_div.hidden = false;
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