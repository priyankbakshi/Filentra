import React from 'react';
import { Quote } from 'lucide-react';

const TestimonialsSection = () => {
  const testimonials = [
    {
      text: "We thought we'd miss the filing deadline. Filentra turned our messy spreadsheet into a clean, accepted XML in 3 days flat.",
      author: "Supply Chain Head",
      company: "Aluminium Importer",
      alignment: "left"
    },
    {
      text: "Didn't expect a refund clause from a compliance vendor. These guys actually delivered.",
      author: "COO",
      company: "Fertilizer Importer, France",
      alignment: "right"
    },
    {
      text: "Finally a team that understands schemas and deadlines. Clean work, no jargon.",
      author: "EU Customs Broker",
      company: "Rotterdam",
      alignment: "center"
    },
    {
      text: "We used Filentra for Q1 late filing. No issues. Delivered in time, refunded our overpayment.",
      author: "CFO",
      company: "Mid-size Steel Firm",
      alignment: "left"
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            What our clients say
          </h2>
          <div className="w-24 h-1 bg-filentra-blue mx-auto"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials.map((testimonial, index) => (
            <div 
              key={index}
              className={`bg-compliance-white p-8 rounded-xl hover-lift fade-in transform ${
                testimonial.alignment === 'right' ? 'md:translate-y-8' : 
                testimonial.alignment === 'center' ? 'md:translate-y-4' : ''
              }`}
              style={{ animationDelay: `${index * 0.2}s` }}
            >
              <Quote className="h-8 w-8 text-filentra-blue mb-4" />
              <blockquote className="text-gray-700 mb-6 leading-relaxed">
                "{testimonial.text}"
              </blockquote>
              <div className="text-sm">
                <div className="font-semibold text-carbon-graphite">{testimonial.author}</div>
                <div className="text-gray-500">{testimonial.company}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;