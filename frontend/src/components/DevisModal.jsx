import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import axios from "axios";
import { toast } from "sonner";
import { FAMILIES } from "../data/content";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const inputCls =
  "w-full border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none transition-colors duration-300 placeholder:text-stone focus:border-terra";

export const DevisModal = ({ open, onClose }) => {
  const [form, setForm] = useState({
    nom: "", email: "", telephone: "", profil: "Professionnel",
    familles: [], adresse_chantier: "", delai: "", message: "",
  });
  const [sending, setSending] = useState(false);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });
  const toggleFamille = (t) =>
    setForm((f) => ({
      ...f,
      familles: f.familles.includes(t) ? f.familles.filter((x) => x !== t) : [...f.familles, t],
    }));

  const submit = async (e) => {
    e.preventDefault();
    setSending(true);
    try {
      await axios.post(`${API}/devis`, { ...form, familles: form.familles });
      toast.success("Demande envoyée. Nous vous rappelons rapidement.", {
        description: "Votre demande de devis a été transmise au comptoir d'Alfortville.",
      });
      setForm({ nom: "", email: "", telephone: "", profil: "Professionnel", familles: [], adresse_chantier: "", delai: "", message: "" });
      onClose();
    } catch (err) {
      toast.error("L'envoi a échoué.", {
        description: "Réessayez ou appelez le 01 43 68 83 80.",
      });
    } finally {
      setSending(false);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[80] flex items-end justify-center bg-navy-deep/60 backdrop-blur-sm sm:items-center sm:p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          data-testid="devis-modal-overlay"
        >
          <motion.div
            className="max-h-[92vh] w-full max-w-2xl overflow-y-auto bg-sand p-6 shadow-2xl sm:p-10"
            initial={{ y: 60, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 60, opacity: 0 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            onClick={(e) => e.stopPropagation()}
            data-testid="devis-modal"
          >
            <div className="flex items-start justify-between gap-6">
              <div>
                <p className="eyebrow">Devis</p>
                <h3 className="mt-2 font-display text-2xl font-medium text-ink sm:text-3xl">
                  Demander un devis
                </h3>
                <p className="mt-2 text-sm text-slate">
                  Réponse rapide du comptoir — ou appelez le 01 43 68 83 80.
                </p>
              </div>
              <button onClick={onClose} data-testid="devis-modal-close" aria-label="Fermer" className="p-1 text-slate transition-colors hover:text-ink">
                <X size={22} />
              </button>
            </div>
            <form onSubmit={submit} className="mt-8 grid gap-4 sm:grid-cols-2" data-testid="devis-form">
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-nom">Nom *</label>
                <input id="devis-nom" data-testid="devis-nom" required value={form.nom} onChange={set("nom")} className={inputCls} placeholder="Votre nom" />
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-profil">Vous êtes</label>
                <select id="devis-profil" data-testid="devis-profil" value={form.profil} onChange={set("profil")} className={inputCls}>
                  <option>Professionnel</option>
                  <option>Particulier</option>
                </select>
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-tel">Téléphone *</label>
                <input id="devis-tel" data-testid="devis-telephone" required type="tel" value={form.telephone} onChange={set("telephone")} className={inputCls} placeholder="06 …" />
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-email">E-mail *</label>
                <input id="devis-email" data-testid="devis-email" required type="email" value={form.email} onChange={set("email")} className={inputCls} placeholder="vous@exemple.fr" />
              </div>
              <div className="sm:col-span-2">
                <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-slate">Familles concernées</p>
                <div className="flex flex-wrap gap-2" data-testid="devis-familles">
                  {FAMILIES.map((f) => (
                    <button
                      type="button"
                      key={f.num}
                      data-testid={`devis-famille-${f.num}`}
                      onClick={() => toggleFamille(f.title)}
                      className={`border px-3 py-1.5 text-xs font-semibold transition-colors duration-200 ${
                        form.familles.includes(f.title)
                          ? "border-terra bg-terra text-white"
                          : "border-line bg-white text-slate hover:border-terra hover:text-terra"
                      }`}
                    >
                      {f.num} · {f.title}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-adresse">Adresse du chantier</label>
                <input id="devis-adresse" data-testid="devis-adresse" value={form.adresse_chantier} onChange={set("adresse_chantier")} className={inputCls} placeholder="Commune, code postal" />
              </div>
              <div>
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-delai">Délai souhaité</label>
                <input id="devis-delai" data-testid="devis-delai" value={form.delai} onChange={set("delai")} className={inputCls} placeholder="Ex. semaine prochaine" />
              </div>
              <div className="sm:col-span-2">
                <label className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate" htmlFor="devis-message">Votre besoin *</label>
                <textarea id="devis-message" data-testid="devis-message" required rows={4} value={form.message} onChange={set("message")} className={inputCls} placeholder="Matériaux, quantités ou surface approximative, livraison grue ou retrait comptoir…" />
              </div>
              <div className="sm:col-span-2">
                <button
                  type="submit"
                  disabled={sending}
                  data-testid="devis-submit-button"
                  className="w-full bg-navy px-6 py-3.5 text-sm font-bold uppercase tracking-widest text-sand transition-colors duration-300 hover:bg-navy-soft disabled:opacity-60"
                >
                  {sending ? "Envoi en cours…" : "Envoyer ma demande"}
                </button>
              </div>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
