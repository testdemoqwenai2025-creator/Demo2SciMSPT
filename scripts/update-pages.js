/**
 * Batch Update Script for SciMSPT Pages
 * =======================================
 * Adds global components integration to all HTML pages:
 * - Global Components CSS
 * - Global Components JS  
 * - Google Analytics 4 tracking
 * - Search overlay support
 */

const fs = require('fs');
const path = require('path');

// Main pages to update (excluding subdirectories like shorts, portfolio-shorts, video-clips, assets)
const MAIN_PAGES = [
  'about.html',
  'dashboard.html', 
  'research.html',
  'startups.html',
  'quantum.html',
  'platform.html',
  'infrastructure.html',
  'studio.html',
  'documentation.html',
  'security.html',
  'monitoring.html',
  'scaling.html',
  'changelog.html',
  'physics-observatory.html',
  'search-results.html',
  'slides.html',
  'pipeline-demo.html',
  'startups-enhancement.html',
  'test-features.html'
];

const GLOBAL_CSS_LINK = '<link rel="stylesheet" href="css/global-components.css">';
const GLOBAL_JS_SCRIPT = `  <!-- Global Components System v3.0 -->
  <script src="js/global-components.js"></script>`;
  
const GA4_SCRIPT = `  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX', { send_page_view: true });
  </script>`;

function updatePage(filePath) {
  console.log(`\n📄 Processing: ${filePath}`);
  
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    
    // Check if already has global components
    if (!content.includes('global-components.css')) {
      // Add CSS link after design-system.css or in head
      const cssInsertPoint = content.indexOf('design-system.css');
      if (cssInsertPoint !== -1) {
        const lineEnd = content.indexOf('>', cssInsertPoint) + 1;
        content = content.slice(0, lineEnd) + '\n' + GLOBAL_CSS_LINK + content.slice(lineEnd);
        modified = true;
        console.log('  ✅ Added global-components.css');
      }
    } else {
      console.log('  ⏭️  Already has global-components.css');
    }
    
    // Check if already has global components JS
    if (!content.includes('global-components.js')) {
      // Replace or add before closing body tag
      if (content.includes('search-system.js')) {
        content = content.replace(
          /<script src="js\/search-system\.js"><\/script>/g,
          GLOBAL_JS_SCRIPT
        );
        modified = true;
        console.log('  ✅ Replaced search-system.js with global-components.js');
      } else {
        // Add before </body>
        content = content.replace('</body>', GLOBAL_JS_SCRIPT + '\n</body>');
        modified = true;
        console.log('  ✅ Added global-components.js');
      }
    } else {
      console.log('  ⏭️  Already has global-components.js');
    }
    
    // Check if already has GA4
    if (!content.includes('googletagmanager.com/gtag/js')) {
      // Add GA4 before </body>
      content = content.replace('</body>', GA4_SCRIPT + '\n</body>');
      modified = true;
      console.log('  ✅ Added Google Analytics 4');
    } else {
      console.log('  ⏭️  Already has Google Analytics 4');
    }
    
    if (modified) {
      fs.writeFileSync(filePath, content, 'utf8');
      console.log('  💾 File updated successfully');
      return { success: true, file: filePath };
    } else {
      console.log('  ℹ️  No changes needed');
      return { success: true, file: filePath, skipped: true };
    }
    
  } catch (error) {
    console.error(`  ❌ Error processing ${filePath}:`, error.message);
    return { success: false, file: filePath, error: error.message };
  }
}

// Main execution
console.log('🚀 SciMSPT Page Updater v3.0');
console.log('================================\n');

const basePath = path.dirname(__dirname); // Go up from scripts directory
const results = [];

MAIN_PAGES.forEach(page => {
  const fullPath = path.join(basePath, page);
  
  if (fs.existsSync(fullPath)) {
    results.push(updatePage(fullPath));
  } else {
    console.log(`\n⚠️  File not found: ${page}`);
    results.push({ success: false, file: page, error: 'File not found' });
  }
});

// Summary
console.log('\n\n================================');
console.log('📊 UPDATE SUMMARY');
console.log('================================');

const success = results.filter(r => r.success && !r.skipped).length;
const skipped = results.filter(r => r.skipped).length;
const failed = results.filter(r => !r.success).length;

console.log(`✅ Updated: ${success} files`);
console.log(`⏭️  Skipped: ${skipped} files`);
console.log(`❌ Failed: ${failed} files`);

if (failed > 0) {
  console.log('\nFailed files:');
  results.filter(r => !r.success).forEach(r => {
    console.log(`  - ${r.file}: ${r.error}`);
  });
}

console.log('\n✨ Update complete!');
