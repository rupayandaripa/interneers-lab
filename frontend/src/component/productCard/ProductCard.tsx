import React, { useState , useEffect} from 'react';
import './ProductCard.css';
import { Product } from 'Product.types';

interface ProductCardProps {
  product: Product;
}

const availableCategories = ["Electronics" , "Fashion" , "Groceries" , "Lifestyle"]

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [expanded , setExpanded] = useState(false)
  const [editMode , seteditMode] = useState(false)
  const [editedProduct , setEditedProduct] = useState<Product>(product)
  const [originalCategories, setOriginalCategories] = useState<string[]>(product.category);
  const [message , setMessage] = useState<{type: 'success' | 'error'; text: string} | null>(null)


  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => setMessage(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);
  

  const toggleCard = () => {
    setExpanded(prev => !prev)
  }

  const toggleCategory = (category: string) => {
    if(!editMode) return ;

    setEditedProduct((prev) => {
      const isSelected = prev.category.includes(category)
      const newCategories = isSelected ? prev.category.filter((cat) => cat !== category) : [...prev.category , category]

      return {
        ...prev,
        category: newCategories
      }
    })
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const {name , value} = e.target;
    setEditedProduct(prev => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSave = async () => {
    try {
      const { _id , product_id, category, created_at , updated_at, ...updatableFields } = editedProduct;

      console.log("Cleaned payload:", updatableFields);
      const response = await fetch(`http://127.0.0.1:8000/products/update/${product.product_id}/` , {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatableFields)
      })

      const categoriesToAdd = editedProduct.category.filter(cat => !originalCategories.includes(cat))
      const categoriesToRemove = originalCategories.filter(cat => !editedProduct.category.includes(cat))

      for (const cat of categoriesToAdd) {
        const res = await fetch(`http://127.0.0.1:8000/products/add/${product.product_id}/${cat}/` , {
          method: 'PUT'
        })
        if (!res.ok) {
          setMessage({ type: 'error', text: `Failed to add category: ${cat}` });
          return;
        }
      }

      for(const cat of categoriesToRemove) {
        const res = await fetch(`http://127.0.0.1:8000/products/delete/${product.product_id}/${cat}/` , {
          method: 'DELETE',
        }) 
        if (!res.ok) {
          setMessage({ type: 'error', text: `Failed to remove category: ${cat}` });
          return;
        }
      }

      const responseBody = await response.json()
      console.log("Backend response: " , responseBody)

      if(!response.ok) {
        setMessage({type: 'error' , text: 'Failed to update product info'})
        throw new Error('Failed to update product')
      }

      setMessage({ type: 'success', text: 'Product updated successfully!' });
      seteditMode(false)
      setTimeout(() => window.location.reload() , 1000)
    }
    catch(error) {
      console.error("Failed to update product" , error)
    }
  }
  return (
    
    <>
    {message && (
      <div className={`message ${message.type}`}>
        {message.text}
      </div>
    )}

    <div className={`product-card ${expanded ? 'expanded' : ''}`}
    onClick={toggleCard}>
      {editMode ? (
        <>
          <input name="name" value={editedProduct.name} onChange={handleChange} />
          <input name="price" value={editedProduct.price} type="number" onChange={handleChange} />
          <textarea name="description" value={editedProduct.description} onChange={handleChange} />

          <div className="category-toggle-group">
            {availableCategories.map((cat) => (
              <button
                key={cat}
                type="button"
                className={`category-button ${editedProduct.category.includes(cat) ? 'selected' : ''}`}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleCategory(cat);
                }}
              >
            {cat}
          </button>
        ))}
      </div>

          <input name="brand" value={editedProduct.brand} onChange={handleChange} />
          <button onClick={(e) => { e.stopPropagation(); handleSave(); }}>Save</button>
        </>
      ) : (
        <>
        <h3>{product.name}</h3>
        <p className="product-price">${product.price}</p>
        <p className="product-description">{product.description}</p>
        <p className="product-category">{product.category.join(", ")}</p>
        <p className="product-brand">{product.brand}</p>
        <button onClick={(e) => {e.stopPropagation(); seteditMode(true)}}>Edit</button>
        </>
      )}
      
    </div>
    </>
    
  );
};

export default ProductCard;
