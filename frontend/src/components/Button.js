import React from 'react';

export const Button = ({ variant = 'primary', children, ...props }) => {
  const buttonClass = `btn btn-${variant}`;
  return (
    <button className={buttonClass} {...props}>
      {children}
    </button>
  );
};

export default Button;
