import React from "react";
import { motion } from "framer-motion";

export const Reveal = ({ children, delay = 0, y = 24, className = "" }) => (
  <motion.div
    initial={{ opacity: 0, y }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-80px" }}
    transition={{ duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] }}
    className={className}
  >
    {children}
  </motion.div>
);

export const Stagger = ({ children, className = "" }) => (
  <motion.div
    initial="hidden"
    whileInView="show"
    viewport={{ once: true, margin: "-80px" }}
    variants={{ hidden: {}, show: { transition: { staggerChildren: 0.12 } } }}
    className={className}
  >
    {children}
  </motion.div>
);

export const Item = ({ children, className = "" }) => (
  <motion.div
    variants={{ hidden: { opacity: 0, y: 24 }, show: { opacity: 1, y: 0, transition: { duration: 0.55, ease: [0.22, 1, 0.36, 1] } } }}
    className={className}
  >
    {children}
  </motion.div>
);
