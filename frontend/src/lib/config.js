// MapMyCareer — site config (brand, support, analytics IDs)
export const BRAND = "MapMyCareer";

// WhatsApp support
export const WHATSAPP_NUMBER = "918448773316"; // country code + number, no '+'
export const whatsappLink = (msg = "Hi, I need help with my Career Blueprint.") =>
  `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;

// Analytics IDs — leave blank until provided; events still push to dataLayer.
export const META_PIXEL_ID = process.env.REACT_APP_META_PIXEL_ID || "";
export const GA4_ID = process.env.REACT_APP_GA4_ID || "";
export const GTM_ID = process.env.REACT_APP_GTM_ID || "";

// Pricing (single source of truth for the landing)
export const PRICE = { student: 199, original: 499 };
