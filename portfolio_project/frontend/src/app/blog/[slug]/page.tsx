'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';

interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  featured_image: string | null;
  author_name: string;
  category: {
    name: string;
    slug: string;
  };
  tags: Array<{ name: string; slug: string }>;
  publish_date: string;
  updated_at: string;
  reading_time: number;
  views_count: number;
  meta_title: string;
  meta_description: string;
  related_posts: Array<{
    id: number;
    title: string;
    slug: string;
    excerpt: string;
    featured_image: string | null;
    publish_date: string;
    reading_time: number;
  }>;
}

const BlogPostPage: React.FC = () => {
  const params = useParams();
  const slug = params.slug as string;
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (slug) {
      fetchPost();
    }
  }, [slug]);

  const fetchPost = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/blog/post/${slug}/`);
      if (response.ok) {
        const data = await response.json();
        setPost(data);
      } else {
        setError('Post not found');
      }
    } catch (error) {
      setError('Error loading post');
      console.error('Error fetching post:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const sharePost = (platform: string) => {
    const url = window.location.href;
    const title = post?.title || '';
    
    let shareUrl = '';
    switch (platform) {
      case 'twitter':
        shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}&url=${encodeURIComponent(url)}`;
        break;
      case 'facebook':
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
        break;
      case 'linkedin':
        shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
        break;
      case 'whatsapp':
        shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
        break;
    }
    
    if (shareUrl) {
      window.open(shareUrl, '_blank', 'width=600,height=400');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Post Not Found</h1>
          <p className="text-gray-600 mb-6">The blog post you're looking for doesn't exist.</p>
          <Link href="/blog" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors">
            Back to Blog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Breadcrumb */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4">
          <nav className="text-sm">
            <Link href="/" className="text-blue-600 hover:text-blue-700">Home</Link>
            <span className="mx-2 text-gray-500">/</span>
            <Link href="/blog" className="text-blue-600 hover:text-blue-700">Blog</Link>
            <span className="mx-2 text-gray-500">/</span>
            <span className="text-gray-700">{post.title}</span>
          </nav>
        </div>
      </div>

      <article className="container mx-auto px-6 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Post Header */}
          <header className="mb-8">
            <div className="flex items-center text-sm text-gray-500 mb-4">
              <Link href={`/blog?category=${post.category.slug}`} className="text-blue-600 hover:text-blue-700">
                {post.category.name}
              </Link>
              <span className="mx-2">•</span>
              <span>{formatDate(post.publish_date)}</span>
              <span className="mx-2">•</span>
              <span>{post.reading_time} min read</span>
              <span className="mx-2">•</span>
              <span>{post.views_count} views</span>
            </div>

            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6 leading-tight">
              {post.title}
            </h1>

            <p className="text-xl text-gray-600 mb-6 leading-relaxed">
              {post.excerpt}
            </p>

            <div className="flex items-center justify-between border-b pb-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                  <span className="text-lg">👤</span>
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{post.author_name}</p>
                  <p className="text-gray-600 text-sm">Stock & Intraday Trader</p>
                </div>
              </div>

              {/* Share Buttons */}
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600 mr-2">Share:</span>
                <button
                  onClick={() => sharePost('twitter')}
                  className="p-2 bg-blue-400 text-white rounded hover:bg-blue-500 transition-colors"
                  title="Share on Twitter"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                  </svg>
                </button>
                <button
                  onClick={() => sharePost('facebook')}
                  className="p-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  title="Share on Facebook"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                </button>
                <button
                  onClick={() => sharePost('linkedin')}
                  className="p-2 bg-blue-700 text-white rounded hover:bg-blue-800 transition-colors"
                  title="Share on LinkedIn"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                </button>
                <button
                  onClick={() => sharePost('whatsapp')}
                  className="p-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
                  title="Share on WhatsApp"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.085"/>
                  </svg>
                </button>
              </div>
            </div>
          </header>

          {/* Featured Image */}
          {post.featured_image && (
            <div className="mb-8">
              <Image
                src={post.featured_image}
                alt={post.title}
                width={800}
                height={400}
                className="w-full h-64 lg:h-96 object-cover rounded-xl"
              />
            </div>
          )}

          {/* Post Content */}
          <div className="prose prose-lg max-w-none mb-12">
            <div 
              dangerouslySetInnerHTML={{ __html: post.content }}
              className="text-gray-800 leading-relaxed"
            />
          </div>

          {/* Tags */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <span
                  key={tag.slug}
                  className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                >
                  {tag.name}
                </span>
              ))}
            </div>
          </div>

          {/* Related Posts */}
          {post.related_posts.length > 0 && (
            <div className="border-t pt-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Related Posts</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {post.related_posts.map((relatedPost) => (
                  <article key={relatedPost.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                    {relatedPost.featured_image && (
                      <Image
                        src={relatedPost.featured_image}
                        alt={relatedPost.title}
                        width={300}
                        height={200}
                        className="w-full h-48 object-cover"
                      />
                    )}
                    <div className="p-4">
                      <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                        <Link href={`/blog/${relatedPost.slug}`} className="hover:text-blue-600 transition-colors">
                          {relatedPost.title}
                        </Link>
                      </h4>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                        {relatedPost.excerpt}
                      </p>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>{formatDate(relatedPost.publish_date)}</span>
                        <span>{relatedPost.reading_time} min read</span>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </div>
          )}
        </div>
      </article>
    </div>
  );
};

export default BlogPostPage;