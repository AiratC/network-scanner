import React, { useEffect } from 'react';
import { useGetMeQuery } from './store/services/authApi';
import { setCredentials, logout } from './store/slices/authSlice';
import { useAppDispatch, useAppSelector } from './store/store';
import Login from './pages/Login/Login';

export const App: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  
  // Автоматически проверяем куку при загрузке приложения
  const { data: userData, isLoading, isError } = useGetMeQuery();

  useEffect(() => {
    if (userData) {
      // Если бэкенд подтвердил куку — восстанавливаем стейт в Redux
      dispatch(setCredentials(userData));
    } else if (isError) {
      // Если токен невалиден — принудительно разлогиниваем в стейте
      dispatch(logout());
    }
  }, [userData, isError, dispatch]);

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#0d1117', color: '#f0f6fc' }}>
        <h3>Инициализация защищенной сессии...</h3>
      </div>
    );
  }

  // Если не авторизован — показываем страницу входа
  if (!isAuthenticated) {
    return <Login />;
  }

  // Если авторизован — показываем основное приложение сканера
  return (
    <div style={{ padding: '20px', color: '#f0f6fc', backgroundColor: '#0d1117', minHeight: '100vh' }}>
      <h1>Панель управления Network Scanner</h1>
      <p>Добро пожаловать в систему!</p>
      {/* Сюда позже встанет наш роутер основных страниц и сканера */}
    </div>
  );
};

export default App;
