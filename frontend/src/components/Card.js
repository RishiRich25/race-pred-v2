import React from 'react';

export const Card = ({ children, className = '', glass = false, ...props }) => {
  const cardClass = glass ? 'card card-glass' : 'card';
  return (
    <div className={`${cardClass} ${className}`} {...props}>
      {children}
    </div>
  );
};

export default Card;
