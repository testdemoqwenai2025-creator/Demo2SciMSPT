/**
 * SciMSPT Phase 3: Video Player JavaScript
 * ========================================
 * Custom video player controls and functionality
 */

class SciMSPTVideoPlayer {
  constructor(container, options = {}) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    if (!this.container) return;
    
    this.video = this.container.querySelector('video');
    if (!this.video) return;
    
    this.options = {
      autoHideControls: true,
      controlsTimeout: 3000,
      showProgress: true,
      ...options
    };
    
    this.init();
  }
  
  init() {
    this.createControls();
    this.bindEvents();
    this.startControlsTimer();
  }
  
  createControls() {
    // Create controls container if not exists
    let controls = this.container.querySelector('.video-controls');
    if (!controls) {
      controls = document.createElement('div');
      controls.className = 'video-controls';
      this.container.appendChild(controls);
    }
    
    controls.innerHTML = `
      <button class="video-play-btn" data-action="play-pause">
        <span class="material-icons-round">play_arrow</span>
      </button>
      
      <div class="video-progress" data-action="seek">
        <div class="video-progress-bar"></div>
      </div>
      
      <span class="video-time">
        <span class="video-current-time">0:00</span> / <span class="video-duration">0:00</span>
      </span>
      
      <div class="video-volume">
        <button class="video-control-btn" data-action="mute">
          <span class="material-icons-round">volume_up</span>
        </button>
      </div>
      
      <button class="video-control-btn" data-action="fullscreen">
        <span class="material-icons-round">fullscreen</span>
      </button>
    `;
    
    this.controls = controls;
    this.playBtn = controls.querySelector('[data-action="play-pause"]');
    this.progressBar = controls.querySelector('.video-progress-bar');
    this.currentTimeEl = controls.querySelector('.video-current-time');
    this.durationEl = controls.querySelector('.video-duration');
    this.muteBtn = controls.querySelector('[data-action="mute"]');
    this.fullscreenBtn = controls.querySelector('[data-action="fullscreen"]');
  }
  
  bindEvents() {
    // Play/Pause
    this.playBtn.addEventListener('click', () => this.togglePlay());
    this.video.addEventListener('click', () => this.togglePlay());
    
    // Video events
    this.video.addEventListener('play', () => this.onPlay());
    this.video.addEventListener('pause', () => this.onPause());
    this.video.addEventListener('timeupdate', () => this.updateProgress());
    this.video.addEventListener('loadedmetadata', () => this.updateDuration());
    this.video.addEventListener('ended', () => this.onEnded());
    
    // Progress bar seeking
    const progressContainer = this.controls.querySelector('.video-progress');
    progressContainer.addEventListener('click', (e) => this.seek(e));
    
    // Mute
    this.muteBtn.addEventListener('click', () => this.toggleMute());
    
    // Fullscreen
    this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
    
    // Show/hide controls on hover
    this.container.addEventListener('mouseenter', () => this.showControls());
    this.container.addEventListener('mouseleave', () => this.hideControlsDelayed());
    this.container.addEventListener('mousemove', () => this.showControls());
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => this.handleKeyboard(e));
  }
  
  togglePlay() {
    if (this.video.paused) {
      this.video.play();
    } else {
      this.video.pause();
    }
  }
  
  onPlay() {
    this.playBtn.innerHTML = '<span class="material-icons-round">pause</span>';
    this.container.classList.add('playing');
  }
  
  onPause() {
    this.playBtn.innerHTML = '<span class="material-icons-round">play_arrow</span>';
    this.container.classList.remove('playing');
  }
  
  onEnded() {
    this.playBtn.innerHTML = '<span class="material-icons-round">replay</span>';
    this.container.classList.remove('playing');
  }
  
  updateProgress() {
    if (this.video.duration) {
      const percent = (this.video.currentTime / this.video.duration) * 100;
      this.progressBar.style.width = `${percent}%`;
      this.currentTimeEl.textContent = this.formatTime(this.video.currentTime);
    }
  }
  
  updateDuration() {
    this.durationEl.textContent = this.formatTime(this.video.duration);
  }
  
  seek(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    this.video.currentTime = percent * this.video.duration;
  }
  
  toggleMute() {
    this.video.muted = !this.video.muted;
    const icon = this.muteBtn.querySelector('.material-icons-round');
    icon.textContent = this.video.muted ? 'volume_off' : 'volume_up';
  }
  
  toggleFullscreen() {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      this.container.requestFullscreen();
    }
  }
  
  formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
  
  showControls() {
    this.controls.style.opacity = '1';
    this.startControlsTimer();
  }
  
  hideControlsDelayed() {
    if (!this.video.paused && this.options.autoHideControls) {
      setTimeout(() => {
        if (!this.video.paused) {
          this.controls.style.opacity = '0';
        }
      }, this.options.controlsTimeout);
    }
  }
  
  startControlsTimer() {
    if (this.controlsTimer) clearTimeout(this.controlsTimer);
    this.controlsTimer = setTimeout(() => {
      if (!this.video.paused && this.options.autoHideControls) {
        this.controls.style.opacity = '0';
      }
    }, this.options.controlsTimeout);
  }
  
  handleKeyboard(e) {
    // Only handle when video is focused or playing
    if (document.activeElement !== this.video && !this.container.contains(document.activeElement)) return;
    
    switch(e.key) {
      case ' ':
      case 'k':
        e.preventDefault();
        this.togglePlay();
        break;
      case 'f':
        this.toggleFullscreen();
        break;
      case 'm':
        this.toggleMute();
        break;
      case 'ArrowLeft':
        this.video.currentTime -= 5;
        break;
      case 'ArrowRight':
        this.video.currentTime += 5;
        break;
      case 'ArrowUp':
        this.video.volume = Math.min(1, this.video.volume + 0.1);
        break;
      case 'ArrowDown':
        this.video.volume = Math.max(0, this.video.volume - 0.1);
        break;
    }
  }
}

// Initialize all video players on page load
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.video-container').forEach(container => {
    new SciMSPTVideoPlayer(container);
  });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SciMSPTVideoPlayer;
}
