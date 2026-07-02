import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseApi = createApi({
   reducerPath: 'api',
   baseQuery: fetchBaseQuery({
      baseUrl: import.meta.env.VITE_BACKEND_URL + '/api',
      // КРИТИЧЕСКИ ВАЖНО: заставляет отправлять куки (включая HttpOnly) с каждым запросом
      credentials: 'include'
   }),
   tagTypes: [
      'User',
      'ScanHistory'
   ],
   // eslint-disable-next-line @typescript-eslint/no-unused-vars
   endpoints: (_builder) => ({})
})