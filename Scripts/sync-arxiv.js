/**
 * SciMSPT - arXiv OAI-PMH Synchronizer
 * 
 * This script syncs preprint data from arXiv using the OAI-PMH protocol.
 * Designed for efficient daily delta synchronization.
 * 
 * Usage: node Scripts/sync-arxiv.js [options]
 * 
 * Rate Limit: 1 request per 3 seconds (strict!)
 * Best Practice: Use OAI-PMH for bulk, query API for specific searches
 * 
 * Categories of Interest:
 *   cs.AI - Artificial Intelligence
 *   cs.LG - Machine Learning
 *   cs.CL - Computation and Language
 *   stat.ML - Machine Learning (Statistics)
 *   q-bio.* - Quantitative Biology (all subcategories)
 *   physics.quant-ph - Quantum Physics
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  oaiEndpoint: 'http://export.arxiv.org/oai2',
  queryEndpoint: 'http://export.arxiv.org/api/query',
  outputDir: process.env.OUTPUT_DIR || 'data/arxiv_sync',
  rateLimitDelay: 3500, // 3.5 seconds between requests (safety margin)
  maxResults: 100, // Max per request
  timeout: 60000,
  debug: process.env.DEBUG === 'true'
};

// Relevant categories for SciMSPT
const RELEVANT_CATEGORIES = [
  { prefix: 'cs.AI', name: 'Artificial Intelligence', domain: 'Computing' },
  { prefix: 'cs.LG', name: 'Machine Learning', domain: 'Computing' },
  { prefix: 'cs.CL', name: 'Computation and Language', domain: 'Computing' },
  { prefix: 'stat.ML', name: 'Machine Learning', domain: 'Statistics' },
  { prefix: 'q-bio.BM', name: 'Biomolecules', domain: 'Biology' },
  { prefix: 'q-bio.QM', name: 'Quantitative Methods', domain: 'Biology' },
  { prefix: 'q-bio.GN', name: 'Genomics', domain: 'Biology' },
  { prefix: 'physics.quant-ph', name: 'Quantum Physics', domain: 'Physics' },
  { prefix: 'cond-mat.mes-hall', name: 'Mesoscale & Nanoscale', domain: 'Materials' }
];

// Logging
const log = {
  info: (msg) => console.log(`[INFO] ${new Date().toISOString()} - ${msg}`),
  error: (msg) => console.error(`[ERROR] ${new Date().toISOString()} - ${msg}`),
  debug: (msg) => CONFIG.debug && console.log(`[DEBUG] ${new Date().toISOString()} - ${msg}`)
};

/**
 * Sleep utility for rate limiting
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Make HTTP request with rate limiting
 */
async function makeRequest(url) {
  await sleep(CONFIG.rateLimitDelay);
  
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    
    const req = client.get(url, { timeout: CONFIG.timeout }, (res) => {
      if (res.statusCode === 503) {
        // arXiv returns 503 when rate limited
        log.warn('Rate limited by arXiv, waiting longer...');
        return sleep(10000).then(() => makeRequest(url)).then(resolve).catch(reject);
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
 * Parse OAI-PMH XML response
 */
function parseOAIResponse(xml) {
  // Simple XML parsing (use xml2js in production)
  const records = [];
  
  // Extract records
  const recordRegex = /<record>([\s\S]*?)<\/record>/g;
  let match;
  
  while ((match = recordRegex.exec(xml)) !== null) {
    const recordContent = match[1];
    
    const extractField = (tag) => {
      const fieldMatch = recordContent.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i'));
      return fieldMatch ? fieldMatch[1].trim() : null;
    };
    
    // Extract metadata fields
    const titleMatch = recordContent.match(/<title>([\s\S]*?)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : null;
    
    // Extract authors
    const authors = [];
    const authorRegex = /<author>([\s\S]*?)<\/author>/g;
    let authorMatch;
    while ((authorMatch = authorRegex.exec(recordContent)) !== null) {
      const nameMatch = authorMatch[1].match(/<name>([\s\S]*?)<\/name>/i);
      if (nameMatch) authors.push(nameMatch[1].trim());
    }
    
    // Extract categories
    const categories = [];
    const catRegex = /<category[^>]*>([\s\S]*?)<\/category>/g;
    let catMatch;
    while ((catMatch = catRegex.exec(recordContent)) !== null) {
      categories.push(catMatch[1].trim());
    }
    
    // Extract abstract
    const abstractMatch = recordContent.match(/<abstract>([\s\S]*?)<\/abstract>/i);
    const abstract = abstractMatch ? abstractMatch[1].trim() : null;
    
    // Extract identifier (arXiv ID)
    const idMatch = recordContent.match(/<identifier>([\s\S]*?)<\/identifier>/i);
    const identifier = idMatch ? idMatch[1].replace('oai:arXiv:', '').trim() : null;
    
    // Extract date
    const dateMatch = recordContent.match(/<datestamp>([\s\S]*?)<\/datestamp>/i);
    const dateStamp = dateMatch ? dateMatch[1].trim() : null;
    
    if (title && identifier) {
      records.push({
        id: identifier,
        title,
        authors,
        abstract,
        categories,
        publishedDate: dateStamp,
        sourceUrl: `https://arxiv.org/abs/${identifier}`,
        pdfUrl: `https://arxiv.org/pdf/${identifier}`
      });
    }
  }
  
  return records;
}

/**
 * Fetch records from OAI-PMH endpoint
 */
async function fetchOAIPMH(fromDate, toDate, setSpec = null) {
  let url = `${CONFIG.oaiEndpoint}?verb=ListRecords&metadataPrefix=oai_dc`;
  
  if (fromDate) url += `&from=${fromDate}`;
  if (toDate) url += `&until=${toDate}`;
  if (setSpec) url += `&set=${setSpec}`;
  
  log.info(`Fetching from OAI-PMH: ${setSpec || 'all sets'}`);
  log.debug(`URL: ${url}`);
  
  try {
    const xml = await makeRequest(url);
    return parseOAIResponse(xml);
  } catch (error) {
    log.error(`OAI-PMH fetch failed: ${error.message}`);
    return [];
  }
}

/**
 * Search using arXiv query API
 */
async function searchArxiv(query, start = 0, maxResults = CONFIG.maxResults) {
  const encodedQuery = encodeURIComponent(query);
  const url = `${CONFIG.queryEndpoint}?search_query=${encodedQuery}&start=${start}&max_results=${maxResults}&sortBy=submittedDate&sortOrder=descending`;
  
  log.info(`Searching arXiv: ${query}`);
  log.debug(`URL: ${url}`);
  
  try {
    const xml = await makeRequest(url);
    return parseQueryResponse(xml);
  } catch (error) {
    log.error(`Search failed: ${error.message}`);
    return [];
  }
}

/**
 * Parse query API response
 */
function parseQueryResponse(xml) {
  const entries = [];
  
  const entryRegex = /<entry>([\s\S]*?)<\/entry>/g;
  let match;
  
  while ((match = entryRegex.exec(xml)) !== null) {
    const content = match[1];
    
    const extractTag = (tag) => {
      const tagMatch = content.match(new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, 'i'));
      return tagMatch ? tagMatch[1].trim() : null;
    };
    
    entries.push({
      id: extractTag('id')?.replace('http://arxiv.org/abs/', ''),
      title: extractTag('title'),
      summary: extractTag('summary'),
      published: extractTag('published'),
      authors: extractAuthors(content),
      categories: extractCategories(content),
      pdfLink: extractTag('link')?.attr?.href || `https://arxiv.org/pdf/${extractTag('id')?.split('/').pop()}`,
      primaryCategory: extractTag('arxiv:primary_category')
    });
  }
  
  return entries;
}

// Helper functions for query parser
function extractAuthors(content) {
  const authors = [];
  const regex = /<author>([\s\S]*?)<\/author>/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const nameMatch = match[1].match(/<name>([\s\S]*?)<\/name>/i);
    if (nameMatch) authors.push(nameMatch[1].trim());
  }
  return authors;
}

function extractCategories(content) {
  const cats = [];
  const regex = /<category[^>]*term="([^"]*)"[^>]*\/?>/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    cats.push(match[1]);
  }
  return cats;
}

/**
 * Classify paper into SciMSPT domains
 */
function classifyPaper(paper) {
  const allCategories = (paper.categories || []).join(' ').toLowerCase();
  const title = (paper.title || '').toLowerCase();
  const text = `${allCategories} ${title}`;
  
  // Domain mapping
  if (/cs\.(ai|lg|cl)|machine.learning|deep.learning|neural/i.test(text)) {
    return { domain: 'Computing', code: 'SD-M', icon: '💻' };
  }
  if (/quant|physics/i.test(text)) {
    return { domain: 'Physics', code: 'SD-S', icon: '⚛️' };
  }
  if (/q-bio|biology|genom|protein/i.test(text)) {
    return { domain: 'Biology', code: 'SD-P', icon: '🧬' };
  }
  if (/cond-mat|material|nanotech/i.test(text)) {
    return { domain: 'Materials', code: 'SD-M', icon: '🔬' };
  }
  
  return { domain: 'General', code: 'SD-G', icon: '📄' };
}

/**
 * Calculate startup potential score
 */
function calculatePotential(paper) {
  let score = 40; // Base score
  
  // Category boosters
  const highValueCategories = ['cs.AI', 'cs.LG', 'quant-ph', 'cond-mat.mes-hall'];
  if (paper.categories?.some(c => highValueCategories.includes(c))) {
    score += 20;
  }
  
  // Title indicators
  const breakthroughWords = [
    'breakthrough', 'novel', 'efficient', 'scalable', 'state-of-the-art',
    'first', 'new method', 'improved', 'robust', 'real-time'
  ];
  
  const titleLower = (paper.title || '').toLowerCase();
  breakthroughWords.forEach(word => {
    if (titleLower.includes(word)) score += 5;
  });
  
  // Author count (more collaborators = more potential)
  if (paper.authors?.length > 5) score += 10;
  
  return Math.min(score, 100);
}

/**
 * Main sync function
 */
async function syncArxiv() {
  log.info('Starting arXiv synchronization');
  log.info(`Output directory: ${CONFIG.outputDir}`);
  
  const results = {
    metadata: {
      syncedAt: new Date().toISOString(),
      source: 'arXiv OAI-PMH + Query API',
      categoriesSynced: RELEVANT_CATEGORIES.length,
      version: '1.0.0'
    },
    papers: [],
    summary: {}
  };
  
  // Create output directory
  fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  
  try {
    // Method 1: Query each relevant category
    for (const category of RELEVANT_CATEGORIES) {
      log.info(`Fetching category: ${category.prefix} (${category.name})`);
      
      const papers = await searchArxiv(`cat:${category.prefix}`);
      
      // Enrich with classification and scoring
      const enrichedPapers = papers.map(paper => ({
        ...paper,
        classification: classifyPaper(paper),
        analysis: {
          ventureScore: calculatePotential(paper),
          isHighPotential: false
        },
        metadata: {
          categoryInfo: category,
          syncedAt: new Date().toISOString()
        }
      }));
      
      // Mark high potential
      enrichedPapers.forEach(p => {
        p.analysis.isHighPotential = p.analysis.ventureScore > 70;
      });
      
      results.papers.push(...enrichedPapers);
      results.summary[category.prefix] = {
        name: category.name,
        count: papers.length,
        highPotential: enrichedPapers.filter(p => p.analysis.isHighPotential).length
      };
      
      log.info(`  Found ${papers.length} papers (${enrichedPapers.filter(p => p.analysis.isHighPotential).length} high potential)`);
    }
    
    // Sort by potential score
    results.papers.sort((a, b) => b.analysis.ventureScore - a.analysis.ventureScore);
    
    // Save results
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputPath = path.join(CONFIG.outputDir, `arxiv-sync-${timestamp}.json`);
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    log.info(`Saved to ${outputPath}`);
    
    // Update latest
    const latestPath = path.join(CONFIG.outputDir, 'latest.json');
    fs.writeFileSync(latestPath, JSON.stringify(results, null, 2));
    
    // Print summary
    console.log('\n═══════════════════════════════════════════');
    console.log('  ARXIV SYNC COMPLETE');
    console.log('═══════════════════════════════════════════');
    console.log(`  Total Papers:       ${results.papers.length}`);
    console.log(`  High Potential:     ${results.papers.filter(p => p.analysis.isHighPotential).length}`);
    console.log('\n  By Category:');
    Object.entries(results.summary).forEach(([code, info]) => {
      console.log(`    ${code}: ${info.count} papers (${info.highPotential} high potential)`);
    });
    console.log(`\n  Output: ${outputPath}`);
    console.log('═══════════════════════════════════════════\n');
    
    return results;
    
  } catch (error) {
    log.error(`Sync failed: ${error.message}`);
    throw error;
  }
}

/**
 * CLI interface
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help')) {
    console.log(`
SciMSPT arXiv Synchronizer

Usage: node Scripts/sync-arxiv.js [options]

Options:
  --categories     List configured categories
  --search <query> Quick search (bypasses full sync)
  --help           Show this help message

Environment Variables:
  OUTPUT_DIR    Output directory (default: data/arxiv_sync)
  DEBUG         Enable debug logging

Examples:
  node Scripts/sync-arxiv.js                    # Full sync
  node Scripts/sync-arxiv.js --search "quantum" # Quick search
  node Scripts/sync-arxiv.js --categories       # List categories

Rate Limit Notes:
  - arXiv allows ~1 request per 3 seconds
  - This script waits 3.5 seconds between requests
  - Bulk sync of 9 categories takes ~35 seconds

Categories Synced:
${RELEVANT_CATEGORIES.map(c => `  ${c.prefix} - ${c.name} (${c.domain})`).join('\n')}
    `);
    process.exit(0);
  }
  
  if (args.includes('--categories')) {
    console.log('\nConfigured Categories:\n');
    RELEVANT_CATEGORIES.forEach(cat => {
      console.log(`${cat.prefix.padEnd(20)} ${cat.name.padEnd(30)} ${cat.domain}`);
    });
    process.exit(0);
  }
  
  // Quick search mode
  const searchIndex = args.indexOf('--search');
  if (searchIndex !== -1 && args[searchIndex + 1]) {
    const query = args[searchIndex + 1];
    log.info(`Quick search mode: ${query}`);
    const results = await searchArxiv(query);
    console.log(JSON.stringify(results, null, 2));
    process.exit(0);
  }
  
  // Full sync mode
  await syncArxiv();
}

// Run if executed directly
if (require.main === module) {
  main().catch(() => process.exit(1));
}

// Exports for testing
module.exports = {
  CONFIG,
  RELEVANT_CATEGORIES,
  syncArxiv,
  searchArxiv,
  classifyPaper,
  calculatePotential
};
