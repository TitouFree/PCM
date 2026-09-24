import { MARQUEE_ITEMS } from "../data/content";

const Row = () => (
  <div className="flex shrink-0 items-center">
    {MARQUEE_ITEMS.map((item, i) => (
      <span key={i} className="flex items-center">
        <span className="px-6 font-display text-lg italic text-sand/90 sm:text-xl">{item}</span>
        <span className="h-1.5 w-1.5 rotate-45 bg-terra" />
      </span>
    ))}
  </div>
);

export const Marquee = ({ dark = true }) => (
  <div
    data-testid="editorial-marquee"
    className={`relative overflow-hidden border-y py-4 ${dark ? "border-navy-deep bg-navy" : "border-line bg-white"}`}
  >
    <div className="flex w-max animate-marquee">
      <Row />
      <Row />
    </div>
  </div>
);
