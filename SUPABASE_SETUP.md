# 🚀 Supabase Setup Guide for SciMSPT

## Quick Start (5 minutes)

### Step 1: Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" 
3. Sign up with GitHub/Google (free!)
4. Create organization: `SciMSPT`

### Step 2: Create Project
1. Click "New Project"
2. Name: `scimspt-production`
3. Database password: Generate strong password (save it!)
4. Region: Closest to your users (US East / EU West)
5. Pricing plan: **Free** (50K MAU, 500MB DB)

### Step 3: Get Credentials
1. Go to **Settings → API**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJ...` (long string)

### Step 4: Configure Authentication
1. Go to **Authentication → Providers**
2. Enable **Google**:
   - Get Client ID/Secret from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Add authorized redirect: `https://xxxxx.supabase.co/auth/v1/callback`
3. Enable **GitHub**:
   - Create OAuth app at [github.com/settings/applications/new](https://github.com/settings/applications/new)
   - Authorization callback: `https://xxxxx.supabase/auth/v1/callback`

### Step 5: Create Database Tables
Run this SQL in **SQL Editor**:

```sql
-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  avatar_url TEXT,
  plan TEXT DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects table
CREATE TABLE IF NOT EXISTS public.projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  type TEXT DEFAULT 'research' CHECK (type IN ('research', 'quantum', 'pipeline')),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Quantum jobs table
CREATE TABLE IF NOT EXISTS public.quantum_jobs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
  circuit_json JSONB NOT NULL,
  backend TEXT NOT NULL,
  shots INTEGER DEFAULT 1024,
  results JSONB,
  status TEXT DEFAULT 'queued' CHECK (status IN ('queued', 'running', 'completed', 'failed')),
  error_message TEXT,
  execution_time_ms INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Pipeline runs table
CREATE TABLE IF NOT EXISTS public.pipeline_runs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  config JSONB NOT NULL,
  results JSONB,
  record_count INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
  error_message TEXT,
  execution_time_ms INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- Datasets table
CREATE TABLE IF NOT EXISTS public.datasets (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  type TEXT NOT NULL,
  format TEXT DEFAULT 'json' CHECK (format IN ('json', 'csv', 'parquet')),
  size_bytes BIGINT DEFAULT 0,
  record_count INTEGER DEFAULT 0,
  schema_info JSONB DEFAULT '{}',
  storage_path TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quantum_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pipeline_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.datasets ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can view own projects" ON public.projects FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own projects" ON public.projects FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own projects" ON public.projects FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own projects" ON public.projects FOR DELETE USING (auth.uid() = user_id);

-- Similar policies for other tables...
CREATE POLICY "Users can view own quantum_jobs" ON public.quantum_jobs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own quantum_jobs" ON public.quantum_jobs FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own pipeline_runs" ON public.pipeline_runs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own pipeline_runs" ON public.pipeline_runs FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own datasets" ON public.datasets FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own datasets" ON public.datasets FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Function to handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, display_name, avatar_url)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user signup
CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Indexes for performance
CREATE INDEX idx_projects_user_id ON public.projects(user_id);
CREATE INDEX idx_quantum_jobs_user_id ON public.quantum_jobs(user_id);
CREATE INDEX idx_pipeline_runs_user_id ON public.pipeline_runs(user_id);
CREATE INDEX idx_datasets_user_id ON public.datasets(user_id);
CREATE INDEX idx_quantum_jobs_status ON public.quantum_jobs(status);
CREATE INDEX idx_pipeline_runs_status ON public.pipeline_runs(status);
```

### Step 6: Update Code
Edit `/js/auth-config.js` with your credentials:

```javascript
supabase: {
  url: 'https://YOUR_REAL_PROJECT_ID.supabase.co',
  anonKey: 'YOUR_REAL_ANON_KEY',
  demoMode: false  // Switch to false!
}
```

### Step 7: Test
1. Open any page in browser
2. Click login button
3. Should redirect to Google/GitHub OAuth
4. After auth, redirected back with session

## Free Tier Limits Reference

| Resource | Free Limit | Pro Upgrade |
|----------|-----------|-------------|
| Users | 50K MAU | Unlimited |
| Database | 500MB | 8GB+ |
| File Storage | 1GB | 100GB+ |
| Bandwidth | 2GB/month | 250GB/month |
| Real-time | 50K connections | Unlimited |
| Edge Functions | 500K invocations | 2M+ |

## Support
- Docs: https://supabase.com/docs
- Discord: https://discord.supabase.com
- GitHub Issues: https://github.com/supabase/supabase/issues
