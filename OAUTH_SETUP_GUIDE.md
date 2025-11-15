# Google OAuth Setup Guide

This guide will help you configure Google OAuth authentication for the marketplace application.

## Prerequisites

- A Google account
- Access to [Google Cloud Console](https://console.cloud.google.com/)

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "Marketplace App")
5. Click "Create"

### 2. Enable Required APIs

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google+ API" or "Google Identity"
3. Click on it and click "Enable"

### 3. Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" user type (unless you have a Google Workspace)
3. Click "Create"
4. Fill in the required fields:
   - **App name**: Marketplace Application
   - **User support email**: Your email
   - **Developer contact email**: Your email
5. Click "Save and Continue"
6. Skip the "Scopes" section (click "Save and Continue")
7. Add test users if needed (your email address)
8. Click "Save and Continue"

### 4. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Select "Web application" as the application type
4. Enter a name (e.g., "Marketplace Web Client")
5. Under "Authorized redirect URIs", add:
   ```
   http://127.0.0.1:5000/auth
   http://localhost:5000/auth
   ```
6. Click "Create"
7. A dialog will appear with your **Client ID** and **Client Secret**
8. Copy both values (you'll need them for the `.env` file)

### 5. Configure Your Application

1. Open the `.env` file in your project root
2. Replace the placeholder values:
   ```
   SECRET_KEY=<generate-a-random-string>
   GOOGLE_CLIENT_ID=<your-client-id-from-step-4>
   GOOGLE_CLIENT_SECRET=<your-client-secret-from-step-4>
   ```

3. Generate a secure SECRET_KEY:
   ```bash
   python3 -c "import os; print(os.urandom(24).hex())"
   ```
   Copy the output and use it as your SECRET_KEY

### 6. Restart Your Application

After updating the `.env` file, restart your Flask application for the changes to take effect.

## Troubleshooting

### Error: "redirect_uri_mismatch"

This means the redirect URI in your Google Cloud Console doesn't match what your application is sending.

**Solution:**
- Make sure you added both `http://127.0.0.1:5000/auth` and `http://localhost:5000/auth` to the Authorized redirect URIs
- The URI must match exactly (including the protocol, domain, port, and path)

### Error: "The server cannot process the request because it is malformed"

This usually means:
- The Client ID or Client Secret is incorrect
- The OAuth consent screen isn't properly configured
- The redirect URI isn't authorized

**Solution:**
- Double-check your credentials in the `.env` file
- Verify the OAuth consent screen is configured
- Ensure redirect URIs are added in Google Cloud Console

### Error: "Access blocked: This app's request is invalid"

This means the OAuth consent screen needs to be properly configured.

**Solution:**
- Complete all required fields in the OAuth consent screen
- Add your email as a test user if the app is in testing mode

## Testing

1. Start your application: `./venv/bin/python application.py`
2. Open your browser and go to `http://127.0.0.1:5000`
3. Click "Login with Google"
4. You should be redirected to Google's login page
5. After logging in, you'll be redirected back to your application

## Security Notes

- **Never commit your `.env` file to version control**
- The `.env` file is already in `.gitignore`
- Keep your Client Secret confidential
- For production, use environment variables instead of a `.env` file
- Consider using a more secure secret key generation method for production

## Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Authlib Flask Documentation](https://docs.authlib.org/en/latest/client/flask.html)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
