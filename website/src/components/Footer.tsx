import React from 'react';
import { FileText, Mail } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-carbon-graphite text-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <FileText className="h-8 w-8 text-fast-pass-green" />
              <span className="text-2xl font-bold">Filentra</span>
            </div>
            <p className="text-gray-300 mb-6 leading-relaxed">
              Helping EU importers achieve CBAM compliance with speed, certainty, and expert execution.
            </p>
            <div className="flex items-center space-x-2 text-gray-300">
              <Mail className="h-5 w-5" />
              <span>priyank@filentra.com</span>
            </div>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Services</h4>
            <ul className="space-y-2 text-gray-300">
              <li>CBAM Express Fix</li>
              <li>CBAM Filing Concierge</li>
              <li>Authorised Declarant Pack</li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Company</h4>
            <ul className="space-y-2 text-gray-300">
              <li>About Us</li>
              <li>Contact</li>
              <li>Refund Terms</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-12 pt-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
            <div className="text-gray-300 text-sm">
              <p>Filentra Ltd (London, pending incorporation)</p>
              <p>Refund terms based on XML validation only</p>
            </div>
            <div className="text-gray-300 text-sm md:text-right">
              <p>Stripe-secured payment</p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;