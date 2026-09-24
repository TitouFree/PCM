import { Phone } from "lucide-react";
import { Reveal } from "../components/Reveal";
import { Marquee } from "../components/Marquee";
import { BRANDS, COMPANY } from "../data/content";

const Fabricants = () => (
  <>
    <section className="bg-navy pb-16 pt-36 text-sand grain sm:pt-44" data-testid="fabricants-hero">
      <div className="container-pcm">
        <p className="eyebrow-light">Fabricants</p>
        <h1 className="mt-4 max-w-3xl font-display text-4xl font-medium leading-[1.08] sm:text-6xl">
          Des marques reconnues, <span className="italic text-terra-light">au comptoir.</span>
        </h1>
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-sand/80">
          Certains de nos fabricants, tels qu'ils figurent dans nos documents
          officiels. La disponibilité exacte se confirme au comptoir.
        </p>
      </div>
    </section>
    <Marquee dark={false} />

    <section className="container-pcm py-16 sm:py-24" data-testid="fabricants-strips">
      <Reveal>
        <p className="eyebrow">Certains de nos fabricants</p>
        <div className="mt-8 space-y-4">
          <div className="border border-line bg-white p-4 sm:p-6">
            <img src="/assets/brands_row1.png" alt="Cifre Cerámica, Recer, Navarti, Weber, Mapei" className="w-full" data-testid="brands-strip-1" />
          </div>
          <div className="border border-line bg-white p-4 sm:p-6">
            <img src="/assets/brands_row2.png" alt="PRB, Placo, Isover, Siniat, Rockwool, Unikalo, Makita" className="w-full" data-testid="brands-strip-2" />
          </div>
        </div>
      </Reveal>

      <div className="mt-14 grid gap-px border border-line bg-line sm:grid-cols-2 lg:grid-cols-4" data-testid="fabricants-grid">
        {BRANDS.map((b, i) => (
          <Reveal key={b} delay={(i % 4) * 0.06} className="bg-white">
            <div className="flex h-full items-center justify-between gap-3 p-6" data-testid={`brand-${i}`}>
              <span className="font-body text-base font-bold text-ink">{b}</span>
              <span className="font-mono text-[10px] uppercase tracking-widest text-stone">{String(i + 1).padStart(2, "0")}</span>
            </div>
          </Reveal>
        ))}
        <Reveal delay={0.2} className="bg-navy">
          <div className="flex h-full flex-col justify-center p-6">
            <p className="font-display text-lg italic text-sand">Et d'autres marques au comptoir.</p>
          </div>
        </Reveal>
      </div>

      <Reveal className="mt-14">
        <div className="flex flex-col items-start justify-between gap-6 border border-line bg-white p-8 sm:flex-row sm:items-center">
          <div>
            <h2 className="font-display text-2xl font-medium text-ink">Une marque, une référence précise ?</h2>
            <p className="mt-2 max-w-lg text-sm leading-relaxed text-slate">
              Le catalogue général liste les références et conditionnements par
              famille. Le comptoir confirme la disponibilité et le prix.
            </p>
          </div>
          <a
            href={COMPANY.phoneHref}
            data-testid="fabricants-phone-button"
            className="flex shrink-0 items-center gap-2 bg-navy px-6 py-3.5 text-xs font-bold uppercase tracking-widest text-sand transition-colors duration-300 hover:bg-navy-soft"
          >
            <Phone size={14} /> {COMPANY.phone}
          </a>
        </div>
      </Reveal>
    </section>
  </>
);

export default Fabricants;
