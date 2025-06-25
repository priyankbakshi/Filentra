import React from 'react';
import { AlertTriangle, Clock, FileX, Users, Euro } from 'lucide-react';

const ProblemSection = () => {
  const problems = [
    {
      icon: FileX,
      title: "Schema errors (XSD-072) trigger NCA warnings",
      description: "Technical validation failures create compliance risks"
    },
    {
      icon: Clock,
      title: "Supplier delays make accurate filings impossible",
      description: "Dependency on slow supplier responses threatens deadlines"
    },
    {
      icon: Euro,
      title: "Q2 deadline: €50/t late-report fines start 31 July",
      description: "Financial penalties escalate quickly for missed submissions"
    },
    {
      icon: Users,
      title: "From Jan 2026, only Authorised Declarants may import",
      description: "New regulatory requirements demand advanced preparation"
    },
    {
      icon: AlertTriangle,
      title: "Big Four audit firms are already at capacity",
      description: "Traditional advisory services can't meet demand surge"
    }
  ];

  return (
    <section className="-mt-[2px] py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-carbon-graphite mb-4">
            Why EU importers are stuck
          </h2>
          <div className="w-24 h-1 bg-filentra-blue mx-auto"></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {problems.map((problem, index) => (
            <div 
              key={index}
              className="bg-compliance-white p-6 rounded-lg hover-lift fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <problem.icon className="h-12 w-12 text-filentra-blue mb-4" />
              <h3 className="text-lg font-semibold text-carbon-graphite mb-2">
                {problem.title}
              </h3>
              <p className="text-gray-600">
                {problem.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProblemSection;