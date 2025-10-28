const SynapseLogo = ({ className = "w-8 h-8", color = "#2563eb" }) => {
  return (
    <svg
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Neural network nodes */}
      <circle cx="20" cy="30" r="8" fill={color} opacity="0.9">
        <animate
          attributeName="opacity"
          values="0.9;1;0.9"
          dur="2s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="50" cy="20" r="10" fill={color}>
        <animate
          attributeName="r"
          values="10;11;10"
          dur="2s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="80" cy="35" r="7" fill={color} opacity="0.9">
        <animate
          attributeName="opacity"
          values="0.9;1;0.9"
          dur="2s"
          begin="0.5s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="30" cy="70" r="9" fill={color} opacity="0.95">
        <animate
          attributeName="opacity"
          values="0.95;1;0.95"
          dur="2s"
          begin="1s"
          repeatCount="indefinite"
        />
      </circle>
      <circle cx="70" cy="75" r="8" fill={color} opacity="0.9">
        <animate
          attributeName="opacity"
          values="0.9;1;0.9"
          dur="2s"
          begin="1.5s"
          repeatCount="indefinite"
        />
      </circle>
      
      {/* Connection lines */}
      <path
        d="M 26 32 Q 35 25 44 22"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.6"
      />
      <path
        d="M 56 24 Q 65 28 74 33"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.6"
      />
      <path
        d="M 24 37 Q 27 50 30 63"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.6"
      />
      <path
        d="M 37 68 Q 50 70 63 73"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.6"
      />
      <path
        d="M 78 42 Q 75 55 72 68"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.6"
      />
      
      {/* Center connecting node */}
      <circle cx="50" cy="50" r="6" fill={color} opacity="0.4" />
      <path
        d="M 50 30 L 50 44"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.4"
      />
      <path
        d="M 28 35 L 45 47"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.4"
      />
      <path
        d="M 72 38 L 55 47"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.4"
      />
      <path
        d="M 35 68 L 46 54"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.4"
      />
      <path
        d="M 65 72 L 54 54"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        opacity="0.4"
      />
    </svg>
  );
};

export default SynapseLogo;
