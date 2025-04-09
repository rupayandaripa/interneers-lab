const url = 'http://127.0.0.1:8000/products/1/'

async function fetchProductData() {
    try {
        const response = await fetch(url)

        if(!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }

        const data = await response.json()

        const productList = document.getElementById('product-list')
        productList.innerHTML = ""

        data.products.forEach(product => {
            const productTile = document.createElement("div")
            productTile.classList.add("product-tile")

            productTile.innerHTML = `
                <h2 class='product-name'>${product['name']}</h2>
                <p class="product-description">${product.description}</p>
                <p class="product-price">$${product.price}</p>
                <p class="product-category">Category: ${product.category}</p>
                <p class="product-brand">Brand: ${product.brand}</p>
                `

            productList.appendChild(productTile)
        })
    }
    catch (error) {
        console.error("Error fetching product data:", error)
    }
}

fetchProductData()