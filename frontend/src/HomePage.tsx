// HomePage.tsx
import React from 'react';
import Sidebar from './component/sidebar/Sidebar';
import ProductList from 'container/ProductList';
import './HomePage.css';

const HomePage: React.FC = () => {
  return (
    <div className="home-layout">
      <aside className="sidebar">
        <Sidebar />
      </aside>
      <main className="product-list">
        <ProductList />
      </main>
    </div>
  );
};

export default HomePage;

