<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frappe REST API Example</title>
</head>
<body>
    <h1>Items</h1>
    <ul id="items"></ul>

    <script>
        // Function to fetch items using the Frappe REST API
        function fetchItems() {
            fetch('http://erpnext.sictadau/api/method/voicebank.www.jinja.search', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': '6fbf08c1e07946d'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const items = document.getElementById('items');
                data.data.forEach(item => {
                    const li = document.createElement('li');
                    li.textContent = item.name + ': ' + item.description;
                    items.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error fetching items:', error);
            });
        }

        // Call the fetchItems function when the page loads
        fetchItems();
    </script>
</body>
</html>
