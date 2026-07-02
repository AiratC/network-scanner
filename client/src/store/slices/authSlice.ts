import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { AuthState, UserData } from "../../types/auth.types";

const initialState: AuthState = {
   user: null,
   isAuthenticated: false
};

const authSlice = createSlice({
   name: 'auth',
   initialState,
   reducers: {
      // Вызовем этот редюсер, когда бэкенд подтвердит успешный логин и отдаст данные юзера
      setCredentials: (state, action: PayloadAction<UserData>) => {
         state.user = action.payload;
         state.isAuthenticated = true;
      },
      // При выходе сбрасываем стейт (бэкенд при этом должен будет стереть куку)
      logout: (state) => {
         state.user = null;
         state.isAuthenticated = false;
      }
   }
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;