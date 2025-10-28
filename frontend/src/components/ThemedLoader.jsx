import SynapseLogo from "./SynapseLogo";

const ThemedLoader = ({ size = "md" }) => {
  const sizeClasses = {
    sm: "w-8 h-8",
    md: "w-12 h-12",
    lg: "w-16 h-16",
  };

  return (
    <div className="flex items-center justify-center">
      <div className="relative">
        <SynapseLogo className={sizeClasses[size]} />
        <div className="absolute inset-0 animate-ping opacity-20">
          <SynapseLogo className={sizeClasses[size]} />
        </div>
      </div>
    </div>
  );
};

export default ThemedLoader;
