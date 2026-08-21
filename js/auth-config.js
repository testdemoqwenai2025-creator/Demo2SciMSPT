/**
 * SciMSPT Authentication Configuration
 * FREE TIER INFRASTRUCTURE
 * 
 * Provider: Supabase Auth (Free Tier - 50K MAU)
 * Alternative: Firebase Auth (Free Tier - No cost for basic auth)
 * 
 * OAuth Providers: Google, GitHub (both free)
 */

const AUTH_CONFIG = {
  // Supabase Configuration (Recommended Free Tier)
  supabase: {
    url: 'https://YOUR_PROJECT.supabase.co', // Users replace with their Supabase URL
    anonKey: 'YOUR_ANON_KEY', // Users replace with their anon key
    enabled: true,
    limits: {
      mau: 50000, // Monthly Active Users free tier
      storage: 1, // GB free
      bandwidth: 2 // GB monthly
    }
  },
  
  // Firebase Configuration (Alternative Free Tier)
  firebase: {
    apiKey: 'YOUR_API_KEY',
    authDomain: 'YOUR_PROJECT.firebaseapp.com',
    projectId: 'YOUR_PROJECT_ID',
    enabled: false, // Set true to use Firebase instead
    limits: {
      mau: null, // Unlimited free for auth
      storage: 5, // GB free
      bandwidth: 1 // GB daily
    }
  },
  
  // OAuth Providers (Both Free)
  providers: {
    google: {
      enabled: true,
      scopes: ['email', 'profile', 'openid'],
      freeTier: true
    },
    github: {
      enabled: true,
      scopes: ['read:user', 'user:email'],
      freeTier: true,
      rateLimit: 5000 // requests/hour
    }
  },
  
  // Session Config
  session: {
    storageKey: 'scimspt-auth-token',
    duration: 3600 * 24 * 7, // 7 days
    autoRefresh: true
  },
  
  // Feature Flags by Plan
  plans: {
    free: {
      quantumJobsPerDay: 10,
      pipelineRunsPerDay: 5,
      storageMB: 100,
      collaborators: 1,
      apiCallsPerHour: 100
    },
    pro: { // $49/mo equivalent features
      quantumJobsPerDay: 1000,
      pipelineRunsPerDay: 100,
      storageMB: 10000,
      collaborators: 10,
      apiCallsPerHour: 10000
    }
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AUTH_CONFIG;
}
