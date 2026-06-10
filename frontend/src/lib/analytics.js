// Lightweight analytics layer — GTM dataLayer + GA4 (gtag) + Meta Pixel (fbq).
// Scripts load only when an ID is configured; events ALWAYS push to dataLayer
// so a GTM container added later can pick everything up retroactively.
import { META_PIXEL_ID, GA4_ID, GTM_ID } from "./config";

let started = false;

const inject = (src, attrs = {}) => {
  const s = document.createElement("script");
  s.async = true;
  s.src = src;
  Object.entries(attrs).forEach(([k, v]) => s.setAttribute(k, v));
  document.head.appendChild(s);
};

export const initAnalytics = () => {
  if (started || typeof window === "undefined") return;
  started = true;
  window.dataLayer = window.dataLayer || [];

  if (GTM_ID) {
    window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
    inject(`https://www.googletagmanager.com/gtm.js?id=${GTM_ID}`);
  }
  if (GA4_ID) {
    inject(`https://www.googletagmanager.com/gtag/js?id=${GA4_ID}`);
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA4_ID);
  }
  if (META_PIXEL_ID) {
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq("init", META_PIXEL_ID);
    window.fbq("track", "PageView");
  }
};

// Generic event -> dataLayer (+ GA4 + Pixel where it maps to a standard event)
export const track = (event, params = {}) => {
  if (typeof window === "undefined") return;
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({ event, ...params });
  if (window.gtag) window.gtag("event", event, params);
  if (window.fbq) {
    const map = { lead_submit: "Lead", begin_questionnaire: "InitiateCheckout", purchase: "Purchase" };
    if (map[event]) window.fbq("track", map[event], params);
    else window.fbq("trackCustom", event, params);
  }
};
