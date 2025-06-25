import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import AboutPage from './components/AboutPage';
import ThankYouExpress from './components/ThankYouExpress';
import ThankYouConcierge from './components/ThankYouConcierge';
import ScrollToTop from './ScrollToTop';


function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="min-h-screen bg-compliance-white">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/thank-you-express" element={<ThankYouExpress />} />
          <Route path="/thank-you-concierge" element={<ThankYouConcierge />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;