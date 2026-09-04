import axios from 'axios';
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:5000',timeout:10000});
export const get=path=>api.get(path).then(r=>r.data);
export const post=(path,data)=>api.post(path,data).then(r=>r.data);
export const patch=(path,data)=>api.patch(path,data).then(r=>r.data);
