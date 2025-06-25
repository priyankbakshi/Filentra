import React from 'react';
import Navigation from './Navigation';
import Footer from './Footer';
import { CheckCircle, Users, Clock, FileText, MessageCircle } from 'lucide-react';

const ThankYouConcierge = () => {
  const steps = [
    {
      icon: Clock,
      title: "Within 12 business hours",
      description: "You'll get a secure link to upload your CBAM data + supplier list"
    },
    {
      icon: Users,
      title: "Day 1: Supplier outreach begins",
      description: "We begin supplier outreach (email + voicemail) within 1 business day"
    },
    {
      icon: FileText,
      title: "Day 5: Filing execution",
      description: "On Day 5, we file your XML based on received data or fallback logic"
    },
    {
      icon: CheckCircle,
      title: "8 business days maximum",
      description: "Delivery within 8 business days max (5-day outreach + 3-day processing)"
    }
  ];

  return (
    <div className="min-h-screen">
      <Navigation />
      
      <section className="pt-24 pb-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <CheckCircle className="h-16 w-16 text-fast-pass-green mx-auto mb-6" />
            <h1 className="text-4xl md:text-5xl font-bold text-carbon-graphite mb-6">
              Thanks for your payment.{' '}
              <span className="text-filentra-blue">Supplier outreach begins.</span>
            </h1>
            <p className="text-xl text-gray-600">
              You've purchased the CBAM Filing Concierge package. Here's what to expect:
            </p>
          </div>

          <div className="space-y-8 mb-16">
            {steps.map((step, index) => (
              <div key={index} className="flex items-start space-x-6 p-6 bg-compliance-white rounded-lg">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-filentra-blue text-white rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <step.icon className="h-6 w-6 text-filentra-blue" />
                    <h3 className="text-lg font-semibold text-carbon-graphite">
                      {step.title}
                    </h3>
                  </div>
                  <p className="text-gray-600">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-gradient-to-r from-filentra-blue to-blue-800 text-white p-8 rounded-xl mb-8">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <MessageCircle className="h-6 w-6 mr-2" />
              Support Contact
            </h3>
            <p className="text-blue-100">
              <strong>priyank@filentra.com</strong>
            </p>
          </div>

          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 text-center">
              <strong>Data Handling:</strong> GDPR compliant, secure uploads, Proton Drive or Zoho WorkDrive optional
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ThankYouConcierge;