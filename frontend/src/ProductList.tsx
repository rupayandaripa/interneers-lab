import React, { useEffect, useState } from 'react';
import ProductCard from './ProductCard';
import { Product } from 'Product';

// const dummyProducts: Product[] = [
//   {
//     id: 1,
//     name: 'Wireless Headphones',
//     price: 59.99,
//     description: 'High-quality sound with noise cancellation.',
//     category: 'Electronics',
//     brand: 'Boat'
//   },
//   {
//     id: 2,
//     name: 'Smart Watch',
//     price: 89.99,
//     description: 'Track your fitness and notifications on the go.',
//     category: 'Electronics',
//     brand: 'Realme'
//   },
//   {
//     id: 3,
//     name: 'Bluetooth Speaker',
//     price: 39.99,
//     description: 'Compact size, powerful sound.',
//     category: 'Electronics',
//     brand: 'Bose'
//   },
// ];

const url = 'http://127.0.0.1:8000/products/1/'


const ProductList: React.FC = () => {
  const [products , setProducts] = useState<Product[]>([])
  const [loading , setLoading] = useState(true)

  useEffect(() => {
    const fetchProducts = async () => {
      try {

        if (!url) {
          throw new Error("Missing API URL. Please check your environment variables.");
        }

        const response = await fetch(url)
        console.log("Fetch URL:", url, "Response:", response);

        if(!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
        }

        const data = await response.json()
        console.log(data)
        setProducts(data.products)

    }
    catch(error) {
        console.error("Error fetching product data:", error)
    }
    finally{
      setLoading(false)
    }
    }

    fetchProducts()
  } , [])

  if(loading) return <p>Loading Products....</p>
  return (
    <div className="product-list">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

export default ProductList;
