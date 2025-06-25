import React from 'react';
import { Clock, Shield, Target, User, CreditCard } from 'lucide-react';
import { Link } from 'react-router-dom';

const WhyFilentraSection = () => {
  const reasons = [
    {
      icon: Clock,
      title: "Speed you can bank on",
      description: "72-hour XML filing guarantee"
    },
    {
      icon: Shield,
      title: "Certainty baked in",
      description: "Refund if XML schema validation fails"
    },
    {
      icon: Target,
      title: "Effort-priced",
      description: "Supplier follow-up is bounded and costed"
    },
    {
      icon: User,
      title: "Founder-led",
      description: "No junior analyst layers. Direct handling."
    },
    {
      icon: CreditCard,
      title: "Flexibility",
      description: "Stripe paylink. One-pager SoW. No POs required."
    }
  ];

  return (
    <section className="py-20 bg-compliance-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            Why EU mid-cap importers trust Filentra
          </h2>
          <div className="w-24 h-1 bg-filentra-blue mx-auto"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {reasons.map((reason, index) => (
            <div 
              key={index}
              className="bg-white p-6 rounded-lg hover-lift fade-in text-center"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <reason.icon className="h-12 w-12 text-filentra-blue mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-carbon-graphite mb-2">
                {reason.title}
              </h3>
              <p className="text-gray-600">
                {reason.description}
              </p>
            </div>
          ))}
        </div>

  {/*      <div className="text-center">
          <Link 
            to="/about"
            className="text-filentra-blue hover:text-blue-700 font-semibold inline-flex items-center"
          >
            About the founder
            <svg className="ml-1 h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </Link>
          
          <div className="mt-6 p-4 bg-white rounded-lg inline-block">
            <p className="text-sm text-gray-600">
              Prefer formal PO or extended SoW? We support that too — just ask.
            </p>
          </div>
  
        </div>
        */}
      </div>
    </section>
  );
};

export default WhyFilentraSection;