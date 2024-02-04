document.getElementById('uploadButton').addEventListener('click', function () {
    const fileInput = document.getElementById('formFile2');
    const contactInfo = document.getElementById('contactInfo');
    const uploadButton = document.getElementById('uploadButton');

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('title', 'Lost here');
    formData.append('contact', contactInfo.value);
    contactInfo.value = ""
    fileInput.value = "";

    fetch('http://127.0.0.1:8000/add_lost_item', {
        method: 'POST',
        body: formData,

    }).then(response => {
        if (response.ok) {

            uploadButton.className = "btn btn-success mt-3 disabled"
            uploadButton.innerText = "Item added succesfully!"

        } else {
            uploadButton.className = 'btn btn-danger mt-3 disabled';
            uploadButton.innerText = "Item Failed to Add"
        }
    }).catch(error => {
        console.error('Error:', error);

        uploadButton.className = 'btn btn-danger mt-3 disabled';
        uploadButton.innerText = "Item Failed to Add"
    });

    setTimeout(function () {
        // Revert the button class back after 3 seconds
        uploadButton.className = 'btn btn-outline-dark mt-3';
        uploadButton.innerText = "Upload"
    }, 3000);

});

document.getElementById("textSubmit").addEventListener('click', function () {
    const textInput = document.getElementById("textInput");
    const uploadButton = document.getElementById("uploadButtonId");
    let resp = null;
    const data = JSON.stringify({ text: textInput.value });

    fetch('http://127.0.0.1:8000/find_matches', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: data,
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                alert('No matching items found.');
            }
        })
        .then(data => {
            if (data.matches && data.matches.length > 0) {
                console.log(data.matches)
                // Render images and contact information for each match
                renderImagesWithContactInfo(data.matches);
            } else {
                alert('No matching items found.');
            }

            textInput.value = "";
        })
        .catch(error => {
            console.error('Error:', error);

        })

    // Function to render images and contact information for each match
    function renderImagesWithContactInfo(matchesArray) {
        const imageContainer = document.getElementById('imageContainer');

        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }

        matchesArray.forEach(match => {
            const imageDiv = document.createElement('div');
            imageDiv.className = 'col';
            const imageElement = new Image();
            imageElement.src = 'http://127.0.0.1:8000/' + match.image_path; // Assuming 'image_path' is the key in the response JSON
            imageElement.alt = 'Image'; // Add alt text for accessibility

            // Add a click event listener to display contact information in an alert
            imageElement.addEventListener('click', () => {
                alert(`Contact: ${match.contact}`);
            });

            imageDiv.appendChild(imageElement);
            imageContainer.appendChild(imageDiv);
        });
    }
});


document.getElementById("imageSubmit").addEventListener('click', function () {
    const fileInput = document.getElementById("formFile1");
    const uploadButton = document.getElementById("imageSubmit");

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fileInput.value = "";

    fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,

    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                alert('No matching items found.');
            }
        })
        .then(data => {
            if (data.matches && data.matches.length > 0) {
                console.log(data.matches)
                // Render images and contact information for each match
                renderImagesWithContactInfo(data.matches);
            } else {
                alert('No matching items found.');
            }

            textInput.value = "";
        })
        .catch(error => {
            console.error('Error:', error);

        })

    // Function to render images and contact information for each match
    function renderImagesWithContactInfo(matchesArray) {
        const imageContainer = document.getElementById('imageContainer');

        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }

        matchesArray.forEach(match => {
            const imageDiv = document.createElement('div');
            imageDiv.className = 'col';
            const imageElement = new Image();
            imageElement.src = 'http://127.0.0.1:8000/' + match.image_path; // Assuming 'image_path' is the key in the response JSON
            imageElement.alt = 'Image'; // Add alt text for accessibility

            // Add a click event listener to display contact information in an alert
            imageElement.addEventListener('click', () => {
                alert(`Contact: ${match.contact}`);
            });

            imageDiv.appendChild(imageElement);
            imageContainer.appendChild(imageDiv);
        });
    }
});