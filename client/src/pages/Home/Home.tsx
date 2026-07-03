import React from 'react';
import styles from './Home.module.css';
import { useAppDispatch, useAppSelector } from '../../store/store';
import { useLogoutMutation } from '../../store/services/authApi';
import { logoutAction } from '../../store/slices/authSlice';
import { useNavigate } from 'react-router';

export const Home: React.FC = () => {
   const dispatch = useAppDispatch();
   const navigate = useNavigate();
   const { user } = useAppSelector((state) => state.auth);
   const [logout, { isLoading: isLoggingOut }] = useLogoutMutation();

   const handleLogout = async () => {
      try {
         // 1. Стучимся на бэкенд, чтобы он удалил HttpOnly куку
         await logout().unwrap();
         navigate('/login')
      } catch (err) {
         console.error('Ошибка при выходе с бэкенда:', err);
      } finally {
         // 2. В любом случае чистим стейт фронтенда, чтобы разлогинить юзера в UI
         dispatch(logoutAction());
      }
   };

   return (
      <div className={styles.container}>
         <header className={styles.header}>
            <div className={styles.welcomeSection}>
               <h1>Панель управления</h1>
               <p>Оператор: {user?.name || user?.email || 'Администратор'}</p>
            </div>
            <button
               className={styles.logoutButton}
               onClick={handleLogout}
               disabled={isLoggingOut}
            >
               {isLoggingOut ? 'Выход...' : 'Выйти из системы'}
            </button>
         </header>

         <main className={styles.dashboardGrid}>
            <div className={styles.card}>
               <h3>Статус сканера</h3>
               <p className={styles.cardValue} style={{ color: '#7ee787' }}>Готов</p>
            </div>

            <div className={styles.card}>
               <h3>Всего сканирований</h3>
               <p className={styles.cardValue}>0</p>
            </div>

            <div className={styles.card}>
               <h3>Найдено устройств</h3>
               <p className={styles.cardValue} style={{ color: '#ffa657' }}>0</p>
            </div>
         </main>
      </div>
   );
};

export default Home;