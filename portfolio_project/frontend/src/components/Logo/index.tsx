import React from 'react';
import Link from 'next/link';
import LogoIcon from './LogoIcon';
import LogoFull from './LogoFull';
import LogoCompact from './LogoCompact';

// Export individual components for specific use cases
export { LogoIcon, LogoFull, LogoCompact };

// Type definitions following SOLID principles - Interface Segregation
interface IconSizeConfig {
  size: number;
}

interface DimensionSizeConfig {
  width: number;
  height: number;
}

// Main Logo component that adapts based on props
interface LogoProps {
  variant?: 'icon' | 'compact' | 'full';
  size?: 'small' | 'medium' | 'large' | 'xl';
  color?: 'default' | 'white' | 'dark';
  className?: string;
  href?: string;
  isScrolled?: boolean;
  showText?: boolean; // For backward compatibility
}

const Logo: React.FC<LogoProps> = ({ 
  variant = 'compact',
  size = 'medium',
  color = 'default',
  className = '',
  href = '/',
  isScrolled = false,
  showText = true // For backward compatibility
}) => {
  // Size mappings for different variants - following Single Responsibility Principle
  const getIconSizeConfig = (size: string): IconSizeConfig => {
    const configs = {
      small: { size: 28 },
      medium: { size: 36 },
      large: { size: 48 },
      xl: { size: 64 }
    };
    return configs[size as keyof typeof configs];
  };

  const getDimensionSizeConfig = (size: string, variant: 'compact' | 'full'): DimensionSizeConfig => {
    const configs = {
      compact: {
        small: { width: 80, height: 28 },
        medium: { width: 100, height: 36 },
        large: { width: 120, height: 42 },
        xl: { width: 140, height: 48 }
      },
      full: {
        small: { width: 200, height: 32 },
        medium: { width: 240, height: 36 },
        large: { width: 270, height: 42 },
        xl: { width: 300, height: 48 }
      }
    };
    return configs[variant][size as keyof typeof configs.compact];
  };

  // Determine color based on scroll state if using default
  const logoColor = color === 'default' && isScrolled ? 'dark' : color;

  const renderLogo = () => {
    switch (variant) {
      case 'icon': {
        const iconConfig = getIconSizeConfig(size);
        return (
          <LogoIcon 
            size={iconConfig.size}
            color={logoColor}
            className="transition-all duration-200"
          />
        );
      }
      case 'full': {
        const dimensionConfig = getDimensionSizeConfig(size, 'full');
        return (
          <LogoFull 
            width={dimensionConfig.width}
            height={dimensionConfig.height}
            color={logoColor}
            className="transition-all duration-200"
          />
        );
      }
      default: { // compact
        const dimensionConfig = getDimensionSizeConfig(size, 'compact');
        return (
          <LogoCompact 
            width={dimensionConfig.width}
            height={dimensionConfig.height}
            color={logoColor}
            showInitials={showText}
            className="transition-all duration-200"
          />
        );
      }
    }
  };

  const logoElement = (
    <div className={`flex items-center transition-all duration-200 hover:opacity-80 ${className}`}>
      {renderLogo()}
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