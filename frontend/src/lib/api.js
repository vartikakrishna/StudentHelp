import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const analyze = (payload) => axios.post(`${API}/analyze`, payload).then((r) => r.data);
export const submitLead = (payload) => axios.post(`${API}/lead`, payload).then((r) => r.data);
export const createOrder = (submission_id) => axios.post(`${API}/create-order`, { submission_id }).then((r) => r.data);
export const verifyPayment = (data) => axios.post(`${API}/verify-payment`, data).then((r) => r.data);
export const generateDeep = (submission_id) => axios.post(`${API}/generate-deep/${submission_id}`).then((r) => r.data);
export const deepStatus = (submission_id) => axios.get(`${API}/generate-deep/${submission_id}/status`).then((r) => r.data);
export const createAddonOrder = (submission_id, addon_ids) => axios.post(`${API}/create-addon-order`, { submission_id, addon_ids }).then((r) => r.data);
export const verifyAddonPayment = (data) => axios.post(`${API}/verify-addon-payment`, data).then((r) => r.data);
export const pdfUrl = (submission_id) => `${API}/report/${submission_id}/pdf`;
export const addonPdfUrl = (submission_id, addon_id) => `${API}/report/${submission_id}/addon/${addon_id}/pdf`;
