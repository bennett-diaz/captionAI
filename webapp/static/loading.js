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

                // !Will need to put all query params here for all models
                const queryParams = new URLSearchParams({
                    image_url: imageUrl,
                    summary: JSON.stringify(response['summary']),
                    sum_response_time: JSON.stringify(response['sum_response_time']),
                    caption_list: JSON.stringify(response['caption_list']),
                    cap_response_time: JSON.stringify(response['cap_response_time']),
                });
                window.location.href = '/results?' + queryParams.toString();
            } catch (error) {
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
        } else {
            console.error('Non-200 or 400 HTTP response:', xhr.status);        }
    };
}

// Call the processImage() function when the user is directed to the loading page
window.onload = function () {
    processImage();
};