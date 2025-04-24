import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  const categories = ['Electronics', 'Fashion', 'Groceries', 'Lifestyle'];

  return (
    <div>
      <h2 className="sidebar-title">Categories</h2>
      <ul className="sidebar-list">
        {categories.map((cat) => (
          <li key={cat}>
            <Link to={`/category/${cat}`} className="sidebar-link">
              {cat}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;

