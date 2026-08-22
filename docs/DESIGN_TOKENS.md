# SciMSPT Design System & Design Tokens
=====================================

Complete documentation of CSS variables, design tokens, and component usage guidelines.

## Table of Contents

1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Spacing Scale](#spacing-scale)
4. [Border Radius](#border-radius)
5. [Shadows & Elevation](#shadows--elevation)
6. [Animation Tokens](#animation-tokens)
7. [Glass/Blur Effects](#glassblur-effects)
8. [Component Library](#component-library)
9. [Accessibility Guidelines](#accessibility-guidelines)
10. [Usage Guidelines](#usage-guidelines)

---

## Color Palette

### Primary Colors (Neural/Cyber Theme)

```css
:root {
  /* Primary Accent - Cyan/Electric Blue */
  --accent-primary: #00E5FF;
  --accent-primary-rgb: 0, 229, 255;
  --accent-primary-hover: #33E8FF;
  --accent-primary-muted: rgba(0, 229, 255, 0.15);
  
  /* Secondary Accent - Purple/Violet */
  --accent-secondary: #a78bfa;
  --accent-secondary-rgb: 167, 139, 250;
  --accent-secondary-hover: #b9a4fb;
  --accent-secondary-muted: rgba(167, 139, 250, 0.15);
  
  /* Gradient */
  --gradient-primary: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
}
```

**When to Use:**
- `--accent-primary`: CTAs, active states, primary buttons, links
- `--accent-secondary`: Secondary actions, badges, highlights
- `--gradient-primary`: Hero sections, premium features

---

### Background Colors

```css
:root {
  --bg-primary: #0a1628;        /* Main background */
  --bg-secondary: #111d32;      /* Cards, panels */
  --bg-tertiary: #16243d;       /* Hover states */
  
  /* Glass Effects */
  --bg-glass: rgba(10, 22, 40, 0.85);
  --bg-glass-light: rgba(16, 35, 60, 0.75);
  --bg-glass-heavy: rgba(10, 20, 35, 0.95);
}
```

---

### Text Colors

```css
:root {
  --text-primary: #e8f4fc;     /* Headings, main text */
  --text-secondary: #94a3b8;   /* Subtitles */
  --text-muted: #64748b;       /* Placeholders */
  --text-accent: #00E5FF;      /* Links */
}
```

---

## Typography

### Font Families

```css
:root {
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-display: 'Orbitron', sans-serif;
  --font-icon: 'Material Icons Round';
}
```

**Usage:**
| Context | Font | Weight |
|---------|------|--------|
| H1-H3 Headings | Playfair Display | 700-900 |
| Body Text | Inter | 400-600 |
| Code/Data | JetBrains Mono | 400 |
| Sci-Tech Labels | Orbitron | 700 |

### Type Scale (Fluid Typography)

```css
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.82rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.5vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.25rem + 1vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.5vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.75rem + 2vw, 3.5rem);
}
```

---

## Spacing Scale (4px Grid)

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
}
```

---

## Border Radius

```css
:root {
  --radius-sm: 0.375rem;   /* Badges */
  --radius-md: 0.5rem;     /* Buttons, inputs */
  --radius-lg: 0.75rem;    /* Cards */
  --radius-xl: 1rem;       /* Modals */
  --radius-full: 9999px;   /* Pills */
}
```

---

## Shadows & Glow Effects

```css
:root {
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.3);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.4);
  --shadow-xl: 0 20px 40px rgba(0,0,0,0.5);
  
  /* SciMSPT Signature Glows */
  --glow-primary: 
    0 0 20px rgba(0, 229, 255, 0.2),
    0 0 40px rgba(0, 229, 255, 0.1);
}
```

---

## Animation Tokens

```css
:root {
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
}
```

---

## Component Examples

### Button Variants

```html
<!-- Primary -->
<button class="btn-primary">Search Papers</button>

<!-- Ghost/Outline -->
<button class="btn-ghost">Cancel</button>

<!-- Icon Only -->
<button aria-label="Settings" class="btn-icon">
  <span class="material-icons-round">settings</span>
</button>
```

### Card Component

```html
<article class="card" role="article">
  <h3>Paper Title</h3>
  <p>Abstract text...</p>
  <span class="badge badge-primary">AI/ML</span>
</article>
```

### Form Input

```html>
<div class="input-field-wrapper">
  <label for="search">Search</label>
  <input id="search" type="search" class="input-field"
         placeholder="Search papers...">
</div>
```

---

## Accessibility Checklist

### Color Contrast (WCAG AA)
- ✅ Body text on background: **14.5:1** (AAA)
- ✅ Large text: **8.2:1** (AA)
- ✅ Links/Accent: **11.2:1** (AAA)

### Keyboard Navigation
- All interactive elements focusable with Tab
- Visible focus indicators (`:focus-visible`)
- Skip link for keyboard users
- Escape closes modals/overlays

### Screen Reader Support
- ARIA labels on icon-only buttons
- Semantic HTML (article, nav, main)
- Live regions for dynamic content
- Alt text for images

### Motion Preferences
- Respects `prefers-reduced-motion`
- No auto-playing animations
- Option to disable animations

---

## Performance Rules

1. **Content always visible** - Never use `opacity: 0` by default
2. **Lazy load images** below fold
3. **Defer non-critical JS**
4. **Inline critical CSS**
5. **Preload fonts** with `display=swap`
6. **Cache assets** via service worker

---

*Version 4.0 | Last Updated: August 2024*
