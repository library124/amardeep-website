import React from 'react';

interface LogoFullProps {
  className?: string;
  width?: number;
  height?: number;
  color?: 'default' | 'white' | 'dark';
}

const LogoFull: React.FC<LogoFullProps> = ({ 
  className = '', 
  width = 270,
  height = 42,
  color = 'default'
}) => {
  const getColors = () => {
    switch (color) {
      case 'white':
        return {
          accent: '#00E676',
          primary: '#ffffff',
          stroke: '#ffffff'
        };
      case 'dark':
        return {
          accent: '#00E676',
          primary: '#1a1a1a',
          stroke: '#1a1a1a'
        };
      default:
        return {
          accent: '#00E676',
          primary: 'url(#blue-gradient)',
          stroke: 'url(#blue-gradient)'
        };
    }
  };

  const colors = getColors();

  return (
    <svg 
      width={width} 
      height={height} 
      viewBox="0 0 270 42" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="blue-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#34568B" />
          <stop offset="100%" stopColor="#1D2B64" />
        </linearGradient>
      </defs>

      {/* LOGOMARK GROUP ("A" as a Candlestick) */}
      <g id="logomark" transform="translate(0, 0)">
        {/* The body of the candlestick (the green box) forming the left leg */}
        <rect 
          fill={colors.accent} 
          x="5" 
          y="12" 
          width="10" 
          height="25" 
          rx="2" 
        />

        {/* The upper wick, which elegantly forms the right leg of the 'A' */}
        <path 
          stroke={colors.stroke}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          d="M10 12 L10 2 C10 2 20 2 30 20 L35 30" 
        />
        
        {/* The lower wick of the candlestick */}
        <path 
          stroke={colors.stroke}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          d="M10 37 L10 40" 
        />

        {/* The crossbar of the 'A' */}
        <path 
          stroke={colors.stroke}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          d="M14 22 L28 22" 
        />
      </g>

      {/* LOGOTYPE GROUP (The Name) */}
      <text 
        fill={colors.primary}
        x="52" 
        y="28"
        fontFamily="'Poppins', 'Helvetica Neue', Arial, sans-serif"
        fontSize="20"
        fontWeight="500"
        letterSpacing="0.2px"
      >
        AMARDEEP ASODE
      </text>
    </svg>
  );
};

export default LogoFull;