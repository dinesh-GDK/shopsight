import React from 'react';
import { Gauge } from 'lucide-react';

/**
 * Confidence threshold slider component
 *
 * Allows users to filter search results by minimum confidence score.
 *
 * @param {number} value - Current confidence value (0.0 - 1.0)
 * @param {function} onChange - Callback when value changes
 * @param {boolean} disabled - Whether the slider is disabled
 */
export default function ConfidenceSlider({ value, onChange, disabled = false }) {
  const handleChange = (e) => {
    const newValue = parseFloat(e.target.value) / 100;
    onChange(newValue);
  };

  const getConfidenceLevel = (score) => {
    if (score >= 0.8) return { label: 'High Match', color: 'text-green-600' };
    if (score >= 0.5) return { label: 'Medium Match', color: 'text-yellow-600' };
    if (score >= 0.3) return { label: 'Low Match', color: 'text-orange-600' };
    return { label: 'Show All', color: 'text-gray-600' };
  };

  const { label, color } = getConfidenceLevel(value);

  return (
    <>
      <style>
        {`
          .confidence-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: ${disabled ? '#9ca3af' : '#3b82f6'};
            cursor: ${disabled ? 'not-allowed' : 'pointer'};
            border: 3px solid white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          }

          .confidence-slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: ${disabled ? '#9ca3af' : '#3b82f6'};
            cursor: ${disabled ? 'not-allowed' : 'pointer'};
            border: 3px solid white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          }
        `}
      </style>

      <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Gauge className="w-5 h-5 text-gray-700" />
            <label className="text-sm font-semibold text-gray-700">
              Confidence Filter
            </label>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`text-sm font-medium ${color}`}>
              {label}
            </span>
            <span className="text-sm font-bold text-primary-600 bg-primary-50 px-2 py-1 rounded">
              {(value * 100).toFixed(0)}%
            </span>
          </div>
        </div>

        <div className="relative">
          <input
            type="range"
            min="0"
            max="100"
            value={value * 100}
            onChange={handleChange}
            disabled={disabled}
            className={`w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer
                       disabled:opacity-50 disabled:cursor-not-allowed
                       confidence-slider`}
            style={{
              background: disabled
                ? '#e5e7eb'
                : `linear-gradient(to right,
                    #3b82f6 0%,
                    #3b82f6 ${value * 100}%,
                    #e5e7eb ${value * 100}%,
                    #e5e7eb 100%)`
            }}
          />
        </div>

        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>Show All (0%)</span>
          <span>Exact Match (100%)</span>
        </div>

        <p className="text-xs text-gray-600 mt-2 text-center italic">
          {value > 0 ? (
            <>Only showing products with <strong>{(value * 100).toFixed(0)}%+</strong> relevance</>
          ) : (
            <>Showing all products regardless of relevance</>
          )}
        </p>
      </div>
    </>
  );
}
