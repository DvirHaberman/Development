var myWorker = new Worker(URL.createObjectURL(new Blob(["(" + worker_function.toString() + ")()"], { type: 'text/javascript' })));

myWorker.onmessage = function(e) {
    console.log(e.data);
    myWorker.postMessage(e.data);
}

$('#btn1').click(() => {
    console.log('clickckckckckck!!!!');
});