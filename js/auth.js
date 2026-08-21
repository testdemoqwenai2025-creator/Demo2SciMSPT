/**
 * SciMSPT Authentication Module
 * Free Tier: Supabase Auth / Firebase Auth
 */

class SciMSPTAuth {
  constructor() {
    this.config = typeof AUTH_CONFIG !== 'undefined' ? AUTH_CONFIG : null;
    this.user = null;
    this.isLoading = false;
    this.listeners = [];
    this.init();
  }

  async init() {
    // Check for existing session
    const savedSession = localStorage.getItem('scimspt-auth-token');
    if (savedSession) {
      try {
        this.user = JSON.parse(savedSession);
        this.notifyListeners();
      } catch (e) {
        console.warn('Failed to parse saved session');
      }
    }
    
    // Setup UI event listeners
    this.setupUIListeners();
  }

  setupUIListeners() {
    document.addEventListener('DOMContentLoaded', () => {
      // Login buttons
      document.querySelectorAll('[data-auth="login-google"]').forEach(btn => {
        btn.addEventListener('click', () => this.loginWithGoogle());
      });
      
      document.querySelectorAll('[data-auth="login-github"]').forEach(btn => {
        btn.addEventListener('click', () => this.loginWithGitHub());
      });
      
      document.querySelectorAll('[data-auth="logout"]').forEach(btn => {
        btn.addEventListener('click', () => this.logout());
      });
      
      this.updateUIForAuthState();
    });
  }

  async loginWithGoogle() {
    this.isLoading = true;
    this.updateUILoading(true);
    
    try {
      // For demo/simulation mode (no backend)
      if (this.isDemoMode()) {
        await this.simulateOAuthLogin({
          provider: 'google',
          email: 'user@gmail.com',
          name: 'Google User',
          avatar: 'https://ui-avatars.com/api/?name=Google+User&background=4285f4&color=fff'
        });
        return;
      }
      
      // Real Supabase/Firebase implementation would go here
      // const { data, error } = await supabase.auth.signInWithOAuth({ provider: 'google' });
      
    } catch (error) {
      console.error('Google login error:', error);
      this.showError('Login failed. Please try again.');
    } finally {
      this.isLoading = false;
      this.updateUILoading(false);
    }
  }

  async loginWithGitHub() {
    this.isLoading = true;
    this.updateUILoading(true);
    
    try {
      // For demo/simulation mode
      if (this.isDemoMode()) {
        await this.simulateOAuthLogin({
          provider: 'github',
          email: 'user@github.com',
          name: 'GitHub User',
          avatar: 'https://ui-avatars.com/api/?name=GitHub+User&background=333&color=fff'
        });
        return;
      }
      
      // Real implementation would go here
      
    } catch (error) {
      console.error('GitHub login error:', error);
      this.showError('Login failed. Please try again.');
    } finally {
      this.isLoading = false;
      this.updateUILoading(false);
    }
  }

  isDemoMode() {
    // Demo mode when no real credentials configured
    return !this.config?.supabase?.url || this.config.supabase.url.includes('YOUR_');
  }

  async simulateOAuthLogin(userData) {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    this.user = {
      id: `demo_${Date.now()}`,
      ...userData,
      plan: 'free',
      loginTime: new Date().toISOString(),
      token: 'demo_token_' + Math.random().toString(36).substr(2, 16)
    };
    
    localStorage.setItem('scimspt-auth-token', JSON.stringify(this.user));
    this.notifyListeners();
    this.updateUIForAuthState();
    this.showSuccess(`Welcome, ${this.user.name}!`);
  }

  logout() {
    this.user = null;
    localStorage.removeItem('scimspt-auth-token');
    this.notifyListeners();
    this.updateUIForAuthState();
    
    // Redirect to home or show logged out state
    window.dispatchEvent(new CustomEvent('auth:logout'));
  }

  isAuthenticated() {
    return !!this.user;
  }

  getUser() {
    return this.user;
  }

  getPlanLimits() {
    const plan = this.user?.plan || 'free';
    return this.config?.plans[plan] || this.config?.plans.free;
  }

  onAuthChange(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(l => l !== callback);
    };
  }

  notifyListeners() {
    this.listeners.forEach(callback => callback(this.user));
  }

  updateUIForAuthState() {
    const authButtons = document.querySelectorAll('[data-auth-show]');
    const userMenu = document.querySelector('[data-user-menu]');
    
    authButtons.forEach(el => {
      const showWhen = el.dataset.authShow; // 'authenticated' or 'unauthenticated'
      const shouldShow = showWhen === 'authenticated' ? this.isAuthenticated() : !this.isAuthenticated();
      el.style.display = shouldShow ? '' : 'none';
    });
    
    if (userMenu && this.user) {
      userMenu.innerHTML = `
        <img src="${this.user.avatar}" alt="${this.user.name}" class="user-avatar">
        <span class="user-name">${this.user.name}</span>
        <span class="user-plan">${this.user.plan}</span>
      `;
    }
  }

  updateUILoading(isLoading) {
    document.querySelectorAll('[data-auth]').forEach(btn => {
      btn.disabled = isLoading;
      btn.classList.toggle('loading', isLoading);
    });
  }

  showError(message) {
    this.showToast(message, 'error');
  }

  showSuccess(message) {
    this.showToast(message, 'success');
  }

  showToast(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `auth-toast auth-toast-${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️'}</span>
      <span class="toast-message">${message}</span>
    `;
    
    // Style the toast
    Object.assign(toast.style, {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      padding: '12px 20px',
      background: type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#00E5FF',
      color: '#fff',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: '500',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      zIndex: '10000',
      animation: 'slideInRight 0.3s ease',
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
    });
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.style.animation = 'slideOutRight 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

// Initialize auth instance
const scimsptAuth = new SciMSPTAuth();

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SciMSPTAuth, scimsptAuth };
}
