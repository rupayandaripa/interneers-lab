import React from 'react';
import ProductList from './ProductList';
import './App.css';
import Header from 'Header';
import { BrowserRouter as Router , Routes , Route } from 'react-router-dom';
import HomePage from 'HomePage';
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

