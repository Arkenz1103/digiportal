<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';
import Dialog from 'primevue/dialog';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

// Define emits to suppress Vue warnings
defineEmits(['navigate']);

const canvas = ref(null);
const ctx = ref(null);
const isDrawing = ref(false);
const currentColor = ref('#0000ff'); // Default to blue
const brushSize = ref(5);
const lastX = ref(0);
const lastY = ref(0);
const currentTool = ref('brush');
const fileInput = ref(null);
const mySketches = ref([]);
const showMySketches = ref(false);
const showSketchDialog = ref(false);
const currentSketch = ref(null);
const showPostToFeedModal = ref(false);
const selectedSketchForPost = ref(null);
const postCaption = ref('');
const showDeleteConfirmDialog = ref(false);
const attachedImage = ref(null);
const imagePosition = ref({ x: 0, y: 0 });
const imageSize = ref({ width: 0, height: 0 });
const imageScale = ref(1);
const isDraggingImage = ref(false);
const isResizingImage = ref(false);
const resizeCorner = ref(null);
const dragStartPos = ref({ x: 0, y: 0 });
const historyStack = ref([]);
const historyStep = ref(-1);
const isCropping = ref(false);
const cropStart = ref({ x: 0, y: 0 });
const cropEnd = ref({ x: 0, y: 0 });
const canvasDrawings = ref(null); // Store drawings separately from image

const tools = [
    { id: 'brush', name: 'Brush', icon: 'pi-pencil', description: 'Free drawing' },
    { id: 'eraser', name: 'Eraser', icon: 'pi-eraser', description: 'Erase parts of your drawing' },
    { id: 'hand', name: 'Hand', icon: 'pi-arrows-h', description: 'Drag and resize photo' },
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
    window.addEventListener('keydown', handleKeyboard);
    loadSketches();
    saveToHistory();
});

const initCanvas = () => {
    const canvasElement = canvas.value;
    if (!canvasElement) {
        console.warn('Canvas element not found');
        return;
    }
    
    ctx.value = canvasElement.getContext('2d');
    
    canvasElement.width = canvasElement.offsetWidth;
    canvasElement.height = canvasElement.offsetHeight;
    
    ctx.value.fillStyle = '#ffffff';
    ctx.value.fillRect(0, 0, canvasElement.width, canvasElement.height);
};

const startDrawing = (e) => {
    const [x, y] = getCoordinates(e);
    
    if (currentTool.value === 'hand' && attachedImage.value) {
        // Check if clicking on resize corner
        const corner = getResizeCorner(x, y);
        if (corner) {
            isResizingImage.value = true;
            resizeCorner.value = corner;
            dragStartPos.value = { 
                x, 
                y, 
                width: imageSize.value.width * imageScale.value, 
                height: imageSize.value.height * imageScale.value,
                startX: imagePosition.value.x,
                startY: imagePosition.value.y
            };
        } else {
            isDraggingImage.value = true;
            dragStartPos.value = { x: x - imagePosition.value.x, y: y - imagePosition.value.y };
        }
    } else {
        isDrawing.value = true;
        [lastX.value, lastY.value] = [x, y];
    }
};

const draw = (e) => {
    const [x, y] = getCoordinates(e);
    
    if (currentTool.value === 'hand' && attachedImage.value) {
        if (isResizingImage.value) {
            handleResize(x, y);
            return;
        } else if (isDraggingImage.value) {
            imagePosition.value = {
                x: x - dragStartPos.value.x,
                y: y - dragStartPos.value.y
            };
            redrawCanvas();
            return;
        }
    }
    
    if (!isDrawing.value) return;
    
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
    if (isDrawing.value) {
        // Save drawings layer after drawing
        saveDrawingsLayer();
        saveToHistory();
    }
    if (isResizingImage.value) {
        saveToHistory();
    }
    if (isDraggingImage.value) {
        saveToHistory();
    }
    isDrawing.value = false;
    isDraggingImage.value = false;
    isResizingImage.value = false;
    resizeCorner.value = null;
};

// Save the drawings layer (without the image)
const saveDrawingsLayer = () => {
    if (!attachedImage.value) return;
    
    // Create a new canvas for drawings
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.value.width;
    tempCanvas.height = canvas.value.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Copy the current canvas
    tempCtx.drawImage(canvas.value, 0, 0);
    
    // Remove the image area by clearing it
    const scaledWidth = imageSize.value.width * imageScale.value;
    const scaledHeight = imageSize.value.height * imageScale.value;
    tempCtx.clearRect(
        imagePosition.value.x - 1,
        imagePosition.value.y - 1,
        scaledWidth + 2,
        scaledHeight + 2
    );
    
    canvasDrawings.value = tempCanvas;
};

// Get resize corner if mouse is near corner
const getResizeCorner = (x, y) => {
    if (!attachedImage.value) return null;
    
    const scaledWidth = imageSize.value.width * imageScale.value;
    const scaledHeight = imageSize.value.height * imageScale.value;
    const cornerSize = 20;
    
    const corners = {
        'top-left': { x: imagePosition.value.x, y: imagePosition.value.y },
        'top-right': { x: imagePosition.value.x + scaledWidth, y: imagePosition.value.y },
        'bottom-left': { x: imagePosition.value.x, y: imagePosition.value.y + scaledHeight },
        'bottom-right': { x: imagePosition.value.x + scaledWidth, y: imagePosition.value.y + scaledHeight }
    };
    
    for (const [corner, pos] of Object.entries(corners)) {
        if (Math.abs(x - pos.x) < cornerSize && Math.abs(y - pos.y) < cornerSize) {
            return corner;
        }
    }
    
    return null;
};

// Handle image resize
const handleResize = (x, y) => {
    const dx = x - dragStartPos.value.x;
    const dy = y - dragStartPos.value.y;
    
    const aspectRatio = imageSize.value.width / imageSize.value.height;
    let newWidth = dragStartPos.value.width;
    let newHeight = dragStartPos.value.height;
    let newX = dragStartPos.value.startX;
    let newY = dragStartPos.value.startY;
    
    switch (resizeCorner.value) {
        case 'bottom-right':
            newWidth = dragStartPos.value.width + dx;
            newHeight = newWidth / aspectRatio;
            newX = dragStartPos.value.startX;
            newY = dragStartPos.value.startY;
            break;
        case 'bottom-left':
            newWidth = dragStartPos.value.width - dx;
            newHeight = newWidth / aspectRatio;
            newX = dragStartPos.value.startX + dx;
            newY = dragStartPos.value.startY;
            break;
        case 'top-right':
            newWidth = dragStartPos.value.width + dx;
            newHeight = newWidth / aspectRatio;
            newX = dragStartPos.value.startX;
            newY = dragStartPos.value.startY + dragStartPos.value.height - newHeight;
            break;
        case 'top-left':
            newWidth = dragStartPos.value.width - dx;
            newHeight = newWidth / aspectRatio;
            newX = dragStartPos.value.startX + dx;
            newY = dragStartPos.value.startY + dragStartPos.value.height - newHeight;
            break;
    }
    
    // Minimum size constraint
    if (newWidth < 50) {
        newWidth = 50;
        newHeight = newWidth / aspectRatio;
    }
    
    imagePosition.value.x = newX;
    imagePosition.value.y = newY;
    imageScale.value = newWidth / imageSize.value.width;
    redrawCanvas();
};

const redrawCanvas = () => {
    if (!attachedImage.value) return;
    
    // Clear canvas
    ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
    ctx.value.fillStyle = '#ffffff';
    ctx.value.fillRect(0, 0, canvas.value.width, canvas.value.height);
    
    // First, draw the saved drawings layer (if exists)
    if (canvasDrawings.value) {
        ctx.value.drawImage(canvasDrawings.value, 0, 0);
    }
    
    // Then draw the attached image on top at the new position with scale
    const scaledWidth = imageSize.value.width * imageScale.value;
    const scaledHeight = imageSize.value.height * imageScale.value;
    
    ctx.value.drawImage(
        attachedImage.value,
        imagePosition.value.x,
        imagePosition.value.y,
        scaledWidth,
        scaledHeight
    );
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

// Computed property for cursor style
const canvasCursor = computed(() => {
    if (currentTool.value === 'hand') {
        return isDraggingImage.value ? 'cursor-grabbing' : 'cursor-grab';
    } else if (currentTool.value === 'eraser') {
        return 'cursor-pointer';
    }
    return 'cursor-crosshair';
});

const saveDrawing = async () => {
    const dataURL = canvas.value.toDataURL();
    
    try {
        const response = await axios.post('/api/sketches/', {
            title: 'Sketch ' + new Date().toLocaleString(),
            image_data: dataURL
        });
        
        if (response.data) {
            // Add to local list
            mySketches.value.unshift({
                id: response.data.id,
                dataURL: response.data.image_data,
                date: new Date(response.data.created_at).toLocaleString()
            });
            
            showSuccess('Sketch saved to My Sketches!', 'Saved');
        }
    } catch (error) {
        console.error('Error saving sketch:', error);
        showError('Failed to save sketch. Please try again.', 'Save Failed');
    }
};

const loadSketches = async () => {
    try {
        const response = await axios.get('/api/sketches/');
        if (response.data) {
            mySketches.value = response.data.map(sketch => ({
                id: sketch.id,
                dataURL: sketch.image_data,
                date: new Date(sketch.created_at).toLocaleString()
            }));
        }
    } catch (error) {
        console.error('Error loading sketches:', error);
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

const deleteSketch = async (id, e) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this sketch?')) {
        try {
            await axios.delete(`/api/sketches/${id}/`);
            mySketches.value = mySketches.value.filter(sketch => sketch.id !== id);
        } catch (error) {
            console.error('Error deleting sketch:', error);
            showError('Failed to delete sketch. Please try again.', 'Delete Failed');
        }
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

// Open post to newsfeed modal
const openPostToFeedModal = () => {
    if (mySketches.value.length === 0) {
        showWarning('Please save a sketch first before posting to newsfeed!', 'No Sketch');
        return;
    }
    showPostToFeedModal.value = true;
};

// Select sketch for posting
const selectSketchForPost = (sketch) => {
    selectedSketchForPost.value = sketch;
};

// Show delete confirmation dialog
const showDeleteConfirmation = () => {
    if (!selectedSketchForPost.value) {
        showWarning('Please select a sketch to delete', 'No Selection');
        return;
    }
    showDeleteConfirmDialog.value = true;
};

// Delete selected sketch from post modal
const deleteSelectedSketch = async () => {
    try {
        const sketchId = selectedSketchForPost.value.id;
        
        // Delete from backend
        await axios.delete(`/api/sketches/${sketchId}/`);
        
        // Remove from local list
        mySketches.value = mySketches.value.filter(sketch => sketch.id !== sketchId);
        
        // Clear selection
        selectedSketchForPost.value = null;
        postCaption.value = '';
        
        // Close confirmation dialog
        showDeleteConfirmDialog.value = false;
        
        showSuccess('Sketch deleted successfully!', 'Deleted');
        
        // Close modal if no more sketches
        if (mySketches.value.length === 0) {
            showPostToFeedModal.value = false;
        }
    } catch (error) {
        console.error('Error deleting sketch:', error);
        showError('Failed to delete sketch. Please try again.', 'Delete Failed');
        showDeleteConfirmDialog.value = false;
    }
};

// Post sketch to newsfeed
const postToNewsfeed = async () => {
    if (!selectedSketchForPost.value) {
        showWarning('Please select a sketch to post', 'No Selection');
        return;
    }
    
    if (!postCaption.value.trim()) {
        showWarning('Please add a caption for your post', 'Caption Required');
        return;
    }
    
    try {
        // Submit sketch to API
        const response = await axios.post('/api/sketch/submit/', {
            caption: postCaption.value,
            file_path: selectedSketchForPost.value.dataURL,
            file_type: 'image'
        });
        
        if (response.data) {
            console.log('Sketch posted successfully:', response.data);
            showSuccess('It will appear in the newsfeed once approved by your teacher.', 'Submitted for Approval');
            
            // Reset and close modal
            showPostToFeedModal.value = false;
            selectedSketchForPost.value = null;
            postCaption.value = '';
        }
    } catch (error) {
        console.error('Error posting to newsfeed:', error);
        showError(error.response?.data?.error || error.message, 'Post Failed');
    }
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.type.match('image.*')) {
        showWarning('Please select an image file.', 'Invalid File');
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        const img = new Image();
        img.onload = () => {
            const hRatio = canvas.value.width / img.width;
            const vRatio = canvas.value.height / img.height;
            const ratio = Math.min(hRatio, vRatio);
            const centerShiftX = (canvas.value.width - img.width * ratio) / 2;
            const centerShiftY = (canvas.value.height - img.height * ratio) / 2;
            
            // Save current drawings before adding image
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.value.width;
            tempCanvas.height = canvas.value.height;
            const tempCtx = tempCanvas.getContext('2d');
            tempCtx.drawImage(canvas.value, 0, 0);
            canvasDrawings.value = tempCanvas;
            
            // Store the image and position for dragging
            attachedImage.value = img;
            imagePosition.value = { x: centerShiftX, y: centerShiftY };
            imageSize.value = { width: img.width * ratio, height: img.height * ratio };
            imageScale.value = 1;
            
            // Draw the image on top of existing drawings
            ctx.value.drawImage(
                img, 
                0, 0, img.width, img.height,
                centerShiftX, centerShiftY, 
                img.width * ratio, img.height * ratio
            );
            
            saveToHistory();
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
};

// Undo/Redo functionality
const saveToHistory = () => {
    const dataURL = canvas.value.toDataURL();
    historyStep.value++;
    historyStack.value = historyStack.value.slice(0, historyStep.value);
    historyStack.value.push(dataURL);
    if (historyStack.value.length > 50) {
        historyStack.value.shift();
        historyStep.value--;
    }
};

const undo = () => {
    if (historyStep.value > 0) {
        historyStep.value--;
        restoreFromHistory();
    }
};

const redo = () => {
    if (historyStep.value < historyStack.value.length - 1) {
        historyStep.value++;
        restoreFromHistory();
    }
};

const restoreFromHistory = () => {
    const img = new Image();
    img.onload = () => {
        ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
        ctx.value.drawImage(img, 0, 0);
    };
    img.src = historyStack.value[historyStep.value];
};

// Keyboard shortcuts
const handleKeyboard = (e) => {
    if (e.ctrlKey && e.key === 'z') {
        e.preventDefault();
        undo();
    } else if (e.ctrlKey && e.key === 'y') {
        e.preventDefault();
        redo();
    }
};

// Image zoom in/out
const zoomIn = () => {
    if (!attachedImage.value) return;
    imageScale.value = Math.min(imageScale.value + 0.1, 3);
    redrawCanvas();
    saveToHistory();
};

const zoomOut = () => {
    if (!attachedImage.value) return;
    imageScale.value = Math.max(imageScale.value - 0.1, 0.1);
    redrawCanvas();
    saveToHistory();
};

// Crop functionality
const startCrop = () => {
    if (!attachedImage.value) {
        showWarning('Please attach an image first!', 'No Image');
        return;
    }
    isCropping.value = true;
    currentTool.value = 'crop';
};

const applyCrop = () => {
    if (!isCropping.value) return;
    
    const x = Math.min(cropStart.value.x, cropEnd.value.x);
    const y = Math.min(cropStart.value.y, cropEnd.value.y);
    const width = Math.abs(cropEnd.value.x - cropStart.value.x);
    const height = Math.abs(cropEnd.value.y - cropStart.value.y);
    
    if (width > 10 && height > 10) {
        const imageData = ctx.value.getImageData(x, y, width, height);
        canvas.value.width = width;
        canvas.value.height = height;
        ctx.value.putImageData(imageData, 0, 0);
        
        attachedImage.value = null;
        saveToHistory();
    }
    
    isCropping.value = false;
    currentTool.value = 'brush';
};
</script>

<template>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-6 border border-indigo-100">
            <!-- Header -->
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
                <div>
                    <h1 class="text-2xl font-bold text-indigo-900">Sketch Pad</h1>
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
                    <button @click="openPostToFeedModal"
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 text-white bg-green-600 hover:bg-green-700 rounded-lg transition-all shadow-sm">
                        <i class="pi pi-send"></i>
                        <span>Post to Newsfeed</span>
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
                    <div class="mb-4 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl flex items-center justify-between gap-3 border-2 border-indigo-200 shadow-sm">
                        <div class="flex items-center gap-2">
                            <!-- Custom Color Picker (First) -->
                            <div class="flex flex-col items-center gap-1 group">
                                <div class="relative">
                                    <input type="color" 
                                           v-model="currentColor"
                                           class="w-8 h-8 cursor-pointer rounded-lg border-2 border-indigo-300 shadow-md hover:shadow-lg transition-all hover:scale-105"
                                           title="Custom Color">
                                    <div class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-indigo-600 rounded-full border border-white"></div>
                                </div>
                                <span class="text-[8px] text-indigo-700 font-semibold uppercase tracking-wide">Custom</span>
                            </div>
                            
                            <!-- Divider -->
                            <div class="w-px h-10 bg-gradient-to-b from-transparent via-indigo-300 to-transparent mx-1"></div>
                            
                            <!-- Preset Colors -->
                            <div v-for="color in colors" 
                                 :key="color.hex" 
                                 @click="currentColor = color.hex"
                                 :style="{ backgroundColor: color.hex }"
                                 :class="{ 
                                     'ring-2 ring-indigo-400 scale-105 shadow-lg': currentColor === color.hex,
                                     'border border-gray-300 shadow-inner': color.hex === '#ffffff',
                                     'border border-gray-700': color.hex === '#000000'
                                 }"
                                 class="w-7 h-7 rounded-lg cursor-pointer shadow-sm transition-all hover:scale-110 hover:shadow-md relative"
                                 :title="color.name">
                                <!-- Checkmark for selected color -->
                                <div v-if="currentColor === color.hex" 
                                     class="absolute inset-0 flex items-center justify-center">
                                    <i class="pi pi-check text-white text-[10px] drop-shadow-lg" 
                                       :class="{ 'text-gray-800': color.hex === '#ffffff' || color.hex === '#ffff00' }"></i>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Action Buttons -->
                        <div class="flex items-center gap-2 flex-wrap">
                            <!-- Undo Button -->
                            <button @click="undo" 
                                    :disabled="historyStep <= 0"
                                    :class="{ 'opacity-50 cursor-not-allowed': historyStep <= 0 }"
                                    class="p-2 text-[#0E1836] hover:bg-[#B8AAFF]/10 rounded-lg transition-colors"
                                    title="Undo (Ctrl+Z)">
                                <i class="pi pi-undo text-lg"></i>
                            </button>
                            
                            <!-- Redo Button -->
                            <button @click="redo" 
                                    :disabled="historyStep >= historyStack.length - 1"
                                    :class="{ 'opacity-50 cursor-not-allowed': historyStep >= historyStack.length - 1 }"
                                    class="p-2 text-[#0E1836] hover:bg-[#B8AAFF]/10 rounded-lg transition-colors"
                                    title="Redo (Ctrl+Y)">
                                <i class="pi pi-refresh text-lg"></i>
                            </button>
                            
                            <div class="w-px h-6 bg-[#B6CFFF]"></div>
                            
                            <!-- Attach Photo -->
                            <button @click="triggerFileInput" 
                                    class="px-3 py-1.5 text-[#0E1836] hover:bg-[#B8AAFF]/10 rounded-lg transition-colors flex items-center gap-1">
                                <i class="pi pi-image"></i>
                                <span>Attach Photo</span>
                            </button>
                        </div>
                        
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
                                :class="['w-full h-[600px] bg-white rounded-lg shadow-inner', canvasCursor]">
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

    <!-- Post to Newsfeed Modal -->
    <div v-if="showPostToFeedModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-indigo-100">
            <div class="px-6 py-4 border-b border-indigo-100 bg-indigo-50 flex justify-between items-center">
                <h3 class="text-lg font-semibold text-indigo-900">Post Sketch to Newsfeed</h3>
                <button @click="showPostToFeedModal = false" class="text-indigo-600 hover:bg-indigo-100 p-1.5 rounded-full transition-colors">
                    <i class="pi pi-times"></i>
                </button>
            </div>
            
            <div class="flex-1 overflow-y-auto p-6">
                <!-- Select Sketch Section -->
                <div class="mb-6">
                    <h4 class="text-md font-semibold text-indigo-900 mb-3">Select a Sketch</h4>
                    
                    <div v-if="mySketches.length === 0" class="text-center py-8 bg-indigo-50 rounded-lg">
                        <i class="pi pi-inbox text-3xl text-indigo-400 mb-2"></i>
                        <p class="text-indigo-600">No saved sketches. Save a sketch first!</p>
                    </div>
                    
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
                        <div v-for="sketch in mySketches" 
                             :key="sketch.id"
                             @click="selectSketchForPost(sketch)"
                             class="relative group cursor-pointer">
                            <img :src="sketch.dataURL" 
                                 class="w-full h-24 object-contain bg-gray-100 rounded-lg border-2 transition-all"
                                 :class="selectedSketchForPost?.id === sketch.id ? 'border-indigo-600 ring-2 ring-indigo-300' : 'border-gray-300 hover:border-indigo-400'">
                            <div v-if="selectedSketchForPost?.id === sketch.id" 
                                 class="absolute top-1 right-1 bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center">
                                <i class="pi pi-check text-xs"></i>
                            </div>
                            <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs p-1 px-2 rounded-b-lg truncate">
                                {{ sketch.date }}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Caption Section -->
                <div class="mb-4">
                    <label class="block text-md font-semibold text-indigo-900 mb-2">Add a Caption</label>
                    <textarea v-model="postCaption"
                              placeholder="Write something about your sketch..."
                              class="w-full px-4 py-3 border border-indigo-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                              rows="4"></textarea>
                </div>
                
                <!-- Preview Section -->
                <div v-if="selectedSketchForPost" class="bg-indigo-50 rounded-lg p-4">
                    <h4 class="text-sm font-semibold text-indigo-900 mb-2">Preview</h4>
                    <div class="bg-white rounded-lg p-3 border border-indigo-200">
                        <img :src="selectedSketchForPost.dataURL" 
                             class="w-full max-h-48 object-contain mb-2 rounded">
                        <p class="text-sm text-gray-700">{{ postCaption || 'No caption' }}</p>
                    </div>
                </div>
            </div>
            
            <div class="px-6 py-4 border-t border-indigo-100 bg-gray-50 flex justify-between items-center">
                <!-- Left side - Delete button -->
                <button 
                    @click="showDeleteConfirmation"
                    class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors flex items-center gap-2"
                    :disabled="!selectedSketchForPost"
                    :class="!selectedSketchForPost ? 'opacity-50 cursor-not-allowed' : ''">
                    <i class="pi pi-trash"></i>
                    <span>Delete</span>
                </button>
                
                <!-- Right side - Cancel and Post buttons -->
                <div class="flex gap-3">
                    <button @click="showPostToFeedModal = false" 
                            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
                        Cancel
                    </button>
                    <button @click="postToNewsfeed"
                            :disabled="!selectedSketchForPost || !postCaption.trim()"
                            :class="!selectedSketchForPost || !postCaption.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:bg-indigo-700'"
                            class="px-6 py-2 bg-indigo-600 text-white rounded-lg transition-colors flex items-center gap-2">
                        <i class="pi pi-send"></i>
                        <span>Post to Newsfeed</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <Dialog v-model:visible="showDeleteConfirmDialog" modal :style="{ width: '90vw', maxWidth: '450px' }" :dismissableMask="true">
      <template #header>
        <div class="flex items-center gap-3">
          <i class="pi pi-exclamation-triangle text-red-600 text-xl"></i>
          <h3 class="text-lg font-bold text-gray-800">Delete Sketch</h3>
        </div>
      </template>

      <div class="py-4">
        <p class="text-gray-700 mb-4">
          Are you sure you want to delete this sketch? This action cannot be undone.
        </p>
        <div v-if="selectedSketchForPost" class="bg-gray-50 rounded-lg p-3 border border-gray-200">
          <img :src="selectedSketchForPost.dataURL" 
               class="w-full max-h-32 object-contain mb-2 rounded">
          <p class="text-xs text-gray-500 text-center">{{ selectedSketchForPost.date }}</p>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-end gap-3">
          <button
            @click="showDeleteConfirmDialog = false"
            class="px-5 py-2.5 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors duration-200"
          >
            Cancel
          </button>
          <button
            @click="deleteSelectedSketch"
            class="px-5 py-2.5 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors duration-200 flex items-center gap-2"
          >
            <i class="pi pi-trash"></i>
            <span>Delete</span>
          </button>
        </div>
      </template>
    </Dialog>
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