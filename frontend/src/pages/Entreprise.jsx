import { Phone } from "lucide-react";
import { Reveal } from "../components/Reveal";
import { Marquee } from "../components/Marquee";
import { COMPANY, SERVICES } from "../data/content";

const Entreprise = ({ onDevis }) => (
  <>
    <section className="relative overflow-hidden bg-navy pb-20 pt-36 text-sand grain sm:pt-44" data-testid="entreprise-hero">
      <div className="container-pcm">
        <p className="eyebrow-light">L'entreprise</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-medium leading-[1.08] sm:text-6xl">
          Un négoce indépendant, <span className="italic text-terra-light">de proximité.</span>
        </h1>
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-sand/80 sm:text-lg">
          Installation de chantier, machines, gros œuvre, toiture, isolation,
          plâtrerie, carrelage, peinture. Un seul fournisseur pour tout le
          chantier, livré sous 24 h.
        </p>
      </div>
    </section>
    <Marquee dark={false} />

    <section className="container-pcm grid gap-12 py-20 sm:py-28 lg:grid-cols-2 lg:gap-20" data-testid="entreprise-presentation">
      <Reveal>
        <p className="eyebrow">Négoce de matériaux · Alfortville (94)</p>
        <h2 className="mt-3 font-display text-3xl font-medium leading-tight text-ink sm:text-4xl">
          Pros & particuliers, <span className="italic text-terra">depuis 2011.</span>
        </h2>
        <div className="mt-6 space-y-5 text-base leading-relaxed text-slate">
          <p>
            Vous n'avez plus à courir d'un dépôt à l'autre. Chaque étape a sa
            rangée chez nous, du parpaing à la dernière couche de peinture, en
            stock ou livrée sous 24 h.
          </p>
          <p>
            Et s'il manque quelque chose, demandez au comptoir : on le trouve.
          </p>
          <p>
            Professionnels du bâtiment et particuliers : nous travaillons aussi
            avec un réseau de poseurs de confiance, sur demande.
          </p>
        </div>
        <div className="mt-8 flex flex-wrap gap-4">
          <button
            onClick={onDevis}
            data-testid="entreprise-devis-button"
            className="bg-terra px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-white transition-colors duration-300 hover:bg-terra-dark"
          >
            Demander un devis
          </button>
          <a
            href={COMPANY.phoneHref}
            data-testid="entreprise-phone-button"
            className="flex items-center gap-2 border border-navy/30 px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-navy transition-colors duration-300 hover:bg-navy hover:text-sand"
          >
            <Phone size={14} /> {COMPANY.phone}
          </a>
        </div>
      </Reveal>
      <Reveal delay={0.12}>
        <div className="relative">
          <img src="/assets/chantier_echafaudage.png" alt="Chantier de construction avec échafaudage" className="h-[420px] w-full object-cover" />
          <div className="absolute -bottom-6 -left-4 bg-terra px-6 py-5 text-white sm:-left-8">
            <p className="font-display text-3xl font-medium">2011</p>
            <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.25em] text-white/80">Année de création</p>
          </div>
        </div>
      </Reveal>
    </section>

    <section className="border-t border-line bg-white py-20 sm:py-28" data-testid="entreprise-services">
      <div className="container-pcm">
        <Reveal>
          <p className="eyebrow">Services</p>
          <h2 className="mt-3 max-w-2xl font-display text-3xl font-medium leading-tight text-ink sm:text-4xl">
            Le comptoir, le stock, <span className="italic text-terra">la livraison.</span>
          </h2>
        </Reveal>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {SERVICES.map((s, i) => (
            <Reveal key={s.title} delay={(i % 3) * 0.08}>
              <div
                data-testid={`service-card-${i}`}
                className="group h-full border border-line bg-sand p-7 transition-all duration-500 hover:-translate-y-1 hover:border-terra/50 hover:shadow-[0_20px_50px_-24px_rgba(13,58,92,0.3)]"
              >
                <span className="font-display text-xl italic text-terra">{String(i + 1).padStart(2, "0")}</span>
                <h3 className="mt-4 font-body text-lg font-bold text-ink">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate">{s.text}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>

    <section className="container-pcm py-20 sm:py-28" data-testid="entreprise-showroom">
      <div className="grid items-center gap-12 lg:grid-cols-2">
        <Reveal className="order-2 lg:order-1">
          <div className="grid grid-cols-2 gap-4">
            <img src="/assets/carreaux_ciment.png" alt="Carreaux de ciment décoratifs" className="h-72 w-full object-cover transition-transform duration-700 hover:scale-[1.03]" />
            <img src="/assets/carrelage_marbre.png" alt="Carrelage aspect marbre grand format" className="mt-10 h-72 w-full object-cover transition-transform duration-700 hover:scale-[1.03]" />
          </div>
        </Reveal>
        <Reveal className="order-1 lg:order-2">
          <p className="eyebrow">Showroom</p>
          <h2 className="mt-3 font-display text-3xl font-medium leading-tight text-ink sm:text-4xl">
            Le carrelage se choisit <span className="italic text-terra">en le touchant.</span>
          </h2>
          <p className="mt-5 text-base leading-relaxed text-slate">
            Grès cérame et faïence de fabricants reconnus, six aspects à comparer
            en vrai dans notre showroom d'Alfortville : pierre, bois, marbre,
            béton, carreau ciment, décor.
          </p>
          <p className="mt-4 text-base leading-relaxed text-slate">
            Conseil technique au comptoir : le bon produit et la bonne méthode de
            pose, expliqués simplement.
          </p>
        </Reveal>
      </div>
    </section>
  </>
);

export default Entreprise;
