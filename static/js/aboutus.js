//retrieve button
    document.getElementById("retrieveDataButton").addEventListener("click", function() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var conversationData = JSON.parse(xhr.responseText);
                var conversationDisplay = document.getElementById("conversationData");

                var html = "<h2>Conversation Data:</h2>";

                html += "<p>Latest Message ID: " + conversationData['msgID'] + "</p>";

                html += "<p>Messages:</p>";
                for (var msgId in conversationData['message']) {
                    if (conversationData['message'].hasOwnProperty(msgId)) {
                        var msgText = conversationData['message'][msgId];
                        html += "<p>Message ID: " + msgId + ", Message Text: " + JSON.stringify(msgText) + "</p>";
                    }
                }

                conversationDisplay.innerHTML = html;
            }
        };
        xhr.open("GET", "/get_conversation_data", true);
        xhr.send();
    });

//    delete button
    document.getElementById("deleteDataButton").addEventListener("click", function() {
        var msgIdToDelete = prompt("Enter the Message ID to delete:");

        if (msgIdToDelete !== null) {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    alert(xhr.responseText);
                }
            };
            xhr.open("POST", "/delete_conversation_data", true);
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhr.send("msgID=" + String(msgIdToDelete));
        }
    });