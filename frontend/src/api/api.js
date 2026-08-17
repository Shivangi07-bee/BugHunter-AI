import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export default api;
export const downloadJson = () =>
    window.open("http://127.0.0.1:8000/report/json", "_blank");

export const downloadHtml = () =>
    window.open("http://127.0.0.1:8000/report/html", "_blank");

export const downloadPdf = () =>
    window.open("http://127.0.0.1:8000/report/pdf", "_blank");