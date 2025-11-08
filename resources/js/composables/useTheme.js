import { ref, watch } from 'vue';

// Global theme state (shared across all components)
const currentTheme = ref('light');
const systemTheme = ref('light');

// Initialize theme from localStorage or default
const initializeTheme = () => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('digiportal_theme') || 'light';
    currentTheme.value = savedTheme;
    
    // Detect system theme
    detectSystemTheme();
    
    // Apply theme immediately
    applyTheme(savedTheme);
    
    // Setup system theme listener
    setupSystemThemeListener();
    
    console.log('🎨 Theme initialized:', savedTheme);
};

// Detect system theme preference
const detectSystemTheme = () => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    systemTheme.value = prefersDark ? 'dark' : 'light';
    console.log('🌓 System theme detected:', systemTheme.value);
};

// Apply theme to document
const applyTheme = (theme) => {
    console.log('🎨 Applying theme:', theme);
    
    // Remove existing theme classes
    document.documentElement.classList.remove('light', 'dark');
    
    let appliedTheme;
    
    if (theme === 'auto') {
        // Use system preference
        detectSystemTheme();
        appliedTheme = systemTheme.value;
    } else {
        appliedTheme = theme;
    }
    
    // Add theme class to html element
    document.documentElement.classList.add(appliedTheme);
    
    // Also add data attribute for CSS targeting
    document.documentElement.setAttribute('data-theme', appliedTheme);
    
    console.log('✅ Theme applied:', appliedTheme);
};

// Set theme (called when user changes theme)
const setTheme = (theme) => {
    console.log('🎨 Setting theme:', theme);
    
    currentTheme.value = theme;
    
    // Save to localStorage
    localStorage.setItem('digiportal_theme', theme);
    
    // Apply theme
    applyTheme(theme);
};

// Setup listener for system theme changes
const setupSystemThemeListener = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    mediaQuery.addEventListener('change', (e) => {
        console.log('🌓 System theme changed:', e.matches ? 'dark' : 'light');
        detectSystemTheme();
        
        // If user is in auto mode, reapply theme
        if (currentTheme.value === 'auto') {
            applyTheme('auto');
        }
    });
};

// Get effective theme (resolves 'auto' to actual theme)
const getEffectiveTheme = () => {
    if (currentTheme.value === 'auto') {
        return systemTheme.value;
    }
    return currentTheme.value;
};

// Composable hook
export function useTheme() {
    return {
        currentTheme,
        systemTheme,
        initializeTheme,
        setTheme,
        applyTheme,
        getEffectiveTheme
    };
}
