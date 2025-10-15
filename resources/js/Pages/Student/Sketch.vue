<script setup>
import { ref, onMounted } from 'vue';

const canvas = ref(null);
const ctx = ref(null);
const isDrawing = ref(false);
const currentColor = ref('#000000');
const brushSize = ref(5);
const lastX = ref(0);
const lastY = ref(0);
const currentTool = ref('brush');
const fileInput = ref(null);
const mySketches = ref([]);
const showMySketches = ref(false);
const showSketchDialog = ref(false);
const currentSketch = ref(null);

const tools = [
    { id: 'brush', name: 'Brush', icon: 'pi-pencil', description: 'Free drawing' },
    { id: 'eraser', name: 'Eraser', icon: 'pi-eraser', description: 'Erase parts of your drawing' },
];

const colors = [
    { hex: '#000000', name: 'Black' },
    { hex: '#ffffff', name: 'White' },
    { hex: '#ff0000', name: 'Red' },
    { hex: '#00ff00', name: 'Green' },
    { hex: '#0000ff', name: 'Blue' },
    { hex: '#ffff00', name: 'Yellow' },
    { hex: '#ff69b4', name: 'Pink' },
    { hex: '#800080', name: 'Purple' },
    { hex: '#ffa500', name: 'Orange' },
    { hex: '#8b4513', name: 'Brown' }
];

const brushSizes = [
    { size: 2, name: 'Extra Small' },
    { size: 4, name: 'Small' },
    { size: 8, name: 'Medium' },
    { size: 16, name: 'Large' },
];

onMounted(() => {
    initCanvas();
    window.addEventListener('resize', initCanvas);
    loadSketches();
});

const initCanvas = () => {
    const canvasElement = canvas.value;
    ctx.value = canvasElement.getContext('2d');
    
    canvasElement.width = canvasElement.offsetWidth;
    canvasElement.height = canvasElement.offsetHeight;
    
    ctx.value.fillStyle = '#ffffff';
    ctx.value.fillRect(0, 0, canvasElement.width, canvasElement.height);
};

const startDrawing = (e) => {
    isDrawing.value = true;
    [lastX.value, lastY.value] = getCoordinates(e);
};

const draw = (e) => {
    if (!isDrawing.value) return;
    
    const [x, y] = getCoordinates(e);
    
    ctx.value.beginPath();
    ctx.value.moveTo(lastX.value, lastY.value);
    ctx.value.lineTo(x, y);
    ctx.value.strokeStyle = currentTool.value === 'eraser' ? '#ffffff' : currentColor.value;
    ctx.value.lineWidth = brushSize.value;
    ctx.value.lineCap = 'round';
    ctx.value.stroke();

    [lastX.value, lastY.value] = [x, y];
};

const getCoordinates = (e) => {
    if (e.type.includes('touch')) {
        return [
            e.touches[0].clientX - e.target.offsetLeft,
            e.touches[0].clientY - e.target.offsetTop
        ];
    }
    return [e.offsetX, e.offsetY];
};

const stopDrawing = () => {
    isDrawing.value = false;
};

const clearCanvas = () => {
    if (confirm('Are you sure you want to clear the canvas?')) {
        const canvasElement = canvas.value;
        ctx.value.fillStyle = '#ffffff';
        ctx.value.fillRect(0, 0, canvasElement.width, canvasElement.height);
    }
};

const setTool = (toolId) => {
    currentTool.value = toolId;
    if (toolId === 'eraser') {
        brushSize.value = 20;
    } else {
        brushSize.value = 5;
    }
};

const saveDrawing = () => {
    const dataURL = canvas.value.toDataURL();
    const sketch = {
        id: Date.now(),
        dataURL: dataURL,
        date: new Date().toLocaleString()
    };
    
    mySketches.value.unshift(sketch);
    saveSketchesToLocalStorage();
    
    alert('Sketch saved to My Sketches!');
};

const saveSketchesToLocalStorage = () => {
    localStorage.setItem('mySketches', JSON.stringify(mySketches.value));
};

const loadSketches = () => {
    const savedSketches = localStorage.getItem('mySketches');
    if (savedSketches) {
        mySketches.value = JSON.parse(savedSketches);
    }
};

const loadSketchToCanvas = (dataURL) => {
    const img = new Image();
    img.onload = () => {
        clearCanvas();
        ctx.value.drawImage(img, 0, 0, canvas.value.width, canvas.value.height);
        showMySketches.value = false;
    };
    img.src = dataURL;
};

const deleteSketch = (id, e) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this sketch?')) {
        mySketches.value = mySketches.value.filter(sketch => sketch.id !== id);
        saveSketchesToLocalStorage();
    }
};

const viewSketch = (sketch) => {
    currentSketch.value = sketch;
    showSketchDialog.value = true;
};

const useSketch = () => {
    if (currentSketch.value) {
        loadSketchToCanvas(currentSketch.value.dataURL);
    }
    showSketchDialog.value = false;
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.match('image.*')) {
        alert('Please select an image file.');
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
            ctx.value.fillStyle = '#ffffff';
            ctx.value.fillRect(0, 0, canvas.value.width, canvas.value.height);
            
            const hRatio = canvas.value.width / img.width;
            const vRatio = canvas.value.height / img.height;
            const ratio = Math.min(hRatio, vRatio);
            const centerShiftX = (canvas.value.width - img.width * ratio) / 2;
            const centerShiftY = (canvas.value.height - img.height * ratio) / 2;
            
            ctx.value.drawImage(
                img, 
                0, 0, img.width, img.height,
                centerShiftX, centerShiftY, 
                img.width * ratio, img.height * ratio
            );
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
};
</script>

<template>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-6 border border-indigo-100">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <div>
                    <h1 class="text-2xl font-bold text-indigo-900">Sketch Pad</h1>
                    <p class="text-indigo-700 text-sm mt-1">Express your creativity with our digital sketchbook</p>
                </div>
                <div class="flex items-center gap-3 w-full sm:w-auto">
                    <button @click="clearCanvas" 
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 text-indigo-700 hover:bg-indigo-50 rounded-lg transition-all border border-indigo-200 hover:border-indigo-300">
                        <i class="pi pi-trash"></i>
                        <span>Clear</span>
                    </button>
                    <button @click="saveDrawing" 
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-all shadow-sm">
                        <i class="pi pi-download"></i>
                        <span>Save</span>
                    </button>
                </div>
            </div>

            <div class="flex gap-6 relative">
                <!-- Left Toolbar -->
                <div class="w-20 flex flex-col gap-4" style="z-index: 10;">
                    <!-- Tools -->
                    <div class="bg-indigo-50 rounded-xl p-2 flex flex-col gap-2 border border-indigo-100">
                        <button v-for="tool in tools" 
                                :key="tool.id"
                                @click="setTool(tool.id)"
                                class="p-3 rounded-lg hover:bg-white transition-all relative group"
                                :class="{ 'bg-white shadow-sm border border-indigo-200': currentTool === tool.id }">
                            <i :class="['pi', tool.icon, 'text-indigo-700', { 'text-indigo-600': currentTool === tool.id }]"></i>
                            
                            <!-- Tooltip - positioned to the right with higher z-index -->
                            <div class="absolute left-full top-1/2 ml-3 px-3 py-1.5 bg-indigo-700 text-white text-xs rounded-lg 
                                        whitespace-nowrap opacity-0 group-hover:opacity-100 transition-all pointer-events-none
                                        z-[100] shadow-lg transform -translate-y-1/2">
                                {{ tool.name }}
                                <div class="absolute right-full top-1/2 transform -translate-y-1/2 w-2 h-2 bg-indigo-700 rotate-45"></div>
                            </div>
                        </button>
                    </div>

                    <!-- Brush Sizes -->
                    <div class="bg-indigo-50 rounded-xl p-2 flex flex-col gap-3 border border-indigo-100">
                        <button v-for="size in brushSizes"
                                :key="size.size"
                                @click="brushSize = size.size"
                                class="p-3 rounded-lg hover:bg-white transition-all relative group"
                                :class="{ 'bg-white shadow-sm border border-indigo-200': brushSize === size.size }">
                            <div class="w-full flex items-center justify-center">
                                <div class="rounded-full bg-indigo-600"
                                     :style="{ 
                                         width: size.size + 'px', 
                                         height: size.size + 'px',
                                         opacity: brushSize === size.size ? '1' : '0.8'
                                     }">
                                </div>
                            </div>
                            
                            <!-- Tooltip - positioned to the right with higher z-index -->
                            <div class="absolute left-full top-1/2 ml-3 px-3 py-1 bg-[#0E1836] text-white text-xs rounded 
                                        whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none
                                        z-[100] shadow-lg transform -translate-y-1/2">
                                {{ size.name }}
                                <div class="absolute right-full top-1/2 transform -translate-y-1/2 w-2 h-2 bg-[#0E1836] rotate-45"></div>
                            </div>
                        </button>
                    </div>

                    <!-- My Sketches Button -->
                    <button @click="showMySketches = !showMySketches"
                            class="p-3 bg-indigo-50 rounded-xl hover:bg-white transition-all border border-indigo-100 flex flex-col items-center justify-center group"
                            :class="{ 'bg-white shadow-sm border-indigo-200': showMySketches }">
                        <i class="pi pi-images text-indigo-600 text-xl mb-1 group-hover:text-indigo-700 transition-colors"></i>
                        <span class="text-xs text-indigo-700 font-medium group-hover:text-indigo-800 transition-colors">My Sketches</span>
                    </button>
                </div>

                <!-- Canvas Area -->
                <div class="flex-1 relative">
                    <!-- My Sketches Panel -->
                    <div v-if="showMySketches" class="absolute left-0 right-0 top-0 bottom-0 bg-white/95 backdrop-blur-sm z-10 rounded-xl p-6 overflow-y-auto border border-indigo-100 shadow-lg">
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-xl font-bold text-indigo-900">My Sketches</h2>
                            <button @click="showMySketches = false" class="text-indigo-600 hover:bg-indigo-50 p-2 rounded-full transition-colors">
                                <i class="pi pi-times"></i>
                            </button>
                        </div>
                        
                        <div v-if="mySketches.length === 0" class="text-center py-12">
                            <div class="bg-indigo-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                                <i class="pi pi-inbox text-2xl text-indigo-600"></i>
                            </div>
                            <h3 class="text-lg font-medium text-indigo-900 mb-1">No sketches yet</h3>
                            <p class="text-indigo-600 text-sm">Start drawing to see your sketches here</p>
                        </div>
                        
                        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                            <div v-for="sketch in mySketches" 
                                 :key="sketch.id"
                                 @click="viewSketch(sketch)"
                                 class="relative group cursor-pointer">
                                <img :src="sketch.dataURL" class="w-full h-32 object-contain bg-gray-100 rounded-lg border border-[#B6CFFF]">
                                <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all rounded-lg"></div>
                                <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs p-1 px-2 rounded-b-lg truncate">
                                    {{ sketch.date }}
                                </div>
                                <button @click.stop="deleteSketch(sketch.id, $event)"
                                        class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                    <i class="pi pi-trash text-xs"></i>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Color Palette with Attach Photo button -->
                    <div class="mb-4 p-3 bg-[#F2FDFF] rounded-xl flex items-center justify-between flex-wrap border border-[#B6CFFF]">
                        <div class="flex items-center gap-2 flex-wrap">
                            <div v-for="color in colors" 
                                 :key="color.hex" 
                                 @click="currentColor = color.hex"
                                 :style="{ backgroundColor: color.hex }"
                                 :class="{ 
                                     'ring-2 ring-offset-2 ring-[#7BBBFE]': currentColor === color.hex,
                                     'border border-[#B6CFFF]': color.hex === '#ffffff'
                                 }"
                                 class="w-8 h-8 rounded-lg cursor-pointer shadow-sm transition-transform hover:scale-110"
                                 :title="color.name">
                            </div>
                            <input type="color" 
                                   v-model="currentColor"
                                   class="w-8 h-8 cursor-pointer">
                        </div>
                        <button @click="triggerFileInput" 
                                class="px-3 py-1.5 text-[#0E1836] hover:bg-[#B8AAFF]/10 rounded-lg transition-colors flex items-center gap-1">
                            <i class="pi pi-image"></i>
                            <span>Attach Photo</span>
                        </button>
                        <input type="file" 
                               ref="fileInput" 
                               @change="handleImageUpload" 
                               accept="image/*" 
                               class="hidden">
                    </div>

                    <!-- Canvas -->
                    <div class="border border-[#B6CFFF] rounded-xl overflow-hidden bg-[#F2FDFF] p-2">
                        <canvas ref="canvas"
                                @mousedown="startDrawing"
                                @mousemove="draw"
                                @mouseup="stopDrawing"
                                @mouseout="stopDrawing"
                                @touchstart="startDrawing"
                                @touchmove="draw"
                                @touchend="stopDrawing"
                                class="w-full h-[600px] bg-white cursor-crosshair rounded-lg shadow-inner">
                        </canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Sketch Dialog -->
    <div v-if="showSketchDialog" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-indigo-100">
            <div class="px-6 py-4 border-b border-indigo-100 bg-indigo-50 flex justify-between items-center">
                <h3 class="text-lg font-semibold text-indigo-900">View Sketch</h3>
                <button @click="showSketchDialog = false" class="text-indigo-600 hover:bg-indigo-100 p-1.5 rounded-full transition-colors">
                    <i class="pi pi-times"></i>
                </button>
            </div>
            <div class="p-6 flex-1 overflow-auto bg-gray-50">
                <div class="bg-white p-4 rounded-lg shadow-sm border border-indigo-50 max-w-2xl mx-auto">
                    <img :src="currentSketch?.dataURL" alt="Sketch" class="max-w-full h-auto mx-auto">
                </div>
            </div>
            <div class="p-4 border-t border-indigo-100 bg-white flex justify-end gap-3 rounded-b-xl">
                <button @click="showSketchDialog = false" class="px-4 py-2.5 text-sm font-medium text-indigo-700 hover:bg-indigo-50 rounded-lg border border-indigo-200 transition-colors">
                    Cancel
                </button>
                <button @click="useSketch" class="px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm transition-colors flex items-center gap-2">
                    <i class="pi pi-palette"></i>
                    <span>Use This Sketch</span>
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Add theme variables */
:root {
  --theme-purple: #B8AAFF;
  --theme-blue: #B6CFFF;
  --theme-light: #F2FDFF;
  --theme-accent: #7BBBFE;
  --theme-dark: #0E1836;
}

canvas {
    touch-action: none;
}

/* Custom color picker styling */
input[type="color"] {
    -webkit-appearance: none;
    appearance: none;
    border: none;
    padding: 0;
    border-radius: 0.5rem;
}

input[type="color"]::-webkit-color-swatch-wrapper {
    padding: 0;
    border-radius: 0.5rem;
}

input[type="color"]::-webkit-color-swatch {
    border: none;
    border-radius: 0.5rem;
}

/* Animation for buttons */
button {
    transition: all 0.3s ease;
}

button:hover {
    transform: scale(1.05);
}

/* Custom styles for inputs */
input:focus, textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(123, 187, 254, 0.2);
}

/* My Sketches panel animation */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Tooltip improvements */
.group:hover .group-hover\:opacity-100 {
    z-index: 50;
}

.pointer-events-none {
    pointer-events: none;
}

/* Dialog animation */
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.3s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}
</style>