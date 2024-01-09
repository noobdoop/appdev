document.addEventListener('DOMContentLoaded', () => {
    let products = []; // Define products array
    let originalProducts = []; // Store the original products array

    // Function to change sort option
    function changeSort(selectedOption) {
        document.getElementById('selectedSort').innerText = selectedOption;

        if (selectedOption === 'Price (Low to High)') {
            // Sort products by ascending price
            products.sort((a, b) => a.price - b.price);
            displayProducts(products); // Display sorted products
        } else if (selectedOption === 'Price (High to Low)') {
            // Sort products by descending price
            products.sort((a, b) => b.price - a.price);
            displayProducts(products); // Display sorted products
        } else if (selectedOption === 'Name (A-Z)') {
            // Sort products by name in ascending order
            products.sort((a, b) => a.name.localeCompare(b.name));
            displayProducts(products); // Display sorted products
        } else if (selectedOption === 'Name (Z-A)') {
            // Sort products by name in descending order
            products.sort((a, b) => b.name.localeCompare(a.name));
            displayProducts(products); // Display sorted products
        } else if (selectedOption === 'Default') {
            // Reset to original arrangement
            products = [...originalProducts];
            displayProducts(products); // Display original products
        }
    }

    function displayProducts(productsArray) {
        // Get the element where you want to display products
        const productContainer = document.querySelector('.productrow .row');
        productContainer.innerHTML = ''; // Clear the existing content

        productsArray.forEach(product => {
            // Create HTML elements for each product
            const productDiv = document.createElement('div');
            productDiv.classList.add('col-3');
            productDiv.innerHTML = `
                <div class="image-box">
                    <a href="/productpage/${product.name.replace(/\s/g, '-').toLowerCase()}">
                        <p class="name">${product.name}</p>
                        <img src="${product.image_url}" alt="${product.name}">
                        <p class="price">$${product.price}</p>
                        <div class="rating">
                            ${'<span class="fa fa-star checked"></span>'.repeat(product.rating)}
                        </div>
                    </a>
                </div>`;
            productContainer.appendChild(productDiv); // Append product to container
        });
    }


    // Function to handle the search functionality
    function handleSearch(query) {
        const filteredProducts = products.filter(product =>
            product.name.toLowerCase().includes(query.toLowerCase())
        );

        displayProducts(filteredProducts); // Display filtered products
    }

    // Call changeSort function on option click
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', () => {
            changeSort(item.innerText); // Pass the selected option text
        });
    });

    // Handle form submission for search
    const searchForm = document.querySelector('.searchbar form');
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        const searchQuery = searchForm.querySelector('input[name="query"]').value.trim();
        handleSearch(searchQuery); // Call the search functionality
    });

    // Fetch products from Flask backend
    fetch('/get_products')
        .then(response => response.json())
        .then(data => {
            // Store retrieved products in the 'products' and 'originalProducts' array
            products = data;
            originalProducts = [...data];
            displayProducts(products); // Display initial products
        })
        .catch(error => console.error('Error:', error));
});