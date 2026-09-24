import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Menu, Phone, X } from "lucide-react";
import { COMPANY } from "../data/content";

const LINKS = [
  { name: "Accueil", path: "/" },
  { name: "L'Entreprise", path: "/entreprise" },
  { name: "Parcours du chantier", path: "/parcours" },
  { name: "Catalogue", path: "/catalogue" },
  { name: "Fabricants", path: "/fabricants" },
  { name: "Contact", path: "/contact" },
];

export const Nav = ({ onDevis }) => {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  useEffect(() => setOpen(false), [location.pathname]);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-line/80 bg-sand/90 backdrop-blur-xl">
      <div className="container-pcm flex h-16 items-center justify-between gap-4 sm:h-20">
        <Link to="/" data-testid="nav-logo" className="flex shrink-0 items-center gap-3">
          <img src="/assets/logo_navy_white.png" alt="Paris Carrelages et Matériaux" className="h-9 w-auto sm:h-11" />
        </Link>
        <nav className="hidden items-center gap-7 lg:flex" data-testid="nav-links">
          {LINKS.slice(1).map((l) => (
            <NavLink
              key={l.path}
              to={l.path}
              data-testid={`nav-${l.path.slice(1)}`}
              className={({ isActive }) =>
                `link-underline text-[13px] font-semibold tracking-wide transition-colors duration-300 ${
                  isActive ? "text-terra" : "text-ink hover:text-terra"
                }`
              }
            >
              {l.name}
            </NavLink>
          ))}
        </nav>
        <div className="hidden items-center gap-3 lg:flex">
          <a
            href={COMPANY.phoneHref}
            data-testid="nav-phone-button"
            className="flex items-center gap-2 border border-navy/25 px-4 py-2 text-[13px] font-semibold text-navy transition-colors duration-300 hover:border-navy hover:bg-navy hover:text-sand"
          >
            <Phone size={14} strokeWidth={2.2} />
            {COMPANY.phone}
          </a>
          <button
            onClick={onDevis}
            data-testid="nav-devis-button"
            className="bg-terra px-5 py-2 text-[13px] font-bold uppercase tracking-wider text-white transition-colors duration-300 hover:bg-terra-dark"
          >
            Demander un devis
          </button>
        </div>
        <button
          className="p-2 lg:hidden"
          onClick={() => setOpen(!open)}
          data-testid="nav-mobile-toggle"
          aria-label="Menu"
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>
      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            className="overflow-hidden border-t border-line bg-sand lg:hidden"
            data-testid="nav-mobile-menu"
          >
            <div className="container-pcm flex flex-col gap-1 py-4">
              {LINKS.map((l) => (
                <NavLink
                  key={l.path}
                  to={l.path}
                  data-testid={`nav-mobile-${l.path === "/" ? "accueil" : l.path.slice(1)}`}
                  className={({ isActive }) =>
                    `py-2.5 font-display text-2xl ${isActive ? "italic text-terra" : "text-ink"}`
                  }
                >
                  {l.name}
                </NavLink>
              ))}
              <button
                onClick={() => { setOpen(false); onDevis(); }}
                data-testid="nav-mobile-devis-button"
                className="mt-3 bg-terra px-5 py-3 text-sm font-bold uppercase tracking-wider text-white"
              >
                Demander un devis
              </button>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
};
