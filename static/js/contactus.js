    function submitFeedback() {
        // Reset previous error messages
        document.getElementById('emailError').textContent = '';
        document.getElementById('phoneError').textContent = '';
        document.getElementById('feedbackError').textContent = '';

        // Validate email, phone, and feedback length (similar to before)

        // Form data is valid, continue with submission
        var formData = new FormData(document.getElementById('feedbackForm'));

        // Use AJAX to send data to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/submit_feedback', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Feedback submitted successfully!');
                window.location.href = '/feedback'; // Redirect to feedback.html
            } else {
                console.error('Failed to submit feedback.');
            }
        };

        // Convert form data to JSON
        var formDataJSON = {};
        formData.forEach(function(value, key) {
            formDataJSON[key] = value;
        });

        // Send JSON data to the server
        xhr.send(JSON.stringify(formDataJSON));
    }