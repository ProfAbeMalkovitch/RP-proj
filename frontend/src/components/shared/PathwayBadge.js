/**
 * Pathway Badge Component
 * Displays pathway with color coding
 */
import React from 'react';
import './PathwayBadge.css';

function PathwayBadge({ pathway }) {
  const getPathwayClass = (pathway) => {
    if (!pathway) return 'pathway-basic';
    const lower = pathway.toLowerCase();
    if (lower === 'basic') return 'pathway-basic';
    if (lower === 'intermediate') return 'pathway-intermediate';
    if (lower === 'accelerated') return 'pathway-accelerated';
    return 'pathway-basic';
  };

  return (
    <span className={`pathway-badge ${getPathwayClass(pathway)}`}>
      {pathway || 'Basic'}
    </span>
  );
}

export default PathwayBadge;





































