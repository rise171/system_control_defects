import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, LoginRequest
from app.repository.auth_repos import AuthRepos
from app.services.auth_services import AuthService
from app.core.security import hash_password, verify_password


class TestAuthReposUnit:
    @pytest.mark.asyncio
    async def test_register_user_success(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.return_value = Mock(scalar=Mock(return_value=None))
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        email = "test@example.com"
        name = "Test User"
        password = "password123"
        role = UserRole.ENGINEER
        user_id = await AuthRepos.register_user(email, name, password, role, mock_session)
        assert user_id is not None
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self):
        mock_session = AsyncMock(spec=AsyncSession)
        existing_user = Mock()
        mock_session.execute.return_value = Mock(scalar=Mock(return_value=existing_user))
    
        user_id = await AuthRepos.register_user(
            "existing@example.com", "Test User", "password123", UserRole.ENGINEER, mock_session
        )
        
        assert user_id is None
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_user = Mock(spec=User)
        mock_user.password_hash = hash_password("correct_password")
        mock_session.execute.return_value = Mock(scalar_one_or_none=Mock(return_value=mock_user))
        
        result = await AuthRepos.authenticate_user("test@example.com", "correct_password", mock_session)
        
        assert result == mock_user
    
    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_user = Mock(spec=User)
        mock_user.password_hash = hash_password("correct_password")
        mock_session.execute.return_value = Mock(scalar_one_or_none=Mock(return_value=mock_user))
        
        result = await AuthRepos.authenticate_user("test@example.com", "wrong_password", mock_session)
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.return_value = Mock(scalar_one_or_none=Mock(return_value=None))
        
        result = await AuthRepos.authenticate_user("nonexistent@example.com", "password", mock_session)
        
        assert result is None


class TestAuthServiceUnit:
    @pytest.mark.asyncio
    async def test_register_user_success(self):
        mock_session = AsyncMock(spec=AsyncSession)
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.ENGINEER
        )
        
        with patch.object(AuthRepos, 'register_user', AsyncMock(return_value=1)):
            with patch.object(AuthService, 'get_user_profile', AsyncMock(return_value=Mock(id=1))):
                user_id = await AuthService.register_user(user_data, mock_session)
                
                assert user_id == 1
    
    @pytest.mark.asyncio
    async def test_register_user_failure(self):
        mock_session = AsyncMock(spec=AsyncSession)
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            name="Test User",
            role=UserRole.ENGINEER
        )
        
        with patch.object(AuthRepos, 'register_user', AsyncMock(return_value=None)):
            # Act & Assert
            result = await AuthService.register_user(user_data, mock_session)
            assert result is None
    
    @pytest.mark.asyncio
    async def test_login_user_success(self):
        mock_session = AsyncMock(spec=AsyncSession)
        email = "test@example.com"
        password = "password123"
        
        expected_token = {
            "access_token": "mock_jwt_token",
            "user_id": 1,
            "role": UserRole.ENGINEER
        }
        
        with patch.object(AuthRepos, 'login_user', AsyncMock(return_value=expected_token)):
            result = await AuthService.login_user(email, password, mock_session)
            
            assert result["access_token"] == expected_token
            assert result["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_user_invalid_credentials(self):
        mock_session = AsyncMock(spec=AsyncSession)
        email = "test@example.com"
        password = "wrong_password"
        
        with patch.object(AuthRepos, 'login_user', AsyncMock(return_value=None)):
            with pytest.raises(HTTPException) as exc_info:
                await AuthService.login_user(email, password, mock_session)
            
            assert exc_info.value.status_code == 401
            assert "Invalid credentials" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_get_user_profile_success(self):
        mock_session = AsyncMock(spec=AsyncSession)
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_user.role = UserRole.ENGINEER
        
        mock_session.execute.return_value = Mock(scalar=Mock(return_value=mock_user))
        
        result = await AuthService.get_user_profile(1, mock_session)
        
        assert result == mock_user
        assert result.id == 1
        assert result.email == "test@example.com"


class TestSecurityUnit:
    def test_hash_and_verify_password(self):
        password = "test_password_123"
        
        hashed = hash_password(password)
        verification_result = verify_password(password, hashed)
        
        assert hashed != password
        assert verification_result is True
    
    def test_verify_wrong_password(self):
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(correct_password)
        
        verification_result = verify_password(wrong_password, hashed)
        
        assert verification_result is False