<template>
  <div class="logo-wrapper" :class="containerClass">
    <!-- Ultra Minimal Logo Design -->
    <svg 
      :width="svgSize" 
      :height="svgSize" 
      viewBox="0 0 100 100" 
      xmlns="http://www.w3.org/2000/svg"
      class="logo-minimal"
    >
      <defs>
        <!-- Single Gradient -->
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
        </linearGradient>
        
        <!-- Glow Effect -->
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <!-- Minimalist D + P Combined Symbol -->
      <g transform="translate(50, 50)">
        <!-- Letter D Shape (Left) -->
        <path
          d="M -20 -25
             L -20 25
             Q -20 25, -10 25
             L -10 25
             Q 5 25, 5 10
             L 5 -10
             Q 5 -25, -10 -25
             Z"
          fill="url(#logoGradient)"
          opacity="0.9"
        />
        
        <!-- Letter P Shape (Right) - Overlapping -->
        <path
          d="M 0 -25
             L 0 25
             M 0 -25
             L 15 -25
             Q 25 -25, 25 -15
             L 25 -5
             Q 25 5, 15 5
             L 0 5"
          fill="none"
          stroke="url(#logoGradient)"
          stroke-width="4"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        
        <!-- Digital Dot Accent -->
        <circle cx="0" cy="0" r="3" fill="#06B6D4" filter="url(#glow)" />
      </g>
    </svg>

    <!-- Modern Typography -->
    <div v-if="showText" class="logo-typography" :class="textClass">
      <div class="logo-main-text">
        <span class="logo-digi">Digi</span><span class="logo-portal">Portal</span>
      </div>
      <div v-if="showTagline" class="logo-tagline">
        Digital Portfolio System
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  showText: {
    type: Boolean,
    default: true
  },
  showTagline: {
    type: Boolean,
    default: false
  },
  layout: {
    type: String,
    default: 'horizontal',
    validator: (value) => ['horizontal', 'vertical', 'stacked'].includes(value)
  },
  theme: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'dark', 'light'].includes(value)
  }
});

const svgSize = computed(() => {
  const sizes = {
    xs: 24,
    sm: 32,
    md: 40,
    lg: 56,
    xl: 72
  };
  return sizes[props.size];
});

const containerClass = computed(() => {
  return [
    `logo-${props.size}`,
    `logo-${props.layout}`,
    `logo-theme-${props.theme}`
  ];
});

const textClass = computed(() => {
  const textSizes = {
    xs: 'text-xs',
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-xl',
    xl: 'text-2xl'
  };
  return textSizes[props.size];
});
</script>

<style scoped>
.logo-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 0.625rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Layout Variations */
.logo-horizontal {
  flex-direction: row;
}

.logo-vertical {
  flex-direction: column;
  text-align: center;
  gap: 0.375rem;
}

.logo-stacked {
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
}

/* Logo Animation */
.logo-minimal {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.logo-wrapper:hover .logo-minimal {
  transform: rotate(-5deg) scale(1.1);
}

/* Typography */
.logo-typography {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.logo-main-text {
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
}

.logo-digi {
  color: #4F46E5;
  transition: color 0.2s ease;
}

.logo-portal {
  color: #7C3AED;
  transition: color 0.2s ease;
}

.logo-tagline {
  font-size: 0.625em;
  font-weight: 500;
  color: #64748B;
  letter-spacing: 0.025em;
  text-transform: uppercase;
  margin-top: 0.125rem;
}

/* Theme Variations */
.logo-theme-dark .logo-digi {
  color: #818CF8;
}

.logo-theme-dark .logo-portal {
  color: #A78BFA;
}

.logo-theme-dark .logo-tagline {
  color: #94A3B8;
}

.logo-theme-light .logo-digi {
  color: #3730A3;
}

.logo-theme-light .logo-portal {
  color: #5B21B6;
}

/* Hover Effects */
.logo-wrapper:hover .logo-digi {
  color: #06B6D4;
}

.logo-wrapper:hover .logo-portal {
  color: #4F46E5;
}

/* Size-specific adjustments */
.logo-xs .logo-tagline {
  display: none;
}

.logo-sm .logo-tagline {
  font-size: 0.5em;
}

/* Responsive */
@media (max-width: 640px) {
  .logo-horizontal {
    gap: 0.5rem;
  }
  
  .logo-main-text {
    font-size: 0.9em;
  }
}

/* Print styles */
@media print {
  .logo-wrapper {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
</style>
