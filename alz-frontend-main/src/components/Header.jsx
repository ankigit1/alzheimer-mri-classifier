import { Brain, Activity } from "lucide-react";

const Header = () => {
  return (
    <header className="bg-slate-200 backdrop-blur-sm rounded-t-3xl overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Left side logo + text */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-tr from-indigo-500 to-purple-500 rounded-lg shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-black">MediScan AI</h1>
              <p className="text-sm text-gray-500">Dementia Diagnosis Assistant</p>
            </div>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-2 text-gray-300">
            <Activity className="w-4 h-4 text-gray-700" />
            <span className="text-sm font-medium text-gray-500">Advanced Neural Analysis</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

//     <div className=" flex items-center justify-center p-8">