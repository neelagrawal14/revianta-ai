import FuturisticBackground from '../../components/common/FuturisticBackground';
import LandingNav from '../../components/landing/LandingNav';
import Hero from '../../components/landing/Hero';
import ProblemSection from '../../components/landing/ProblemSection';
import HowItWorks from '../../components/landing/HowItWorks';
import IntelligenceEngine from '../../components/landing/IntelligenceEngine';
import ResearchWorkspace from '../../components/landing/ResearchWorkspace';
import RiskIntelligence from '../../components/landing/RiskIntelligence';
import KnowledgeGraphSection from '../../components/landing/KnowledgeGraphSection';
import ResearchExplorer from '../../components/landing/ResearchExplorer';
import FinalCTA from '../../components/landing/FinalCTA';
import Footer from '../../components/landing/Footer';

export default function LandingPage() {
  return (
    <div className="relative">
      <FuturisticBackground variant="cinematic" />
      <LandingNav />
      <Hero />
      <ProblemSection />
      <HowItWorks />
      <IntelligenceEngine />
      <ResearchWorkspace />
      <RiskIntelligence />
      <KnowledgeGraphSection />
      <ResearchExplorer />
      <FinalCTA />
      <Footer />
    </div>
  );
}
