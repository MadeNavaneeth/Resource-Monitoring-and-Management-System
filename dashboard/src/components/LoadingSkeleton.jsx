import React from 'react';
import './LoadingSkeleton.css';

const LoadingSkeleton = ({ count = 3 }) => {
    return (
        <div className="loading-skeleton-container">
            {[...Array(count)].map((_, i) => (
                <div key={i} className="skeleton-card">
                    <div className="skeleton-header">
                        <div className="skeleton-title pulse"></div>
                        <div className="skeleton-badge pulse"></div>
                    </div>
                    <div className="skeleton-body">
                        <div className="skeleton-line pulse"></div>
                        <div className="skeleton-line short pulse"></div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default LoadingSkeleton;
