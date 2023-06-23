function startDictation(fieldId) {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();
        recognition.onresult = function (e) {
            var text = e.results[0][0].transcript.trim();
            if (text.endsWith('.')) {
                text = text.slice(0, -1);
            }
            document.getElementById(fieldId).value = text;
            recognition.stop();
        };
        recognition.onerror = function (e) {
            recognition.stop();
        };
    }
}

