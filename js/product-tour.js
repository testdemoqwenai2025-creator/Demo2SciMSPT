/**
 * ============================================
 * SCIMSPT PRODUCT TOUR SYSTEM
 * Interactive Guided Tour for VC Investor Demos
 * Version: 1.0.0
 * ============================================
 * 
 * Features:
 * - Auto-playing guided tour with configurable timing
 * - Spotlight effects on UI elements
 * - Glass-morphism tooltip design
 * - Keyboard navigation support (Arrow keys, Escape, Space)
 * - Touch-friendly for mobile devices
 * - WCAG accessible with ARIA labels and focus trap
 * - localStorage integration for tour completion tracking
 * - URL parameter trigger support
 * 
 * Usage:
 *   SciMSPTTour.start('quantum')     // Start quantum module tour
 *   SciMSPTTour.start('pipeline')    // Start pipeline module tour  
 *   SciMSPTTour.start('security')    // Start security module tour
 *   
 * URL Triggers:
 *   ?tour=quantum   ?tour=pipeline   ?tour=security
 */

(function(global) {
  'use strict';

  // ============================================
  // TOUR CONFIGURATIONS
  // ============================================

  const TOUR_CONFIGS = {
    quantum: {
      id: 'quantum',
      name: 'Quantum Workspace Tour',
      description: 'Explore our quantum chemistry simulation platform',
      steps: [
        {
          id: 'q-step-1',
          target: '.hero-section',
          title: 'Welcome to Quantum Workspace',
          description: 'Your gateway to quantum chemistry simulation. Access IBM Qiskit, Google Cirq, Microsoft Azure Quantum, and more from a unified interface.',
          position: 'bottom',
          action: null,
          highlightPadding: 20
        },
        {
          id: 'q-step-2',
          target: '.circuit-builder',
          title: 'Circuit Builder',
          description: 'Design quantum circuits with intuitive drag-and-drop gates. Build complex algorithms visually without writing code.',
          position: 'right',
          action: null,
          highlightPadding: 12,
          scrollOffset: 100
        },
        {
          id: 'q-step-3',
          target: '.backend-selector',
          title: 'Backend Selector',
          description: 'Choose from simulators or real quantum hardware. Each backend shows queue status, qubit count, and availability in real-time.',
          position: 'left',
          action: null,
          highlightPadding: 12,
          scrollOffset: 150
        },
        {
          id: 'q-step-4',
          target: '.code-editor-container, .editor-wrapper, .ibm-code-panel, [class*="code-editor"], [class*="CodeEditor"]',
          title: 'Qiskit Code Editor',
          description: 'Full-featured IDE with syntax highlighting, auto-completion, and integrated Qiskit documentation. Write, test, and debug quantum code.',
          position: 'left',
          action: null,
          highlightPadding: 12,
          fallbackPosition: { x: 50, y: 40 }
        },
        {
          id: 'q-step-5',
          target: '.run-btn, .execute-btn, button[class*="run"], .job-execution',
          title: 'Job Execution',
          description: 'Submit jobs to quantum backends with one click. Monitor progress, view queue position, and receive notifications on completion.',
          position: 'top',
          action: null,
          highlightPadding: 8,
          scrollOffset: 200
        },
        {
          id: 'q-step-6',
          target: '.results-panel, .output-panel, [class*="result"], [class*="visualization"]',
          title: 'Results Visualization',
          description: 'Interactive charts, statevector visualizations, and measurement histograms. Export results or continue analysis in Pipeline Studio.',
          position: 'left',
          action: null,
          highlightPadding: 16,
          scrollOffset: 250
        }
      ],
      defaultTiming: 5000
    },

    pipeline: {
      id: 'pipeline',
      name: 'Pipeline Studio Tour',
      description: 'Discover synthetic data generation and transformation',
      steps: [
        {
          id: 'p-step-1',
          target: '.hero-section',
          title: 'Pipeline Studio Overview',
          description: 'Generate, transform, and analyze research datasets on-demand. Our visual pipeline builder makes data science accessible.',
          position: 'bottom',
          action: null,
          highlightPadding: 20
        },
        {
          id: 'p-step-2',
          target: '.stage-header:first-child, .pipeline-stage[data-stage="source"], [class*="source"]',
          title: 'Data Source Stage',
          description: 'Configure data sources from databases, APIs, files, or generate synthetic data. Support for CSV, JSON, SQL, and custom formats.',
          position: 'right',
          action: null,
          highlightPadding: 16,
          scrollOffset: 100
        },
        {
          id: 'p-step-3',
          target: '.stage-header:nth-child(2), .pipeline-stage[data-stage="transform"], [class*="transform"]',
          title: 'Transform Stage',
          description: 'Apply transformations: normalize, aggregate, join, filter, or use AI-powered feature engineering. Visual flow shows data changes.',
          position: 'right',
          action: null,
          highlightPadding: 16,
          scrollOffset: 150
        },
        {
          id: 'p-step-4',
          target: '.stage-header:nth-child(3), .pipeline-stage[data-stage="analyze"], [class*="analyze"]',
          title: 'Analyze Stage',
          description: 'Run statistical analysis, ML models, or custom scripts. Built-in visualization tools for immediate insights.',
          position: 'left',
          action: null,
          highlightPadding: 16,
          scrollOffset: 200
        },
        {
          id: 'p-step-5',
          target: '.results-grid, .export-section, [class*="export"], button[class*="export"]',
          title: 'Output & Export',
          description: 'Export results in multiple formats, schedule recurring pipelines, or feed data directly into Quantum Workspace for advanced analysis.',
          position: 'top',
          action: null,
          highlightPadding: 16,
          scrollOffset: 250
        }
      ],
      defaultTiming: 5000
    },

    security: {
      id: 'security',
      name: 'Security Dashboard Tour',
      description: 'Explore enterprise-grade security features',
      steps: [
        {
          id: 's-step-1',
          target: '.section-header, h2.section-title',
          title: 'Security Dashboard',
          description: 'Multi-layer protection architecture overview. Monitor security status, compliance metrics, and threat intelligence at a glance.',
          position: 'bottom',
          action: null,
          highlightPadding: 24
        },
        {
          id: 's-step-2',
          target: '.security-card.accent-cyan, .security-card:first-child',
          title: 'Encryption Tools',
          description: 'End-to-end encryption for data at rest and in transit. AES-256, RSA, and quantum-resistant algorithms available.',
          position: 'left',
          action: null,
          highlightPadding: 16,
          scrollOffset: 80
        },
        {
          id: 's-step-3',
          target: '[class*="nucleotide"], [class*="dna"], [class*="sequencer"], .security-card.accent-purple',
          title: 'Nucleotide Sequencer',
          description: 'DNA-based encryption tool for ultra-secure data encoding. Convert sensitive information to nucleotide sequences.',
          position: 'right',
          action: null,
          highlightPadding: 16,
          scrollOffset: 150
        },
        {
          id: 's-step-4',
          target: '.security-card.accent-green, [class*="access"], [class*="permission"], [class*="oauth"]',
          title: 'Access Control',
          description: 'OAuth 2.0 / OIDC authentication with role-based access control. Fine-grained permissions for teams and projects.',
          position: 'left',
          action: null,
          highlightPadding: 16,
          scrollOffset: 220
        },
        {
          id: 's-step-5',
          target: '[class*="audit"], [class*="log"], [class*="activity"], .security-card:last-child',
          title: 'Audit Log',
          description: 'Complete activity trail with timestamps, user actions, and system events. GDPR-compliant data retention policies.',
          position: 'top',
          action: null,
          highlightPadding: 16,
          scrollOffset: 300
        }
      ],
      defaultTiming: 5000
    }
  };

  // ============================================
  // STORAGE KEYS
  // ============================================

  const STORAGE_KEYS = {
    completed: 'scimspt_tour_completed',
    dismissed: 'scimspt_tour_dismissed',
    lastTour: 'scimspt_tour_last'
  };

  // ============================================
  // PRODUCT TOUR CLASS
  // ============================================

  class ProductTour {
    constructor() {
      this.currentStep = 0;
      this.steps = [];
      this.config = null;
      this.isActive = false;
      this.isPaused = false;
      this.autoAdvanceTimer = null;
      this.autoAdvanceTimeRemaining = 0;
      this.autoAdvanceStartTime = 0;
      this.animationFrameId = null;
      this.elements = {
        overlay: null,
        backdrop: null,
        spotlight: null,
        tooltip: null,
        progressBar: null,
        floatingBtn: null,
        completion: null
      };
      this.focusableElements = [];
      this.previouslyFocusedElement = null;
      this.observers = [];
      this.boundHandlers = {};
      
      this._init();
    }

    // ==========================================
    // INITIALIZATION
    // ==========================================

    _init() {
      this._bindEventHandlers();
      this._createDOMElements();
      this._createFloatingButton();
      this._checkURLTrigger();
      this._showFloatingButtonWithDelay();
    }

    _bindEventHandlers() {
      this.boundHandlers = {
        onKeyDown: this._handleKeyDown.bind(this),
        onResize: this._handleResize.bind(this),
        onTouchStart: this._handleTouch.bind(this),
        onClick: this._handleDocumentClick.bind(this)
      };
    }

    _createDOMElements() {
      // Main overlay container
      this.elements.overlay = this._createElement('div', 'tour-overlay');
      this.elements.overlay.setAttribute('role', 'dialog');
      this.elements.overlay.setAttribute('aria-modal', 'true');
      this.elements.overlay.setAttribute('aria-label', 'Product tour');

      // Backdrop (darkens everything)
      this.elements.backdrop = this._createElement('div', 'tour-overlay-backdrop');
      this.elements.overlay.appendChild(this.elements.backdrop);

      // Spotlight element
      this.elements.spotlight = this._createElement('div', 'tour-spotlight');
      this.elements.overlay.appendChild(this.elements.spotlight);

      // Tooltip container
      this.elements.tooltip = this._createTooltip();
      this.elements.overlay.appendChild(this.elements.tooltip);

      // Progress bar
      this.elements.progressBar = this._createProgressBar();
      document.body.appendChild(this.elements.progressBar);

      // Completion screen
      this.elements.completion = this._createCompletionScreen();
      document.body.appendChild(this.elements.completion);

      // Add overlay to DOM
      document.body.appendChild(this.elements.overlay);
    }

    _createTooltip() {
      const tooltip = this._createElement('div', 'tour-tooltip');
      tooltip.innerHTML = `
        <div class="tour-tooltip-arrow"></div>
        <div class="tour-timer-ring">
          <svg viewBox="0 0 32 32">
            <circle class="timer-bg" cx="16" cy="16" r="14"></circle>
            <circle class="timer-progress" cx="16" cy="16" r="14" 
                    stroke-dasharray="88" stroke-dashoffset="0"></circle>
          </svg>
        </div>
        <div class="tour-step-badge">STEP</div>
        <h3 class="tour-tooltip-title"></h3>
        <p class="tour-tooltip-description"></p>
        <div class="tour-progress-dots"></div>
        <div class="tour-tooltip-actions">
          <div class="tour-btn-group">
            <button class="tour-btn tour-btn-secondary" data-action="prev" aria-label="Previous step">
              ← Back
            </button>
            <button class="tour-btn tour-btn-pause" data-action="pause" aria-label="Pause tour">
              ⏸ Pause
            </button>
          </div>
          <div class="tour-btn-group">
            <span class="tour-step-counter"></span>
            <button class="tour-btn tour-btn-primary" data-action="next" aria-label="Next step">
              Next →
            </button>
            <button class="tour-btn tour-btn-skip" data-action="skip" aria-label="Skip tour">
              ✕ Skip
            </button>
          </div>
        </div>
        <div class="tour-keyboard-hints">
          <span class="tour-key-hint"><span class="tour-key">→</span> Next</span>
          <span class="tour-key-hint"><span class="tour-key">←</span> Back</span>
          <span class="tour-key-hint"><span class="tour-key">Space</span> Pause</span>
          <span class="tour-key-hint"><span class="tour-key">Esc</span> Close</span>
        </div>
      `;

      // Bind button actions
      tooltip.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          this._handleAction(btn.dataset.action);
        });
      });

      return tooltip;
    }

    _createProgressBar() {
      const bar = this._createElement('div', 'tour-progress-bar-container');
      bar.innerHTML = '<div class="tour-progress-bar-fill"></div>';
      return bar;
    }

    _createCompletionScreen() {
      const completion = this._createElement('div', 'tour-completion');
      completion.innerHTML = `
        <div class="tour-completion-card">
          <div class="tour-completion-icon">✓</div>
          <h2 class="tour-completion-title">Tour Complete!</h2>
          <p class="tour-completion-text">
            You've explored all the key features. Ready to dive deeper?
          </p>
          <div class="tour-completion-actions">
            <button class="tour-btn tour-btn-primary" data-action="restart">
              🔄 Take Tour Again
            </button>
            <button class="tour-btn tour-btn-secondary" data-action="close">
              Start Exploring
            </button>
          </div>
        </div>
      `;

      completion.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          this._handleAction(btn.dataset.action);
        });
      });

      return completion;
    }

    _createFloatingButton() {
      this.elements.floatingBtn = this._createElement('button', 'tour-floating-btn');
      this.elements.floatingBtn.setAttribute('aria-label', 'Take guided tour');
      this.elements.floatingBtn.setAttribute('type', 'button');
      this.elements.floatingBtn.innerHTML = `
        <span class="tour-floating-btn-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </span>
        <span>Take Tour</span>
      `;
      this.elements.floatingBtn.addEventListener('click', () => {
        this.start(this._detectCurrentTourType());
      });
      document.body.appendChild(this.elements.floatingBtn);
    }

    _showFloatingButtonWithDelay() {
      setTimeout(() => {
        if (!this.isActive) {
          this.elements.floatingBtn.classList.add('visible');
        }
      }, 2000);
    }

    // ==========================================
    // PUBLIC API - START/STOP
    // ==========================================

    /**
     * Start a guided tour
     * @param {string} tourType - 'quantum' | 'pipeline' | 'security'
     * @param {object} options - Optional configuration overrides
     */
    start(tourType, options = {}) {
      if (this.isActive) return;

      const config = TOUR_CONFIGS[tourType];
      if (!config) {
        console.error(`[ProductTour] Unknown tour type: ${tourType}`);
        console.error(`Available tours: ${Object.keys(TOUR_CONFIGS).join(', ')}`);
        return;
      }

      this.config = { ...config, ...options };
      this.steps = this.config.steps;
      this.currentStep = 0;
      this.isPaused = false;

      // Store reference to currently focused element
      this.previouslyFocusedElement = document.activeElement;

      // Hide floating button
      this.elements.floatingBtn.classList.remove('visible');

      // Activate overlay
      this.isActive = true;
      this.elements.overlay.classList.add('active');
      this.elements.progressBar.classList.add('active');
      document.body.classList.add('tour-focus-trap-active');

      // Attach event listeners
      this._attachEventListeners();

      // Show first step
      this._showStep(0);

      // Emit start event
      this._emitEvent('start', { tourType, stepsCount: this.steps.length });
    }

    /**
     * Stop the current tour
     */
    stop() {
      if (!this.isActive) return;

      this._clearAutoAdvance();
      this._cancelAnimationFrame();
      this._detachEventListeners();
      this._cleanupObservers();

      // Reset state
      this.isActive = false;
      this.isPaused = false;
      this.currentStep = 0;

      // Hide UI elements
      this.elements.overlay.classList.remove('active');
      this.elements.progressBar.classList.remove('active');
      this.elements.tooltip.classList.remove('visible');
      this.elements.completion.classList.remove('active');
      document.body.classList.remove('tour-focus-trap-active');

      // Show floating button again
      setTimeout(() => {
        if (!this.isActive) {
          this.elements.floatingBtn.classList.add('visible');
        }
      }, 500);

      // Restore focus
      if (this.previouslyFocusedElement && typeof this.previouslyFocusedElement.focus === 'function') {
        this.previouslyFocusedElement.focus();
      }

      // Emit event
      this._emitEvent('stop');
    }

    /**
     * Navigate to specific step
     * @param {number} stepIndex - Step index (0-based)
     */
    goToStep(stepIndex) {
      if (!this.isActive || stepIndex < 0 || stepIndex >= this.steps.length) return;
      this._clearAutoAdvance();
      this._showStep(stepIndex);
    }

    /**
     * Pause/resume auto-advance
     */
    togglePause() {
      if (!this.isActive) return;

      this.isPaused = !this.isPaused;
      const pauseBtn = this.elements.tooltip.querySelector('[data-action="pause"]');
      
      if (this.isPaused) {
        this._pauseAutoAdvance();
        pauseBtn.textContent = '▶ Resume';
        pauseBtn.classList.add('paused');
        this._emitEvent('pause');
      } else {
        this._resumeAutoAdvance();
        pauseBtn.textContent = '⏸ Pause';
        pauseBtn.classList.remove('paused');
        this._emitEvent('resume');
      }
    }

    // ==========================================
    // STEP DISPLAY LOGIC
    // ==========================================

    async _showStep(stepIndex) {
      this.currentStep = stepIndex;
      const step = this.steps[stepIndex];
      if (!step) return;

      // Find target element
      const targetElement = await this._findTargetElement(step);
      
      // Position spotlight
      if (targetElement) {
        this._positionSpotlight(targetElement, step.highlightPadding || 12);
        
        // Scroll element into view if needed
        if (step.scrollOffset) {
          this._scrollToElement(targetElement, step.scrollOffset);
        }
      } else {
        // Use fallback position if element not found
        if (step.fallbackPosition) {
          this._positionSpotlightAtCoordinates(
            step.fallbackPosition.x,
            step.fallbackPosition.y,
            200,
            150
          );
        } else {
          // Center of viewport as last resort
          this._positionSpotlightAtCoordinates(50, 40, 300, 200);
        }
      }

      // Update tooltip content
      this._updateTooltipContent(step, stepIndex);

      // Position tooltip
      this._positionTooltip(step.position || 'bottom', targetElement);

      // Update progress bar
      this._updateProgressBar();

      // Show tooltip with animation
      requestAnimationFrame(() => {
        this.elements.tooltip.classList.add('visible');
        this.elements.spotlight.classList.add('pulse');
      });

      // Start auto-advance timer
      this._startAutoAdvance(this.config.defaultTiming || 5000);

      // Emit event
      this._emitEvent('stepChange', { step: stepIndex, total: this.steps.length });
    }

    _updateTooltipContent(step, index) {
      const badge = this.elements.tooltip.querySelector('.tour-step-badge');
      const title = this.elements.tooltip.querySelector('.tour-tooltip-title');
      const desc = this.elements.tooltip.querySelector('.tour-tooltip-description');
      const counter = this.elements.tooltip.querySelector('.tour-step-counter');
      const dotsContainer = this.elements.tooltip.querySelector('.tour-progress-dots');
      const nextBtn = this.elements.tooltip.querySelector('[data-action="next"]');
      const prevBtn = this.elements.tooltip.querySelector('[data-action="prev"]');

      badge.textContent = `STEP ${index + 1}`;
      title.textContent = step.title;
      desc.textContent = step.description;
      counter.textContent = `${index + 1} / ${this.steps.length}`;

      // Update buttons visibility/state
      prevBtn.style.visibility = index === 0 ? 'hidden' : 'visible';
      nextBtn.textContent = index === this.steps.length - 1 ? 'Finish ✓' : 'Next →';

      // Generate progress dots
      dotsContainer.innerHTML = '';
      this.steps.forEach((_, i) => {
        const dot = this._createElement('div', 'tour-dot');
        dot.setAttribute('role', 'button');
        dot.setAttribute('aria-label', `Go to step ${i + 1}`);
        dot.setAttribute('tabindex', '0');
        
        if (i === index) dot.classList.add('active');
        else if (i < index) dot.classList.add('completed');
        
        dot.addEventListener('click', () => this.goToStep(i));
        dotsContainer.appendChild(dot);
      });

      // Announce to screen readers
      this._announceToScreenReader(`Step ${index + 1}: ${step.title}`);
    }

    // ==========================================
    // SPOTLIGHT POSITIONING
    // ==========================================

    _positionSpotlight(element, padding = 12) {
      const rect = element.getBoundingClientRect();
      
      this.elements.spotlight.style.left = `${rect.left - padding}px`;
      this.elements.spotlight.style.top = `${rect.top - padding}px`;
      this.elements.spotlight.style.width = `${rect.width + padding * 2}px`;
      this.elements.spotlight.style.height = `${rect.height + padding * 2}px`;
    }

    _positionSpotlightAtCoordinates(percentX, percentY, width, height) {
      const x = (window.innerWidth * percentX) / 100 - width / 2;
      const y = (window.innerHeight * percentY) / 100 - height / 2;
      
      this.elements.spotlight.style.left = `${x}px`;
      this.elements.spotlight.style.top = `${y}px`;
      this.elements.spotlight.style.width = `${width}px`;
      this.elements.spotlight.style.height = `${height}px`;
    }

    // ==========================================
    // TOOLTIP POSITIONING
    // ==========================================

    _positionTooltip(preferredPosition, targetElement) {
      const tooltip = this.elements.tooltip;
      const spotlightRect = this.elements.spotlight.getBoundingClientRect();
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;
      const tooltipWidth = 360;
      const tooltipHeight = 280; // Approximate
      const gap = 20;

      // Remove existing position classes
      tooltip.classList.remove('position-top', 'position-bottom', 'position-left', 'position-right');

      let position = preferredPosition;
      let left, top;

      // Calculate initial position based on preference
      switch (position) {
        case 'top':
          left = spotlightRect.left + spotlightRect.width / 2 - tooltipWidth / 2;
          top = spotlightRect.top - tooltipHeight - gap;
          break;
        case 'bottom':
          left = spotlightRect.left + spotlightRect.width / 2 - tooltipWidth / 2;
          top = spotlightRect.bottom + gap;
          break;
        case 'left':
          left = spotlightRect.left - tooltipWidth - gap;
          top = spotlightRect.top + spotlightRect.height / 2 - tooltipHeight / 2;
          break;
        case 'right':
          left = spotlightRect.right + gap;
          top = spotlightRect.top + spotlightRect.height / 2 - tooltipHeight / 2;
          break;
        default:
          left = spotlightRect.left + spotlightRect.width / 2 - tooltipWidth / 2;
          top = spotlightRect.bottom + gap;
          position = 'bottom';
      }

      // Adjust if out of bounds
      const adjusted = this._adjustPositionIfNeeded(left, top, tooltipWidth, tooltipHeight, position);
      left = adjusted.left;
      top = adjusted.top;
      position = adjusted.position;

      // Apply position
      tooltip.style.left = `${Math.max(16, Math.min(left, viewportWidth - tooltipWidth - 16))}px`;
      tooltip.style.top = `${Math.max(16, Math.min(top, viewportHeight - tooltipHeight - 16))}px`;
      tooltip.classList.add(`position-${position}`);
    }

    _adjustPositionIfNeeded(left, top, width, height, position) {
      const margin = 16;
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // Check horizontal bounds
      if (left < margin) left = margin;
      if (left + width > viewportWidth - margin) left = viewportWidth - width - margin;

      // Check vertical bounds and flip if necessary
      if (top < margin) {
        // Flip to bottom
        top = margin;
        position = 'bottom';
      }
      if (top + height > viewportHeight - margin) {
        // Flip to top
        top = viewportHeight - height - margin;
        position = 'top';
      }

      return { left, top, position };
    }

    // ==========================================
    // AUTO-ADVANCE TIMER
    // ==========================================

    _startAutoAdvance(duration) {
      this._clearAutoAdvance();
      
      this.autoAdvanceTimeRemaining = duration;
      this.autoAdvanceStartTime = performance.now();
      
      const timerCircle = this.elements.tooltip.querySelector('.timer-progress');
      const circumference = 88; // 2 * PI * 14

      const updateTimer = () => {
        if (!this.isActive || this.isPaused) return;

        const elapsed = performance.now() - this.autoAdvanceStartTime;
        this.autoAdvanceTimeRemaining = Math.max(0, duration - elapsed);

        // Update circular progress
        const progress = elapsed / duration;
        timerCircle.style.strokeDashoffset = circumference * (1 - progress);

        if (elapsed >= duration) {
          this._nextStep();
        } else {
          this.animationFrameId = requestAnimationFrame(updateTimer);
        }
      };

      this.animationFrameId = requestAnimationFrame(updateTimer);
    }

    _clearAutoAdvance() {
      if (this.autoAdvanceTimer) {
        clearTimeout(this.autoAdvanceTimer);
        this.autoAdvanceTimer = null;
      }
      this._cancelAnimationFrame();
    }

    _cancelAnimationFrame() {
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
    }

    _pauseAutoAdvance() {
      this._cancelAnimationFrame();
      this.autoAdvanceTimeRemaining = Math.max(0, this.autoAdvanceTimeRemaining);
    }

    _resumeAutoAdvance() {
      if (this.autoAdvanceTimeRemaining > 0) {
        this._startAutoAdvance(this.autoAdvanceTimeRemaining);
      }
    }

    // ==========================================
    // NAVIGATION ACTIONS
    // ==========================================

    _handleAction(action) {
      switch (action) {
        case 'next':
          this._nextStep();
          break;
        case 'prev':
          this._prevStep();
          break;
        case 'pause':
          this.togglePause();
          break;
        case 'skip':
          this._skipTour();
          break;
        case 'restart':
          this._restartTour();
          break;
        case 'close':
          this.stop();
          break;
      }
    }

    _nextStep() {
      if (this.currentStep < this.steps.length - 1) {
        this.elements.tooltip.classList.remove('visible');
        this.elements.spotlight.classList.remove('pulse');
        
        setTimeout(() => {
          this._showStep(this.currentStep + 1);
        }, 200);
      } else {
        this._completeTour();
      }
    }

    _prevStep() {
      if (this.currentStep > 0) {
        this.elements.tooltip.classList.remove('visible');
        this.elements.spotlight.classList.remove('pulse');
        
        setTimeout(() => {
          this._showStep(this.currentStep - 1);
        }, 200);
      }
    }

    _skipTour() {
      this._markAsDismissed();
      this.stop();
      this._emitEvent('skip');
    }

    _completeTour() {
      this._markAsCompleted();
      this._showCompletionScreen();
      this._emitEvent('complete');
    }

    _restartTour() {
      this.elements.completion.classList.remove('active');
      this._showStep(0);
    }

    _showCompletionScreen() {
      this.elements.overlay.classList.remove('active');
      this.elements.tooltip.classList.remove('visible');
      this.elements.progressBar.classList.remove('active');
      this.elements.completion.classList.add('active');
    }

    // ==========================================
    // EVENT HANDLERS
    // ==========================================

    _attachEventListeners() {
      document.addEventListener('keydown', this.boundHandlers.onKeyDown);
      window.addEventListener('resize', this.boundHandlers.onResize);
      document.addEventListener('touchstart', this.boundHandlers.onTouchStart, { passive: true });
    }

    _detachEventListeners() {
      document.removeEventListener('keydown', this.boundHandlers.onKeyDown);
      window.removeEventListener('resize', this.boundHandlers.onResize);
      document.removeEventListener('touchstart', this.boundHandlers.onTouchStart);
    }

    _handleKeyDown(e) {
      if (!this.isActive) return;

      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
          e.preventDefault();
          this._nextStep();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault();
          this._prevStep();
          break;
        case 'Escape':
          e.preventDefault();
          this._skipTour();
          break;
        case ' ':
          e.preventDefault();
          this.togglePause();
          break;
        case 'Home':
          e.preventDefault();
          this.goToStep(0);
          break;
        case 'End':
          e.preventDefault();
          this.goToStep(this.steps.length - 1);
          break;
      }
    }

    _handleResize() {
      if (!this.isActive) return;
      
      // Reposition current step elements
      const step = this.steps[this.currentStep];
      if (step) {
        this._findTargetElement(step).then(target => {
          if (target) {
            this._positionSpotlight(target, step.highlightPadding || 12);
            this._positionTooltip(step.position || 'bottom', target);
          }
        });
      }
    }

    _handleTouch(e) {
      // Handle swipe gestures for mobile
      if (!this.isActive) return;
      
      const touch = e.touches[0];
      if (!touch) return;

      this.touchStartX = touch.clientX;
      this.touchStartY = touch.clientY;
    }

    _handleDocumentClick(e) {
      // Handle click outside tooltip
      if (this.isActive && !this.elements.tooltip.contains(e.target)) {
        // Could advance or do nothing depending on UX preference
      }
    }

    // ==========================================
    // ELEMENT DETECTION
    // ==========================================

    async _findTargetElement(step) {
      const selector = step.target;
      if (!selector) return null;

      // Try direct selector match first
      let element = document.querySelector(selector);
      
      if (element) return element;

      // Try multiple selectors (comma-separated)
      const selectors = selector.split(',').map(s => s.trim());
      for (const sel of selectors) {
        element = document.querySelector(sel);
        if (element) return element;
      }

      // Wait for element to appear (with timeout)
      return new Promise((resolve) => {
        let attempts = 0;
        const maxAttempts = 10;
        const interval = 100;

        const observer = new MutationObserver(() => {
          for (const sel of selectors) {
            const el = document.querySelector(sel);
            if (el) {
              observer.disconnect();
              resolve(el);
              return;
            }
          }
          attempts++;
          if (attempts >= maxAttempts) {
            observer.disconnect();
            resolve(null);
          }
        });

        observer.observe(document.body, {
          childList: true,
          subtree: true
        });

        this.observers.push(observer);

        // Timeout fallback
        setTimeout(() => {
          observer.disconnect();
          resolve(null);
        }, maxAttempts * interval);
      });
    }

    _scrollToElement(element, offset = 100) {
      const rect = element.getBoundingClientRect();
      const isInViewport = (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
      );

      if (!isInViewport) {
        const scrollTop = window.pageYOffset + rect.top - offset;
        window.scrollTo({
          top: scrollTop,
          behavior: 'smooth'
        });
        
        // Wait for scroll to complete
        return new Promise(resolve => setTimeout(resolve, 400));
      }
      return Promise.resolve();
    }

    // ==========================================
    // PROGRESS BAR
    // ==========================================

    _updateProgressBar() {
      const fill = this.elements.progressBar.querySelector('.tour-progress-bar-fill');
      const progress = ((this.currentStep + 1) / this.steps.length) * 100;
      fill.style.width = `${progress}%`;
    }

    // ==========================================
    // STORAGE / PERSISTENCE
    // ==========================================

    _markAsCompleted() {
      try {
        const completed = JSON.parse(localStorage.getItem(STORAGE_KEYS.completed) || '{}');
        completed[this.config.id] = {
          completedAt: new Date().toISOString(),
          stepCount: this.steps.length
        };
        localStorage.setItem(STORAGE_KEYS.completed, JSON.stringify(completed));
      } catch (e) {
        console.warn('[ProductTour] Could not save completion status:', e);
      }
    }

    _markAsDismissed() {
      try {
        const dismissed = JSON.parse(localStorage.getItem(STORAGE_KEYS.dismissed) || '{}');
        dismissed[this.config.id] = {
          dismissedAt: new Date().toISOString()
        };
        localStorage.setItem(STORAGE_KEYS.dismissed, JSON.stringify(dismissed));
      } catch (e) {
        console.warn('[ProductTour] Could not save dismissal:', e);
      }
    }

    isTourCompleted(tourId) {
      try {
        const completed = JSON.parse(localStorage.getItem(STORAGE_KEYS.completed) || '{}');
        return !!completed[tourId];
      } catch (e) {
        return false;
      }
    }

    isTourDismissed(tourId) {
      try {
        const dismissed = JSON.parse(localStorage.getItem(STORAGE_KEYS.dismissed) || '{}');
        return !!dismissed[tourId];
      } catch (e) {
        return false;
      }
    }

    resetTourProgress(tourId) {
      try {
        const completed = JSON.parse(localStorage.getItem(STORAGE_KEYS.completed) || '{}');
        delete completed[tourId];
        localStorage.setItem(STORAGE_KEYS.completed, JSON.stringify(completed));

        const dismissed = JSON.parse(localStorage.getItem(STORAGE_KEYS.dismissed) || '{}');
        delete dismissed[tourId];
        localStorage.setItem(STORAGE_KEYS.dismissed, JSON.stringify(dismissed));
      } catch (e) {
        console.warn('[ProductTour] Could not reset tour progress:', e);
      }
    }

    // ==========================================
    // URL PARAMETER TRIGGER
    // ==========================================

    _checkURLTrigger() {
      const params = new URLSearchParams(window.location.search);
      const tourParam = params.get('tour');
      
      if (tourParam && TOUR_CONFIGS[tourParam]) {
        // Small delay to ensure page is ready
        setTimeout(() => {
          this.start(tourParam);
        }, 1000);
      }
    }

    _detectCurrentTourType() {
      const path = window.location.pathname.toLowerCase();
      
      if (path.includes('quantum')) return 'quantum';
      if (path.includes('pipeline')) return 'pipeline';
      if (path.includes('security')) return 'security';
      
      // Default to quantum
      return 'quantum';
    }

    // ==========================================
    // AUTO-START ON FIRST VISIT
    // ==========================================

    checkAndAutoStart(tourType) {
      if (this.isTourCompleted(tourType) || this.isTourDismissed(tourType)) {
        return false;
      }

      // Check if user has visited before
      const hasVisitedBefore = localStorage.getItem(STORAGE_KEYS.lastTour);
      
      if (!hasVisitedBefore) {
        // First visit - start tour after short delay
        localStorage.setItem(STORAGE_KEYS.lastTour, tourType);
        setTimeout(() => {
          this.start(tourType);
        }, 1500);
        return true;
      }

      return false;
    }

    // ==========================================
    // ACCESSIBILITY
    // ==========================================

    _announceToScreenReader(message) {
      // Create or get live region
      let liveRegion = document.getElementById('tour-live-region');
      if (!liveRegion) {
        liveRegion = this._createElement('div', 'tour-sr-only');
        liveRegion.id = 'tour-live-region';
        liveRegion.setAttribute('role', 'status');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        document.body.appendChild(liveRegion);
      }
      liveRegion.textContent = message;
    }

    // ==========================================
    // UTILITY METHODS
    // ==========================================

    _createElement(tag, className) {
      const element = document.createElement(tag);
      if (className) element.className = className;
      return element;
    }

    _cleanupObservers() {
      this.observers.forEach(observer => observer.disconnect());
      this.observers = [];
    }

    _emitEvent(eventName, detail = {}) {
      const event = new CustomEvent(`scimspt:tour:${eventName}`, {
        bubbles: true,
        detail: {
          tourId: this.config?.id,
          currentStep: this.currentStep,
          totalSteps: this.steps?.length,
          ...detail
        }
      });
      document.dispatchEvent(event);
    }

    // ==========================================
    // CLEANUP
    // ==========================================

    destroy() {
      this.stop();
      
      // Remove DOM elements
      Object.values(this.elements).forEach(el => {
        if (el && el.parentNode) {
          el.parentNode.removeChild(el);
        }
      });

      // Clear storage references
      this.elements = {};
      this.steps = [];
      this.config = null;
    }
  }

  // ============================================
  // EXPORTS
  // ============================================

  // Create singleton instance
  const SciMSPTTour = new ProductTour();

  // Expose globally
  global.SciMSPTTour = SciMSPTTour;

  // CommonJS/Module support
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = SciMSPTTour;
  }

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      // Check for page-specific auto-start
      const pageConfig = {
        '/quantum.html': 'quantum',
        '/pipeline.html': 'pipeline',
        '/security.html': 'security'
      };
      
      const currentPage = pageConfig[window.location.pathname.split('/').pop()] || null;
      if (currentPage) {
        SciMSPTTour.checkAndAutoStart(currentPage);
      }
    });
  } else {
    // DOM already ready
    const pageConfig = {
      '/quantum.html': 'quantum',
      '/pipeline.html': 'pipeline',
      '/security.html': 'security'
    };
    
    const currentPage = pageConfig[window.location.pathname.split('/').pop()] || null;
    if (currentPage) {
      SciMSPTTour.checkAndAutoStart(currentPage);
    }
  }

})(typeof window !== 'undefined' ? window : this);
