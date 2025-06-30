import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface LogoProps {
  size?: 'small' | 'medium' | 'large' | 'xl' | 'xxl';
  className?: string;
  href?: string;
  isScrolled?: boolean;
  showText?: boolean;
}

const Logo: React.FC<LogoProps> = ({ 
  size = 'large', // Increased default size
  className = '',
  href = '/',
  isScrolled = false,
  showText = false // Default to false for navbar
}) => {
  // Size mappings - reduced by 10% from the 2x size as requested, maintaining aspect ratio of logo.svg (270:42)
  const getSizeConfig = () => {
    const configs = {
      small: { width: 194, height: 31 }, // 216*0.9, 34*0.9 (10% reduction)
      medium: { width: 292, height: 45 }, // 324*0.9, 50*0.9
      large: { width: 389, height: 60 }, // 432*0.9, 67*0.9
      xl: { width: 486, height: 76 }, // 540*0.9, 84*0.9 (10% reduction from doubled size)
      xxl: { width: 583, height: 91 } // 648*0.9, 101*0.9
    };

    return configs[size];
  };

  const sizeConfig = getSizeConfig();

  const logoElement = (
    <div className={`flex items-center transition-all duration-200 hover:opacity-80 ${className}`}>
      <Image
        src="/logo.svg"
        alt="Amardeep Asode Logo"
        width={sizeConfig.width}
        height={sizeConfig.height}
        className="object-contain transition-all duration-200"
        priority
      />
    </div>
  );

  // If href is provided, wrap in Link
  if (href) {
    return (
      <Link href={href} className="inline-block">
        {logoElement}
      </Link>
    );
  }

  return logoElement;
};

export default Logo;