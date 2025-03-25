<script setup>
import { ref, onMounted } from 'vue';
import { Head } from '@inertiajs/vue3';

const canvas = ref(null);
const ctx = ref(null);
const isDrawing = ref(false);
const currentColor = ref('#000000');
const brushSize = ref(5);
const lastX = ref(0);
const lastY = ref(0);
const currentTool = ref('brush');

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
    { size: 2, name: 'Extra Small' },    // Smallest dot
    { size: 4, name: 'Small' },          // Second smallest
    { size: 8, name: 'Medium' },         // Medium dot
    { size: 16, name: 'Large' },         // Largest dot
];

onMounted(() => {
    initCanvas();
    window.addEventListener('resize', initCanvas);
});

const initCanvas = () => {
    const canvasElement = canvas.value;
    ctx.value = canvasElement.getContext('2d');
    
    // Set canvas size
    canvasElement.width = canvasElement.offsetWidth;
    canvasElement.height = canvasElement.offsetHeight;
    
    // Set initial canvas background
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
    ctx.value.strokeStyle = currentColor.value;
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
        currentColor.value = '#ffffff';
        brushSize.value = 20;
    } else {
        currentColor.value = '#000000';
        brushSize.value = 5;
    }
};

const saveDrawing = () => {
    const link = document.createElement('a');
    link.download = `sketch-${new Date().toISOString().slice(0, 10)}.png`;
    link.href = canvas.value.toDataURL();
    link.click();
};
</script>

<template>
    <Head title="Sketch Pad" />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-xl shadow-lg p-6">
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Sketch Pad</h1>
                </div>
                <div class="flex items-center gap-3">
                    <button @click="clearCanvas" 
                            class="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                        <i class="pi pi-trash mr-2"></i>
                        Clear
                    </button>
                    <button @click="saveDrawing" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        <i class="pi pi-download mr-2"></i>
                        Save
                    </button>
                </div>
            </div>

            <div class="flex gap-6">
                <!-- Left Toolbar -->
                <div class="w-20 flex flex-col gap-4">
                    <!-- Tools -->
                    <div class="bg-gray-50 rounded-xl p-2 flex flex-col gap-2">
                        <button v-for="tool in tools" 
                                :key="tool.id"
                                @click="setTool(tool.id)"
                                class="p-3 rounded-lg hover:bg-white transition-all relative group"
                                :class="{ 'bg-white shadow-sm': currentTool === tool.id }">
                            <i :class="['pi', tool.icon, 'text-gray-700']"></i>
                            
                            <!-- Tooltip -->
                            <div class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded 
                                        whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
                                {{ tool.name }}
                            </div>
                        </button>
                    </div>

                    <!-- Brush Sizes -->
                    <div class="bg-gray-50 rounded-xl p-2 flex flex-col gap-3">
                        <button v-for="size in brushSizes"
                                :key="size.size"
                                @click="brushSize = size.size"
                                class="p-3 rounded-lg hover:bg-white transition-all relative group"
                                :class="{ 'bg-white shadow-sm': brushSize === size.size }">
                            <div class="w-full flex items-center justify-center">
                                <div class="rounded-full bg-gray-800"
                                     :style="{ 
                                         width: size.size + 'px', 
                                         height: size.size + 'px',
                                         opacity: '0.9'
                                     }">
                                </div>
                            </div>
                            
                            <!-- Tooltip -->
                            <div class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded 
                                        whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
                                {{ size.name }}
                            </div>
                        </button>
                    </div>
                </div>

                <!-- Canvas Area -->
                <div class="flex-1">
                    <!-- Color Palette -->
                    <div class="mb-4 p-3 bg-gray-50 rounded-xl flex items-center gap-2 flex-wrap">
                        <div v-for="color in colors" 
                             :key="color.hex" 
                             @click="currentColor = color.hex"
                             :style="{ backgroundColor: color.hex }"
                             :class="{ 
                                 'ring-2 ring-offset-2 ring-blue-500': currentColor === color.hex,
                                 'border border-gray-300': color.hex === '#ffffff'
                             }"
                             class="w-8 h-8 rounded-lg cursor-pointer shadow-sm transition-transform hover:scale-110"
                             :title="color.name">
                        </div>
                        <input type="color" 
                               v-model="currentColor"
                               class="w-8 h-8 cursor-pointer">
                    </div>

                    <!-- Canvas -->
                    <div class="border border-gray-200 rounded-xl overflow-hidden bg-gray-50 p-2">
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
</template>

<style scoped>
canvas {
    touch-action: none;
}

/* Custom color picker styling */
input[type="color"] {
    -webkit-appearance: none;
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
</style> 