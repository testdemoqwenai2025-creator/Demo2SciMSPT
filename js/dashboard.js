/**
 * SciMSPT Data Visualization Dashboard v1.0
 * ============================================
 * D3.js-powered research analytics dashboard
 * Features:
 * - Research trend charts
 * - Topic distribution
 * - Citation networks
 * - Funding allocation
 * - Interactive filters
 */

class SciMSPTDashboard {
  constructor(containerId, options = {}) {
    this.containerId = containerId;
    this.container = document.getElementById(containerId);
    
    if (!this.container) {
      console.error(`Container #${containerId} not found`);
      return;
    }
    
    // Configuration
    this.config = {
      width: options.width || 800,
      height: options.height || 500,
      colors: {
        primary: '#00E5FF',
        secondary: '#a78bfa',
        success: '#10B981',
        warning: '#FBBF24',
        error: '#EF4444',
        info: '#3B82F6'
      },
      animations: {
        duration: 800,
        easing: d3.easeCubicInOut
      },
      ...options
    };
    
    // State
    this.data = null;
    this.charts = {};
    
    // Initialize
    this.init();
  }

  init() {
    console.log('📊 Initializing Dashboard...');
    
    // Setup container
    this.setupContainer();
    
    // Load sample data (replace with real data)
    this.loadSampleData();
    
    // Render initial charts
    this.renderAllCharts();
    
    console.log('✅ Dashboard initialized');
  }

  setupContainer() {
    this.container.className = 'scimspt-dashboard';
    this.container.innerHTML = `
      <div class="dashboard-header">
        <h2>Research Analytics Dashboard</h2>
        <div class="dashboard-controls">
          <select id="timeRange" class="dash-select">
            <option value="7d">Last 7 Days</option>
            <option value="30d" selected>Last 30 Days</option>
            <option value="90d">Last 3 Months</option>
            <option value="1y">Last Year</option>
          </select>
          <button class="dash-btn refresh" title="Refresh Data">
            <span class="material-icons-round">refresh</span>
          </button>
          <button class="dash-btn export" title="Export Chart">
            <span class="material-icons-round">download</span>
          </button>
        </div>
      </div>
      
      <div class="dashboard-grid">
        <!-- KPI Cards -->
        <div class="kpi-row">
          <div class="kpi-card" id="kpi-total-papers">
            <div class="kpi-icon">📄</div>
            <div class="kpi-value">--</div>
            <div class="kpi-label">Total Papers</div>
            <div class="kpi-trend positive">+12.5%</div>
          </div>
          <div class="kpi-card" id="kpi-citations">
            <div class="kpi-icon">📚</div>
            <div class="kpi-value">--</div>
            <div class="kpi-label">Total Citations</div>
            <div class="kpi-trend positive">+8.3%</div>
          </div>
          <div class="kpi-card" id="kpi-topics">
            <div class="kpi-icon">🏷️</div>
            <div class="kpi-value">--</div>
            <div class="kpi-label">Active Topics</div>
            <div class="kpi-trend neutral">0%</div>
          </div>
          <div class="kpi-card" id="kpi-impact">
            <div class="kpi-icon">⭐</div>
            <div class="kpi-value">--</div>
            <div class="kpi-label">Avg Impact Factor</div>
            <div class="kpi-trend positive">+2.1%</div>
          </div>
        </div>
        
        <!-- Main Charts Row -->
        <div class="chart-container large" id="trendChart">
          <div class="chart-header">
            <h3>Publication Trends</h3>
            <div class="chart-legend"></div>
          </div>
          <div class="chart-body"></div>
        </div>
        
        <div class="chart-container" id="topicChart">
          <div class="chart-header">
            <h3>Topic Distribution</h3>
          </div>
          <div class="chart-body"></div>
        </div>
        
        <div class="chart-container" id="sourceChart">
          <div class="chart-header">
            <h3>Paper Sources</h3>
          </div>
          <div class="chart-body"></div>
        </div>
        
        <!-- Bottom Row -->
        <div class="chart-container wide" id="heatmapChart">
          <div class="chart-header">
            <h3>Research Activity Heatmap</h3>
          </div>
          <div class="chart-body"></div>
        </div>
      </div>
      
      <style>${this.getStyles()}</style>
    `;
    
    // Inject D3.js if not present
    this.injectD3();
  }

  injectD3() {
    if (typeof d3 !== 'undefined') return;
    
    const script = document.createElement('script');
    script.src = 'https://d3js.org/d3.v7.min.js';
    script.onload = () => this.renderAllCharts();
    document.head.appendChild(script);
  }

  getStyles() {
    return `
      .scimspt-dashboard {
        font-family: var(--font-body, 'Inter', sans-serif);
        color: var(--text-primary, #e8f4fc);
        opacity: 1 !important;
        visibility: visible !important;
      }
      
      .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.1));
      }
      
      .dashboard-header h2 {
        margin: 0;
        font-family: var(--font-heading, 'Playfair Display', serif);
        font-size: 24px;
      }
      
      .dashboard-controls {
        display: flex;
        gap: 12px;
        align-items: center;
      }
      
      .dash-select {
        padding: 8px 12px;
        background: var(--bg-secondary, #111d32);
        border: 1px solid var(--border-default, rgba(148, 163, 184, 0.2));
        border-radius: var(--radius-md, 8px);
        color: var(--text-primary, #e8f4fc);
        font-size: 14px;
        cursor: pointer;
      }
      
      .dash-btn {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: transparent;
        border: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.15));
        border-radius: var(--radius-md, 8px);
        color: var(--text-muted, #64748b);
        cursor: pointer;
        transition: all 0.2s ease;
      }
      
      .dash-btn:hover {
        background: var(--accent-primary-muted, rgba(0, 229, 255, 0.15));
        color: var(--accent-primary, #00E5FF);
        border-color: var(--accent-primary, #00E5FF);
      }
      
      /* KPI Cards */
      .kpi-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
      }
      
      .kpi-card {
        background: var(--bg-glass, rgba(10, 22, 40, 0.85));
        backdrop-filter: blur(8px);
        border: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.1));
        border-radius: var(--radius-xl, 16px);
        padding: 20px;
        text-align: center;
        opacity: 1 !important;
        visibility: visible !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      
      .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg, 0 10px 25px rgba(0, 0, 0, 0.4));
      }
      
      .kpi-icon { font-size: 32px; margin-bottom: 8px; }
      .kpi-value { font-size: 28px; font-weight: 700; font-family: var(--font-mono, monospace); }
      .kpi-label { font-size: 13px; color: var(--text-secondary, #94a3b8); margin-top: 4px; }
      .kpi-trend { font-size: 12px; font-weight: 600; margin-top: 8px; }
      .kpi-trend.positive { color: var(--text-success, #10B981); }
      .kpi-trend.negative { color: var(--text-error, #EF4444); }
      .kpi-trend.neutral { color: var(--text-muted, #64748b); }
      
      /* Chart Grid */
      .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
      }
      
      .chart-container {
        background: var(--bg-glass, rgba(10, 22, 40, 0.85));
        backdrop-filter: blur(8px);
        border: 1px solid var(--border-subtle, rgba(0, 229, 255, 0.1));
        border-radius: var(--radius-xl, 16px);
        padding: 20px;
        opacity: 1 !important;
        visibility: visible !important;
      }
      
      .chart-container.large {
        grid-column: span 2;
      }
      
      .chart-container.wide {
        grid-column: span 2;
      }
      
      .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
      }
      
      .chart-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }
      
      .chart-body {
        position: relative;
        min-height: 300px;
      }
      
      /* D3 Chart Styles */
      .axis path,
      .axis line {
        stroke: var(--text-muted, #64748b);
        stroke-width: 1;
      }
      
      .axis text {
        fill: var(--text-secondary, #94a3b8);
        font-size: 12px;
      }
      
      .grid-line {
        stroke: var(--border-subtle, rgba(0, 229, 255, 0.08));
        stroke-dasharray: 4,4;
      }
      
      .tooltip {
        position: absolute;
        background: var(--bg-glass-heavy, rgba(10, 20, 35, 0.98));
        backdrop-filter: blur(16px);
        border: 1px solid var(--accent-primary, #00E5FF);
        border-radius: var(--radius-md, 8px);
        padding: 12px;
        font-size: 13px;
        pointer-events: none;
        z-index: 100;
        box-shadow: var(--shadow-lg, 0 10px 25px rgba(0, 0, 0, 0.4));
      }
      
      @media (max-width: 1024px) {
        .dashboard-grid { grid-template-columns: 1fr; }
        .chart-container.large, .chart-container.wide { grid-column: span 1; }
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
      }
      
      @media (max-width: 640px) {
        .kpi-row { grid-template-columns: 1fr; }
        .dashboard-header { flex-direction: column; gap: 16px; align-items: flex-start; }
      }
    `;
  }

  loadSampleData() {
    // Sample data - replace with real API calls
    this.data = {
      trends: [
        { date: '2024-01', papers: 120, citations: 450 },
        { date: '2024-02', papers: 145, citations: 520 },
        { date: '2024-03', papers: 168, citations: 610 },
        { date: '2024-04', papers: 190, citations: 720 },
        { date: '2024-05', papers: 215, citations: 850 },
        { date: '2024-06', papers: 240, citations: 980 },
        { date: '2024-07', papers: 265, citations: 1120 },
        { date: '2024-08', papers: 290, citations: 1280 }
      ],
      topics: [
        { name: 'Quantum Computing', count: 245, percentage: 28 },
        { name: 'Machine Learning', count: 198, percentage: 23 },
        { name: 'Materials Science', count: 156, percentage: 18 },
        { name: 'Biotechnology', count: 134, percentage: 15 },
        { name: 'Neural Networks', count: 87, percentage: 10 },
        { name: 'Other', count: 56, percentage: 6 }
      ],
      sources: [
        { name: 'ArXiv', count: 520, color: '#B31B1B' },
        { name: 'PubMed', count: 280, color: '#006699' },
        { name: 'IEEE', count: 145, color: '#006699' },
        { name: 'Nature', count: 89, color: '#FF0000' },
        { name: 'Science', count: 67, color: '#CC0000' }
      ],
      heatmap: this.generateHeatmapData(),
      kpis: {
        totalPapers: 1101,
        totalCitations: 5530,
        activeTopics: 42,
        avgImpactFactor: 8.7
      }
    };
  }

  generateHeatmapData() {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const hours = Array.from({ length: 24 }, (_, i) => i);
    
    return days.map(day => ({
      day,
      values: hours.map(hour => ({
        hour,
        value: Math.floor(Math.random() * 100)
      }))
    }));
  }

  renderAllCharts() {
    if (typeof d3 === 'undefined') return;
    
    this.updateKPIs();
    this.renderTrendChart();
    this.renderTopicChart();
    this.renderSourceChart();
    this.renderHeatmapChart();
  }

  updateKPIs() {
    if (!this.data?.kpis) return;
    
    const kpis = this.data.kpis;
    
    this.animateValue('#kpi-total-papers .kpi-value', kpis.totalPapers);
    this.animateValue('#kpi-citations .kpi-value', kpis.totalCitations);
    this.animateValue('#kpi-topics .kpi-value', kpis.activeTopics);
    this.animateValue('#kpi-impact .kpi-value', kpis.avgImpactFactor, 1);
  }

  animateValue(selector, target, decimals = 0) {
    const el = this.container.querySelector(selector);
    if (!el) return;
    
    const start = 0;
    const duration = 1000;
    const startTime = performance.now();
    
    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // Ease out cubic
      
      const current = start + (target - start) * eased;
      el.textContent = decimals > 0 ? current.toFixed(decimals) : Math.floor(current).toLocaleString();
      
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    };
    
    requestAnimationFrame(update);
  }

  renderTrendChart() {
    const container = this.container.querySelector('#trendChart .chart-body');
    if (!container || !this.data?.trends) return;
    
    // Clear previous
    container.innerHTML = '';
    
    const margin = { top: 20, right: 30, bottom: 40, left: 50 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;
    
    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Scales
    const x = d3.scaleBand()
      .domain(this.data.trends.map(d => d.date))
      .range([0, width])
      .padding(0.3);
    
    const y = d3.scaleLinear()
      .domain([0, d3.max(this.data.trends, d => d.papers)])
      .nice()
      .range([height, 0]);
    
    // Grid lines
    svg.append('g')
      .attr('class', 'grid')
      .call(d3.axisLeft(y).tickSize(-width).tickFormat(''))
      .selectAll('line')
      .attr('class', 'grid-line');
    
    // X Axis
    svg.append('g')
      .attr('class', 'axis')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'rotate(-45)')
      .style('text-anchor', 'end');
    
    // Y Axis
    svg.append('g')
      .attr('class', 'axis')
      .call(d3.axisLeft(y));
    
    // Bars
    svg.selectAll('.bar')
      .data(this.data.trends)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.date))
      .attr('width', x.bandwidth())
      .attr('y', height)
      .attr('height', 0)
      .attr('fill', this.config.colors.primary)
      .attr('rx', 4)
      .on('mouseover', (event, d) => this.showTooltip(event, `${d.date}: ${d.papers} papers`))
      .on('mouseout', () => this.hideTooltip())
      .transition()
      .duration(this.config.animations.duration)
      .delay((d, i) => i * 50)
      .attr('y', d => y(d.papers))
      .attr('height', d => height - y(d.papers));
    
    // Line overlay for citations
    const line = d3.line()
      .x(d => x(d.date) + x.bandwidth() / 2)
      .y(d => y(d.citations / 5)); // Scale down citations
    
    const path = svg.append('path')
      .datum(this.data.trends)
      .attr('fill', 'none')
      .attr('stroke', this.config.colors.secondary)
      .attr('stroke-width', 2)
      .attr('d', line);
    
    const totalLength = path.node().getTotalLength();
    path.attr('stroke-dasharray', totalLength)
      .attr('stroke-dashoffset', totalLength)
      .transition()
      .duration(2000)
      .ease(d3.easeLinear)
      .attr('stroke-dashoffset', 0);
  }

  renderTopicChart() {
    const container = this.container.querySelector('#topicChart .chart-body');
    if (!container || !this.data?.topics) return;
    
    container.innerHTML = '';
    
    const size = Math.min(container.clientWidth, 300);
    const radius = size / 2;
    
    const svg = d3.select(container)
      .append('svg')
      .attr('width', size)
      .attr('height', size)
      .append('g')
      .attr('transform', `translate(${radius},${radius})`);
    
    const pie = d3.pie()
      .value(d => d.count)
      .sort(null)
      .padAngle(0.02);
    
    const arc = d3.arc()
      .innerRadius(radius * 0.5)
      .outerRadius(radius * 0.85);
    
    const arcHover = d3.arc()
      .innerRadius(radius * 0.5)
      .outerRadius(radius * 0.95);
    
    const color = d3.scaleOrdinal()
      .range([
        this.config.colors.primary,
        this.config.colors.secondary,
        this.config.colors.success,
        this.config.colors.warning,
        this.config.colors.info,
        this.config.colors.error
      ]);
    
    const arcs = svg.selectAll('.arc')
      .data(pie(this.data.topics))
      .enter()
      .append('g')
      .attr('class', 'arc');
    
    arcs.append('path')
      .attr('fill', d => color(d.data.name))
      .attr('d', arc)
      .attr('opacity', 0.8)
      .on('mouseover', function(event, d) {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('d', arcHover)
          .attr('opacity', 1);
        this.showTooltip(event, `${d.data.name}: ${d.data.count} (${d.data.percentage}%)`);
      }.bind(this))
      .on('mouseout', function() {
        d3.select(this)
          .transition()
          .duration(200)
          .attr('d', arc)
          .attr('opacity', 0.8);
        this.hideTooltip();
      }.bind(this))
      .each(function(d) {
        this._current = d;
      })
      .transition()
      .duration(this.config.animations.duration)
      .attrTween('d', function(d) {
        const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
        return function(t) {
          return arc(interpolate(t));
        };
      });
    
    // Center label
    arcs.append('text')
      .attr('transform', d => `translate(${arc.centroid(d)})`)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('fill', 'white')
      .style('font-size', '11px')
      .style('font-weight', '600')
      .text(d => d.data.percentage > 8 ? `${d.data.percentage}%` : '');
  }

  renderSourceChart() {
    const container = this.container.querySelector('#sourceChart .chart-body');
    if (!container || !this.data?.sources) return;
    
    container.innerHTML = '';
    
    const margin = { top: 20, right: 30, bottom: 60, left: 80 };
    const width = container.clientWidth - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;
    
    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    const x = d3.scaleLinear()
      .domain([0, d3.max(this.data.sources, d => d.count)])
      .range([0, width]);
    
    const y = d3.scaleBand()
      .domain(this.data.sources.map(d => d.name))
      .range([0, height])
      .padding(0.2);
    
    // Bars
    svg.selectAll('.bar')
      .data(this.data.sources)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('y', d => y(d.name))
      .attr('height', y.bandwidth())
      .attr('x', 0)
      .attr('width', 0)
      .attr('fill', d => d.color)
      .attr('rx', 4)
      .on('mouseover', (event, d) => this.showTooltip(event, `${d.name}: ${d.count} papers`))
      .on('mouseout', () => this.hideTooltip())
      .transition()
      .duration(this.config.animations.duration)
      .delay((d, i) => i * 100)
      .attr('width', d => x(d.count));
    
    // Labels
    svg.selectAll('.label')
      .data(this.data.sources)
      .enter()
      .append('text')
      .attr('class', 'label')
      .attr('y', d => y(d.name) + y.bandwidth() / 2)
      .attr('x', d => x(d.count) + 5)
      .attr('dy', '0.35em')
      .style('fill', 'var(--text-secondary, #94a3b8)')
      .style('font-size', '12px')
      .text(d => d.count)
      .attr('opacity', 0)
      .transition()
      .delay(this.config.animations.duration)
      .attr('opacity', 1);
    
    // Y axis
    svg.append('g')
      .call(d3.axisLeft(y));
  }

  renderHeatmapChart() {
    const container = this.container.querySelector('#heatmapChart .chart-body');
    if (!container || !this.data?.heatmap) return;
    
    container.innerHTML = '';
    
    const cellSize = 40;
    const width = 24 * cellSize;
    const height = 7 * cellSize;
    const margin = { top: 40, right: 20, bottom: 40, left: 60 };
    
    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    const colorScale = d3.scaleSequential()
      .interpolator(d3.interpolatePlasma)
      .domain([0, 100]);
    
    // Day labels
    svg.selectAll('.day-label')
      .data(this.data.heatmap)
      .enter()
      .append('text')
      .attr('class', 'day-label')
      .attr('x', -10)
      .attr('y', (_, i) => i * cellSize + cellSize / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'middle')
      .style('fill', 'var(--text-secondary, #94a3b8)')
      .style('font-size', '12px')
      .text(d => d.day);
    
    // Hour labels
    svg.selectAll('.hour-label')
      .data(Array.from({ length: 24 }, (_, i) => i))
      .enter()
      .append('text')
      .attr('class', 'hour-label')
      .attr('x', d => d * cellSize + cellSize / 2)
      .attr('y', -10)
      .attr('text-anchor', 'middle')
      .style('fill', 'var(--text-muted, #64748b)')
      .style('font-size', '10px')
      .text(d => `${d}:00`);
    
    // Cells
    this.data.heatmap.forEach((dayData, dayIndex) => {
      dayData.values.forEach((cell, hourIndex) => {
        svg.append('rect')
          .attr('x', hourIndex * cellSize)
          .attr('y', dayIndex * cellSize)
          .attr('width', cellSize - 2)
          .attr('height', cellSize - 2)
          .attr('rx', 4)
          .attr('fill', colorScale(cell.value))
          .attr('opacity', 0)
          .on('mouseover', (event) => {
            this.showTooltip(event, 
              `${dayData.day} at ${hourIndex}:00<br>Activity: ${cell.value}%`
            );
          })
          .on('mouseout', () => this.hideTooltip())
          .transition()
          .duration(500)
          .delay(dayIndex * 50 + hourIndex * 10)
          .attr('opacity', 0.85);
      });
    });
  }

  showTooltip(event, html) {
    let tooltip = document.querySelector('.tooltip');
    
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      document.body.appendChild(tooltip);
    }
    
    tooltip.style.display = 'block';
    tooltip.innerHTML = html;
    tooltip.style.left = event.pageX + 10 + 'px';
    tooltip.style.top = event.pageY - 10 + 'px';
  }

  hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
      tooltip.style.display = 'none';
    }
  }

  // ============================================
  // PUBLIC API
  // ============================================

  setData(data) {
    this.data = data;
    this.renderAllCharts();
  }

  refresh() {
    // Fetch new data and re-render
    this.loadSampleData(); // Replace with actual fetch
    this.renderAllCharts();
  }

  exportChart(chartId) {
    const chartContainer = this.container.querySelector(`#${chartId}`);
    if (!chartContainer) return;
    
    const svg = chartContainer.querySelector('svg');
    if (!svg) return;
    
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svg);
    const blob = new Blob([svgString], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `${chartId}-chart.svg`;
    a.click();
    
    URL.revokeObjectURL(url);
  }

  destroy() {
    if (this.container) {
      this.container.innerHTML = '';
    }
  }
}

// Export
window.SciMSPTDashboard = SciMSPTDashboard;

if (typeof module !== 'undefined' && module.exports) {
  module.exports = SciMSPTDashboard;
}
