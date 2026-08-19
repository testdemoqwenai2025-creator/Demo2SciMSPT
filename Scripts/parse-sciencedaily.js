/**
 * SciMSPT - ScienceDaily RSS Parser
 * 
 * This script fetches and parses ScienceDaily RSS feeds
 * to extract weekly scientific breakthroughs.
 * 
 * Usage: node Scripts/parse-sciencedaily.js [options]
 * 
 * Options:
 *   --output <dir>    Output directory (default: data/weekly_digest)
 *   --weeks <n>       Number of weeks to parse (default: 1)
 *   --categories      List available categories
 *   --help            Show this help message
 * 
 * Environment Variables:
 *   SCIENCE_DAILY_URL  Custom RSS URL (optional)
 *   DEBUG              Enable debug logging
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  baseUrl: 'https://www.sciencedaily.com',
  rssFeed: process.env.SCIENCE_DAILY_URL || 'https://www.sciencedaily.com/rss/all.xml',
  outputDir: process.env.OUTPUT_DIR || 'data/weekly_digest',
  maxWeeks: parseInt(process.env.WEEKS) || 1,
  timeout: 30000, // 30 seconds
  debug: process.env.DEBUG === 'true'
};

// Category mapping for domain classification
const CATEGORY_MAP = {
  'Matter & Energy': {
    domains: ['physics', 'quantum', 'materials', 'energy', 'semiconductor'],
    code: 'SD-S',
    icon: '⚛️'
  },
  'Computers & Math': {
    domains: ['cs', 'ai', 'ml', 'mathematics', 'computing'],
    code: 'SD-M',
    icon: '💻'
  },
  'Plants & Animals': {
    domains: ['biology', 'biotech', 'genetics', 'evolution'],
    code: 'SD-P',
    icon: '🧬'
  },
  'Earth & Climate': {
    domains: ['climate', 'environmental', 'earth', 'geology'],
    code: 'SD-E',
    icon: '🌍'
  },
  'Fossils & Ruins': {
    domains: ['paleontology', 'archaeology', 'history'],
    code: 'SD-F',
    icon: '🦕'
  },
  'Space & Time': {
    domains: ['space', 'astronomy', 'cosmology', 'time'],
    code: 'SD-T',
    icon: '🚀'
  }
};

// Logging utility
const log = {
  info: (msg) => console.log(`[INFO] ${new Date().toISOString()} - ${msg}`),
  error: (msg) => console.error(`[ERROR] ${new Date().toISOString()} - ${msg}`),
  debug: (msg) => CONFIG.debug && console.log(`[DEBUG] ${new Date().toISOString()} - ${msg}`)
};

/**
 * Fetch URL content with proper error handling
 */
function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    
    const req = client.get(url, { timeout: CONFIG.timeout }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        log.info(`Following redirect to ${res.headers.location}`);
        return fetchUrl(res.headers.location).then(resolve).catch(reject);
      }
      
      if (res.statusCode !== 200) {
        return reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
      }
      
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

/**
 * Parse XML RSS feed into JSON objects
 */
function parseRSS(xmlString) {
  const items = [];
  
  // Simple XML parser (for production, use xml2js or similar)
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  let match;
  
  while ((match = itemRegex.exec(xmlString)) !== null) {
    const itemContent = match[1];
    
    const extractTag = (tag) => {
      const tagMatch = itemContent.match(new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, 'i'));
      return tagMatch ? tagMatch[1].replace(/<!\[CDATA\[(.*?)\]\]>/g, '$1').trim() : null;
    };
    
    items.push({
      title: extractTag('title'),
      link: extractTag('link'),
      description: extractTag('description'),
      pubDate: extractTag('pubDate'),
      category: extractTag('category'),
      guid: extractTag('guid')
    });
  }
  
  return items;
}

/**
 * Classify article into research domain
 */
function classifyArticle(article) {
  const text = `${article.title} ${article.description} ${article.category || ''}`.toLowerCase();
  
  for (const [category, info] of Object.entries(CATEGORY_MAP)) {
    for (const domain of info.domains) {
      if (text.includes(domain)) {
        return {
          category,
          code: info.code,
          icon: info.icon,
          confidence: 'high'
        };
      }
    }
  }
  
  // Default classification
  return {
    category: 'General Science',
    code: 'SD-G',
    icon: '🔬',
    confidence: 'low'
  };
}

/**
 * Extract DOI or identifier from article
 */
function extractIdentifier(article) {
  // Try to find DOI in link or description
  const doiMatch = article.link?.match(/10\.\d{4,}/);
  if (doiMatch) return { type: 'doi', value: doiMatch[0] };
  
  // Use GUID as fallback
  if (article.guid) return { type: 'guid', value: article.guid };
  
  // Generate from title hash
  const hash = Buffer.from(article.title).toString('base64').slice(0, 12);
  return { type: 'generated', value: `SD-${hash}` };
}

/**
 * Calculate venture potential score (simplified)
 */
function calculateVentureScore(article, classification) {
  let score = 50; // Base score
  
  // Boost for high-impact categories
  const highImpactCategories = ['Computers & Math', 'Matter & Energy'];
  if (highImpactCategories.includes(classification.category)) score += 15;
  
  // Keywords that indicate commercial potential
  const commercialKeywords = [
    'ai', 'machine learning', 'quantum', 'breakthrough', 'novel',
    'efficient', 'scalable', 'patent', 'startup', 'venture'
  ];
  
  const text = `${article.title} ${article.description}`.toLowerCase();
  commercialKeywords.forEach(keyword => {
    if (text.includes(keyword)) score += 5;
  });
  
  // Cap at 100
  return Math.min(score, 100);
}

/**
 * Process articles and generate structured output
 */
async function processArticles() {
  log.info(`Fetching RSS feed: ${CONFIG.rssFeed}`);
  
  try {
    const xmlContent = await fetchUrl(CONFIG.rssFeed);
    log.debug(`Fetched ${xmlContent.length} bytes`);
    
    const rawArticles = parseRSS(xmlContent);
    log.info(`Parsed ${rawArticles.length} articles from feed`);
    
    // Process each article
    const processedArticles = rawArticles.map(article => {
      const classification = classifyArticle(article);
      const identifier = extractIdentifier(article);
      const ventureScore = calculateVentureScore(article, classification);
      
      return {
        id: identifier.value,
        idType: identifier.type,
        title: article.title,
        summary: article.description?.replace(/<[^>]*>/g, '').substring(0, 500), // Strip HTML
        source: 'ScienceDaily',
        sourceUrl: article.link,
        publishedDate: article.pubDate ? new Date(article.pubDate).toISOString() : new Date().toISOString(),
        
        classification: {
          primaryCategory: classification.category,
          domainCode: classification.code,
          icon: classification.icon,
          confidence: classification.confidence
        },
        
        analysis: {
          venturePotentialScore: ventureScore,
          isHighPotential: ventureScore > 70,
          tags: extractTags(article.title + ' ' + (article.description || ''))
        },
        
        metadata: {
          parsedAt: new Date().toISOString(),
          parserVersion: '1.0.0'
        }
      };
    });
    
    // Filter and sort by potential
    const highPotential = processedArticles
      .filter(a => a.analysis.isHighPotential)
      .sort((a, b) => b.analysis.venturePotentialScore - a.analysis.venturePotentialScore);
    
    log.info(`Identified ${highPotential.length} high-potential articles (score > 70)`);
    
    return {
      metadata: {
        generatedAt: new Date().toISOString(),
        totalArticles: processedArticles.length,
        highPotentialCount: highPotential.length,
        source: 'ScienceDaily RSS',
        parserVersion: '1.0.0'
      },
      articles: processedArticles,
      highPotential: highPotential.slice(0, 20) // Top 20 for startup generation
    };
    
  } catch (error) {
    log.error(`Failed to process articles: ${error.message}`);
    throw error;
  }
}

/**
 * Extract relevant tags from text
 */
function extractTags(text) {
  const tags = new Set();
  
  const tagKeywords = [
    'artificial-intelligence', 'machine-learning', 'deep-learning',
    'quantum-computing', 'nanotechnology', 'biotechnology',
    'renewable-energy', 'materials-science', 'robotics',
    'genomics', 'neuroscience', 'climate-change'
  ];
  
  const lowerText = text.toLowerCase();
  tagKeywords.forEach(tag => {
    if (lowerText.includes(tag.replace(/-/g, ' '))) {
      tags.add(tag);
    }
  });
  
  return Array.from(tags);
}

/**
 * Save output files
 */
function saveOutput(data) {
  const timestamp = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  const weekNumber = getWeekNumber(new Date());
  const year = new Date().getFullYear();
  
  // Ensure output directory exists
  const dirPath = path.join(CONFIG.outputDir, `${year}`, `week${weekNumber}`);
  fs.mkdirSync(dirPath, { recursive: true });
  
  // Save full dataset
  const fullPath = path.join(dirPath, `sciencedaily-${timestamp}.json`);
  fs.writeFileSync(fullPath, JSON.stringify(data, null, 2));
  log.info(`Saved full dataset to ${fullPath}`);
  
  // Save high-potential only
  const highPotPath = path.join(dirPath, `high-potential-${timestamp}.json`);
  fs.writeFileSync(highPotPath, JSON.stringify(data.highPotential, null, 2));
  log.info(`Saved high-potential articles to ${highPotPath}`);
  
  // Update "latest" symlink/copy
  const latestDir = path.join(CONFIG.outputDir, 'latest');
  fs.mkdirSync(latestDir, { recursive: true });
  
  fs.writeFileSync(
    path.join(latestDir, 'articles.json'),
    JSON.stringify(data.articles, null, 2)
  );
  fs.writeFileSync(
    path.join(latestDir, 'high-potential.json'),
    JSON.stringify(data.highPotential, null, 2)
  );
  fs.writeFileSync(
    path.join(latestDir, 'metadata.json'),
    JSON.stringify(data.metadata, null, 2)
  );
  
  log.info(`Updated latest/ directory`);
  
  return { fullPath, highPotPath, latestDir };
}

/**
 * Get ISO week number
 */
function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

/**
 * Main execution function
 */
async function main() {
  const args = process.argv.slice(2);
  
  // Parse command line arguments
  if (args.includes('--help')) {
    console.log(`
SciMSPT ScienceDaily Parser

Usage: node Scripts/parse-sciencedaily.js [options]

Options:
  --output <dir>    Output directory (default: ${CONFIG.outputDir})
  --weeks <n>       Number of weeks to parse (default: ${CONFIG.maxWeeks})
  --categories      List available categories
  --help            Show this help message

Environment Variables:
  SCIENCE_DAILY_URL  Custom RSS URL
  OUTPUT_DIR         Output directory
  WEEKS              Number of weeks
  DEBUG              Enable debug logging

Examples:
  node Scripts/parse-sciencedaily.js
  node Scripts/parse-sciencedaily.js --output ./data/custom
  DEBUG=true node Scripts/parse-sciencedaily.js
    `);
    process.exit(0);
  }
  
  if (args.includes('--categories')) {
    console.log('\nAvailable Categories:\n');
    Object.entries(CATEGORY_MAP).forEach(([name, info]) => {
      console.log(`${info.icon} ${name} (${info.code})`);
      console.log(`   Domains: ${info.domains.join(', ')}\n`);
    });
    process.exit(0);
  }
  
  // Parse output directory argument
  const outputIndex = args.indexOf('--output');
  if (outputIndex !== -1 && args[outputIndex + 1]) {
    CONFIG.outputDir = args[outputIndex + 1];
  }
  
  log.info('Starting ScienceDaily RSS Parser');
  log.info(`Output directory: ${CONFIG.outputDir}`);
  
  try {
    const data = await processArticles();
    const paths = saveOutput(data);
    
    console.log('\n═══════════════════════════════════════════');
    console.log('  PARSE COMPLETE');
    console.log('═══════════════════════════════════════════');
    console.log(`  Total Articles:     ${data.metadata.totalArticles}`);
    console.log(`  High Potential:     ${data.metadata.highPotentialCount}`);
    console.log(`  Output Files:`);
    console.log(`    - ${paths.fullPath}`);
    console.log(`    - ${paths.highPotPath}`);
    console.log(`    - ${paths.latestDir}/ (latest)`);
    console.log('═══════════════════════════════════════════\n');
    
    // Exit with success
    process.exit(0);
    
  } catch (error) {
    log.error(`Parser failed: ${error.message}`);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

// Export for testing
module.exports = {
  CONFIG,
  parseRSS,
  classifyArticle,
  calculateVentureScore,
  processArticles,
  saveOutput
};
