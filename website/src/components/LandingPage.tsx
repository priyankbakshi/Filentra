import React from 'react';
import Navigation from './Navigation';
import HeroSection from './sections/HeroSection';
import ProblemSection from './sections/ProblemSection';
import ServicesSection from './sections/ServicesSection';
import ComparisonSection from './sections/ComparisonSection';
import WhyFilentraSection from './sections/WhyFilentraSection';
import TestimonialsSection from './sections/TestimonialsSection';
import Footer from './Footer';

const LandingPage = () => {
  return (
    <div className="min-h-screen">
      <Navigation />
      <HeroSection />
      <ProblemSection />
      <ServicesSection />
      <ComparisonSection />
      <WhyFilentraSection />
      <TestimonialsSection />
      <Footer />
    </div>
  );
};

export default LandingPage;