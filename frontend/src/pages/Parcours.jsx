import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { Reveal } from "../components/Reveal";
import { Marquee } from "../components/Marquee";
import { FAMILIES } from "../data/content";

const Parcours = ({ onDevis }) => (
  <>
    <section className="relative overflow-hidden bg-navy pb-20 pt-36 text-sand grain sm:pt-44" data-testid="parcours-hero">
      <div className="container-pcm">
        <p className="eyebrow-light">Le parcours du chantier</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-medium leading-[1.08] sm:text-6xl">
          Onze familles, <span className="italic text-terra-light">dans l'ordre du chantier.</span>
        </h1>
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-sand/80 sm:text-lg">
          Du premier film de protection au dernier profilé de finition, chaque
          étape a sa rangée chez nous. Suivez le fil.
        </p>
      </div>
    </section>
    <Marquee />

    <section className="container-pcm py-20 sm:py-28" data-testid="parcours-list">
      <div className="space-y-16 sm:space-y-24">
        {FAMILIES.map((f, i) => (
          <Reveal key={f.num}>
            <article
              data-testid={`parcours-family-${f.num}`}
              className={`grid items-center gap-8 lg:grid-cols-12 ${i % 2 ? "" : ""}`}
            >
              <div className={`lg:col-span-5 ${i % 2 ? "lg:order-2" : ""}`}>
                {f.img ? (
                  <div className="group overflow-hidden">
                    <img
                      src={f.img}
                      alt={f.title}
                      className="h-64 w-full object-cover transition-transform duration-700 group-hover:scale-105 sm:h-80"
                    />
                  </div>
                ) : (
                  <div className="flex h-64 items-center justify-center bg-navy sm:h-80">
                    <span className="font-display text-[7rem] font-medium italic text-navy-soft sm:text-[9rem]">{f.num}</span>
                  </div>
                )}
              </div>
              <div className={`lg:col-span-7 ${i % 2 ? "lg:order-1 lg:pr-8" : "lg:pl-8"}`}>
                <div className="flex items-baseline gap-5">
                  <span className="font-display text-4xl italic text-terra sm:text-5xl">{f.num}</span>
                  <span className="hidden font-mono text-[10px] uppercase tracking-[0.3em] text-stone sm:block">
                    Étape {f.num} / 11
                  </span>
                </div>
                <h2 className="mt-4 font-display text-3xl font-medium leading-tight text-ink sm:text-4xl">{f.title}</h2>
                <p className="mt-4 max-w-xl text-base leading-relaxed text-slate">{f.desc}</p>
                <div className="mt-6 flex flex-wrap items-center gap-5">
                  <button
                    onClick={onDevis}
                    data-testid={`parcours-devis-${f.num}`}
                    className="group flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-navy transition-colors hover:text-terra"
                  >
                    Demander un devis
                    <ArrowRight size={14} className="transition-transform duration-300 group-hover:translate-x-1" />
                  </button>
                  <Link
                    to="/catalogue"
                    data-testid={`parcours-catalogue-${f.num}`}
                    className="link-underline text-xs font-bold uppercase tracking-widest text-slate transition-colors hover:text-navy"
                  >
                    Voir les références au catalogue
                  </Link>
                </div>
              </div>
            </article>
          </Reveal>
        ))}
      </div>
    </section>

    <section className="border-t border-line bg-white py-16" data-testid="parcours-cta">
      <div className="container-pcm flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-center">
        <p className="max-w-xl font-display text-2xl font-medium italic leading-snug text-ink">
          « Et s'il manque quelque chose, demandez au comptoir : on le trouve. »
        </p>
        <a
          href="/contact"
          data-testid="parcours-contact-link"
          className="bg-terra px-7 py-4 text-xs font-bold uppercase tracking-widest text-white transition-colors duration-300 hover:bg-terra-dark"
        >
          Passez au comptoir
        </a>
      </div>
    </section>
  </>
);

export default Parcours;
