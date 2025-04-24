import React from "react";

const Header: React.FC = () => {
    return (
        <>
        <header className="header">
            <div className="logo">
                MyStore
            </div>
            <nav className="nav">
                <a href = '/'>Home</a>
                <a href = "/products">Products</a>
                <a href = "/contact">Contact</a>
            </nav>
        </header>
        </>
    );
}

export default Header