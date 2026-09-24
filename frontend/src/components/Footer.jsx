import { Link } from "react-router-dom";
import { Instagram, Mail, Phone } from "lucide-react";
import { COMPANY, DOWNLOADS, HOURS, SOURCES } from "../data/content";

export const Footer = () => (
  <footer className="relative overflow-hidden bg-navy text-sand grain" data-testid="footer">
    <div className="container-pcm grid gap-12 py-16 sm:py-20 lg:grid-cols-12">
      <div className="lg:col-span-5">
        <div className="inline-block bg-white px-4 py-3">
          <img src="/assets/logo_navy_white.png" alt="Paris Carrelages et Matériaux" className="h-12 w-auto" />
        </div>
        <p className="mt-6 font-display text-2xl italic text-sand/90">{COMPANY.baseline}.</p>
        <p className="mt-3 max-w-sm text-sm leading-relaxed text-sand/60">{COMPANY.hook}.</p>
        <p className="mt-6 font-mono text-[11px] uppercase tracking-[0.28em] text-terra-light">
          Négoce indépendant · Alfortville (94) · Depuis 2011
        </p>
      </div>
      <div className="lg:col-span-3">
        <p className="font-mono text-[11px] font-bold uppercase tracking-[0.28em] text-terra-light">Contact</p>
        <ul className="mt-5 space-y-3 text-sm text-sand/80">
          <li>{COMPANY.address1}<br />{COMPANY.address2}</li>
          <li>
            <a href={COMPANY.phoneHref} data-testid="footer-phone" className="flex items-center gap-2 transition-colors hover:text-white">
              <Phone size={13} /> {COMPANY.phone}
            </a>
          </li>
          <li>
            <a href={`mailto:${COMPANY.email}`} data-testid="footer-email" className="flex items-center gap-2 transition-colors hover:text-white">
              <Mail size={13} /> {COMPANY.email}
            </a>
          </li>
          <li>
            <a href={COMPANY.instagramHref} target="_blank" rel="noreferrer" data-testid="footer-instagram" className="flex items-center gap-2 transition-colors hover:text-white">
              <Instagram size={13} /> {COMPANY.instagram}
            </a>
          </li>
        </ul>
      </div>
      <div className="lg:col-span-2">
        <p className="font-mono text-[11px] font-bold uppercase tracking-[0.28em] text-terra-light">Horaires</p>
        <ul className="mt-5 space-y-2.5 text-[13px] text-sand/80">
          {HOURS.map((h) => (
            <li key={h.day}>
              <span className="block font-semibold text-sand">{h.day}</span>
              <span className="text-sand/60">{h.time}</span>
            </li>
          ))}
        </ul>
      </div>
      <div className="lg:col-span-2">
        <p className="font-mono text-[11px] font-bold uppercase tracking-[0.28em] text-terra-light">Documents</p>
        <ul className="mt-5 space-y-2.5 text-[13px]">
          {DOWNLOADS.map((d) => (
            <li key={d.id}>
              <a href={d.href} download data-testid={`footer-download-${d.id}`} className="link-underline text-sand/80 transition-colors hover:text-white">
                {d.title}
              </a>
            </li>
          ))}
          {SOURCES.map((s) => (
            <li key={s.id}>
              <a href={s.href} download data-testid={`footer-source-${s.id}`} className="link-underline text-sand/50 transition-colors hover:text-white">
                {s.title}
              </a>
            </li>
          ))}
          <li>
            <Link to="/catalogue" data-testid="footer-catalogue-link" className="link-underline text-sand/80 transition-colors hover:text-white">
              Consulter en ligne
            </Link>
          </li>
        </ul>
      </div>
    </div>
    <div className="border-t border-sand/15">
      <div className="container-pcm flex flex-col items-start justify-between gap-2 py-5 text-[11px] uppercase tracking-widest text-sand/40 sm:flex-row sm:items-center">
        <span>© 2026 {COMPANY.name}</span>
        <span>{COMPANY.website}</span>
      </div>
    </div>
  </footer>
);
