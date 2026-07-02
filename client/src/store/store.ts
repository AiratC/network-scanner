import { configureStore } from "@reduxjs/toolkit";
import { baseApi } from "./api/baseApi";
import { useDispatch, useSelector, type TypedUseSelectorHook } from "react-redux";
import authReducer from './slices/authSlice';

export const store = configureStore({
   reducer: {
      [baseApi.reducerPath]: baseApi.reducer,
      auth: authReducer,
   },
   // Добавляем мидлвар для поддержки кэширования, инвалидации и опросов RTK Query
   middleware: (getDefaultMiddleware) => {
      return getDefaultMiddleware().concat(baseApi.middleware);
   }
});

// Типизация для дальнейшего использования в хуках
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch= typeof store.dispatch;

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;