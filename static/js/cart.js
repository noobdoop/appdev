document.addEventListener('DOMContentLoaded', () => {
    const addToCartButton = document.getElementById('addToCartBtn');
    const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
    const modalBody = document.querySelector('#cartModal .modal-body');

    addToCartButton.addEventListener('click', () => {
        fetch('/get_products') // Replace with the appropriate endpoint to get product details
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(productData => {
                // Assuming productData contains the fetched product details
                const { name, price, description } = productData;

                // Construct HTML to display product details in the modal
                const productDetailsHTML = `
                    <p><strong>Name:</strong> ${name}test</p>
                    <p><strong>Price:</strong> $${price}</p>
                    <p><strong>Description:</strong> ${description}</p>
                    <!-- Add other relevant product details -->
                `;

                // Set the content of the modal's body to the product details HTML
                modalBody.innerHTML = productDetailsHTML;

                // Show the cart modal
                cartModal.show();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
