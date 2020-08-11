function results_worker_function() {
    // importScripts('../js/jquery_3_4_1_min.js')
    var data = 0;
    var run_flag = 0;

    function wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        origin = e.data.origin;
        mission_id = e.data.mission_id;
        run_id = e.data.run_id;
        function_name = e.data.function_name;
        while (true) {
            await wait(1000)
            await fetch(origin + "/api/AnalyseTask/get_mission_results/" + analyse_mission_name).then(response => response.json())
                .then((data) => postMessage(data));
        }
    }
}