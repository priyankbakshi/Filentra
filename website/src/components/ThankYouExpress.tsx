import React from 'react';
import Navigation from './Navigation';
import Footer from './Footer';
import { CheckCircle, Clock, Shield, MessageCircle } from 'lucide-react';

const ThankYouExpress = () => {
  const steps = [
    {
      icon: Clock,
      title: "Within 12 business hours",
      description: "We'll send you a secure upload link for your CBAM spreadsheet"
    },
    {
      icon: CheckCircle,
      title: "Immediate processing",
      description: "We begin work immediately once data is received"
    },
    {
      icon: Shield,
      title: "72-hour delivery",
      description: "Delivery guaranteed within 72 hours (working days)"
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
              <span className="text-filentra-blue">We're getting started.</span>
            </h1>
            <p className="text-xl text-gray-600">
              You've purchased the CBAM Express Fix package. Here's what happens next:
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

          <div className="bg-gradient-to-r from-filentra-blue to-blue-800 text-white p-8 rounded-xl">
            <h3 className="text-xl font-bold mb-4 flex items-center">
              <MessageCircle className="h-6 w-6 mr-2" />
              Support Contact
            </h3>
            <p className="mb-4">
              <strong>priyank@filentra.com</strong>
            </p>
            <p className="text-blue-100">
              (Respond within 1 business day)
            </p>
          </div>

          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600 text-center">
              <strong>Note:</strong> All data processed under GDPR. Files are encrypted.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default ThankYouExpress;