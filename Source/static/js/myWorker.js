function worker_function() {
    // importScripts('../js/jquery_3_4_1_min.js')
    var data = 0;
    var run_flag = 0;

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        var run_flag = e.data.run;
        while (run_flag) {
            await sleep(1500)
                // const absolute = new URL("api/AnalyseSetup/get_names", e.data);
                // fetch("http://127.0.0.1:5000/api/AnalyseSetup/get_names").then(response => response.json())
                //     .then(data => postMessage(data));
                // fetch("http://127.0.0.1:5000/api/OctopusFunction/get_names").then(response => response.json())
                //     .then(data => postMessage(data));
                // fetch("http://127.0.0.1:5000/api/AnalyseSetup/get_names").then(response => response.json())
                //     .then(data => postMessage(data));
            postMessage(1);
        }
    }
}