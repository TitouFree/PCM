import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";
import { ChevronLeft, ChevronRight, Download, ZoomIn, ZoomOut } from "lucide-react";
import { Reveal } from "../components/Reveal";
import { CATALOGUE_SECTIONS, DOWNLOADS, SOURCES } from "../data/content";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

const DOCS = [
  { id: "courte", label: "Plaquette courte (fusionnée)", file: "/documents/PCM_Plaquette_Courte_Fusionnee.pdf" },
  { id: "complete", label: "Plaquette complète (fusionnée)", file: "/documents/PCM_Plaquette_Complete_Fusionnee.pdf" },
  { id: "catalogue", label: "Catalogue général (source)", file: "/documents/Catalogue_General_PCM.pdf" },
  { id: "magazine", label: "Le Magazine (source)", file: "/documents/Ebauche_Magazine_PCM.pdf" },
];

const Catalogue = () => {
  const [params] = useSearchParams();
  const initDoc = DOCS.find((d) => d.id === params.get("doc")) || DOCS[2];
  const initPage = Math.max(1, parseInt(params.get("page") || "1", 10) || 1);
  const [doc, setDoc] = useState(initDoc);
  const [numPages, setNumPages] = useState(null);
  const [page, setPage] = useState(initPage);
  const [scale, setScale] = useState(1);
  const [error, setError] = useState(false);

  const selectDoc = (d) => { setDoc(d); setPage(1); setNumPages(null); setError(false); };
  const zoom = (d) => setScale((s) => Math.min(2.5, Math.max(0.5, +(s + d).toFixed(2))));

  return (
    <>
      <section className="bg-navy pb-16 pt-36 text-sand grain sm:pt-44" data-testid="catalogue-hero">
        <div className="container-pcm">
          <p className="eyebrow-light">Catalogue & documents</p>
          <h1 className="mt-4 max-w-3xl font-display text-4xl font-medium leading-[1.08] sm:text-6xl">
            Consultez, zoomez, <span className="italic text-terra-light">téléchargez.</span>
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-relaxed text-sand/80">
            La visionneuse reprend les documents officiels page par page, sans
            aucune modification. Les références, conditionnements et marques sont
            ceux du catalogue général d'origine.
          </p>
        </div>
      </section>

      <section className="container-pcm py-14 sm:py-20" data-testid="catalogue-viewer-section">
        <Reveal>
          <div className="flex flex-wrap items-center gap-2" data-testid="catalogue-doc-tabs">
            {DOCS.map((d) => (
              <button
                key={d.id}
                onClick={() => selectDoc(d)}
                data-testid={`catalogue-tab-${d.id}`}
                className={`border px-4 py-2.5 text-xs font-bold uppercase tracking-wider transition-colors duration-300 ${
                  doc.id === d.id
                    ? "border-navy bg-navy text-sand"
                    : "border-line bg-white text-slate hover:border-navy hover:text-navy"
                }`}
              >
                {d.label}
              </button>
            ))}
          </div>

          <div className="mt-6 flex flex-wrap items-center justify-between gap-4 border border-line bg-white px-4 py-3">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1}
                data-testid="viewer-prev-page"
                aria-label="Page précédente"
                className="border border-line p-2 text-navy transition-colors hover:bg-navy hover:text-sand disabled:opacity-30"
              >
                <ChevronLeft size={16} />
              </button>
              <span className="min-w-28 text-center font-mono text-xs uppercase tracking-widest text-slate" data-testid="viewer-page-indicator">
                Page {page}{numPages ? ` / ${numPages}` : ""}
              </span>
              <button
                onClick={() => setPage((p) => Math.min(numPages || p, p + 1))}
                disabled={numPages ? page >= numPages : false}
                data-testid="viewer-next-page"
                aria-label="Page suivante"
                className="border border-line p-2 text-navy transition-colors hover:bg-navy hover:text-sand disabled:opacity-30"
              >
                <ChevronRight size={16} />
              </button>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => zoom(-0.2)} data-testid="viewer-zoom-out" aria-label="Zoom arrière" className="border border-line p-2 text-navy transition-colors hover:bg-navy hover:text-sand">
                <ZoomOut size={16} />
              </button>
              <span className="w-14 text-center font-mono text-xs text-slate" data-testid="viewer-zoom-level">{Math.round(scale * 100)}%</span>
              <button onClick={() => zoom(0.2)} data-testid="viewer-zoom-in" aria-label="Zoom avant" className="border border-line p-2 text-navy transition-colors hover:bg-navy hover:text-sand">
                <ZoomIn size={16} />
              </button>
              <a
                href={doc.file}
                download
                data-testid="viewer-download"
                className="ml-2 flex items-center gap-2 bg-terra px-4 py-2 text-xs font-bold uppercase tracking-wider text-white transition-colors hover:bg-terra-dark"
              >
                <Download size={14} /> Télécharger
              </a>
            </div>
          </div>

          <div className="mt-8 overflow-x-auto border border-line bg-[#E9E5DC] p-4 sm:p-8" data-testid="viewer-canvas-wrap">
            {error ? (
              <p className="py-20 text-center text-sm text-slate" data-testid="viewer-error">
                La visionneuse n'a pas pu charger ce document.{" "}
                <a href={doc.file} download className="font-bold text-terra underline">Téléchargez-le directement.</a>
              </p>
            ) : (
              <Document
                file={doc.file}
                onLoadSuccess={({ numPages: n }) => setNumPages(n)}
                onLoadError={() => setError(true)}
                loading={<p className="py-24 text-center font-mono text-xs uppercase tracking-widest text-slate" data-testid="viewer-loading">Chargement du document…</p>}
              >
                <Page
                  pageNumber={page}
                  scale={scale}
                  width={Math.min(900, typeof window !== "undefined" ? window.innerWidth - 80 : 900)}
                  renderTextLayer={false}
                  renderAnnotationLayer={false}
                />
              </Document>
            )}
          </div>

          {doc.id === "catalogue" && (
            <div className="mt-8 border border-line bg-white p-5 sm:p-6" data-testid="catalogue-index">
              <p className="eyebrow">Accès direct par section</p>
              <div className="mt-4 grid gap-1.5 sm:grid-cols-2 lg:grid-cols-3">
                {CATALOGUE_SECTIONS.map((s) => (
                  <button
                    key={s.name}
                    onClick={() => setPage(s.page)}
                    data-testid={`catalogue-jump-${s.page}`}
                    className={`flex items-baseline justify-between gap-3 px-3 py-2 text-left text-[13px] transition-colors duration-200 ${
                      page >= s.page ? "bg-sand text-ink" : "text-slate hover:bg-sand hover:text-ink"
                    }`}
                  >
                    <span className="font-semibold">{s.name}</span>
                    <span className="shrink-0 font-mono text-[10px] text-terra">p. {s.page}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          <p className="mt-6 max-w-3xl text-[13px] leading-relaxed text-stone" data-testid="catalogue-search-note">
            La recherche par référence n'est pas proposée : les pages du catalogue
            d'origine sont des visuels non indexables, et nous préférons ne pas
            risquer d'afficher une référence erronée. Pour toute référence,
            appelez le 01 43 68 83 80 — le comptoir vous répond.
          </p>
        </Reveal>
      </section>

      <section className="border-t border-line bg-white py-16" data-testid="catalogue-downloads">
        <div className="container-pcm">
          <h2 className="font-display text-2xl font-medium text-ink sm:text-3xl">Tous les téléchargements</h2>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            {[...DOWNLOADS, ...SOURCES].map((d) => (
              <a
                key={d.id}
                href={d.href}
                download
                data-testid={`catalogue-download-${d.id}`}
                className="group border border-line bg-sand p-6 transition-all duration-300 hover:border-terra/60"
              >
                <p className="font-display text-xl font-medium text-ink group-hover:text-terra">{d.title}</p>
                <p className="mt-1 text-[13px] text-slate">{d.subtitle}</p>
                <p className="mt-4 flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-terra">
                  <Download size={12} /> PDF · {d.size}
                </p>
              </a>
            ))}
          </div>
        </div>
      </section>
    </>
  );
};

export default Catalogue;
