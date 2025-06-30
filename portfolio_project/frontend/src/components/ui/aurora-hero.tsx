"use client";

import { motion } from "framer-motion";
import React from "react";
import Image from "next/image";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { Button as MovingBorderButton } from "@/components/ui/moving-border";

export function AuroraHero() {
  return (
    <AuroraBackground>
      <motion.div
        initial={{ opacity: 0.0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4 sm:px-6 lg:px-8"
      >
        <div className="flex flex-col lg:flex-row items-center justify-between gap-8 sm:gap-12 max-w-7xl mx-auto w-full">
          <div className="flex-1 text-center lg:text-left max-w-2xl lg:max-w-none">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-6 leading-tight"
            >
              Amardeep Asode
            </motion.h1>
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-lg sm:text-xl md:text-2xl lg:text-3xl text-blue-600 dark:text-blue-400 font-semibold mb-4 sm:mb-6"
            >
              Stock & Intraday Trader
            </motion.h2>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="text-base sm:text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-6 sm:mb-8 leading-relaxed max-w-2xl mx-auto lg:mx-0"
            >
              Expert in intraday strategies for consistent results. 
              Transforming trading performance through proven methodologies.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <MovingBorderButton
                borderRadius="1.75rem"
                className="bg-white dark:bg-slate-900 text-black dark:text-white border-neutral-200 dark:border-slate-800"
                containerClassName="w-auto h-auto"
              >
                Connect with Amardeep
              </MovingBorderButton>
            </motion.div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.5 }}
            className="flex-1 flex justify-center lg:justify-end"
          >
            <div className="relative group">
              {/* Background Decorative Elements */}
              <div className="absolute inset-0 -m-4 sm:-m-8">
                {/* Gradient Orbs */}
                <div className="absolute top-0 right-0 w-20 h-20 sm:w-32 sm:h-32 bg-gradient-to-br from-blue-400/30 to-purple-500/30 rounded-full blur-xl animate-pulse"></div>
                <div className="absolute bottom-0 left-0 w-16 h-16 sm:w-24 sm:h-24 bg-gradient-to-tr from-green-400/30 to-blue-500/30 rounded-full blur-lg animate-pulse delay-1000"></div>
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-24 h-24 sm:w-40 sm:h-40 bg-gradient-to-r from-orange-300/20 to-pink-400/20 rounded-full blur-2xl animate-pulse delay-500"></div>
              </div>

              {/* Main Image Container */}
              <div className="relative">
                {/* Floating Card Design */}
                <div className="relative w-64 h-80 sm:w-80 sm:h-96 lg:w-96 lg:h-[28rem] rounded-3xl overflow-hidden shadow-2xl bg-white dark:bg-gray-800 transform transition-all duration-500 group-hover:scale-105 group-hover:shadow-3xl">
                  {/* Image with Modern Aspect Ratio */}
                  <div className="relative w-full h-full overflow-hidden rounded-3xl">
                    <Image
                      src="/owner_landing_page.jpg"
                      alt="Amardeep Asode - Professional Stock & Intraday Trader"
                      width={400}
                      height={500}
                      className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                      priority
                    />
                    
                    {/* Gradient Overlay for Modern Effect */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                  </div>

                  {/* Geometric Frame Accent */}
                  <div className="absolute inset-0 rounded-3xl border-2 border-white/20 dark:border-gray-700/30"></div>
                  
                  {/* Inner Glow Effect */}
                  <div className="absolute inset-0 rounded-3xl shadow-inner shadow-white/10"></div>
                </div>

                {/* Floating Achievement Cards */}
                <motion.div 
                  initial={{ opacity: 0, x: 50, y: -20 }}
                  animate={{ opacity: 1, x: 0, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.2 }}
                  className="absolute -top-2 -right-2 sm:-top-4 sm:-right-4 lg:-right-8"
                >
                  <div className="bg-white dark:bg-gray-800 rounded-xl sm:rounded-2xl p-2 sm:p-4 shadow-xl border border-gray-100 dark:border-gray-700 backdrop-blur-sm bg-white/90 dark:bg-gray-800/90">
                    <div className="text-center">
                      <div className="text-lg sm:text-2xl font-bold text-green-600 mb-0.5 sm:mb-1">5+</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">Years Experience</div>
                    </div>
                  </div>
                </motion.div>
                
                <motion.div 
                  initial={{ opacity: 0, x: -50, y: 20 }}
                  animate={{ opacity: 1, x: 0, y: 0 }}
                  transition={{ duration: 0.6, delay: 1.4 }}
                  className="absolute -bottom-2 -left-2 sm:-bottom-4 sm:-left-4 lg:-left-8"
                >
                  <div className="bg-white dark:bg-gray-800 rounded-xl sm:rounded-2xl p-2 sm:p-4 shadow-xl border border-gray-100 dark:border-gray-700 backdrop-blur-sm bg-white/90 dark:bg-gray-800/90">
                    <div className="text-center">
                      <div className="text-lg sm:text-2xl font-bold text-blue-600 mb-0.5 sm:mb-1">85%</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 font-medium">Success Rate</div>
                    </div>
                  </div>
                </motion.div>

                              </div>

              {/* Geometric Accent Shapes */}
              <div className="absolute -z-10 inset-0">
                <div className="absolute top-8 right-8 w-16 h-16 border-2 border-blue-200/50 dark:border-blue-800/50 rounded-lg rotate-12 animate-pulse"></div>
                <div className="absolute bottom-12 left-8 w-12 h-12 border-2 border-purple-200/50 dark:border-purple-800/50 rounded-full animate-pulse delay-700"></div>
                <div className="absolute top-1/3 left-4 w-8 h-8 bg-gradient-to-br from-green-400/30 to-blue-500/30 rounded-md rotate-45 animate-pulse delay-1000"></div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </AuroraBackground>
  );
}