import React from 'react';
import ProductList from './container/ProductList';
import './App.css';
import Header from 'component/header/Header';

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

