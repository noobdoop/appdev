    function showConfirmationModal(index) {
        var modal = document.getElementById('confirmationModal' + index);
        modal.style.display = 'block';
    }

    function hideConfirmationModal(index) {
        var modal = document.getElementById('confirmationModal' + index);
        modal.style.display = 'none';
    }

    function deleteRow(index) {
        hideConfirmationModal(index);

        // Send AJAX request to delete the row on the server
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/delete_feedback/' + index, true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log('Row deleted successfully');
                // Reload the page to reflect the changes
                window.location.reload();
            } else {
                console.error('Failed to delete row.');
            }
        };

        xhr.send();
    }