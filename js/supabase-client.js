/**
 * SciMSPT Supabase Client
 * Real Integration with Error Handling
 */

class SciMSPTSupabase {
  constructor() {
    this.client = null;
    this.isConnected = false;
    this.initialized = false;
  }

  async init() {
    if (this.initialized) return this.client;

    try {
      // Dynamic import of Supabase JS (loaded from CDN)
      const { createClient } = await import('@supabase/supabase-js');
      
      const config = typeof AUTH_CONFIG !== 'undefined' ? AUTH_CONFIG : null;
      
      if (!config?.supabase?.url || config.supabase.url.includes('PROJECT_ID')) {
        console.warn('⚠️ Supabase not configured. Using demo mode.');
        this.setupDemoMode();
        return this.client;
      }

      this.client = createClient(
        config.supabase.url,
        config.supabase.anonKey,
        {
          auth: {
            autoRefreshToken: true,
            persistSession: true,
            detectSessionInUrl: true
          }
        }
      );

      this.isConnected = true;
      this.initialized = true;
      console.log('✅ Supabase connected successfully');
      
      return this.client;

    } catch (error) {
      console.error('❌ Supabase initialization failed:', error);
      this.setupDemoMode();
      return this.client;
    }
  }

  setupDemoMode() {
    // Mock client for development/demo
    this.client = {
      auth: {
        getUser: () => Promise.resolve({ data: { user: null }, error: null }),
        signInWithOAuth: () => Promise.resolve({ data: { user: null }, error: null }),
        signOut: () => Promise.resolve({ error: null }),
        onAuthStateChange: (callback) => ({ data: { subscription: { unsubscribe: () => {} } } }),
        getSession: () => Promise.resolve({ data: { session: null }, error: null })
      },
      from: (table) => ({
        select: () => ({
          order: () => ({ limit: () => Promise.resolve({ data: [], error: null }) }),
          eq: () => ({ single: () => Promise.resolve({ data: null, error: null }) }),
          insert: () => Promise.resolve({ data: null, error: null }),
          update: () => Promise.resolve({ data: null, error: null }),
          delete: () => Promise.resolve({ data: null, error: null })
        })
      }),
      isConnected: false,
      isDemo: true
    };
    this.isConnected = false;
    this.initialized = true;
  }

  // Auth helpers
  async signInWithGoogle() {
    await this.init();
    const { data, error } = await this.client.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: window.location.origin + '/dashboard.html'
      }
    });
    return { data, error };
  }

  async signInWithGitHub() {
    await this.init();
    const { data, error } = await this.client.auth.signInWithOAuth({
      provider: 'github',
      options: {
        redirectTo: window.location.origin + '/dashboard.html'
      }
    });
    return { data, error };
  }

  async signOut() {
    await this.init();
    return await this.client.auth.signOut();
  }

  async getCurrentUser() {
    await this.init();
    const { data: { user }, error } = await this.client.auth.getUser();
    return { user, error };
  }

  // Database helpers
  async getProjects(userId) {
    await this.init();
    const { data, error } = await this.client
      .from('projects')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });
    return { data, error };
  }

  async saveQuantumJob(jobData) {
    await this.init();
    const { data, error } = await this.client
      .from('quantum_jobs')
      .insert([jobData])
      .select()
      .single();
    return { data, error };
  }

  async savePipelineRun(runData) {
    await this.init();
    const { data, error } = await this.client
      .from('pipeline_runs')
      .insert([runData])
      .select()
      .single();
    return { data, error };
  }

  // Connection status
  getStatus() {
    return {
      connected: this.isConnected,
      initialized: this.initialized,
      isDemo: this.client?.isDemo || false,
      url: this.client?._supabaseUrl || 'Not configured'
    };
  }
}

// Singleton instance
const scimsptSupabase = new SciMSPTSupabase();

// Auto-initialize when DOM ready
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    scimsptSupabase.init().then(() => {
      window.dispatchEvent(new CustomEvent('supabase:ready'));
    });
  });
}

export default scimsptSupabase;
if (typeof module !== 'undefined') module.exports = { SciMSPTSupabase, scimsptSupabase };
