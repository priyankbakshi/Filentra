import React from 'react';
import { Check, X, Clock, Users, Shield, Star } from 'lucide-react';

const ComparisonSection = () => {
  const features = [
    { name: "Schema-compliant XML filing", express: true, concierge: true },
    { name: "Turnaround time", express: "72 hours", concierge: "5–7 day supplier chase + 72h filing" },
    { name: "Number of suppliers outreach included", express: false, concierge: "20 suppliers outreach" },
    { name: "Supplier follow-up methods", express: false, concierge: "Email + voicemail, multilingual, 5-day window" },
    { name: "Legal fallback memo (Art. 4-2)", express: false, concierge: true },
    { name: "Extra suppliers supported", express: false, concierge: "+€500 per 5 suppliers" },
    { name: "Refund policy", express: "100% if XML schema fails (€2,000)", concierge: "Refund for XML schema fails only (€2,000); supplier outreach is effort-based, hence no refund for that" },
    { name: "Best for", express: "Teams with supplier data on hand", concierge: "Teams waiting on supplier responses" }
  ];

  const scrollToComparison = () => {
    const element = document.getElementById('comparison');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="comparison" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            Feature Comparison
          </h2>
          <div className="w-24 h-1 bg-filentra-blue mx-auto"></div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full table-fixed bg-white rounded-xl shadow-lg overflow-hidden">
	   <colgroup>
  		<col className="w-1/3" />
  		<col className="w-1/3" />
  		<col className="w-1/3" />
	    </colgroup>

            <thead>
              <tr className="bg-compliance-white">
                <th className="px-6 py-4 text-left text-carbon-graphite font-semibold">Feature</th>
                <th className="px-6 py-4 text-center">
                  <div className="space-y-2">
                    <div className="flex items-center justify-center space-x-2">
                      <span className="badge badge-fastest">Fastest Fix</span>
                    </div>
                    <div className="text-lg font-bold text-carbon-graphite">CBAM Express Fix</div>
                    <div className="text-2xl font-bold text-filentra-blue">€2,000</div>
                  </div>
                </th>
                <th className="px-6 py-4 text-center">
                  <div className="space-y-2">
                    <div className="flex items-center justify-center space-x-2">
                      <span className="badge badge-popular">Most Popular</span>
                    </div>
                    <div className="text-lg font-bold text-carbon-graphite">CBAM Filing Concierge</div>
                    <div className="text-2xl font-bold text-filentra-blue">€4,000 + add-ons</div>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              {features.map((feature, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-compliance-white' : 'bg-white'}>
                  <td className="px-6 py-4 font-medium text-carbon-graphite">
                    {feature.name}
                  </td>
                  <td className="px-6 py-4 text-center">
                    {typeof feature.express === 'boolean' ? (
                      feature.express ? (
                        <Check className="h-5 w-5 text-fast-pass-green mx-auto" />
                      ) : (
                        <X className="h-5 w-5 text-red-500 mx-auto" />
                      )
                    ) : (
                      <span className="text-sm text-gray-600">{feature.express}</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-center">
                    {typeof feature.concierge === 'boolean' ? (
                      feature.concierge ? (
                        <Check className="h-5 w-5 text-fast-pass-green mx-auto" />
                      ) : (
                        <X className="h-5 w-5 text-red-500 mx-auto" />
                      )
                    ) : (
                      <span className="text-sm text-gray-600">{feature.concierge}</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
<tfoot>
  <tr className="bg-compliance-white">
    <td className="px-6 py-4"></td>
    <td className="px-6 py-4 text-center">
      <a
        href="https://buy.stripe.com/3cI9ATbyKbBWdTwesvdfG01"
        target="_blank"
        rel="noopener noreferrer"
        className="w-full inline-block bg-filentra-blue text-white px-6 py-3 rounded-lg font-semibold text-center hover:bg-blue-700 transition-colors"
      >
        Buy Now
      </a>
    </td>
    <td className="px-6 py-4 text-center">
      <a
        href="https://buy.stripe.com/fZu8wP46ifSc9DgacfdfG03"
        target="_blank"
        rel="noopener noreferrer"
        className="w-full inline-block bg-fast-pass-green text-white px-6 py-3 rounded-lg font-semibold text-center hover:bg-green-600 transition-colors"
      >
        Buy Now
      </a>
    </td>
  </tr>
</tfoot>

          </table>
        </div>

<div className="text-center mt-8">
  <p className="text-gray-600 mb-4 text-sm md:text-base">
    Not sure which package is right for you?
  </p>
  <a 
    href="https://calendly.com/filentra/15min" 
    target="_blank"
    rel="noopener noreferrer"
    className="inline-block bg-white border border-filentra-blue text-filentra-blue px-6 py-2 rounded-full font-semibold text-sm md:text-base hover:bg-filentra-blue hover:text-white transition-colors"
  >
    Book a Free 15-min Call
  </a>
</div>


      </div>
    </section>
  );
};

export default ComparisonSection;