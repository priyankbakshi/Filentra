import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FileText, Menu, X } from 'lucide-react';

const Navigation = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    if (location.pathname !== '/') {
      window.location.href = `/#${sectionId}`;
      return;
    }

    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-md' : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="flex items-center space-x-2">
            <FileText className={`h-8 w-8 ${isScrolled ? 'text-filentra-blue' : 'text-white'}`} />
            <span className={`text-xl font-bold ${isScrolled ? 'text-carbon-graphite' : 'text-white'}`}>
              Filentra
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center space-x-8">
            <button
              onClick={() => scrollToSection('services')}
              className={`hover:text-filentra-blue transition-colors ${
                isScrolled ? 'text-carbon-graphite' : 'text-white'
              }`}
            >
              Services
            </button>
            <button
              onClick={() => scrollToSection('comparison')}
              className={`hover:text-filentra-blue transition-colors ${
                isScrolled ? 'text-carbon-graphite' : 'text-white'
              }`}
            >
              Pricing
            </button>
            <Link
              to="/about"
              className={`hover:text-filentra-blue transition-colors ${
                isScrolled ? 'text-carbon-graphite' : 'text-white'
              }`}
            >
              About
            </Link>
          </div>

          {/* Mobile Toggle */}
          <button
            className={`md:hidden ${isScrolled ? 'text-carbon-graphite' : 'text-white'}`}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Dropdown */}
        {isMobileMenuOpen && (
          <div className="md:hidden bg-white border-t shadow">
            <div className="px-4 pt-4 pb-3 space-y-2">
              <button
                onClick={() => scrollToSection('services')}
                className="block w-full text-left text-carbon-graphite hover:text-filentra-blue"
              >
                Services
              </button>
              <button
                onClick={() => scrollToSection('comparison')}
                className="block w-full text-left text-carbon-graphite hover:text-filentra-blue"
              >
                Pricing
              </button>
              <Link
                to="/about"
                className="block text-carbon-graphite hover:text-filentra-blue"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                About
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
