# SciMSPT Worker Backend Deployment Guide

## 🎯 Overview
Deploy the Cloudflare Worker backend for handling comments, authentication, and API requests for the SciMSPT platform.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐
│   Browser   │────▶│  Cloudflare      │────▶│  GitHub API       │
│  (SciMSPT)  │◀────│  Worker          │◀────│  (Private Repo)   │
└─────────────┘     └──────────────────┘     └───────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Cloudflare   │
                    │  KV Storage   │
                    │ (Rate Limit)  │
                    └──────────────┘
```

---

## 📋 Prerequisites

1. **Cloudflare Account** (free tier is sufficient)
2. **GitHub Personal Access Token** with `repo` scope
3. **Node.js** 18+ installed
4. **Wrangler CLI** installed globally

---

## 🔧 Step 1: Install Wrangler CLI

```bash
# Install Wrangler globally
npm install -g wrangler

# Verify installation
wrangler --version
```

---

## 🔐 Step 2: Authenticate with Cloudflare

```bash
# Login to your Cloudflare account
wrangler login

# This will open a browser window for authentication
# After login, you'll see success message
```

---

## 📁 Step 3: Prepare Worker Code

The worker code should be in `/worker/` directory of your SciMSPT-private repo.

### Expected Structure:
```
worker/
├── src/
│   ├── index.ts        # Main worker code
│   ├── types.ts        # Type definitions
│   └── utils/
│       ├── auth.ts     # Authentication helpers
│       └── rate-limit.ts # Rate limiting logic
├── wrangler.toml       # Configuration
└── package.json
```

---

## ⚙️ Step 4: Configure Worker Secrets

Navigate to your worker directory and set the required secrets:

```bash
cd /path/to/SciMSPT-private/worker

# GitHub Personal Access Token (with repo scope)
wrangler secret put GITHUB_REPO_TOKEN
# Enter your PAT when prompted

# Repository owner (your GitHub username or org name)
wrangler secret put GITHUB_REPO_OWNER
# Enter: testdemoqwenai2025-creator

# Repository name
wrangler secret put GITHUB_REPO_NAME
# Enter: SciMSPT-private
```

---

## 💾 Step 5: Create KV Namespace for Rate Limiting

```bash
# Create KV namespace for rate limiting
wrangler kv namespace create RATE_LIMIT

# Note the ID returned - add it to wrangler.toml:
# [[kv_namespaces]]
# binding = "RATE_LIMIT"
# id = "your_kv_namespace_id"
```

---

## 🚀 Step 6: Deploy Worker

```bash
# Deploy to Cloudflare Workers
wrangler deploy

# You'll see output like:
# Published your-worker-name (production)
# https://scimspt-comments.YOUR-SUBDOMAIN.workers.dev
```

**Save this URL!** You'll need it for the frontend configuration.

---

## 🔗 Step 7: Connect Frontend to Worker

Update your `index.html` to include the worker endpoint:

```javascript
// Add this before other JavaScript
window.SCIMSPT_CONFIG = {
  commentEndpoint: 'https://scimspt-comments.YOUR-SUBDOMAIN.workers.dev',
  githubClientId: 'YOUR_GITHUB_CLIENT_ID', // From OAuth setup
  apiVersion: 'v1'
};
```

---

## ✅ Step 8: Test Worker Deployment

### Test Health Endpoint
```bash
curl -X GET https://scimspt-comments.YOUR-SUBDOMAIN.workers.dev/health
# Should return: {"status":"ok","timestamp":"..."}
```

### Test Comment Submission (with valid token)
```bash
curl -X POST https://scimspt-comments.YOUR-SUBDOMAIN.workers.dev/comment \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "short_id": "SD-M-01",
    "author": "Test User",
    "author_login": "testuser",
    "body": "This is a test comment!",
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
  }'
```

---

## 📊 Monitoring & Analytics

### Cloudflare Dashboard
1. Go to **Cloudflare Dashboard → Workers & Pages**
2. Click on your worker
3. View **Analytics**, **Logs**, and **Metrics**

### Key Metrics to Monitor:
- Request count
- Error rate (should be < 1%)
- Average response time (< 200ms)
- KV read/write operations

---

## 🔒 Security Configuration

### Allowed Origins
Configure CORS in your worker to only allow requests from your domain:

```typescript
// In worker src/index.ts
const ALLOWED_ORIGINS = [
  'https://testdemoqwenai2025-creator.github.io',
  'http://localhost:3000' // For development
];
```

### Rate Limits
The worker includes built-in rate limiting:
- **Per-user**: 10 comments per hour
- **Global**: 1000 comments per day
- Adjust in `utils/rate-limit.ts` as needed

---

## 🔄 Continuous Deployment (Optional)

### Option A: GitHub Actions
Create `.github/workflows/deploy-worker.yml`:

```yaml
name: Deploy Worker
on:
  push:
    paths: ['worker/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          workingDirectory: worker
```

### Option B: Manual Deploy
Run `wrangler deploy` whenever you push changes to the worker directory.

---

## 💰 Cost Estimates

| Feature | Free Tier | Paid |
|---------|-----------|------|
| Requests/day | 100,000 | Unlimited |
| CPU time | 10ms/request | More |
| KV reads | 100K/day | $0.50/M |
| KV writes | 1K/day | $5.00/M |

> **For SciMSPT usage (~100 users)**, free tier is more than sufficient!

---

## 🆘 Troubleshooting

### Issue: "Authentication failed"
- **Cause**: Invalid GitHub token
- **Fix**: Verify `GITHUB_REPO_TOKEN` secret is correct

### Issue: "Rate limit exceeded"
- **Cause**: Too many requests from single user
- **Fix**: Check KV namespace is properly configured

### Issue: "CORS error"
- **Cause**: Origin not allowed
- **Fix**: Add domain to `ALLOWED_ORIGINS` array

### Issue: "KV namespace not found"
- **Cause**: Namespace not created or bound
- **Fix**: Run `wrangler kv namespace create RATE_LIMIT` again

---

## 📚 Additional Resources

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/)
- [KV Storage Docs](https://developers.cloudflare.com/workers/runtime-apis/kv/)
- [GitHub REST API](https://docs.github.com/en/rest)

---

## 🎯 Next Steps After Deployment

1. ✅ Set up monitoring alerts
2. ✅ Configure custom domain (optional)
3. ✅ Add analytics tracking
4. ✅ Implement comment moderation UI
5. ✅ Add email notifications for new comments

---

**Last Updated**: August 20, 2026  
**Version**: 1.0  
**Infrastructure**: Cloudflare Workers + KV + GitHub API
