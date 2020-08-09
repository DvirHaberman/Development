function worker_function() {
    var data = 0;

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    onmessage = async function(e) {
        await sleep(3000)
        $.ajax({
            url: 'api/' + e.data + '/get_names',
            async: false,
            success: (response) => {
                data = response.data[0];
            }
        });
        postMessage(data)
    }
}