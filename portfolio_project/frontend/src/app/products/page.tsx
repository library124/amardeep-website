'use client';

import React, { useEffect, useState } from 'react';
import api from '../../utils/api';
import { Product } from '../../types';

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await api.get('/products/'); // Assuming Django API endpoint for products
        setProducts(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch products.');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return <div className="container mx-auto p-8 text-center">Loading products...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-8 text-center text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Digital Products</h1>
      {products.length === 0 ? (
        <p className="text-lg text-gray-600">No products found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold mb-2">{product.name}</h2>
              <p className="text-gray-700 mb-2">{product.description}</p>
              <p className="text-gray-900 font-bold mb-4">${parseFloat(product.price.toString()).toFixed(2)}</p>
              <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                Purchase / Download
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductsPage;