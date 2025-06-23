'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string | null;
  author_name: string;
  category_name: string;
  tags: Array<{ name: string; slug: string }>;
  publish_date: string;
  reading_time: number;
  views_count: number;
  is_featured: boolean;
}

interface Category {
  id: number;
  name: string;
  slug: string;
  post_count: number;
}

const BlogPage: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  useEffect(() => {
    fetchPosts();
    fetchCategories();
  }, [selectedCategory]);

  const fetchPosts = async () => {
    try {
      const url = selectedCategory 
        ? `http://localhost:8000/api/blog/?category=${selectedCategory}`
        : 'http://localhost:8000/api/blog/';
      
      const response = await fetch(url);
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('Error fetching posts:', error);
      // Fallback to demo data
      setDemoPosts();
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/blog/categories/');
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
      // Fallback to demo categories
      setCategories([
        { id: 1, name: 'Trading Strategy', slug: 'trading-strategy', post_count: 12 },
        { id: 2, name: 'Market Analysis', slug: 'market-analysis', post_count: 8 },
        { id: 3, name: 'Risk Management', slug: 'risk-management', post_count: 6 },
        { id: 4, name: 'Technical Analysis', slug: 'technical-analysis', post_count: 10 },
      ]);
    }
  };

  const setDemoPosts = () => {
    const demoPosts: BlogPost[] = [
      {
        id: 1,
        title: "Advanced Intraday Trading Strategies for Consistent Profits",
        slug: "advanced-intraday-trading-strategies",
        excerpt: "Discover proven intraday trading techniques that can help you maximize profits while minimizing risks. Learn about technical indicators, market timing, and risk management strategies used by professional traders.",
        featured_image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop",
        author_name: "Amardeep Asode",
        category_name: "Trading Strategy",
        tags: [{ name: "Intraday", slug: "intraday" }, { name: "Strategy", slug: "strategy" }],
        publish_date: "2024-01-15",
        reading_time: 8,
        views_count: 1250,
        is_featured: true
      },
      {
        id: 2,
        title: "Market Analysis: Key Indicators to Watch This Week",
        slug: "market-analysis-key-indicators",
        excerpt: "Stay ahead of market movements with our weekly analysis. We break down the most important economic indicators and market signals that every trader should monitor.",
        featured_image: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&h=600&fit=crop",
        author_name: "Amardeep Asode",
        category_name: "Market Analysis",
        tags: [{ name: "Analysis", slug: "analysis" }, { name: "Indicators", slug: "indicators" }],
        publish_date: "2024-01-12",
        reading_time: 5,
        views_count: 890,
        is_featured: false
      },
      {
        id: 3,
        title: "Risk Management: Protecting Your Trading Capital",
        slug: "risk-management-trading-capital",
        excerpt: "Learn essential risk management techniques that separate successful traders from the rest. Discover position sizing, stop-loss strategies, and portfolio diversification methods.",
        featured_image: "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=800&h=600&fit=crop",
        author_name: "Amardeep Asode",
        category_name: "Risk Management",
        tags: [{ name: "Risk", slug: "risk" }, { name: "Capital", slug: "capital" }],
        publish_date: "2024-01-10",
        reading_time: 6,
        views_count: 1100,
        is_featured: false
      },
      {
        id: 4,
        title: "Technical Analysis Masterclass: Reading Chart Patterns",
        slug: "technical-analysis-chart-patterns",
        excerpt: "Master the art of reading chart patterns with this comprehensive guide. Learn to identify support and resistance levels, trend lines, and reversal patterns.",
        featured_image: "https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=800&h=600&fit=crop",
        author_name: "Amardeep Asode",
        category_name: "Technical Analysis",
        tags: [{ name: "Charts", slug: "charts" }, { name: "Patterns", slug: "patterns" }],
        publish_date: "2024-01-08",
        reading_time: 10,
        views_count: 1450,
        is_featured: false
      },
      {
        id: 5,
        title: "Options Trading Strategies for Beginners",
        slug: "options-trading-strategies-beginners",
        excerpt: "Get started with options trading using these beginner-friendly strategies. Learn about calls, puts, and basic option strategies to enhance your trading portfolio.",
        featured_image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
        author_name: "Amardeep Asode",
        category_name: "Trading Strategy",
        tags: [{ name: "Options", slug: "options" }, { name: "Beginners", slug: "beginners" }],
        publish_date: "2024-01-05",
        reading_time: 7,
        views_count: 980,
        is_featured: false
      }
    ];
    setPosts(demoPosts);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const featuredPost = posts.find(post => post.is_featured) || posts[0];
  const regularPosts = posts.filter(post => !post.is_featured || post.id !== featuredPost?.id);

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        {/* Loading Header */}
        <div className="bg-white border-b border-gray-100">
          <div className="container mx-auto px-6 py-16">
            <div className="max-w-4xl mx-auto text-center">
              <div className="h-12 bg-gray-200 rounded-lg w-80 mx-auto mb-4 animate-pulse"></div>
              <div className="h-6 bg-gray-200 rounded w-96 mx-auto animate-pulse"></div>
            </div>
          </div>
        </div>
        
        {/* Loading Content */}
        <div className="container mx-auto px-6 py-16">
          <div className="max-w-6xl mx-auto">
            {/* Loading Categories */}
            <div className="flex flex-wrap gap-3 mb-12">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="h-10 bg-gray-200 rounded-full w-24 animate-pulse"></div>
              ))}
            </div>
            
            {/* Loading Posts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
              <div className="lg:col-span-2 animate-pulse">
                <div className="bg-gray-200 rounded-2xl aspect-video mb-6"></div>
                <div className="h-8 bg-gray-200 rounded mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
              </div>
              {[1, 2].map((i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 rounded-2xl aspect-video mb-4"></div>
                  <div className="h-6 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Modern Hero Section */}
      <section className="bg-white border-b border-gray-100">
        <div className="container mx-auto px-6 py-16">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 tracking-tight">
              Trading Insights
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed max-w-2xl mx-auto">
              Expert analysis, proven strategies, and market insights to help you succeed in trading. 
              Learn from 5+ years of professional trading experience.
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-6 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Modern Category Filter */}
          <div className="flex flex-wrap gap-3 mb-12">
            <button
              onClick={() => setSelectedCategory('')}
              className={`px-6 py-3 rounded-full text-sm font-medium transition-all duration-200 ${
                selectedCategory === '' 
                  ? 'bg-gray-900 text-white shadow-lg' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              All Articles
            </button>
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.slug)}
                className={`px-6 py-3 rounded-full text-sm font-medium transition-all duration-200 ${
                  selectedCategory === category.slug 
                    ? 'bg-gray-900 text-white shadow-lg' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {category.name}
                <span className="ml-2 text-xs opacity-75">({category.post_count})</span>
              </button>
            ))}
          </div>

          {/* Featured Article + Grid Layout */}
          {featuredPost && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
              {/* Featured Article - Large */}
              <Link 
                href={`/blog/${featuredPost.slug}`}
                className="lg:col-span-2 group cursor-pointer"
              >
                <article className="relative overflow-hidden rounded-2xl bg-white border border-gray-100 hover:border-gray-200 transition-all duration-300 hover:shadow-xl">
                  <div className="relative aspect-video overflow-hidden">
                    {featuredPost.featured_image ? (
                      <Image
                        src={featuredPost.featured_image}
                        alt={featuredPost.title}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                        <span className="text-6xl text-blue-600">📈</span>
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  
                  <div className="p-8">
                    <div className="flex items-center gap-4 mb-4">
                      <Badge className="bg-blue-600 hover:bg-blue-700 text-white">
                        Featured
                      </Badge>
                      <Badge variant="secondary">
                        {featuredPost.category_name}
                      </Badge>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <Avatar className="h-6 w-6">
                          <AvatarImage src="/owner_landing_page.jpg" />
                          <AvatarFallback>AA</AvatarFallback>
                        </Avatar>
                        <span>{featuredPost.author_name}</span>
                        <span>•</span>
                        <span>{formatDate(featuredPost.publish_date)}</span>
                      </div>
                    </div>
                    
                    <h2 className="text-3xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors line-clamp-2">
                      {featuredPost.title}
                    </h2>
                    
                    <p className="text-gray-600 text-lg leading-relaxed mb-6 line-clamp-3">
                      {featuredPost.excerpt}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span>{featuredPost.reading_time} min read</span>
                        <span>•</span>
                        <span>{featuredPost.views_count} views</span>
                      </div>
                      <span className="text-blue-600 font-medium group-hover:text-blue-700 transition-colors">
                        Read Article →
                      </span>
                    </div>
                  </div>
                </article>
              </Link>

              {/* Regular Articles - Grid */}
              {regularPosts.slice(0, 2).map((post) => (
                <Link 
                  key={post.id}
                  href={`/blog/${post.slug}`}
                  className="group cursor-pointer"
                >
                  <article className="relative overflow-hidden rounded-2xl bg-white border border-gray-100 hover:border-gray-200 transition-all duration-300 hover:shadow-lg h-full">
                    <div className="relative aspect-video overflow-hidden">
                      {post.featured_image ? (
                        <Image
                          src={post.featured_image}
                          alt={post.title}
                          fill
                          className="object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                          <span className="text-4xl text-blue-600">📊</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="p-6">
                      <div className="flex items-center gap-3 mb-3">
                        <Badge variant="secondary" className="text-xs">
                          {post.category_name}
                        </Badge>
                        <div className="flex items-center gap-2 text-xs text-gray-500">
                          <Avatar className="h-5 w-5">
                            <AvatarImage src="/owner_landing_page.jpg" />
                            <AvatarFallback>AA</AvatarFallback>
                          </Avatar>
                          <span>{post.author_name}</span>
                        </div>
                      </div>
                      
                      <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors line-clamp-2">
                        {post.title}
                      </h3>
                      
                      <p className="text-gray-600 leading-relaxed mb-4 line-clamp-3 text-sm">
                        {post.excerpt}
                      </p>
                      
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <div className="flex items-center gap-2">
                          <span>{formatDate(post.publish_date)}</span>
                          <span>•</span>
                          <span>{post.reading_time} min read</span>
                        </div>
                        <span className="text-blue-600 font-medium group-hover:text-blue-700 transition-colors">
                          Read →
                        </span>
                      </div>
                    </div>
                  </article>
                </Link>
              ))}
            </div>
          )}

          {/* Additional Articles Grid */}
          {regularPosts.length > 2 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {regularPosts.slice(2).map((post) => (
                <Link 
                  key={post.id}
                  href={`/blog/${post.slug}`}
                  className="group cursor-pointer"
                >
                  <article className="relative overflow-hidden rounded-xl bg-white border border-gray-100 hover:border-gray-200 transition-all duration-300 hover:shadow-lg h-full">
                    <div className="relative aspect-video overflow-hidden">
                      {post.featured_image ? (
                        <Image
                          src={post.featured_image}
                          alt={post.title}
                          fill
                          className="object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                          <span className="text-3xl text-blue-600">📈</span>
                        </div>
                      )}
                    </div>
                    
                    <div className="p-5">
                      <div className="flex items-center gap-2 mb-3">
                        <Badge variant="secondary" className="text-xs">
                          {post.category_name}
                        </Badge>
                      </div>
                      
                      <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">
                        {post.title}
                      </h3>
                      
                      <p className="text-gray-600 text-sm leading-relaxed mb-3 line-clamp-2">
                        {post.excerpt}
                      </p>
                      
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{formatDate(post.publish_date)}</span>
                        <span>{post.reading_time} min read</span>
                      </div>
                    </div>
                  </article>
                </Link>
              ))}
            </div>
          )}

          {/* Empty State */}
          {posts.length === 0 && (
            <div className="text-center py-16">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-4xl text-gray-400">📝</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">No articles found</h3>
              <p className="text-gray-600 max-w-md mx-auto">
                {selectedCategory 
                  ? 'No articles in this category yet. Try browsing other categories or check back later.' 
                  : 'No blog posts available at the moment. Check back soon for trading insights and market analysis.'}
              </p>
              {selectedCategory && (
                <button
                  onClick={() => setSelectedCategory('')}
                  className="mt-6 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  View All Articles
                </button>
              )}
            </div>
          )}

          {/* Newsletter CTA */}
          <div className="mt-20 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-8 md:p-12 text-center">
            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
              Stay Updated with Trading Insights
            </h3>
            <p className="text-gray-600 text-lg mb-8 max-w-2xl mx-auto">
              Get weekly market analysis, trading strategies, and exclusive insights delivered directly to your inbox.
            </p>
            <Link
              href="/#newsletter"
              className="inline-flex items-center px-8 py-4 bg-gray-900 text-white font-semibold rounded-lg hover:bg-gray-800 transition-colors"
            >
              Subscribe to Newsletter
              <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogPage;