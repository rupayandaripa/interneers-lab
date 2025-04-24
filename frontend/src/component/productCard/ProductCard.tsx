import React, { useState } from 'react';
import './ProductCard.css';
import { Product } from 'Product.types';

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [expanded , setExpanded] = useState(false)

  const toggleCard = () => {
    setExpanded(prev => !prev)
  }
  return (

    <div className={`product-card ${expanded ? 'expanded' : ''}`}
    onClick={toggleCard}>
      <h3>{product.name}</h3>
      <p className="product-price">${product.price}</p>
      <p className="product-description">{product.description}</p>
      <p className="product-category">{product.category}</p>
      <p className="product-brand">{product.brand}</p>
    </div>
  );
};

export default ProductCard;
