function processImage() {
    // Get the image URL from the URL parameters
    const imageUrl = window.location.search.substring(1).split('&')[0].split('=')[1];

    // Create an HTTP request to the backend
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/process_image', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Prepare the request data (if needed)
    const data = {
        image_url: imageUrl
    };

    // Send the request to the backend
    xhr.send(JSON.stringify(data));

    // Define a callback function to handle the response from the backend
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Parse the response data (assuming it's JSON)
            try {
                console.log(xhr.responseText);
                const response = JSON.parse(xhr.responseText);
    
                // Redirect to the Results page with the witty captions
                window.location.href = '/results?image_url=' + encodeURIComponent(imageUrl) +
                    '&caption_list=' + encodeURIComponent(JSON.stringify(response.captions));
            } catch (error) {
                // Handle JSON parsing error
                console.error('Error parsing JSON response:', error);
            }
        } else if (xhr.status === 400) {
            try {
                const errorResponse = JSON.parse(xhr.responseText);
                const errorMessage = errorResponse.error || 'An error occurred';
                window.location.href = '/error?error_message=' + encodeURIComponent(errorMessage);
            } catch (error) {
                console.error('Error handling error response:', error);
            }
        
        // delete this

        } else {
            // Handle errors if necessary
            console.error('Error:', xhr.status);
    
            // Redirect to the error page or display an error message to the user
            // The ? indicates the start of query parameters in the URL.
            window.location.href = '/error?error_message=' + encodeURIComponent('Other error');
        }
    };
}

// Call the processImage() function when the user is directed to the loading page
window.onload = function () {
    processImage();
};