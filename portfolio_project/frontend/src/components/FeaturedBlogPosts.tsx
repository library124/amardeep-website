'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string | null;
  author_name: string;
  category_name: string;
  publish_date: string;
  reading_time: number;
  is_featured: boolean;
}

const FeaturedBlogPosts: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedPosts();
  }, []);

  const fetchFeaturedPosts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/blog/featured/');
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('Error fetching featured posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-white rounded-xl shadow-lg overflow-hidden animate-pulse">
            <div className="h-48 bg-gray-200"></div>
            <div className="p-6">
              <div className="h-4 bg-gray-200 rounded mb-2"></div>
              <div className="h-6 bg-gray-200 rounded mb-3"></div>
              <div className="h-4 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No featured posts available at the moment.</p>
        <Link href="/blog" className="text-blue-600 hover:text-blue-700 font-medium mt-2 inline-block">
          View All Posts →
        </Link>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {posts.map((post) => (
        <article key={post.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow group">
          {post.featured_image ? (
            <div className="relative h-48 overflow-hidden">
              <Image
                src={post.featured_image}
                alt={post.title}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
              />
            </div>
          ) : (
            <div className="h-48 bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
              <span className="text-4xl text-blue-600">📈</span>
            </div>
          )}
          
          <div className="p-6">
            <div className="flex items-center text-sm text-gray-500 mb-2">
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                {post.category_name}
              </span>
              <span className="mx-2">•</span>
              <span>{formatDate(post.publish_date)}</span>
            </div>

            <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors">
              <Link href={`/blog/${post.slug}`}>
                {post.title}
              </Link>
            </h3>

            <p className="text-gray-600 mb-4 line-clamp-3 text-sm leading-relaxed">
              {post.excerpt}
            </p>

            <div className="flex items-center justify-between">
              <div className="flex items-center text-sm text-gray-500">
                <span>{post.reading_time} min read</span>
              </div>
              
              <Link
                href={`/blog/${post.slug}`}
                className="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
              >
                Read More →
              </Link>
            </div>
          </div>
        </article>
      ))}
      
      {/* View All Posts Link */}
      <div className="lg:col-span-3 text-center mt-8">
        <Link
          href="/blog"
          className="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
        >
          View All Blog Posts
          <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default FeaturedBlogPosts;