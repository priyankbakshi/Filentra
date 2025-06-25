import React from 'react';
import { Zap, Users, Star } from 'lucide-react';

const ServicesSection = () => {
  const services = [
    {
      icon: Zap,
      title: "CBAM Express Fix",
      description: "Upload your spreadsheet. We clean, map, and validate your spreadsheet. We deliver a schema-compliant XML within 72 hours of final handoff. Refund guaranteed if it fails schema checks.",
      badge: "Fastest Fix",
      badgeClass: "badge-fastest"
    },
    {
      icon: Users,
      title: "CBAM Filing Concierge",
      description: "We chase up to 20 suppliers over 5 business days via multilingual email and voicemail. Then we file your XML within 72 hours based on available data. Silent suppliers? We file fallback legal memos under Art. 4-2.",
      badge: "Most Popular",
      badgeClass: "badge-popular"
    },
    {
      icon: Star,
      title: "Authorised Declarant Pack",
      description: "Want to be ready for Jan 2026? We're building a full Authorised Declarant service. We draft and file your entire Authorised Declarant dossier—including ICP, bank guarantee calc, and NCA responses. Reach out if you'd like early access or co-develop this with us.",
      badge: "Coming Q4",
      badgeClass: "badge badge-gray-100 text-gray-800"
    }
  ];

  return (
    <section id="services" className="py-20 bg-compliance-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            One platform. Three compliance tools.
          </h2>
          <div className="w-24 h-1 bg-filentra-blue mx-auto"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div 
              key={index}
              className="bg-white p-8 rounded-xl shadow-lg hover-lift fade-in relative"
              style={{ animationDelay: `${index * 0.2}s` }}
            >
              <div className="flex items-center justify-between mb-6">
                <service.icon className="h-12 w-12 text-filentra-blue" />
                <span className={`badge ${service.badgeClass}`}>
                  {service.badge}
                </span>
              </div>
              
              <h3 className="text-xl font-bold text-carbon-graphite mb-4">
                {service.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed">
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;