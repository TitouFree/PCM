import { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes, useLocation } from "react-router-dom";
import Lenis from "lenis";
import { AnimatePresence, motion } from "framer-motion";
import { Toaster } from "sonner";
import "@/index.css";
import { Nav } from "./components/Nav";
import { Footer } from "./components/Footer";
import { DevisModal } from "./components/DevisModal";
import Home from "./pages/Home";
import Entreprise from "./pages/Entreprise";
import Parcours from "./pages/Parcours";
import Catalogue from "./pages/Catalogue";
import Fabricants from "./pages/Fabricants";
import Contact from "./pages/Contact";

const PageWrap = ({ children }) => (
  <motion.main
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -10 }}
    transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
  >
    {children}
  </motion.main>
);

const Shell = () => {
  const [devisOpen, setDevisOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    let raf;
    const loop = (t) => { lenis.raf(t); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    return () => { cancelAnimationFrame(raf); lenis.destroy(); };
  }, []);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
  }, [location.pathname]);

  const openDevis = () => setDevisOpen(true);

  return (
    <div className="min-h-screen bg-sand font-body text-ink">
      <Nav onDevis={openDevis} />
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<PageWrap><Home onDevis={openDevis} /></PageWrap>} />
          <Route path="/entreprise" element={<PageWrap><Entreprise onDevis={openDevis} /></PageWrap>} />
          <Route path="/parcours" element={<PageWrap><Parcours onDevis={openDevis} /></PageWrap>} />
          <Route path="/catalogue" element={<PageWrap><Catalogue /></PageWrap>} />
          <Route path="/fabricants" element={<PageWrap><Fabricants /></PageWrap>} />
          <Route path="/contact" element={<PageWrap><Contact onDevis={openDevis} /></PageWrap>} />
          <Route path="*" element={<PageWrap><Home onDevis={openDevis} /></PageWrap>} />
        </Routes>
      </AnimatePresence>
      <Footer />
      <DevisModal open={devisOpen} onClose={() => setDevisOpen(false)} />
      <Toaster position="bottom-right" richColors />
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <Shell />
    </BrowserRouter>
  );
}

export default App;
