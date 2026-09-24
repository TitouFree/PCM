import { useRef } from "react";
import { Link } from "react-router-dom";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowDown, ArrowRight, Download, FileText, Phone } from "lucide-react";
import { MaskedLine, Reveal } from "../components/Reveal";
import { Marquee } from "../components/Marquee";
import { COMPANY, DOWNLOADS, FAMILIES } from "../data/content";

const STATS = [
  { value: "2011", label: "Négoce indépendant" },
  { value: "11", label: "Familles de produits" },
  { value: "24 h", label: "Livraison chantier" },
  { value: "6 h 30", label: "Ouverture du comptoir" },
];

const Hero = ({ onDevis }) => {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "22%"]);
  const scale = useTransform(scrollYProgress, [0, 1], [1.02, 1.12]);

  return (
    <section ref={ref} className="relative flex min-h-[100svh] items-end overflow-hidden bg-navy-deep grain" data-testid="hero">
      <motion.div className="absolute inset-0" style={{ y, scale }}>
        <img
          src="/assets/cover_herringbone.png"
          alt="Sol en bâtons rompus — showroom Paris Carrelages et Matériaux"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-navy-deep via-navy-deep/35 to-navy-deep/10" />
      </motion.div>

      <div className="container-pcm relative z-10 w-full pb-24 pt-40 sm:pb-28">
        <div className="mb-6 overflow-hidden">
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 0.2 }}
            className="eyebrow-light"
          >
            Négoce de matériaux · Alfortville (94) · Depuis 2011
          </motion.p>
        </div>
        <h1 className="font-display text-[13vw] font-medium leading-[1.02] tracking-tight text-sand sm:text-7xl lg:text-[6.2rem]" data-testid="hero-title">
          <MaskedLine delay={0.35}>Des fondations</MaskedLine>
          <MaskedLine delay={0.5} className="italic text-terra-light">aux finitions.</MaskedLine>
        </h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 0.85, ease: [0.16, 1, 0.3, 1] }}
          className="mt-6 max-w-xl text-base leading-relaxed text-sand/85 sm:text-lg"
        >
          {COMPANY.hook}. Gros œuvre, toiture, isolation, plâtrerie, carrelage,
          peinture, machines et protection de chantier — tout votre chantier,
          chez un seul négoce indépendant.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.9, delay: 1.05, ease: [0.16, 1, 0.3, 1] }}
          className="mt-9 flex flex-wrap items-center gap-4"
        >
          <button
            onClick={onDevis}
            data-testid="hero-devis-button"
            className="group flex items-center gap-3 bg-terra px-7 py-4 text-sm font-bold uppercase tracking-widest text-white transition-all duration-300 hover:bg-terra-dark"
          >
            Demander un devis
            <ArrowRight size={16} className="transition-transform duration-300 group-hover:translate-x-1" />
          </button>
          <a
            href="#telechargements"
            data-testid="hero-downloads-button"
            className="flex items-center gap-3 border border-sand/40 px-7 py-4 text-sm font-bold uppercase tracking-widest text-sand transition-all duration-300 hover:border-sand hover:bg-sand hover:text-navy"
          >
            <Download size={16} />
            Les plaquettes PDF
          </a>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6, duration: 1 }}
        className="absolute bottom-6 right-6 hidden items-center gap-2 font-mono text-[10px] uppercase tracking-[0.3em] text-sand/60 sm:flex"
      >
        Défiler <ArrowDown size={12} className="animate-bounce" />
      </motion.div>
    </section>
  );
};

const Downloads = () => (
  <section id="telechargements" className="container-pcm py-20 sm:py-28" data-testid="downloads-section">
    <Reveal>
      <p className="eyebrow">Documents officiels</p>
      <h2 className="mt-3 max-w-2xl font-display text-3xl font-medium leading-tight text-ink sm:text-5xl">
        Deux plaquettes, un catalogue. <span className="italic text-terra">À emporter.</span>
      </h2>
      <p className="mt-4 max-w-2xl text-base leading-relaxed text-slate">
        La plaquette courte pour la prospection et les rendez-vous, la plaquette
        complète avec toutes les références du catalogue général, et le catalogue
        d'origine. Versions haute qualité pour l'impression, versions allégées pour l'e-mail.
      </p>
    </Reveal>
    <div className="mt-12 grid gap-6 lg:grid-cols-12">
      {DOWNLOADS.map((d, i) => (
        <Reveal
          key={d.id}
          delay={i * 0.12}
          className={i === 0 ? "lg:col-span-5" : i === 1 ? "lg:col-span-7" : "lg:col-span-12"}
        >
          <article
            data-testid={`download-card-${d.id}`}
            className={`group flex h-full flex-col justify-between border border-line bg-white p-7 transition-all duration-500 hover:-translate-y-1 hover:border-terra/50 hover:shadow-[0_24px_60px_-24px_rgba(13,58,92,0.35)] sm:p-9 ${
              i === 2 ? "lg:flex-row lg:items-center lg:gap-10" : ""
            }`}
          >
            <div className="flex-1">
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center bg-navy text-sand">
                  <FileText size={18} />
                </span>
                <span className="font-mono text-[10px] uppercase tracking-[0.25em] text-stone">PDF · A4</span>
              </div>
              <h3 className="mt-5 font-display text-2xl font-medium text-ink">{d.title}</h3>
              <p className="mt-1 text-sm font-semibold text-terra">{d.subtitle}</p>
              <p className="mt-3 text-sm leading-relaxed text-slate">{d.detail}</p>
            </div>
            <div className="mt-7 flex flex-wrap gap-3">
              <a
                href={d.href}
                download
                data-testid={`download-${d.id}-hq`}
                className="flex items-center gap-2 bg-navy px-5 py-3 text-xs font-bold uppercase tracking-wider text-sand transition-colors duration-300 hover:bg-navy-soft"
              >
                <Download size={14} /> Haute qualité · {d.size}
              </a>
              {d.emailHref && (
                <a
                  href={d.emailHref}
                  download
                  data-testid={`download-${d.id}-email`}
                  className="flex items-center gap-2 border border-navy/25 px-5 py-3 text-xs font-bold uppercase tracking-wider text-navy transition-colors duration-300 hover:border-navy hover:bg-navy hover:text-sand"
                >
                  <Download size={14} /> E-mail · {d.emailSize}
                </a>
              )}
              {d.id === "catalogue" && (
                <Link
                  to="/catalogue"
                  data-testid="download-catalogue-view"
                  className="flex items-center gap-2 border border-navy/25 px-5 py-3 text-xs font-bold uppercase tracking-wider text-navy transition-colors duration-300 hover:border-navy hover:bg-navy hover:text-sand"
                >
                  Consulter en ligne
                </Link>
              )}
            </div>
          </article>
        </Reveal>
      ))}
    </div>
  </section>
);

const FamiliesPreview = () => (
  <section className="border-y border-line bg-white py-20 sm:py-28" data-testid="families-preview">
    <div className="container-pcm">
      <Reveal className="flex flex-wrap items-end justify-between gap-6">
        <div>
          <p className="eyebrow">Le parcours du chantier</p>
          <h2 className="mt-3 max-w-xl font-display text-3xl font-medium leading-tight text-ink sm:text-5xl">
            Onze familles, <span className="italic text-terra">dans l'ordre du chantier.</span>
          </h2>
        </div>
        <Link
          to="/parcours"
          data-testid="families-preview-link"
          className="group flex items-center gap-2 text-sm font-bold uppercase tracking-widest text-navy transition-colors hover:text-terra"
        >
          Suivre le parcours
          <ArrowRight size={16} className="transition-transform duration-300 group-hover:translate-x-1" />
        </Link>
      </Reveal>
      <div className="mt-12 grid gap-px border border-line bg-line sm:grid-cols-2 lg:grid-cols-3">
        {FAMILIES.map((f, i) => (
          <Reveal key={f.num} delay={(i % 3) * 0.08}>
            <Link
              to="/parcours"
              data-testid={`family-card-${f.num}`}
              className="group flex h-full flex-col justify-between gap-8 bg-white p-6 transition-colors duration-500 hover:bg-navy sm:p-7"
            >
              <span className="font-display text-2xl italic text-terra">{f.num}</span>
              <div>
                <h3 className="font-body text-lg font-bold leading-snug text-ink transition-colors duration-500 group-hover:text-sand">
                  {f.title}
                </h3>
                <p className="mt-2 text-[13px] leading-relaxed text-slate transition-colors duration-500 group-hover:text-sand/70">
                  {f.desc}
                </p>
              </div>
            </Link>
          </Reveal>
        ))}
        <Reveal delay={0.16}>
          <div className="flex h-full flex-col justify-between gap-8 bg-terra p-6 text-white sm:p-7">
            <span className="font-mono text-[10px] uppercase tracking-[0.25em] text-white/70">Et en plus</span>
            <p className="font-display text-xl italic leading-snug">
              « Et s'il manque quelque chose, demandez au comptoir : on le trouve. »
            </p>
          </div>
        </Reveal>
      </div>
    </div>
  </section>
);

const ShowroomBand = ({ onDevis }) => (
  <section className="relative overflow-hidden bg-navy py-20 text-sand grain sm:py-28" data-testid="showroom-band">
    <div className="container-pcm grid items-center gap-12 lg:grid-cols-2">
      <Reveal>
        <p className="eyebrow-light">Notre métier d'origine</p>
        <h2 className="mt-3 font-display text-3xl font-medium leading-tight sm:text-5xl">
          Le carrelage se choisit <span className="italic text-terra-light">en le touchant.</span>
        </h2>
        <p className="mt-5 max-w-lg text-base leading-relaxed text-sand/75">
          Grès cérame et faïence de fabricants reconnus, six aspects à comparer en
          vrai dans notre showroom d'Alfortville : pierre, bois, marbre, béton,
          carreau ciment, décor.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <button
            onClick={onDevis}
            data-testid="showroom-devis-button"
            className="bg-terra px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-white transition-colors duration-300 hover:bg-terra-dark"
          >
            Demander un devis
          </button>
          <a
            href={COMPANY.phoneHref}
            data-testid="showroom-phone-button"
            className="flex items-center gap-2 border border-sand/40 px-6 py-3.5 text-xs font-bold uppercase tracking-widest transition-colors duration-300 hover:bg-sand hover:text-navy"
          >
            <Phone size={14} /> {COMPANY.phone}
          </a>
        </div>
      </Reveal>
      <Reveal delay={0.15}>
        <div className="grid grid-cols-2 gap-4">
          <img src="/assets/carrelage_marbre.png" alt="Carrelage aspect marbre" className="mt-8 h-64 w-full object-cover transition-transform duration-700 hover:scale-[1.03] sm:h-80" />
          <img src="/assets/faience_niche.png" alt="Faïence et niche salle de bain" className="h-64 w-full object-cover transition-transform duration-700 hover:scale-[1.03] sm:h-80" />
        </div>
      </Reveal>
    </div>
  </section>
);

const Stats = () => (
  <section className="container-pcm py-16 sm:py-20" data-testid="stats-section">
    <div className="grid grid-cols-2 gap-px border border-line bg-line lg:grid-cols-4">
      {STATS.map((s, i) => (
        <Reveal key={s.label} delay={i * 0.08} className="bg-sand">
          <div className="p-7 sm:p-9">
            <p className="font-display text-4xl font-medium text-navy sm:text-5xl">{s.value}</p>
            <p className="mt-2 font-mono text-[10px] uppercase tracking-[0.25em] text-slate">{s.label}</p>
          </div>
        </Reveal>
      ))}
    </div>
    <Reveal delay={0.1}>
      <p className="mt-14 max-w-3xl font-display text-2xl font-medium leading-snug text-ink sm:text-3xl">
        Un seul fournisseur pour tout le chantier — du parpaing à la dernière
        couche de peinture, <span className="italic text-terra">en stock ou livré sous 24 h.</span>
      </p>
      <p className="mt-5 max-w-2xl text-base leading-relaxed text-slate">
        Vous n'avez plus à courir d'un dépôt à l'autre. Chaque étape a sa rangée
        chez nous. Et s'il manque quelque chose, demandez au comptoir : on le trouve.
      </p>
    </Reveal>
  </section>
);

const Home = ({ onDevis }) => (
  <>
    <Hero onDevis={onDevis} />
    <Marquee />
    <Stats />
    <Downloads />
    <FamiliesPreview />
    <ShowroomBand onDevis={onDevis} />
  </>
);

export default Home;
