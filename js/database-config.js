/**
 * SciMSPT Database Configuration
 * FREE TIER OPTIONS
 * 
 * Primary: Supabase (PostgreSQL) - 500MB free, 50K MAU
 * Alternative: PlanetScale - 5GB free, 1B row reads/month
 * Cache: Upstash Redis (10K commands/day free)
 */

const DB_CONFIG = {
  // Supabase PostgreSQL (Primary Free Tier)
  supabase: {
    url: process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://YOUR_PROJECT.supabase.co',
    anonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'YOUR_ANON_KEY',
    
    tables: {
      users: 'users',
      projects: 'projects',
      quantum_jobs: 'quantum_jobs',
      pipeline_runs: 'pipeline_runs',
      datasets: 'datasets',
      api_keys: 'api_keys',
      audit_logs: 'audit_logs'
    },
    
    freeTier: {
      databaseSize: '500 MB',
      rowsReadMonthly: '5 billion',
      rowsWrittenMonthly: '50 million',
      concurrentConnections: 60,
      backupRetention: '28 days'
    }
  },
  
  // PlanetScale (Alternative Free Tier)
  planetScale: {
    host: process.env.PLANETSCALE_HOST || 'YOUR_HOST.us-east-1.psdb.cloud',
    username: process.env.PLANETSCALE_USERNAME || 'YOUR_USERNAME',
    password: process.env.PLANETSCALE_PASSWORD || 'YOUR_PASSWORD',
    
    freeTier: {
      databaseSize: '5 GB',
      rowsReadMonthly: '1 billion',
      rowsWrittenMonthly: '10 million',
      readUnits: '1 billion',
      writeUnits: '25 million'
    }
  },
  
  // Upstash Redis (Cache Layer - Free)
  redis: {
    url: process.env.UPSTASH_REDIS_REST_URL || 'https://YOUR.upstash.io',
    token: process.env.UPSTASH_REDIS_REST_TOKEN || 'YOUR_TOKEN',
    
    freeTier: {
      commandsPerDay: 10000,
      maxCommandsPerSecond: 100,
      storage: '10,000 keys',
      connections: 1000
    }
  },
  
  // Cloudflare R2 Storage (File Storage - Free)
  r2: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID || 'YOUR_ACCOUNT_ID',
    accessKeyId: process.env.R2_ACCESS_KEY_ID || 'YOUR_ACCESS_KEY',
    secretAccessKey: process.env.R2_SECRET_KEY || 'YOUR_SECRET_KEY',
    bucket: 'scimspt-files',
    publicUrl: 'https://pub-YOUR_BUCKET.r2.dev',
    
    freeTier: {
      storage: '10 GB',
      classAOperations: '1M/month',
      classBOperations: '10M/month',
      egressBandwidth: 'UNLIMITED FREE' // Key advantage over S3!
    }
  }
};

module.exports = DB_CONFIG;
