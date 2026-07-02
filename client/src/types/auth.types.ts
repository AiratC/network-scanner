// authSlice
export interface UserData {
   name: string;
   email: string;
};

export interface AuthState {
   user: UserData | null;
   isAuthenticated: boolean;
};

// authApi
export interface UserResponse {
   email: string;
   name: string;
};

export interface LoginCredentials {
   email: string;
   password: string;
}

