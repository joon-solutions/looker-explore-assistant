import React, { useEffect } from 'react';
import { useOAuthAuthentication } from '../../hooks/useOAuthAuthentication';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { setAuthenticated, setToken, setExpiry } from '../../slices/authSlice';

// Export a function that takes both access_token and expires_in
export const isTokenExpired = (access_token: string | null, expires_in: number | null) => {
  console.group('Token Verification Check');
  console.log('Current token:', access_token);
  console.log('Expiry time:', new Date(expires_in).toLocaleString());
  console.log('Current time:',  new Date().toLocaleString());
  
  if (!expires_in) {
    console.log('No expiry time found, treating as expired');
    console.groupEnd();
    return true;
  }
  
  const expiryTime = new Date(expires_in).getTime();
  const currentTime = new Date().getTime();
  const isExpired = currentTime >= expiryTime;
  
  console.log('Token expired?', isExpired);
  console.log('Time until expiration:', (expiryTime - currentTime) / 1000, 'seconds');
  console.log('Expiry in local time:', new Date(expiryTime).toLocaleString());
  console.groupEnd();
  return isExpired;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const dispatch = useDispatch();
  const authenticate = useOAuthAuthentication();
  const { access_token, expires_in } = useSelector((state: RootState) => state.auth);
  


  useEffect(() => {
    const initializeAuth = async () => {
      if (!access_token || isTokenExpired(access_token, expires_in)) {
        try {
          const authResult = await authenticate();
          if (authResult?.access_token) {
            const newExpiry = Date.now() + (authResult.expires_in * 1000);
            dispatch(setAuthenticated(true));
            dispatch(setToken(authResult.access_token));
            dispatch(setExpiry(newExpiry));
          }
        } catch (error) {
          console.error('Auth failed:', error);
        }
      }
    };

    initializeAuth();
  }, []);

  return <>{children}</>;
};
