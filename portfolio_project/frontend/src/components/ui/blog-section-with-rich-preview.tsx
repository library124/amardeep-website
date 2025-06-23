"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import Image from "next/image";
import Link from "next/link";

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

interface BlogProps {
  posts?: BlogPost[];
  loading?: boolean;
}

function Blog({ posts = [], loading = false }: BlogProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  // Default demo data if no posts provided
  const defaultPosts: BlogPost[] = [
    {
      id: 1,
      title: "Advanced Intraday Trading Strategies for Consistent Profits",
      slug: "advanced-intraday-trading-strategies",
      excerpt: "Discover proven intraday trading techniques that can help you maximize profits while minimizing risks. Learn about technical indicators, market timing, and risk management strategies used by professional traders.",
      featured_image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop",
      author_name: "Amardeep Asode",
      category_name: "Trading Strategy",
      publish_date: "2024-01-15",
      reading_time: 8,
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
      publish_date: "2024-01-12",
      reading_time: 5,
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
      publish_date: "2024-01-10",
      reading_time: 6,
      is_featured: false
    }
  ];

  const displayPosts = posts.length > 0 ? posts : defaultPosts;
  const featuredPost = displayPosts.find(post => post.is_featured) || displayPosts[0];
  const regularPosts = displayPosts.filter(post => post.id !== featuredPost.id).slice(0, 2);

  if (loading) {
    return (
      <div className="w-full py-20 lg:py-40">
        <div className="container mx-auto flex flex-col gap-14">
          <div className="flex w-full flex-col sm:flex-row sm:justify-between sm:items-center gap-8">
            <div className="h-12 bg-gray-200 rounded-lg w-80 animate-pulse"></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="md:col-span-2 animate-pulse">
              <div className="bg-gray-200 rounded-md aspect-video mb-4"></div>
              <div className="h-4 bg-gray-200 rounded mb-2 w-1/4"></div>
              <div className="h-8 bg-gray-200 rounded mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            </div>
            {[1, 2].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-gray-200 rounded-md aspect-video mb-4"></div>
                <div className="h-4 bg-gray-200 rounded mb-2 w-1/4"></div>
                <div className="h-6 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full py-20 lg:py-40">
      <div className="container mx-auto flex flex-col gap-14">
        <div className="flex w-full flex-col sm:flex-row sm:justify-between sm:items-center gap-8">
          <h4 className="text-3xl md:text-5xl tracking-tighter max-w-xl font-regular">
            Latest Trading Insights
          </h4>
          <Link 
            href="/blog"
            className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
          >
            View All Articles →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Featured Article */}
          <Link 
            href={`/blog/${featuredPost.slug}`}
            className="flex flex-col gap-4 hover:opacity-75 cursor-pointer md:col-span-2 group"
          >
            <div className="relative bg-muted rounded-md aspect-video overflow-hidden">
              {featuredPost.featured_image ? (
                <Image
                  src={featuredPost.featured_image}
                  alt={featuredPost.title}
                  fill
                  className="object-cover group-hover:scale-105 transition-transform duration-300"
                />
              ) : (
                <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                  <span className="text-6xl text-blue-600">📈</span>
                </div>
              )}
            </div>
            
            <div className="flex flex-row gap-4 items-center">
              <Badge variant="default" className="bg-blue-600 hover:bg-blue-700">
                {featuredPost.category_name}
              </Badge>
              <p className="flex flex-row gap-2 text-sm items-center">
                <span className="text-muted-foreground">By</span>
                <Avatar className="h-6 w-6">
                  <AvatarImage src="/owner_landing_page.jpg" />
                  <AvatarFallback>AA</AvatarFallback>
                </Avatar>
                <span>{featuredPost.author_name}</span>
                <span className="text-muted-foreground">•</span>
                <span className="text-muted-foreground">{formatDate(featuredPost.publish_date)}</span>
              </p>
            </div>
            
            <div className="flex flex-col gap-2">
              <h3 className="max-w-3xl text-4xl tracking-tight group-hover:text-blue-600 transition-colors">
                {featuredPost.title}
              </h3>
              <p className="max-w-3xl text-muted-foreground text-base">
                {featuredPost.excerpt}
              </p>
              <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
                <span>{featuredPost.reading_time} min read</span>
              </div>
            </div>
          </Link>

          {/* Regular Articles */}
          {regularPosts.map((post) => (
            <Link 
              key={post.id}
              href={`/blog/${post.slug}`}
              className="flex flex-col gap-4 hover:opacity-75 cursor-pointer group"
            >
              <div className="relative bg-muted rounded-md aspect-video overflow-hidden">
                {post.featured_image ? (
                  <Image
                    src={post.featured_image}
                    alt={post.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
                    <span className="text-4xl text-blue-600">📊</span>
                  </div>
                )}
              </div>
              
              <div className="flex flex-row gap-4 items-center">
                <Badge variant="secondary">
                  {post.category_name}
                </Badge>
                <p className="flex flex-row gap-2 text-sm items-center">
                  <span className="text-muted-foreground">By</span>
                  <Avatar className="h-6 w-6">
                    <AvatarImage src="/owner_landing_page.jpg" />
                    <AvatarFallback>AA</AvatarFallback>
                  </Avatar>
                  <span>{post.author_name}</span>
                </p>
              </div>
              
              <div className="flex flex-col gap-1">
                <h3 className="max-w-3xl text-2xl tracking-tight group-hover:text-blue-600 transition-colors">
                  {post.title}
                </h3>
                <p className="max-w-3xl text-muted-foreground text-base line-clamp-3">
                  {post.excerpt}
                </p>
                <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
                  <span>{formatDate(post.publish_date)}</span>
                  <span>•</span>
                  <span>{post.reading_time} min read</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export { Blog };