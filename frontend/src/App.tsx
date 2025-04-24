import React from 'react';
import ProductList from './container/ProductList';
import './App.css';
import Header from 'component/header/Header';
import HomePage from 'HomePage';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import CategoryPage from 'CategoryPage';

const App: React.FC = () => {
  return (
    <Router>
      <div className='app'>
      <Header />
      <main style = {{padding: '20px'}}>
        <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/category/:categoryId" element={<CategoryPage/>}/>
        </Routes>
      </main>
      </div>
    </Router>
  );
};

export default App;

