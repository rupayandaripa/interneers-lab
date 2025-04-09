import React from 'react';
import ProductList from './ProductList';
import './App.css';
import Header from 'Header';

const App: React.FC = () => {
  return (
    <div className='app'>
      <Header />
      <main style = {{padding: '20px'}}>
      <ProductList />
      </main>
      </div>
  );
};

export default App;

