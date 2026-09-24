import { Instagram, Mail, MapPin, Phone, Truck } from "lucide-react";
import { Reveal } from "../components/Reveal";
import { COMPANY, DELIVERY, HOURS } from "../data/content";

const Contact = ({ onDevis }) => (
  <>
    <section className="bg-navy pb-16 pt-36 text-sand grain sm:pt-44" data-testid="contact-hero">
      <div className="container-pcm">
        <p className="eyebrow-light">Contact & accès</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-medium leading-[1.08] sm:text-6xl">
          Le comptoir est ouvert <span className="italic text-terra-light">dès 6 h 30.</span>
        </h1>
      </div>
    </section>

    <section className="container-pcm py-16 sm:py-24" data-testid="contact-content">
      <div className="grid gap-10 lg:grid-cols-12">
        <Reveal className="lg:col-span-5">
          <div className="space-y-8">
            <div>
              <p className="eyebrow flex items-center gap-2"><MapPin size={13} /> Adresse</p>
              <p className="mt-3 font-display text-2xl font-medium leading-snug text-ink">
                {COMPANY.address1}<br />{COMPANY.address2}
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <a
                href={COMPANY.phoneHref}
                data-testid="contact-phone-button"
                className="flex items-center gap-2 bg-navy px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-sand transition-colors duration-300 hover:bg-navy-soft"
              >
                <Phone size={14} /> {COMPANY.phone}
              </a>
              <a
                href={`mailto:${COMPANY.email}`}
                data-testid="contact-email-button"
                className="flex items-center gap-2 border border-navy/30 px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-navy transition-colors duration-300 hover:bg-navy hover:text-sand"
              >
                <Mail size={14} /> {COMPANY.email}
              </a>
            </div>
            <div className="flex flex-wrap gap-x-8 gap-y-2 text-sm text-slate">
              <span>{COMPANY.website}</span>
              <a href={COMPANY.instagramHref} target="_blank" rel="noreferrer" data-testid="contact-instagram" className="flex items-center gap-1.5 transition-colors hover:text-terra">
                <Instagram size={14} /> {COMPANY.instagram}
              </a>
            </div>
            <div className="overflow-hidden border border-line">
              <img src="/assets/plan_acces.png" alt="Plan d'accès — 110 rue Édouard Vaillant, Alfortville" className="w-full" data-testid="contact-map" />
            </div>
          </div>
        </Reveal>

        <div className="lg:col-span-7">
          <Reveal>
            <div className="border border-line bg-white p-7 sm:p-9" data-testid="contact-hours-card">
              <p className="eyebrow">Horaires</p>
              <ul className="mt-5 divide-y divide-line">
                {HOURS.map((h) => (
                  <li key={h.day} className="flex items-center justify-between gap-4 py-3.5" data-testid={`hours-${h.day}`}>
                    <span className="text-sm font-bold text-ink">{h.day}</span>
                    <span className={`text-sm ${h.time === "Fermé" ? "font-semibold text-terra" : "text-slate"}`}>{h.time}</span>
                  </li>
                ))}
              </ul>
            </div>
          </Reveal>

          <Reveal delay={0.1}>
            <div className="mt-6 border border-line bg-white p-7 sm:p-9" data-testid="contact-delivery-card">
              <p className="eyebrow flex items-center gap-2"><Truck size={13} /> Nous livrons</p>
              <div className="mt-5 flex flex-wrap gap-2">
                {DELIVERY.zones.map((z) => (
                  <span key={z} className="border border-line bg-sand px-3.5 py-1.5 text-xs font-semibold text-ink" data-testid={`zone-${z}`}>
                    {z}
                  </span>
                ))}
              </div>
              <p className="mt-4 text-sm leading-relaxed text-slate">
                {DELIVERY.note} {DELIVERY.fleet} Livraison sous 24 h.
              </p>
            </div>
          </Reveal>

          <Reveal delay={0.15}>
            <div className="mt-6 bg-terra p-7 text-white sm:p-9" data-testid="contact-devis-card">
              <p className="font-mono text-[11px] font-bold uppercase tracking-[0.28em] text-white/75">Devis</p>
              <h2 className="mt-3 font-display text-2xl font-medium sm:text-3xl">Passez au comptoir — ou demandez un devis en ligne.</h2>
              <p className="mt-3 max-w-lg text-sm leading-relaxed text-white/85">
                Professionnels du bâtiment et particuliers. Réseau de poseurs de
                confiance sur demande.
              </p>
              <button
                onClick={onDevis}
                data-testid="contact-devis-button"
                className="mt-6 bg-white px-7 py-3.5 text-xs font-bold uppercase tracking-widest text-terra transition-colors duration-300 hover:bg-sand"
              >
                Demander un devis
              </button>
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  </>
);

export default Contact;
