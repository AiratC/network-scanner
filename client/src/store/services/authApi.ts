import type { LoginCredentials, UserResponse } from "../../types/auth.types";
import { baseApi } from "../api/baseApi";


export const authApi = baseApi.injectEndpoints({
   overrideExisting: false,
   endpoints: (builder) => ({
      login: builder.mutation<UserResponse, LoginCredentials>({
         query: (credentials) => ({
            url: '/auth/login', // Твой будущий роут на бэкенде
            method: 'POST',
            body: credentials,
         }),
         invalidatesTags: ['User'], // Сбрасываем кэш юзера при входе
      }),
      logout: builder.mutation<void, void>({
         query: () => ({
            url: '/auth/logout', // Твой будущий роут на бэкенде
            method: 'POST'
         }),
         invalidatesTags: ['User'], // Сбрасываем кэш юзера при выходе
      }),
      // Новый запрос на проверку профиля
      getMe: builder.query<UserResponse, void>({
         query: () => '/auth/get-me',
         providesTags: ['User'],
      }),
   }),
});

// Экспортируем автогенерируемый хук для компонента
export const { 
   useLoginMutation,
   useLogoutMutation,
   useGetMeQuery
} = authApi;