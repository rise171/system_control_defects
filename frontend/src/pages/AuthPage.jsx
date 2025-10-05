import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../axios';
import { useNavigate } from 'react-router-dom';
import './AuthPage.css';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [formErrors, setFormErrors] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login: authLogin } = useAuth();
  const navigate = useNavigate();

  const validateForm = () => {
    const errors = {
      name: '',
      email: '',
      password: '',
    };
    let isValid = true;

    if (!isLogin && !formData.name.trim()) {
      errors.name = 'Имя пользователя обязательно';
      isValid = false;
    } else if (!isLogin && formData.name.length < 2) {
      errors.name = 'Имя пользователя должно быть не менее 2 символов';
      isValid = false;
    }

    if (!formData.email.trim()) {
      errors.email = 'Email обязателен';
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Введите корректный email';
      isValid = false;
    }

    if (!formData.password) {
      errors.password = 'Пароль обязателен';
      isValid = false;
    } else if (formData.password.length < 6) {
      errors.password = 'Пароль должен быть не менее 6 символов';
      isValid = false;
    }

    setFormErrors(errors);
    return isValid;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Очищаем ошибку поля при вводе
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      if (isLogin) {
        // Логин - используем существующий эндпоинт
        const requestData = {
          login: formData.email,
          password: formData.password
        };

        console.log("Отправляем запрос авторизации:", requestData);
        const response = await api.post('/user/login', requestData);
        console.log("Ответ сервера:", response.data);

        if (response.data) {
          const userData = {
            id: response.data.user?.id || response.data.id || response.data.user_id,
            email: formData.email,
            name: response.data.user?.name || formData.email.split('@')[0],
            role: response.data.role || 'engineer'
          };

          if (!userData.id && response.data.user) {
            console.log("Ищем ID в объекте пользователя:", response.data.user);
            userData.id = response.data.user.id || response.data.user.user_id;
          }

          if (!userData.id) {
            console.error("Не удалось найти ID пользователя в ответе:", response.data);
            throw new Error("Не удалось получить ID пользователя");
          }
          
          const token = response.data.access_token || response.data.token;
          authLogin(userData, token);
          navigate(userData.role === 'admin' ? '/admin' : '/user');
        } else {
          throw new Error("Неверный формат ответа от сервера");
        }
      } else {
        // Регистрация - используем новый формат согласно API
        const requestData = {
          email: formData.email,
          password: formData.password,
          name: formData.name,
          role: 'engineer' // По умолчанию создаем инженера
        };

        console.log("Отправляем запрос регистрации:", requestData);
        const response = await api.post('/auth/register', requestData);
        console.log("Ответ сервера:", response.data);

        if (response.data) {
          setIsLogin(true);
          setFormData(prev => ({
            ...prev,
            name: '',
            password: ''
          }));
          setError('Регистрация успешна! Теперь вы можете войти.');
        }
      }

    } catch (err) {
      console.error("Ошибка авторизации:", err);
      if (err.response) {
        console.log("Статус ошибки:", err.response.status);
        console.log("Данные ошибки:", err.response.data);
        
        // Более детальная обработка ошибок
        if (err.response.status === 400) {
          const errorData = err.response.data;
          if (errorData.detail) {
            if (typeof errorData.detail === 'string') {
              setError(errorData.detail);
            } else if (Array.isArray(errorData.detail)) {
              setError(errorData.detail.map(err => err.msg || err.message).join(', '));
            } else {
              setError('Неверные данные. Проверьте введенную информацию.');
            }
          } else if (errorData.message) {
            setError(errorData.message);
          } else {
            setError('Неверные данные. Проверьте введенную информацию.');
          }
        } else if (err.response.status === 409) {
          setError('Пользователь с таким email уже существует');
        } else if (err.response.status === 401) {
          setError('Неверный email или пароль');
        } else if (err.response.status === 500) {
          setError('Ошибка сервера. Попробуйте позже.');
        } else {
          setError(err.response?.data?.detail || err.message || "Произошла ошибка");
        }
      } else {
        setError("Ошибка сети. Проверьте подключение к интернету.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>{isLogin ? 'Вход' : 'Регистрация'}</h2>
        {error && <div className={`message-box ${error.includes('успешна') ? 'success-message' : 'error-message'}`}>
          {error}
        </div>}
        
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label htmlFor="name">Имя пользователя</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className={formErrors.name ? 'error' : ''}
                disabled={isLoading}
                placeholder="Введите ваше имя"
              />
              {formErrors.name && <span className="error-text">{formErrors.name}</span>}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className={formErrors.email ? 'error' : ''}
              disabled={isLoading}
              placeholder="user@example.com"
            />
            {formErrors.email && <span className="error-text">{formErrors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Пароль</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={formErrors.password ? 'error' : ''}
              disabled={isLoading}
              placeholder="Не менее 6 символов"
            />
            {formErrors.password && <span className="error-text">{formErrors.password}</span>}
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading 
              ? 'Загрузка...' 
              : (isLogin ? 'Войти' : 'Зарегистрироваться')
            }
          </button>
        </form>

        <p className="toggle-form">
          {isLogin ? "Нет аккаунта? " : "Уже есть аккаунт? "}
          <button
            className="toggle-button"
            onClick={() => {
              setIsLogin(!isLogin);
              setFormData({
                name: '',
                email: '',
                password: ''
              });
              setFormErrors({
                name: '',
                email: '',
                password: ''
              });
              setError('');
            }}
            disabled={isLoading}
          >
            {isLogin ? 'Зарегистрироваться' : 'Войти'}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthPage;