"use client";

import { motion } from "framer-motion";
import React from "react";
import Image from "next/image";
import { SimpleButton } from "@/components/ui/simple-button";

// Interface for hero content - following Single Responsibility Principle
interface HeroContent {
  name: string;
  title: string;
  description: string;
  buttonText: string;
  imageSrc: string;
  imageAlt: string;
}

// Interface for animation configuration - Dependency Inversion Principle
interface AnimationConfig {
  initial: { opacity: number; y?: number; scale?: number };
  animate: { opacity: number; y?: number; scale?: number };
  transition: { duration: number; delay: number };
}

// Hero content configuration - Open/Closed Principle
const heroContent: HeroContent = {
  name: "Amardeep Asode",
  title: "Stock & Intraday Trader",
  description: "Expert in intraday strategies for consistent results. Transforming trading performance through proven methodologies.",
  buttonText: "Connect with Amardeep",
  imageSrc: "/owner_landing_page.jpg",
  imageAlt: "Amardeep Asode - Professional Stock & Intraday Trader"
};

// Animation configurations - Single Responsibility Principle
const animationConfigs: Record<string, AnimationConfig> = {
  container: {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay: 0.3 }
  },
  name: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay: 0.2 }
  },
  title: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay: 0.4 }
  },
  description: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay: 0.6 }
  },
  button: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.8, delay: 0.8 }
  },
  image: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    transition: { duration: 1, delay: 0.5 }
  }
};

// Text content component - Single Responsibility Principle
const HeroTextContent: React.FC<{ content: HeroContent }> = ({ content }) => {
  return (
    <div className="flex flex-col justify-center h-full max-w-2xl">
      <motion.h1 
        {...animationConfigs.name}
        className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-6 leading-tight"
      >
        {content.name}
      </motion.h1>
      
      <motion.h2 
        {...animationConfigs.title}
        className="text-xl sm:text-2xl md:text-3xl lg:text-4xl text-blue-600 dark:text-blue-400 font-semibold mb-6 sm:mb-8"
      >
        {content.title}
      </motion.h2>
      
      <motion.p 
        {...animationConfigs.description}
        className="text-lg sm:text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 sm:mb-10 leading-relaxed"
      >
        {content.description}
      </motion.p>
      
      <motion.div {...animationConfigs.button}>
        <SimpleButton
          as="a"
          href="mailto:amardipasode@gmail.com?subject=Trading Consultation Request&body=Hi Amardeep,%0D%0A%0D%0AI would like to connect with you regarding trading consultation.%0D%0A%0D%0AThank you!"
          variant="primary"
          size="lg"
          className="hover:scale-105 cursor-pointer"
          target="_blank"
          rel="noopener noreferrer"
        >
          {content.buttonText}
        </SimpleButton>
      </motion.div>
    </div>
  );
};

// Image component - Single Responsibility Principle
const HeroImage: React.FC<{ content: HeroContent }> = ({ content }) => {
  return (
    <motion.div 
      {...animationConfigs.image}
      className="relative h-full flex items-center justify-center w-full"
    >
      <div className="relative w-full max-w-md lg:max-w-lg aspect-[3/4] lg:aspect-[4/5]">
        <Image
          src={content.imageSrc}
          alt={content.imageAlt}
          fill
          className="object-cover object-center rounded-2xl shadow-2xl hover:shadow-3xl transition-shadow duration-300"
          priority
          sizes="(max-width: 768px) 90vw, 45vw"
        />
        
        {/* Subtle overlay for modern effect */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/5 via-transparent to-transparent rounded-2xl"></div>
        
        {/* Modern border accent */}
        <div className="absolute inset-0 rounded-2xl ring-1 ring-white/20 dark:ring-white/10"></div>
      </div>
    </motion.div>
  );
};

// Main hero component - Interface Segregation Principle
export const SplitHero: React.FC = () => {
  return (
    <section className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <motion.div
        {...animationConfigs.container}
        className="container mx-auto px-4 sm:px-6 lg:px-8 min-h-screen flex items-center"
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 w-full py-12 lg:py-0">
          {/* Left Column - Text Content */}
          <div className="flex items-center justify-center lg:justify-start order-2 lg:order-1">
            <HeroTextContent content={heroContent} />
          </div>
          
          {/* Right Column - Image */}
          <div className="flex items-center justify-center order-1 lg:order-2 min-h-[60vh] lg:min-h-[80vh]">
            <HeroImage content={heroContent} />
          </div>
        </div>
      </motion.div>
    </section>
  );
};

export default SplitHero;