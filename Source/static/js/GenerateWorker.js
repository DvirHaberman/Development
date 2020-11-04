function init_worker() {
    if (myWorker) {
        myWorker.terminate();
        myWorker = null;
    }
    myWorker = new Worker(URL.createObjectURL(new Blob(["(" + generate_worker_function.toString() + ")()"], { type: 'text/javascript' })));
}

function generate_worker_function() {
    // importScripts('../js/jquery_3_4_1_min.js')
    var data = 0;
    var run_flag = 0;

    function wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        origin = e.data.origin;
        mission_id = e.data.mission_id;
        while (1) {
            await wait(1000);
            await fetch(origin + "/dummyapi/GenerateMission/get_by_id/" + mission_id).then(response => response.json())
                .then(data => postMessage(data));
        }
    }
}