// Function to perform a GET request for fetching data
async function getData(url) {
    try {
        // Send a GET request to the specified URL
        const response = await fetch(url);
        // Check if the response status is not OK (status code is not 200-299)
        if (!response.ok) {
            // Throw an error if the response status is not OK
            throw new Error('Failed to fetch data');
        }
        // Parse and return the JSON response
        return response.json();
    } catch (error) {
        // Log any errors to the console
        console.error('Error:', error);
    }
}

// Function to display data on the page
function displayData(data, containerId) {
    // Get the container element by its ID
    const container = document.getElementById(containerId);
    // Clear any existing content in the container
    container.innerHTML = '';

    // Check if the data is an array
    if (Array.isArray(data)) {
        // Check if the array has elements
        if (data.length > 0) {
            // Create a new unordered list element
            const ul = document.createElement('ul');
            // Iterate over each item in the data array
            data.forEach(item => {
                // Create a new list item element for each data item
                const li = document.createElement('li');
                // Set the text content of the list item with the data item's properties
                li.textContent = `ID: ${item.id}, Name: ${item.name}, Email: ${item.email}, Filename: ${item.filename}`;
                // Append the list item to the unordered list
                ul.appendChild(li);
            });
            // Append the unordered list to the container
            container.appendChild(ul);
        } else {
            // Display a message if there is no data
            container.textContent = 'No data available.';
        }
    } else {
        // Display an error message if the data format is incorrect
        container.textContent = 'Error: Data is not in the expected format.';
    }
}

// Function to handle form submission for uploading data
document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Create a FormData object from the form
    const formData = new FormData(this);
    // Create an empty object to hold the form data
    const data = {};
    // Populate the data object with form data
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Define the API endpoint URL
    const apiUrl = 'https://example.execute-api.us-east-1.amazonaws.com/v1/items';
    // Send a PUT request to the API endpoint with the form data
    const response = await fetch(apiUrl, {
        method: 'PUT', // Set the request method to PUT
        headers: {
            'Content-Type': 'application/json' // Set the request headers
        },
        body: JSON.stringify(data) // Set the request body to the stringified data object
    });
    // Parse the JSON response
    const result = await response.json();
    // Log the upload response
    console.log('Upload response:', result);

    // Refresh data after successful upload
    if (result.success) {
        // Fetch the updated data
        const newData = await getData(apiUrl);
        // Display the updated data
        displayData(newData, 'viewDataContainer');
    }

    // Clear upload form fields
    this.reset(); // Reset the form fields
});

// Function to handle form submission for deleting an item
document.getElementById('deleteForm').addEventListener('submit', async function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get and trim the delete ID value
    const deleteId = document.getElementById('deleteId').value.trim();
    // Alert if no ID is entered
    if (!deleteId) {
        alert('Please enter the ID of the item to delete.');
        return;
    }

    // Define the API endpoint URL for deleting the item
    const apiUrl = `https://example.execute-api.us-east-1.amazonaws.com/v1/items/${deleteId}`;
    // Send a DELETE request to the API endpoint
    const response = await fetch(apiUrl, {
        method: 'DELETE' // Set the request method to DELETE
    });
    // Parse the JSON response
    const result = await response.json();
    // Log the delete response
    console.log('Delete response:', result);

    // Refresh data after successful delete
    if (result.success) {
        // Fetch the updated data
        const newData = await getData(apiUrl);
        // Display the updated data
        displayData(newData, 'viewDataContainer');
    }

    // Clear delete form field
    document.getElementById('deleteId').value = ''; // Clear the delete ID input field
});

// Function to handle form submission for querying data
document.getElementById('queryForm').addEventListener('submit', async function(event) {
    // Prevent the default form submission behavior
    event.preventDefault();

    // Get the query type value
    const queryType = document.getElementById('queryType').value;
    // Get and trim the query value
    const queryValue = document.getElementById('queryValue').value.trim();
    // Get the query button element
    const queryBtn = document.getElementById('queryBtn');
    // Get the query results header element
    const queryResultsHeader = document.getElementById('queryResultsHeader');
    // Get the query data container element
    const queryDataContainer = document.getElementById('queryDataContainer');

    // Alert if no query value is entered
    if (!queryValue) {
        alert('Please enter a value for the query.');
        return;
    }

    // Check if the query button text is 'Query'
    if (queryBtn.textContent === 'Query') {
        // Define the API endpoint URL for querying data
        const queryUrl = `https://example.execute-api.us-east-1.amazonaws.com/v1/items?${queryType}=${queryValue}`;
        // Fetch the queried data
        const data = await getData(queryUrl);
        // Display the queried data
        displayData(data, 'queryDataContainer');
        // Show the query results header
        queryResultsHeader.style.display = 'block';
        // Change the query button text to 'Cancel Query'
        queryBtn.textContent = 'Cancel Query';
    } else {
        // Clear the query results display
        queryDataContainer.innerHTML = '';
        // Hide the query results header
        queryResultsHeader.style.display = 'none';
        // Change the query button text to 'Query'
        queryBtn.textContent = 'Query';
    }
});

// Function to handle button click event for viewing all data and toggling hide/show
document.getElementById('viewDataBtn').addEventListener('click', async function() {
    // Define the API endpoint URL for fetching all items
    const apiUrl = 'https://example.execute-api.us-east-1.amazonaws.com/v1/items';
    // Get the view data container element
    const viewDataContainer = document.getElementById('viewDataContainer');
    // Get the all items header element
    const allItemsHeader = document.getElementById('allItemsHeader');
    // Get the view data button element
    const button = document.getElementById('viewDataBtn');

    // Check if the button text is 'View Items'
    if (button.textContent === 'View Items') {
        // Fetch all data items
        const data = await getData(apiUrl);
        // Display all data items
        displayData(data, 'viewDataContainer');
        // Show the all items header
        allItemsHeader.style.display = 'block';
        // Change the button text to 'Hide Items'
        button.textContent = 'Hide Items';
    } else {
        // Clear the data display
        viewDataContainer.innerHTML = '';
        // Hide the all items header
        allItemsHeader.style.display = 'none';
        // Change the button text to 'View Items'
        button.textContent = 'View Items';
    }
});
