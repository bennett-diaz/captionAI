function getImageUrl() {
    // Get the image URL from the HTML element
    return document.getElementById("imageUrl").textContent;
}

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
            const response = JSON.parse(xhr.responseText);

            // Redirect to the Results page with the witty captions
            window.location.href = '/results?image_url=' + encodeURIComponent(imageUrl) +
                '&caption_list=' + encodeURIComponent(JSON.stringify(response.captions));
        } else {
            // Handle errors if necessary
            console.error('Error:', xhr.status);
        }
    };
}

// Call the processImage() function when the user is directed to the loading page
window.onload = function () {
    processImage();
};