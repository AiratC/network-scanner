import React, { useState } from 'react';
import styles from './Login.module.css';
import { useNavigate } from 'react-router';
import { setCredentials } from '../../store/slices/authSlice';
import { useLoginMutation } from '../../store/services/authApi';
import { useAppDispatch } from '../../store/store';

export const Login: React.FC = () => {
   const [email, setEmail] = useState('');
   const [password, setPassword] = useState('');
   const [localError, setLocalError] = useState<string | null>(null);

   const [login, { isLoading }] = useLoginMutation();
   const dispatch = useAppDispatch();
   const navigate = useNavigate();

   const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setLocalError(null);

      // Валидация перед отправкой
      if (!email.trim() || !password.trim()) {
         setLocalError('Пожалуйста, заполните все поля');
         return;
      }

      try {
         // Отправляем запрос. Благодаря credentials: 'include' в baseApi, 
         // бэкенд сам установит HttpOnly куку в браузер.
         const userData = await login({ email, password }).unwrap();

         // Сохраняем данные пользователя (name, email) в Redux
         dispatch(setCredentials(userData));

         // Перенаправляем на главную страницу сканера
         navigate('/');
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
         // Корректный перехват ошибок от FastAPI / RTK Query
         if (err?.data?.detail) {
            setLocalError(err.data.detail);
         } else {
            setLocalError('Не удалось связаться с сервером. Проверьте сеть.');
         }
      }
   };

   return (
      <div className={styles.pageContainer}>
         <div className={styles.authCard}>
            <h1 className={styles.title}>Network Scanner</h1>
            <p className={styles.subtitle}>Войдите в свой аккаунт для управления сканером</p>

            <form onSubmit={handleSubmit} noValidate>
               {localError && (
                  <div className={styles.errorMessage}>
                     {localError}
                  </div>
               )}

               <div className={styles.formGroup}>
                  <label htmlFor="email" className={styles.label}>
                     Email адрес
                  </label>
                  <input
                     type="email"
                     id="email"
                     className={styles.input}
                     placeholder="name@company.com"
                     value={email}
                     onChange={(e) => setEmail(e.target.value)}
                     disabled={isLoading}
                     autoComplete="email"
                  />
               </div>

               <div className={styles.formGroup}>
                  <label htmlFor="password" className={styles.label}>
                     Пароль
                  </label>
                  <input
                     type="password"
                     id="password"
                     className={styles.input}
                     placeholder="••••••••"
                     value={password}
                     onChange={(e) => setPassword(e.target.value)}
                     disabled={isLoading}
                     autoComplete="current-password"
                  />
               </div>

               <button
                  type="submit"
                  className={styles.submitButton}
                  disabled={isLoading}
               >
                  {isLoading ? 'Вход...' : 'Войти'}
               </button>
            </form>
         </div>
      </div>
   );
};

export default Login;