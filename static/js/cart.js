// Declare shoppingCart in the global scope and retrieve data from localStorage on page load
let shoppingCart = JSON.parse(localStorage.getItem('shoppingCart')) || [];

// Declare the updateCart function
function updateCart() {
    const modal = document.querySelector('#cartModal .modal-body');
    modal.innerHTML = '';

    if (shoppingCart.length === 0) {
        modal.innerHTML = '<p>Cart is empty... add something!</p>';
    } else {
        let totalPrice = 0;

        for (const item of shoppingCart) {
            modal.innerHTML += `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                    <div class="cart-item-details">
                        <p>Name: ${item.name}</p>
                        <p>Price: $${item.price}</p>
                        <p>Quantity: ${item.quantity}</p>
                        <button type="button" class="btn btn-danger remove-btn" onclick="removeItem('${item.id}')">Remove</button>
                        <hr>
                    </div>
                </div>`;

            totalPrice += item.price * item.quantity;
        }

        // Display total price at the bottom
        modal.innerHTML += `<p>Total Price: $${totalPrice.toFixed(2)}</p>`;
    }

    // Save the updated shopping cart to localStorage
    localStorage.setItem('shoppingCart', JSON.stringify(shoppingCart));
}

document.addEventListener('DOMContentLoaded', () => {
    const addToCartButton = document.getElementById('addToCartBtn');

    addToCartButton.addEventListener('click', () => {
        const productId = addToCartButton.getAttribute('data-product-id');
        const existingItem = shoppingCart.find(item => item.id === productId);

        if (existingItem) {
            // If the item already exists in the cart, increment the quantity
            existingItem.quantity++;
        } else {
            // If the item is not in the cart, add a new item
            const productName = addToCartButton.getAttribute('data-product-name');
            const productImage = addToCartButton.getAttribute('data-product-image');
            const productDescription = addToCartButton.getAttribute('data-product-description');
            const productPrice = addToCartButton.getAttribute('data-product-price');
            const productRating = addToCartButton.getAttribute('data-product-rating');

            // Create a cart item object
            const cartItem = {
                id: productId,
                name: productName,
                image: productImage,
                description: productDescription,
                price: parseFloat(productPrice),
                rating: parseInt(productRating),
                quantity: 1,
            };

            // Append the cart item to the shopping cart array
            shoppingCart.push(cartItem);
        }

        // Log the updated shopping cart (you can remove this in production)
        console.log(shoppingCart);

        // Update the cart display
        updateCart();
    });
});

// Declare the removeItem function
function removeItem(productId) {
    // Find the item with the given productId
    const existingItem = shoppingCart.find(item => item.id === productId);
    if (existingItem) {
        // If the item exists in the cart and has a quantity greater than 1, decrease it by 1
        if (existingItem.quantity > 1) {
            existingItem.quantity -= 1;
        } else {
            // If quantity is 1, remove the item from the cart
            const index = shoppingCart.findIndex(item => item.id === productId);
            shoppingCart.splice(index, 1);
        }

        // Update the cart display
        updateCart();
    }
}
