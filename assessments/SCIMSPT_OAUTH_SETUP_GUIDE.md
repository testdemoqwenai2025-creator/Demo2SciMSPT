# SciMSPT OAuth Setup Guide

## 🎯 Overview
This guide walks you through setting up GitHub OAuth authentication for the SciMSPT platform. Once configured, users can sign in with their GitHub accounts.

---

## 🔧 Step 1: Create GitHub OAuth App

### 1.1 Navigate to GitHub Settings
1. Go to **https://github.com/settings/developers**
2. Click **"New OAuth App"** button

### 1.2 Fill in OAuth App Details
| Field | Value |
|-------|-------|
| **Application name** | `SciMSPT Research Platform` |
| **Homepage URL** | `https://testdemoqwenai2025-creator.github.io/SciMSPT/` |
| **Application description** | `Research platform for transforming scientific papers into investment opportunities` |
| **Authorization callback URL** | `https://testdemoqwenai2025-creator.github.io/SciMSPT/` |

> **Note**: GitHub OAuth supports a single callback URL. The implicit-flow callback (`#access_token=...`) preserves the original URL fragment.

### 1.3 Register Application
1. Click **"Register application"**
2. On the next page, you'll see your **Client ID** (public)

### 1.4 Generate Client Secret
1. Click **"Generate a new client secret"**
2. **Copy the secret value immediately** - you won't be able to see it again!

---

## 🔐 Step 2: Store Credentials Securely

### Option A: GitHub Actions Secret (Recommended for Worker Backend)
1. Go to your **SciMSPT-private** repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Name: `OAUTH_CLIENT_SECRET`
5. Value: *(paste the Client Secret you copied)*
6. Click **Add secret**

### Option B: Environment Variable (For Frontend Only)
Create a `.env` file in your project:
```env
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
```

> ⚠️ **Security Warning**: Never commit secrets to public repositories!

---

## 🔗 Step 3: Integrate with SciMSPT Code

### 3.1 Update Login Modal JavaScript

Once you have your Client ID, update the `oauthLogin()` function in `index.html`:

```javascript
function oauthLogin(provider) {
  const clientId = 'YOUR_GITHUB_CLIENT_ID_HERE'; // Replace with your actual Client ID
  const redirectUri = encodeURIComponent('https://testdemoqwenai2025-creator.github.io/SciMSPT/');
  
  if (provider === 'github') {
    // GitHub OAuth using Implicit Grant Flow
    const authUrl = `https://github.com/login/oauth/authorize?` +
      `client_id=${clientId}&` +
      `redirect_uri=${redirectUri}&` +
      `scope=read:user&` +
      `state=${Math.random().toString(36).substring(7)}`;
    
    window.location.href = authUrl;
  } 
  else if (provider === 'google') {
    // Google OAuth setup required separately
    alert('Google OAuth coming soon! For now, use GitHub or email/password.');
  }
}
```

### 3.2 Handle OAuth Callback

Add this code to handle the OAuth callback when GitHub redirects back:

```javascript
// Check for OAuth callback on page load
(function checkOAuthCallback() {
  const hash = window.location.hash;
  if (hash.includes('access_token')) {
    const params = new URLSearchParams(hash.substring(1));
    const token = params.get('access_token');
    
    if (token) {
      // Store token securely
      sessionStorage.setItem('scimspt_token', token);
      
      // Fetch user info
      fetch('https://api.github.com/user', {
        headers: { 'Authorization': `token ${token}` }
      })
      .then(res => res.json())
      .then(user => {
        console.log('Logged in as:', user.login);
        // Update UI to show logged-in state
        showLoggedInState(user);
      })
      .catch(err => console.error('Auth error:', err));
      
      // Clean URL
      history.replaceState(null, '', window.location.pathname);
    }
  }
})();

function showLoggedInState(user) {
  // Update login button to show user info
  const loginBtn = document.querySelector('.btn-login');
  if (loginBtn) {
    loginBtn.innerHTML = `<img src="${user.avatar_url}" class="avatar"> ${user.login}`;
    loginBtn.onclick = () => logout();
  }
}

function logout() {
  sessionStorage.removeItem('scimspt_token');
  location.reload();
}
```

### 3.3 Add CSS for Avatar

```css
.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
  vertical-align: middle;
}
```

---

## ✅ Step 4: Test OAuth Flow

1. **Clear browser cache** (or use incognito mode)
2. **Go to**: https://testdemoqwenai2025-creator.github.io/SciMSPT/
3. **Click "Login" button**
4. **Click "Continue with GitHub"**
5. **Authorize the application** on GitHub's consent screen
6. **Verify you're redirected back** and logged in

---

## 🚀 Step 5: Deploy Worker Backend (Optional but Recommended)

For production use with comment storage and rate limiting:

### Prerequisites
- Node.js 18+
- Cloudflare account (free tier)

### Deploy Cloudflare Worker

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Navigate to worker directory
cd /path/to/SciMSPT-private/worker

# Set secrets
wrangler secret put GITHUB_REPO_TOKEN
wrangler secret put GITHUB_REPO_OWNER
wrangler secret put GITHUB_REPO_NAME

# Create KV namespace for rate limiting
wrangler kv namespace create RATE_LIMIT

# Deploy!
wrangler deploy
```

### Configure Worker Endpoint

After deployment, update your site's JavaScript:

```javascript
window.SCIMSPT_COMMENT_ENDPOINT = 'https://scimspt-comments.YOUR-SUBDOMAIN.workers.dev';
```

---

## 📋 OAuth Scopes Explained

| Scope | Purpose | Required? |
|-------|---------|-----------|
| `read:user` | Read user profile (name, login, avatar) | ✅ Yes |
| `public_repo` | Write comments to public repos | Optional (for comments) |

> For the Worker pattern (recommended), you only need `read:user` scope since the Worker uses its own server-side token for writing.

---

## 🔒 Security Best Practices

1. **Use HTTPS always** (GitHub Pages provides this automatically)
2. **Validate state parameter** to prevent CSRF attacks
3. **Store tokens securely** (sessionStorage, not localStorage)
4. **Implement token expiration checks**
5. **Rate limit API calls** from the frontend
6. **Never expose Client Secret** in frontend code

---

## 🆘 Troubleshooting

### Issue: "Redirect URI mismatch"
- **Cause**: Callback URL doesn't match exactly
- **Fix**: Ensure trailing slashes match in both GitHub settings and code

### Issue: "Access denied"
- **Cause**: User denied authorization or scope issue
- **Fix**: Check requested scopes match what's configured

### Issue: Token not working
- **Cause**: Token expired or invalid
- **Fix**: Implement proper error handling and re-auth flow

---

## 📞 Next Steps

After OAuth is working:
1. ✅ Set up Google OAuth (optional)
2. ✅ Deploy Worker backend for comments
3. ✅ Add user preferences storage
4. ✅ Implement session persistence
5. ✅ Add admin dashboard features

---

**Last Updated**: August 20, 2026  
**Version**: 1.0  
**Platform**: SciMSPT Research Platform
