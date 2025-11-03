import React from 'react';

const Logo = ({ size = 'medium', variant = 'light' }) => {
  const sizes = {
    small: { container: 'px-2 py-1', circle: 'w-6 h-6', icon: '14', text: 'text-sm' },
    medium: { container: 'px-3 py-2', circle: 'w-8 h-8', icon: '18', text: 'text-lg' },
    large: { container: 'px-4 py-3', circle: 'w-10 h-10', icon: '22', text: 'text-xl' }
  };

  const currentSize = sizes[size];

  return (
    <div className={`flex items-center rounded-lg ${currentSize.container}`} 
         style={{backgroundColor: variant === 'dark' ? '#121E3C' : 'transparent'}}>
      {/* Green circle with person icon */}
      <div className={`flex items-center justify-center ${currentSize.circle} rounded-full mr-2`} 
           style={{backgroundColor: '#2F8140'}}>
        <svg width={currentSize.icon} height={currentSize.icon} viewBox="0 0 24 24" fill="white">
          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
      </div>
      {/* Logo text */}
      <div className="flex items-center">
        <span className={`${currentSize.text} font-bold font-montserrat`} 
              style={{color: variant === 'dark' ? 'white' : '#121E3C'}}>
          Service
        </span>
        <span className={`${currentSize.text} font-bold font-montserrat`} 
              style={{color: '#2F8140'}}>
          Hub
        </span>
      </div>
    </div>
  );
};

export default Logo;