import React from 'react';
import { Calendar, Clock, AlertTriangle } from 'lucide-react';

const UrgencySection = () => {
  const scrollToComparison = () => {
    const element = document.getElementById('comparison');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="py-20 bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            31 July filing deadline is closing fast.
          </h2>
          <div className="w-24 h-1 bg-red-500 mx-auto"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <Calendar className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-carbon-graphite mb-2">
              Q2 reporting deadline = €50/t penalty risk
            </h3>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <Clock className="h-12 w-12 text-orange-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-carbon-graphite mb-2">
              Supply chain response time = 5 days minimum
            </h3>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <AlertTriangle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-carbon-graphite mb-2">
              Book before Big Four slots vanish
            </h3>
          </div>
        </div>
        
        <div className="text-center">
          <button
            onClick={scrollToComparison}
            className="bg-fast-pass-green text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-green-600 transition-all duration-200 hover-lift"
          >
            Explore Compliance Packages
          </button>
        </div>
      </div>
    </section>
  );
};

export default UrgencySection;