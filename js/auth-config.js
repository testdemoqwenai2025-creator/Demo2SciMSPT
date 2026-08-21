/**
 * SciMSPT Authentication Configuration
 * SUPABASE FREE TIER - Ready to Connect
 * 
 * Setup Guide:
 * 1. Create free account at https://supabase.com
 * 2. New Project → Get URL + anon key
 * 3. Enable Auth → Providers → Google & GitHub
 * 4. Replace values below
 */

const AUTH_CONFIG = {
  // Supabase Configuration (Free Tier - 50K MAU)
  supabase: {
    // === REPLACE THESE WITH YOUR SUPABASE CREDENTIALS ===
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://PROJECT_ID.supabase.co',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'YOUR_ANON_KEY_HERE',
    
    // Demo mode settings
    demoMode: true, // Set to false when real credentials are added
    
    enabled: true,
    limits: {
      mau: 50000, // Monthly Active Users free tier
      storage: 1, // GB free
      bandwidth: 2 // GB monthly
    }
  },
  
  // Firebase Configuration (Alternative Free Tier)
  firebase: {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || '',
    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || '',
    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || '',
    enabled: false,
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
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      scopes: ['email', 'profile', 'openid'],
      freeTier: true,
      setupUrl: 'https://console.cloud.google.com/apis/credentials'
    },
    github: {
      enabled: true,
      clientId: process.env.GITHUB_CLIENT_ID || '',
      scopes: ['read:user', 'user:email'],
      freeTier: true,
      rateLimit: 5000,
      setupUrl: 'https://github.com/settings/developers'
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
  },
  
  // Environment check
  isConfigured: function() {
    return this.supabase.url && !this.supabase.url.includes('PROJECT_ID') && 
           this.supabase.anonKey && !this.supabase.anonKey.includes('YOUR_');
  }
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AUTH_CONFIG;
}
