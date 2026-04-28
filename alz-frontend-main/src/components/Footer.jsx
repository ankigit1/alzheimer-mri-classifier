import { Heart, Shield, Stethoscope, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-slate-200 mt-auto rounded-b-3xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Top Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 text-center">
          {/* Patient Care */}
          <div className="flex flex-col items-center space-y-3">
            <div className="flex items-center justify-center w-12 h-12 bg-red-100 rounded-xl">
              <Heart className="w-6 h-6 text-red-500" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-700">Patient Care</h3>
              <p className="text-sm text-gray-500">Advanced AI diagnostics</p>
            </div>
          </div>

          {/* Privacy Secure */}
          <div className="flex flex-col items-center space-y-3">
            <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-xl">
              <Shield className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-700">Privacy Secure</h3>
              <p className="text-sm text-gray-500">HIPAA compliant platform</p>
            </div>
          </div>

          {/* Clinical Grade */}
          <div className="flex flex-col items-center space-y-3">
            <div className="flex items-center justify-center w-12 h-12 bg-yellow-100 rounded-xl">
              <Stethoscope className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-700">Clinical Grade</h3>
              <p className="text-sm text-gray-500">Validated algorithms</p>
            </div>
          </div>
        </div>

        {/* Social Icons Section */}
        <div className="mt-10 mb-6 text-center">
          <p className="text-sm font-medium text-gray-600 mb-3">Let’s Connect</p>
          <div className="flex justify-center">
            <a
              href="https://www.linkedin.com/in/ankitagg98?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-full bg-blue-100 hover:bg-blue-200 shadow-sm transition"
            >
              <Linkedin className="w-5 h-5 text-blue-600" />
            </a>
          </div>
        </div>

        {/* Bottom Note */}
        <div className="pt-6 border-t border-gray-300 text-center">
          <p className="text-xs text-gray-500">
            © 2025 MediScan AI. For research purposes only. Always consult healthcare professionals.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;