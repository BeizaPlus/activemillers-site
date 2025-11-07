import HeroSection from './components/HeroSection';
import MobileHeroSection from './components/MobileHeroSection';
import SocialSection from './components/SocialSection';

function App() {
  return (
    <div className="min-h-screen bg-white">
      {/* Desktop Hero Section */}
      <div className="hidden lg:block">
        <HeroSection />
      </div>

      {/* Mobile Hero Section */}
      <div className="block lg:hidden">
        <MobileHeroSection />
      </div>

      {/* Social Section */}
      <SocialSection />
    </div>
  );
}

export default App;