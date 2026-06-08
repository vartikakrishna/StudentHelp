import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

export const analyze = (payload) => axios.post(`${API}/analyze`, payload).then((r) => r.data);
export const createOrder = (submission_id) => axios.post(`${API}/create-order`, { submission_id }).then((r) => r.data);
export const verifyPayment = (data) => axios.post(`${API}/verify-payment`, data).then((r) => r.data);
export const pdfUrl = (submission_id) => `${API}/report/${submission_id}/pdf`;
