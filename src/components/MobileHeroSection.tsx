import React from 'react';
import ActiveLogo from './ActiveLogo';

const MobileHeroSection: React.FC = () => {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: 'url("http://activemillers.com/wp-content/uploads/2025/09/ActiveWebsite_Overhaul_Mobile_V1.png")'
        }}
      />

      {/* Background Overlay for better text readability */}
      <div className="absolute inset-0 bg-black/20" />

      {/* Content Container */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-6 flex flex-col items-center justify-center min-h-screen py-12 space-y-8">

        {/* Logo */}
        <div className="mb-8">
          <ActiveLogo className="w-24 h-auto mx-auto" />
        </div>

        {/* CTA Button */}
        <div className="mb-6">
          <a
            href="https://gem.godaddy.com/signups/176cee535f3e46b081fddeedb369bf0e/join"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center bg-red-600 text-white font-black text-base uppercase px-6 py-3 rounded-lg border-4 border-red-600 shadow-2xl hover:bg-red-700 hover:transform hover:-translate-y-1 transition-all duration-300"
          >
            Get Free ePUB
          </a>
        </div>

        {/* Heading */}
        <h1 className="text-3xl sm:text-4xl font-black text-white uppercase tracking-wider leading-tight text-center px-4 drop-shadow-lg">
          Immersive Pieces
        </h1>
      </div>
    </section>
  );
};

export default MobileHeroSection;
