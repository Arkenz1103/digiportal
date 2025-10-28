<template>
  <div class="logo-container" :class="sizeClass">
    <!-- Modern Minimalist Logo Design -->
    <svg 
      :width="width" 
      :height="height" 
      viewBox="0 0 200 200" 
      xmlns="http://www.w3.org/2000/svg"
      class="logo-svg"
    >
      <!-- Gradient Definitions -->
      <defs>
        <!-- Primary Gradient - Blue to Purple -->
        <linearGradient id="primaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
          <stop offset="50%" style="stop-color:#8B5CF6;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#EC4899;stop-opacity:1" />
        </linearGradient>
        
        <!-- Accent Gradient - Cyan to Blue -->
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#06B6D4;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1" />
        </linearGradient>

        <!-- Shadow Filter -->
        <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.15"/>
        </filter>
      </defs>

      <!-- Modern Book/Portfolio Icon -->
      <g transform="translate(100, 100)">
        <!-- Book Base - Simplified -->
        <path
          d="M -50 -30 
             L -50 30 
             Q -50 40, -40 40
             L 40 40
             Q 50 40, 50 30
             L 50 -30
             Q 50 -40, 40 -40
             L -40 -40
             Q -50 -40, -50 -30"
          fill="url(#primaryGradient)"
          opacity="0.1"
          class="book-bg"
        />
        
        <!-- Book Pages - Modern Abstract -->
        <path
          d="M -35 -25
             L -35 25
             L 0 30
             L 35 25
             L 35 -25
             L 0 -20
             Z"
          fill="none"
          stroke="url(#primaryGradient)"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="book-pages"
        />
        
        <!-- Center Divider -->
        <line
          x1="0"
          y1="-20"
          x2="0"
          y2="30"
          stroke="url(#primaryGradient)"
          stroke-width="3"
          stroke-linecap="round"
          class="book-spine"
        />
        
        <!-- Digital Arrow/Cursor - Modernized -->
        <g transform="translate(0, -5)">
          <path
            d="M -8 -8
               L 8 -8
               L 0 8
               Z"
            fill="url(#accentGradient)"
            class="cursor-icon"
            filter="url(#shadow)"
          />
        </g>
        
        <!-- Decorative Dots -->
        <circle cx="-45" cy="-35" r="3" fill="url(#accentGradient)" opacity="0.6" />
        <circle cx="45" cy="-35" r="3" fill="url(#primaryGradient)" opacity="0.6" />
        <circle cx="0" cy="45" r="3" fill="url(#accentGradient)" opacity="0.8" />
      </g>
    </svg>
    
    <!-- Text Logo -->
    <div v-if="showText" class="logo-text" :class="textSizeClass">
      <span class="text-gradient-primary">DIGI</span><span class="text-gradient-accent">PORTAL</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'xlarge'].includes(value)
  },
  showText: {
    type: Boolean,
    default: true
  },
  orientation: {
    type: String,
    default: 'horizontal',
    validator: (value) => ['horizontal', 'vertical', 'icon-only'].includes(value)
  }
});

// Computed dimensions based on size
const dimensions = computed(() => {
  const sizes = {
    small: { width: 32, height: 32 },
    medium: { width: 48, height: 48 },
    large: { width: 64, height: 64 },
    xlarge: { width: 96, height: 96 }
  };
  return sizes[props.size];
});

const width = computed(() => dimensions.value.width);
const height = computed(() => dimensions.value.height);

const sizeClass = computed(() => {
  return {
    'logo-small': props.size === 'small',
    'logo-medium': props.size === 'medium',
    'logo-large': props.size === 'large',
    'logo-xlarge': props.size === 'xlarge',
    'logo-horizontal': props.orientation === 'horizontal',
    'logo-vertical': props.orientation === 'vertical',
    'logo-icon-only': props.orientation === 'icon-only'
  };
});

const textSizeClass = computed(() => {
  const textSizes = {
    small: 'text-sm',
    medium: 'text-lg',
    large: 'text-2xl',
    xlarge: 'text-4xl'
  };
  return textSizes[props.size];
});
</script>

<style scoped>
.logo-container {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  user-select: none;
}

.logo-horizontal {
  flex-direction: row;
}

.logo-vertical {
  flex-direction: column;
  gap: 0.5rem;
}

.logo-icon-only .logo-text {
  display: none;
}

.logo-svg {
  transition: transform 0.3s ease;
}

.logo-container:hover .logo-svg {
  transform: scale(1.05);
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

.book-pages {
  animation: float 3s ease-in-out infinite;
}

.cursor-icon {
  animation: float 3s ease-in-out infinite;
  animation-delay: 0.5s;
}

/* Text Styling */
.logo-text {
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1;
}

.text-gradient-primary {
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-gradient-accent {
  background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-left: 0.125rem;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .logo-svg {
    filter: brightness(1.1);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .logo-horizontal {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .logo-text {
    font-size: 0.875em;
  }
}
</style>
