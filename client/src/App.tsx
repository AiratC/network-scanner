import React, { useEffect } from 'react';
import { useGetMeQuery } from './store/services/authApi';
import { setCredentials, logoutAction } from './store/slices/authSlice';
import { useAppDispatch, useAppSelector } from './store/store';
import Login from './pages/Login/Login';
import Home from './pages/Home/Home';
import { Route, Routes } from 'react-router';

export const App: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated, user } = useAppSelector((state) => state.auth);
  
  // Автоматически проверяем куку при загрузке приложения
  const { data: userData, isLoading, isError } = useGetMeQuery();

  useEffect(() => {
    if (userData) {
      // Если бэкенд подтвердил куку — восстанавливаем стейт в Redux
      dispatch(setCredentials(userData));
    } else if (isError) {
      // Если токен невалиден — принудительно разлогиниваем в стейте
      dispatch(logoutAction());
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
  if (!isAuthenticated && !user) {
    return <Login />;
  }

  // Если авторизован — рендерим полноценную главную страницу
  return (
    <Routes>
      <Route path='/login' element={<Login />}></Route>
      <Route path='/' element={<Home/>}></Route>
    </Routes>
  );
};

export default App;
