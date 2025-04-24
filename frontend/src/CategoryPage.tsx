import React, { useEffect , useState} from 'react';
import { useParams } from 'react-router-dom';
import ProductList from './container/ProductList';
import Sidebar from 'component/sidebar/Sidebar';
import { Product } from 'Product.types';
import ProductCard from 'component/productCard/ProductCard';
import Spinner from 'component/spinner/Spinner';


const CategoryPage: React.FC = () => {
  const { categoryId } = useParams();
  const [products , setProducts] = useState<Product[]>([])
  const [loading , setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log(categoryId)
        const response = await fetch(`http://127.0.0.1:8000/products/category/${categoryId}/`)
        const data = await response.json()
        console.log(data['product'])
        setProducts(data['product'])
      } catch (error) {
        console.error('Error fetching data:', error);
      }
      finally{
        setLoading(false)
      }
    };

    fetchData();
  }, [categoryId]);

  if(loading) return <Spinner />
  return (
    
    <div className="home-layout">
      <aside className="sidebar">
        <Sidebar />
      </aside>
      <main className="product-list">
      {products.map(product => (
        <ProductCard key={product.product_id} product={product} />
      ))}
      </main>
    </div>
   
  );
};

export default CategoryPage;
