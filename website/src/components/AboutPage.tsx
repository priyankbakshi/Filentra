import React from 'react';
import Navigation from './Navigation';
import Footer from './Footer';
import { ArrowRight, Target, Shield, Users } from 'lucide-react';

const AboutPage = () => {
  const scrollToComparison = () => {
    window.location.href = '/#comparison';
  };

  const values = [
    {
      icon: Target,
      title: "Precision",
      description: "We never guess. Every submission is schema-tested."
    },
    {
      icon: Shield,
      title: "Clarity",
      description: "No jargon. We speak the language of customs officers, not consultants."
    },
    {
      icon: Users,
      title: "Accountability",
      description: "Refund-backed. SLA-based. Outcome-first."
    }
  ];

  return (
    <div className="min-h-screen">
      <Navigation />
      
      <section className="pt-24 pb-20 bg-gradient-to-br from-filentra-blue to-blue-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Built for speed.{' '}
            <span className="text-fast-pass-green">Backed by real execution.</span>
          </h1>
          <p className="text-xl text-blue-100 leading-relaxed">
            Filentra is not a law firm or a consultancy. We're a founder-led compliance engine 
            that solves filings fast and protects your import rights.
          </p>
        </div>
      </section>

      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-carbon-graphite mb-8">Who We Are</h2>
          
          <div className="prose prose-lg text-gray-600 space-y-6">
            <ul className="space-y-4">
              <li className="flex items-start">
                <span className="block w-2 h-2 bg-filentra-blue rounded-full mt-3 mr-4 flex-shrink-0"></span>
                <span>Based in London, serving EU importers across iron and steel, cement, aluminium, fertilisers, electricity, and hydrogen sectors.</span>
              </li>
              <li className="flex items-start">
                <span className="block w-2 h-2 bg-filentra-blue rounded-full mt-3 mr-4 flex-shrink-0"></span>
                <span>Founder-led, with background in cross-border staffing, logistics regulation, and emissions policy navigation.</span>
              </li>
              <li className="flex items-start">
                <span className="block w-2 h-2 bg-filentra-blue rounded-full mt-3 mr-4 flex-shrink-0"></span>
                <span>We've scaled platforms for 700+ clients and handled filings across 10+ jurisdictions in past ventures.</span>
              </li>
              <li className="flex items-start">
                <span className="block w-2 h-2 bg-filentra-blue rounded-full mt-3 mr-4 flex-shrink-0"></span>
                <span>Direct access to our founder — not junior analysts or templated chatbots.</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section className="py-20 bg-compliance-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-carbon-graphite mb-8">Why We Exist</h2>
          
          <div className="prose prose-lg text-gray-600 space-y-6">
            <p>
              The EU's CBAM regime is moving faster than traditional advisory can handle.
            </p>
            <p>
              Importers need rapid, schema-valid XMLs, fallback legal logic, and human-led outreach — 
              not 60-page PDFs or PowerPoint slide decks.
            </p>
            <p>
              We built Filentra to solve for velocity, certainty, and defensibility.
            </p>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-carbon-graphite mb-16 text-center">Our Values</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <div 
                key={index}
                className="text-center p-8 bg-compliance-white rounded-xl hover-lift"
              >
                <value.icon className="h-16 w-16 text-filentra-blue mx-auto mb-6" />
                <h3 className="text-xl font-bold text-carbon-graphite mb-4">
                  {value.title}
                </h3>
                <p className="text-gray-600">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

{/*      <section className="py-20 bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-500">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-carbon-graphite mb-6">
            31 July CBAM deadline is approaching fast.
          </h2>
          <button
            onClick={scrollToComparison}
            className="inline-flex items-center bg-fast-pass-green text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-green-600 transition-all duration-200 hover-lift"
          >
            Explore Compliance Packages
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </div>
      </section>
*/}
      <Footer />
    </div>
  );
};

export default AboutPage;