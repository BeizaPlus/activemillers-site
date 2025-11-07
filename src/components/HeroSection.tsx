import React from 'react';
import ActiveLogo from './ActiveLogo';
import EmailSignupForm from './EmailSignupForm';

const HeroSection: React.FC = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Ken Burns Effect */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat ken-burns"
        style={{
          backgroundImage: 'url("http://activemillers.com/wp-content/uploads/2025/09/ActiveWebsite_Overhaul_v4.png")'
        }}
      />

      {/* Background Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-white via-white/20 to-transparent mix-blend-screen opacity-100" />

      {/* Content Container */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center min-h-screen py-12 lg:py-20">

          {/* Left Column - Logo */}
          <div className="flex justify-center lg:justify-start order-2 lg:order-1">
            <div className="w-3/5 sm:w-2/5 lg:w-2/5 max-w-xs">
              <ActiveLogo className="w-full h-auto opacity-90" />
            </div>
          </div>

          {/* Right Column - Form */}
          <div className="flex justify-center lg:justify-center order-1 lg:order-2">
            <div className="w-full max-w-md">
              <EmailSignupForm />
            </div>
          </div>
        </div>

        {/* Bottom Section with CTA and Heading */}
        <div className="relative z-10 flex flex-col items-center justify-end pb-12 lg:pb-20">
          <div className="text-center space-y-6 lg:space-y-8">
            {/* CTA Button */}
            <div className="mb-6 lg:mb-8">
              <a
                href="mailto:info@activemillers.com"
                className="inline-flex items-center justify-center bg-red-600 text-white font-black text-base lg:text-lg uppercase px-6 py-3 rounded-lg border-4 lg:border-8 border-red-600 shadow-2xl hover:bg-red-700 hover:transform hover:-translate-y-1 transition-all duration-300"
              >
                let's talk
              </a>
            </div>

            {/* Heading */}
            <h3 className="text-3xl sm:text-4xl lg:text-5xl font-black text-black uppercase tracking-wider leading-tight drop-shadow-sm">
              Immersive Pieces.
            </h3>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
