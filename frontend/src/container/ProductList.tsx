import React, { useEffect, useState } from 'react';
import ProductCard from '../component/productCard/ProductCard';
import { Product } from 'Product.types';
import Spinner from 'component/spinner/Spinner';

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

  if(loading) return <Spinner />
  return (
    <div className="product-list">
      {products.map(product => (
        <ProductCard key={product.product_id} product={product} />
      ))}
    </div>
  );
};

export default ProductList;
