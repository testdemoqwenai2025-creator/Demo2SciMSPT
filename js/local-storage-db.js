/**
 * SciMSPT Local Storage Persistence Layer
 * Works offline as fallback/demo when Supabase not configured
 * 
 * @version 1.0.0
 * @license MIT
 */

class LocalStorageDB {
  constructor() {
    this.prefix = 'scimspt_';
    this.tables = ['projects', 'quantum_jobs', 'pipeline_runs', 'datasets', 'user_preferences'];
    this.version = '1.0.0';
    this.init();
  }

  /**
   * Initialize storage structure and load demo data if empty
   */
  init() {
    // Check if we need to migrate or initialize
    const versionKey = this.prefix + '_version';
    const storedVersion = localStorage.getItem(versionKey);
    
    // Initialize tables
    this.tables.forEach(table => {
      if (!localStorage.getItem(this.prefix + table)) {
        localStorage.setItem(this.prefix + table, JSON.stringify([]));
      }
    });
    
    // Add demo data if projects table is empty
    if (this.getAll('projects').length === 0) {
      console.log('[LocalDB] Initializing with demo data...');
      this.addDemoData();
    }
    
    // Update version marker
    localStorage.setItem(versionKey, this.version);
    
    console.log(`[LocalDB] Initialized v${this.version}`);
  }

  /**
   * Add sample demo data for first-time users
   */
  addDemoData() {
    // Sample projects for demo
    const demoProjects = [
      {
        id: this.generateId(),
        name: 'Quantum Chemistry Simulation',
        description: 'H2 molecule energy calculation using VQE algorithm',
        type: 'quantum',
        status: 'active',
        metadata: { qubits: 4, backend: 'ibmq_qasm_simulator', shots: 1024 },
        created_at: new Date(Date.now() - 86400000 * 2).toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: this.generateId(),
        name: 'Research Pipeline - Clinical Trials',
        description: 'Synthetic patient data generation for drug response prediction',
        type: 'pipeline',
        status: 'active',
        metadata: { records: 5000, format: 'csv', features: 12 },
        created_at: new Date(Date.now() - 86400000 * 5).toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: this.generateId(),
        name: 'Security Dataset Analysis',
        description: 'Authentication event pattern analysis with anomaly detection',
        type: 'research',
        status: 'archived',
        metadata: { records: 10000, anomalies_detected: 47 },
        created_at: new Date(Date.now() - 86400000 * 10).toISOString(),
        updated_at: new Date().toISOString()
      }
    ];

    // Sample quantum jobs
    const demoQuantumJobs = [
      {
        id: this.generateId(),
        project_id: demoProjects[0].id,
        circuit_json: { gates: ['h', 'cnot', 'measure'], qubits: 2 },
        backend: 'qasm_simulator',
        shots: 1024,
        results: { '00': 512, '11': 512 },
        status: 'completed',
        execution_time_ms: 145,
        created_at: new Date().toISOString()
      },
      {
        id: this.generateId(),
        project_id: demoProjects[0].id,
        circuit_json: { gates: ['rx', 'ry', 'cz', 'measure'], qubits: 4 },
        backend: 'qasm_simulator',
        shots: 2048,
        results: { '0000': 256, '1111': 230, '0011': 200, '1100': 215, '0101': 192, '1010': 198, 'others': 757 },
        status: 'completed',
        execution_time_ms: 287,
        created_at: new Date(Date.now() - 3600000).toISOString()
      }
    ];

    // Sample pipeline runs
    const demoPipelineRuns = [
      {
        id: this.generateId(),
        config: { source: 'random', transform: ['normalize', 'encode'], analysis: ['stats'] },
        results: { records_generated: 5000, columns: 12, size_kb: 225 },
        record_count: 5000,
        status: 'completed',
        execution_time_ms: 892,
        created_at: new Date().toISOString()
      },
      {
        id: this.generateId(),
        config: { source: 'synthetic', transform: ['scale', 'noise'], analysis: ['correlation'] },
        results: { records_generated: 10000, columns: 8, size_kb: 450 },
        record_count: 10000,
        status: 'completed',
        execution_time_ms: 1456,
        created_at: new Date(Date.now() - 7200000).toISOString()
      }
    ];

    // Sample datasets
    const demoDatasets = [
      {
        id: this.generateId(),
        name: 'Molecular Structures Dataset',
        description: '3D molecular coordinates for ML training',
        format: 'csv',
        size_bytes: 2450000,
        rows: 15000,
        columns: 25,
        created_at: new Date(Date.now() - 86400000 * 3).toISOString()
      }
    ];

    this.saveAll('projects', demoProjects);
    this.saveAll('quantum_jobs', demoQuantumJobs);
    this.saveAll('pipeline_runs', demoPipelineRuns);
    this.saveAll('datasets', demoDatasets);
    
    console.log('[LocalDB] Demo data loaded successfully');
  }

  /**
   * Generate a unique ID
   * @returns {string} Unique identifier
   */
  generateId() {
    return 'local_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Get all items from a table
   * @param {string} table - Table name
   * @returns {Array} All items in the table
   */
  getAll(table) {
    try {
      return JSON.parse(localStorage.getItem(this.prefix + table) || '[]');
    } catch (e) {
      console.error(`[LocalDB] Error reading ${table}:`, e);
      return [];
    }
  }

  /**
   * Save all items to a table (replaces existing)
   * @param {string} table - Table name
   * @param {Array} data - Data array to save
   * @returns {Array} Saved data
   */
  saveAll(table, data) {
    localStorage.setItem(this.prefix + table, JSON.stringify(data));
    return data;
  }

  /**
   * Get a single item by ID
   * @param {string} table - Table name
   * @param {string} id - Item ID
   * @returns {Object|null} Found item or null
   */
  get(table, id) {
    return this.getAll(table).find(item => item.id === id) || null;
  }

  /**
   * Add a new item to a table
   * @param {string} table - Table name
   * @param {Object} item - Item data
   * @returns {Object} Added item with generated fields
   */
  add(table, item) {
    const items = this.getAll(table);
    item.id = item.id || this.generateId();
    item.created_at = item.created_at || new Date().toISOString();
    item.updated_at = new Date().toISOString();
    items.unshift(item); // Add to beginning
    this.saveAll(table, items);
    this._emit('add', table, item);
    return item;
  }

  /**
   * Update an existing item
   * @param {string} table - Table name
   * @param {string} id - Item ID
   * @param {Object} updates - Fields to update
   * @returns {Object|null} Updated item or null if not found
   */
  update(table, id, updates) {
    const items = this.getAll(table);
    const index = items.findIndex(item => item.id === id);
    if (index !== -1) {
      items[index] = { ...items[index], ...updates, updated_at: new Date().toISOString() };
      this.saveAll(table, items);
      this._emit('update', table, items[index]);
      return items[index];
    }
    return null;
  }

  /**
   * Delete an item by ID
   * @param {string} table - Table name
   * @param {string} id - Item ID
   * @returns {Array} Remaining items
   */
  delete(table, id) {
    const items = this.getAll(table);
    const filtered = items.filter(item => item.id !== id);
    this.saveAll(table, filtered);
    this._emit('delete', table, id);
    return filtered;
  }

  /**
   * Query items with filters
   * @param {string} table - Table name
   * @param {Object} filters - Filter criteria
   * @returns {Array} Filtered items
   */
  query(table, filters = {}) {
    let items = this.getAll(table);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (typeof value === 'function') {
        items = items.filter(value);
      } else if (value instanceof RegExp) {
        items = items.filter(item => value.test(item[key]));
      } else {
        items = items.filter(item => item[key] === value);
      }
    });
    
    return items;
  }

  /**
   * Clear all items from a table
   * @param {string} table - Table name
   */
  clear(table) {
    localStorage.setItem(this.prefix + table, JSON.stringify([]));
    this._emit('clear', table);
  }

  /**
   * Clear all tables
   */
  clearAll() {
    this.tables.forEach(table => this.clear(table));
    console.log('[LocalDB] All data cleared');
  }

  /**
   * Get database statistics
   * @returns {Object} Database stats
   */
  getStats() {
    const stats = {
      projects: this.getAll('projects').length,
      quantum_jobs: this.getAll('quantum_jobs').length,
      pipeline_runs: this.getAll('pipeline_runs').length,
      datasets: this.getAll('datasets').length,
      storage_used: this._getStorageSize(),
      last_updated: new Date().toISOString()
    };
    
    // Calculate total records across all tables
    stats.total_records = stats.projects + stats.quantum_jobs + stats.pipeline_runs + stats.datasets;
    
    return stats;
  }

  /**
   * Export all data as JSON
   * @returns {string} JSON string of all data
   */
  exportJSON() {
    const data = {};
    this.tables.forEach(table => {
      data[table] = this.getAll(table);
    });
    data.exported_at = new Date().toISOString();
    data.version = this.version;
    return JSON.stringify(data, null, 2);
  }

  /**
   * Import data from JSON
   * @param {string} jsonString - JSON string to import
   * @returns {boolean} Success status
   */
  importJSON(jsonString) {
    try {
      const data = JSON.parse(jsonString);
      this.tables.forEach(table => {
        if (data[table]) {
          this.saveAll(table, data[table]);
        }
      });
      console.log('[LocalDB] Data imported successfully');
      return true;
    } catch (e) {
      console.error('[LocalDB] Import failed:', e);
      return false;
    }
  }

  /**
   * Calculate current storage size
   * @private
   * @returns {number} Size in bytes
   */
  _getStorageSize() {
    let total = 0;
    this.tables.forEach(table => {
      const item = localStorage.getItem(this.prefix + table);
      if (item) total += item.length * 2; // UTF-16 chars
    });
    return total;
  }

  /**
   * Emit events for reactive updates
   * @private
   * @param {string} action - Action type
   * @param {string} table - Table name
   * @param {*} data - Event data
   */
  _emit(action, table, data) {
    if (typeof window !== 'undefined' && window.CustomEvent) {
      window.dispatchEvent(new CustomEvent('localdb-change', {
        detail: { action, table, data }
      }));
    }
  }

  /**
   * Subscribe to database changes
   * @param {Function} callback - Callback function
   * @returns {Function} Unsubscribe function
   */
  onChange(callback) {
    if (typeof window !== 'undefined') {
      window.addEventListener('localdb-change', callback);
      return () => window.removeEventListener('localdb-change', callback);
    }
    return () => {};
  }
}

// Create singleton instance
const localDB = new LocalStorageDB();

// Make available globally
if (typeof window !== 'undefined') {
  window.localDB = localDB;
  window.LocalStorageDB = LocalStorageDB;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { LocalStorageDB, localDB };
}
