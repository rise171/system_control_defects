import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, LoginRequest
from app.repository.auth_repos import AuthRepos
from app.services.auth_services import AuthService


class TestAuthReposMock:
    @pytest.mark.asyncio
    async def test_register_user_mock_dependencies(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = Mock()
        mock_result.scalar.return_value = None
        
        mock_session.execute.return_value = mock_result
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        with patch('app.repository.auth_repos.hash_password') as mock_hash:
            with patch('app.repository.auth_repos.User') as mock_user_class:
                mock_hash.return_value = "hashed_password"
                mock_new_user = Mock()
                mock_new_user.id = 1
                mock_user_class.return_value = mock_new_user
                
                user_id = await AuthRepos.register_user(
                    "test@example.com", "Test User", "password123", UserRole.ENGINEER, mock_session
                )
                
                assert user_id == 1
                mock_hash.assert_called_once_with("password123")
                mock_user_class.assert_called_once_with(
                    email="test@example.com",
                    name="Test User",
                    password_hash="hashed_password",
                    role=UserRole.ENGINEER
                )
                mock_session.add.assert_called_once_with(mock_new_user)
                mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_login_user_mock_authentication(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.role = UserRole.ENGINEER
        mock_user.password_hash = "hashed_password"
        
        with patch.object(AuthRepos, 'authenticate_user', AsyncMock(return_value=mock_user)):
            with patch('app.repository.auth_repos.create_jwt_token') as mock_create_token:
                mock_create_token.return_value = "mock_jwt_token"
                
                result = await AuthRepos.login_user("test@example.com", "password123", mock_session)
                
                assert result == {
                    "access_token": "mock_jwt_token",
                    "user_id": 1,
                    "role": UserRole.ENGINEER
                }
                mock_create_token.assert_called_once_with(data={"sub": "1"})


class TestAuthServiceMock:
    @pytest.mark.asyncio
    async def test_register_user_service_mock_chain(self):
        mock_session = AsyncMock(spec=AsyncSession)
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.ENGINEER
        )
        with patch.object(AuthRepos, 'register_user', AsyncMock(return_value=1)):
            with patch.object(AuthService, 'get_user_profile') as mock_get_profile:
                mock_user = Mock()
                mock_user.id = 1
                mock_get_profile.return_value = mock_user
                
                # Act
                result = await AuthService.register_user(user_data, mock_session)
                
                # Assert
                assert result == 1
                AuthRepos.register_user.assert_called_once_with(
                    "test@example.com", "Test User", "password123", UserRole.ENGINEER, mock_session
                )
    
    @pytest.mark.asyncio
    async def test_register_user_service_user_not_found_after_creation(self):
        mock_session = AsyncMock(spec=AsyncSession)
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.ENGINEER
        )
        
        with patch.object(AuthRepos, 'register_user', AsyncMock(return_value=1)):
            with patch.object(AuthService, 'get_user_profile', AsyncMock(return_value=None)):
                with pytest.raises(HTTPException) as exc_info:
                    await AuthService.register_user(user_data, mock_session)
                
                assert exc_info.value.status_code == 404
    
    @pytest.mark.asyncio
    async def test_login_user_service_mock_repository(self):
        mock_session = AsyncMock(spec=AsyncSession)
        email = "test@example.com"
        password = "password123"
        
        expected_token_response = {
            "access_token": "mock_jwt_token",
            "user_id": 1,
            "role": UserRole.ENGINEER
        }
        
        with patch.object(AuthRepos, 'login_user', AsyncMock(return_value=expected_token_response)):
            result = await AuthService.login_user(email, password, mock_session)
            
            assert result == {
                "access_token": expected_token_response,
                "token_type": "bearer"
            }
            AuthRepos.login_user.assert_called_once_with(email, password, mock_session)


class TestIntegrationMocks:
    
    @pytest.mark.asyncio
    async def test_complete_auth_flow_mock(self):
        mock_session = AsyncMock(spec=AsyncSession)
        
        register_data = UserCreate(
            email="newuser@example.com",
            password="secure_password",
            name="New User",
            role=UserRole.READER
        )
        
        login_data = LoginRequest(
            email="newuser@example.com",
            password="secure_password"
        )
        
        with patch.object(AuthRepos, 'register_user', AsyncMock(return_value=1)):
            with patch.object(AuthService, 'get_user_profile', AsyncMock(return_value=Mock(id=1))):
                user_id = await AuthService.register_user(register_data, mock_session)
                
                assert user_id == 1
        
        with patch.object(AuthRepos, 'login_user', AsyncMock(return_value={
            "access_token": "jwt_token_123",
            "user_id": 1,
            "role": UserRole.READER
        })):
            login_result = await AuthService.login_user(
                login_data.email, login_data.password, mock_session
            )
            assert login_result["token_type"] == "bearer"
            assert "access_token" in login_result
    
    @pytest.mark.asyncio
    async def test_user_roles_mock_validation(self):
        mock_session = AsyncMock(spec=AsyncSession)
        
        test_cases = [
            (UserRole.ADMIN, "admin_access"),
            (UserRole.MANAGER, "manager_access"),
            (UserRole.ENGINEER, "engineer_access"),
            (UserRole.READER, "reader_access"),
        ]
        
        for role, expected_access in test_cases:
            with patch.object(AuthRepos, 'login_user', AsyncMock(return_value={
                "access_token": f"token_for_{role.value}",
                "user_id": 1,
                "role": role
            })):
                result = await AuthService.login_user(
                    f"user_{role.value}@example.com", "password", mock_session
                )

                assert result["token_type"] == "bearer"
                auth_result = result["access_token"]
                assert auth_result["role"] == role