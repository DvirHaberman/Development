function analyse_worker_function() {
    // importScripts('../js/jquery_3_4_1_min.js')
    var data = 0;
    var run_flag = 0;

    function wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        origin = e.data.origin;
        analyse_mission_name = e.data.analyse_mission_name;
        while (true) {
            await wait(1000)
            await fetch(origin + "/api/AnalyseTask/get_mission_results/" + analyse_mission_name).then(response => response.json())
                .then((data) => postMessage(data));
        }
    }
}