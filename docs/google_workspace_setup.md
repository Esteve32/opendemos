# Google Workspace Setup Guide

This guide will help you set up Google Workspace integration for the Gemini HTML Manager.

## Prerequisites

- Google account
- Access to Google Cloud Console
- Python 3.7+ installed

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "New Project" or select existing project
3. Enter project name (e.g., "Gemini HTML Manager")
4. Click "Create"

### 2. Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for and enable:
   - **Google Drive API**
   - **Google Docs API**

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" for user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For application type, select "Desktop application"
5. Name it "Gemini HTML Manager"
6. Click "Create"

### 4. Download Credentials

1. Click the download button next to your newly created OAuth client
2. Save the file as `credentials.json` in your project root directory
3. **Important**: Keep this file secure and never commit it to version control

### 5. Configure Application

1. Copy `config.example.yaml` to `config.yaml`
2. Ensure the `credentials_file` path is correct:
   ```yaml
   google:
     credentials_file: credentials.json
   ```

### 6. Test Authentication

Run the setup command:
```bash
python scripts/gemini_manager.py setup
```

This will:
- Check for credentials file
- Open a browser for authentication
- Save authentication tokens
- Test API access

### 7. Grant Permissions

When the browser opens:
1. Sign in to your Google account
2. Review the permissions requested:
   - View and manage Google Drive files
   - View and manage Google Docs
3. Click "Allow"

## Troubleshooting

### Common Issues

**"Credentials file not found"**
- Ensure `credentials.json` is in the project root
- Check the file path in `config.yaml`

**"Authentication failed"**
- Make sure APIs are enabled in Google Cloud Console
- Verify OAuth consent screen is configured
- Check that your email is added as a test user

**"Permission denied"**
- Review OAuth scopes in the consent screen
- Ensure you granted all required permissions

**"Invalid client"**
- Download fresh credentials from Google Cloud Console
- Ensure you selected "Desktop application" type

### Re-authentication

If you need to re-authenticate:
1. Delete `token.json` file
2. Run `python scripts/gemini_manager.py setup` again

## Security Best Practices

### Protecting Credentials

1. **Never commit credentials to version control**
   - `credentials.json` and `token.json` are in `.gitignore`
   
2. **Limit scope of permissions**
   - Only request necessary Google API scopes
   
3. **Use test users during development**
   - Add specific users to OAuth consent screen
   
4. **Regular credential rotation**
   - Regenerate credentials periodically
   
5. **Monitor API usage**
   - Check Google Cloud Console for unusual activity

### Production Deployment

For production use:
1. Create a production Google Cloud project
2. Configure OAuth consent screen for public use
3. Use environment variables for credentials
4. Implement proper access controls
5. Set up monitoring and logging

## API Quotas and Limits

### Google Drive API
- 1,000 requests per 100 seconds per user
- 10,000 requests per 100 seconds

### Google Docs API  
- 300 requests per 100 seconds per user
- 3,000 requests per 100 seconds

### Managing Usage
- The application implements basic rate limiting
- Monitor usage in Google Cloud Console
- Consider implementing more sophisticated caching

## Advanced Configuration

### Custom Scopes
Modify scopes in `config.yaml` if you need additional permissions:
```yaml
google:
  scopes:
    - https://www.googleapis.com/auth/documents
    - https://www.googleapis.com/auth/drive
    - https://www.googleapis.com/auth/drive.file
    - https://www.googleapis.com/auth/spreadsheets  # For Google Sheets
```

### Service Account (Advanced)
For server-to-server authentication:
1. Create a service account in Google Cloud Console
2. Download the service account key
3. Modify the authentication code to use service account credentials
4. Grant appropriate permissions to the service account

## Support

If you encounter issues:
1. Check the Google Cloud Console for API quotas and errors
2. Review the [Google Drive API documentation](https://developers.google.com/drive/api)
3. Check the [Google Docs API documentation](https://developers.google.com/docs/api)
4. Open an issue on the project repository