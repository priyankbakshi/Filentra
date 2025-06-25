import React from 'react';
import { ArrowDown } from 'lucide-react';

const HeroSection = () => {
  const scrollToComparison = () => {
    const element = document.getElementById('comparison');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="gradient-hero min-h-screen flex items-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-filentra-blue/90 to-blue-800/90" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="text-white space-y-8 fade-in">
            <h1 className="text-4xl md:text-6xl font-bold leading-tight">
              CBAM compliance.{' '}
              <span className="text-fast-pass-green">Delivered.</span>
            </h1>

            <p className="text-xl md:text-2xl text-blue-100 leading-relaxed">
              Filentra fixes your CBAM filings fast, gets XMLs accepted first-time, 
              and helps you stay compliant—all before the deadline and penalties hit.
            </p>

            <button
              onClick={scrollToComparison}
              className="inline-flex items-center bg-fast-pass-green text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-green-600 transition-all duration-200 hover-lift focus:outline-none focus-visible:ring-2 focus-visible:ring-white"
            >
              Explore Compliance Packages
              <ArrowDown className="ml-2 h-5 w-5" />
            </button>
          </div>

          <div className="lg:flex justify-center items-center">
            <div className="float-animation">
              <img
                src="/hero-visual.png"
                alt="CBAM Compliance Supply Chain"
                className="w-full max-w-lg rounded-lg shadow-2xl"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Wave bottom - cleaned */}
      <div className="absolute bottom-0 left-0 w-full overflow-hidden block bg-gradient-to-br from-filentra-blue/90 to-blue-800/90">
        <svg viewBox="0 0 1428 174" className="w-full h-auto block align-bottom">
          <g stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
            <g transform="translate(-2.000000, 44.000000)" fill="#FFFFFF" fillRule="nonzero">
              <path d="M0,0 C90.7283404,0.927527913 147.912752,27.187927 291.910178,59.9119003 C387.908462,81.7278826 543.605069,89.334785 759,82.7326078 C469.336065,156.254352 216.336065,153.6679 0,74.9732496" opacity="0.100000001"></path>
              <path d="M100,104.708498 C277.413333,72.2345949 426.147877,52.5246657 546.203633,45.5787101 C666.259389,38.6327546 810.524845,41.7979068 979,55.0741668 C931.069965,56.122511 810.303266,74.8455141 616.699903,111.243176 C423.096539,147.640838 250.863238,145.462612 100,104.708498 Z" opacity="0.100000001"></path>
              <path d="M1046,51.6521276 C1130.83045,29.328812 1279.08318,17.607883 1439,40.1656806 L1439,120 C1271.17211,77.9435312 1140.17211,55.1609071 1046,51.6521276 Z" opacity="0.200000003"></path>
            </g>
            <g transform="translate(-4.000000, 76.000000)" fill="#FFFFFF" fillRule="nonzero">
              <path d="M0.457,34.035 C57.086,53.198 98.208,65.809 123.822,71.865 C181.454,85.495 234.295,90.29 272.033,93.459 C311.355,96.759 396.635,95.801 461.025,91.663 C486.76,90.01 518.727,86.372 556.926,80.752 C595.747,74.596 622.372,70.008 636.799,66.991 C663.913,61.324 712.501,49.503 727.605,46.128 C780.47,34.317 818.839,22.532 856.324,15.904 C922.689,4.169 955.676,2.522 1011.185,0.432 C1060.705,1.477 1097.39,3.129 1121.236,5.387 C1161.703,9.219 1208.621,17.821 1235.4,22.304 C1285.855,30.748 1354.351,47.432 1440.886,72.354 L1441.191,104.352 L1.121,104.031 L0.457,34.035 Z"></path>
            </g>
          </g>
        </svg>
      </div>
    </section>
  );
};

export default HeroSection;
