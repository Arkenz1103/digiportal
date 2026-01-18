<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from '../../composables/useToast';
import Dialog from 'primevue/dialog';

// Initialize toast
const { showSuccess, showError, showInfo, showWarning } = useToast();

// Define emits to suppress Vue warnings
defineEmits(['navigate']);

// Archived view mode state
const isViewingArchived = ref(false);
const viewingArchivedSchoolYear = ref(null);

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
const selectedSketchesForPost = ref([]); // Changed to array for multiple selection
const postCaption = ref('');
const showDeleteConfirmDialog = ref(false);
const showClearCanvasDialog = ref(false);
const sketchToDelete = ref(null);
const isPostingToFeed = ref(false);
const showPostConfirmDialog = ref(false); // New confirmation dialog
const currentPreviewIndex = ref(0); // For navigating multiple selected sketches
// Multiple images support
const attachedImages = ref([]); // Array of { image, position, size, scale }
const selectedImageIndex = ref(-1); // Currently selected image for manipulation
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
    // Check if we're in archived view mode
    const savedArchivedView = localStorage.getItem('student_viewing_archived_school_year');
    if (savedArchivedView) {
        try {
            const archivedData = JSON.parse(savedArchivedView);
            isViewingArchived.value = true;
            viewingArchivedSchoolYear.value = archivedData;
            console.log('📂 Sketch: Restored archived view mode:', archivedData.name);
        } catch (e) {
            console.error('Error parsing student archived view data:', e);
            localStorage.removeItem('student_viewing_archived_school_year');
        }
    }
    
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
    // Prevent drawing in archived mode
    if (isViewingArchived.value) {
        showWarning('Drawing is disabled in archived school year', 'Read-only Mode');
        return;
    }
    
    const [x, y] = getCoordinates(e);
    
    if (currentTool.value === 'hand' && attachedImages.value.length > 0) {
        // Check if clicking on any image's resize corner or body
        for (let i = attachedImages.value.length - 1; i >= 0; i--) {
            const img = attachedImages.value[i];
            const corner = getResizeCornerForImage(x, y, img);
            if (corner) {
                selectedImageIndex.value = i;
                isResizingImage.value = true;
                resizeCorner.value = corner;
                dragStartPos.value = { 
                    x, 
                    y, 
                    width: img.size.width * img.scale, 
                    height: img.size.height * img.scale,
                    startX: img.position.x,
                    startY: img.position.y
                };
                return;
            }
            
            // Check if clicking inside image bounds
            const scaledWidth = img.size.width * img.scale;
            const scaledHeight = img.size.height * img.scale;
            if (x >= img.position.x && x <= img.position.x + scaledWidth &&
                y >= img.position.y && y <= img.position.y + scaledHeight) {
                selectedImageIndex.value = i;
                isDraggingImage.value = true;
                dragStartPos.value = { x: x - img.position.x, y: y - img.position.y };
                return;
            }
        }
        // Clicked outside all images, deselect
        selectedImageIndex.value = -1;
    }
    
    // Start drawing
    isDrawing.value = true;
    [lastX.value, lastY.value] = [x, y];
};

const draw = (e) => {
    const [x, y] = getCoordinates(e);
    
    if (currentTool.value === 'hand' && selectedImageIndex.value >= 0) {
        const img = attachedImages.value[selectedImageIndex.value];
        if (isResizingImage.value) {
            handleResize(x, y, img);
            return;
        } else if (isDraggingImage.value) {
            img.position = {
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
    if (isResizingImage.value || isDraggingImage.value) {
        saveToHistory();
    }
    isDrawing.value = false;
    isDraggingImage.value = false;
    isResizingImage.value = false;
    resizeCorner.value = null;
};

// Save the drawings layer (without the images)
const saveDrawingsLayer = () => {
    // Create a new canvas for drawings only
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.value.width;
    tempCanvas.height = canvas.value.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Copy the current canvas
    tempCtx.drawImage(canvas.value, 0, 0);
    
    // Clear all image areas to isolate drawings
    for (const img of attachedImages.value) {
        const scaledWidth = img.size.width * img.scale;
        const scaledHeight = img.size.height * img.scale;
        tempCtx.clearRect(
            img.position.x - 1,
            img.position.y - 1,
            scaledWidth + 2,
            scaledHeight + 2
        );
    }
    
    canvasDrawings.value = tempCanvas;
};

// Get resize corner for a specific image
const getResizeCornerForImage = (x, y, img) => {
    const scaledWidth = img.size.width * img.scale;
    const scaledHeight = img.size.height * img.scale;
    const cornerSize = 20;
    
    const corners = {
        'top-left': { x: img.position.x, y: img.position.y },
        'top-right': { x: img.position.x + scaledWidth, y: img.position.y },
        'bottom-left': { x: img.position.x, y: img.position.y + scaledHeight },
        'bottom-right': { x: img.position.x + scaledWidth, y: img.position.y + scaledHeight }
    };
    
    for (const [corner, pos] of Object.entries(corners)) {
        if (Math.abs(x - pos.x) < cornerSize && Math.abs(y - pos.y) < cornerSize) {
            return corner;
        }
    }
    
    return null;
};

// Handle image resize
const handleResize = (x, y, img) => {
    const dx = x - dragStartPos.value.x;
    const dy = y - dragStartPos.value.y;
    
    const aspectRatio = img.size.width / img.size.height;
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
    
    img.position.x = newX;
    img.position.y = newY;
    img.scale = newWidth / img.size.width;
    redrawCanvas();
};

const redrawCanvas = () => {
    // Clear canvas
    ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);
    ctx.value.fillStyle = '#ffffff';
    ctx.value.fillRect(0, 0, canvas.value.width, canvas.value.height);
    
    // First, draw the saved drawings layer (if exists)
    if (canvasDrawings.value) {
        ctx.value.drawImage(canvasDrawings.value, 0, 0);
    }
    
    // Then draw all attached images
    for (let i = 0; i < attachedImages.value.length; i++) {
        const img = attachedImages.value[i];
        const scaledWidth = img.size.width * img.scale;
        const scaledHeight = img.size.height * img.scale;
        
        ctx.value.drawImage(
            img.image,
            img.position.x,
            img.position.y,
            scaledWidth,
            scaledHeight
        );
        
        // Draw resize handles for selected image when hand tool is active
        if (currentTool.value === 'hand' && i === selectedImageIndex.value) {
            drawResizeHandles(img);
        }
    }
};

// Draw resize handles at corners of selected image
const drawResizeHandles = (img) => {
    const scaledWidth = img.size.width * img.scale;
    const scaledHeight = img.size.height * img.scale;
    const handleSize = 12;
    
    // Draw border around selected image
    ctx.value.strokeStyle = '#4F46E5';
    ctx.value.lineWidth = 2;
    ctx.value.setLineDash([5, 5]);
    ctx.value.strokeRect(img.position.x, img.position.y, scaledWidth, scaledHeight);
    ctx.value.setLineDash([]);
    
    // Corner positions
    const corners = [
        { x: img.position.x, y: img.position.y }, // top-left
        { x: img.position.x + scaledWidth, y: img.position.y }, // top-right
        { x: img.position.x, y: img.position.y + scaledHeight }, // bottom-left
        { x: img.position.x + scaledWidth, y: img.position.y + scaledHeight } // bottom-right
    ];
    
    // Draw corner handles
    for (const corner of corners) {
        // White fill
        ctx.value.fillStyle = '#ffffff';
        ctx.value.fillRect(
            corner.x - handleSize / 2,
            corner.y - handleSize / 2,
            handleSize,
            handleSize
        );
        // Indigo border
        ctx.value.strokeStyle = '#4F46E5';
        ctx.value.lineWidth = 2;
        ctx.value.strokeRect(
            corner.x - handleSize / 2,
            corner.y - handleSize / 2,
            handleSize,
            handleSize
        );
    }
};

const clearCanvas = () => {
    showClearCanvasDialog.value = true;
};

const confirmClearCanvas = () => {
    const canvasElement = canvas.value;
    ctx.value.fillStyle = '#ffffff';
    ctx.value.fillRect(0, 0, canvasElement.width, canvasElement.height);
    // Clear all attached images
    attachedImages.value = [];
    selectedImageIndex.value = -1;
    canvasDrawings.value = null;
    showClearCanvasDialog.value = false;
    showInfo('Canvas cleared', 'Cleared');
};

const setTool = (toolId) => {
    currentTool.value = toolId;
    if (toolId === 'eraser') {
        brushSize.value = 20;
    } else {
        brushSize.value = 5;
    }
    // Redraw canvas to show/hide resize handles
    if (attachedImages.value.length > 0) {
        redrawCanvas();
    }
};

// Computed property for cursor style
const canvasCursor = computed(() => {
    if (currentTool.value === 'hand') {
        if (isResizingImage.value) return 'cursor-nwse-resize';
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

const deleteSketch = (id, e) => {
    e.stopPropagation();
    sketchToDelete.value = id;
    showDeleteConfirmDialog.value = true;
};

const confirmDeleteSketch = async () => {
    try {
        await axios.delete(`/api/sketches/${sketchToDelete.value}/`);
        mySketches.value = mySketches.value.filter(sketch => sketch.id !== sketchToDelete.value);
        showDeleteConfirmDialog.value = false;
        sketchToDelete.value = null;
        showSuccess('Sketch deleted successfully', 'Deleted');
    } catch (error) {
        console.error('Error deleting sketch:', error);
        showError('Failed to delete sketch. Please try again.', 'Delete Failed');
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
    selectedSketchesForPost.value = [];
    currentPreviewIndex.value = 0;
    showPostToFeedModal.value = true;
};

// Toggle sketch selection for posting (multiple selection)
const toggleSketchSelection = (sketch) => {
    const index = selectedSketchesForPost.value.findIndex(s => s.id === sketch.id);
    if (index === -1) {
        selectedSketchesForPost.value.push(sketch);
    } else {
        selectedSketchesForPost.value.splice(index, 1);
    }
    // Reset preview index if needed
    if (currentPreviewIndex.value >= selectedSketchesForPost.value.length) {
        currentPreviewIndex.value = Math.max(0, selectedSketchesForPost.value.length - 1);
    }
};

// Check if sketch is selected
const isSketchSelected = (sketch) => {
    return selectedSketchesForPost.value.some(s => s.id === sketch.id);
};

// Navigate preview
const prevPreview = () => {
    if (currentPreviewIndex.value > 0) {
        currentPreviewIndex.value--;
    }
};

const nextPreview = () => {
    if (currentPreviewIndex.value < selectedSketchesForPost.value.length - 1) {
        currentPreviewIndex.value++;
    }
};

// Show post confirmation dialog
const showPostConfirmation = () => {
    if (selectedSketchesForPost.value.length === 0) {
        showWarning('Please select at least one sketch to post', 'No Selection');
        return;
    }
    showPostConfirmDialog.value = true;
};

// Post sketch to newsfeed
const postToNewsfeed = async () => {
    if (selectedSketchesForPost.value.length === 0) {
        showWarning('Please select at least one sketch to post', 'No Selection');
        return;
    }
    
    // Prevent double submission
    if (isPostingToFeed.value) {
        console.log('Already posting, please wait...');
        return;
    }
    
    try {
        isPostingToFeed.value = true;
        showPostConfirmDialog.value = false;
        
        // Submit all selected sketches
        const sketchData = selectedSketchesForPost.value.map(sketch => sketch.dataURL);
        
        const response = await axios.post('/api/sketch/submit/', {
            caption: postCaption.value.trim() || '',
            file_path: sketchData[0], // Primary sketch
            file_type: 'image',
            additional_files: sketchData.slice(1) // Additional sketches if any
        });
        
        if (response.data) {
            console.log('Sketch posted successfully:', response.data);
            showSuccess('It will appear in the newsfeed once approved by your teacher.', 'Submitted for Approval');
            
            // Reset and close modal
            showPostToFeedModal.value = false;
            selectedSketchesForPost.value = [];
            postCaption.value = '';
            currentPreviewIndex.value = 0;
        }
    } catch (error) {
        console.error('Error posting to newsfeed:', error);
        showError(error.response?.data?.error || error.message, 'Post Failed');
    } finally {
        isPostingToFeed.value = false;
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
            // Save current canvas state as drawings before adding new image
            if (attachedImages.value.length === 0) {
                // First image - save existing drawings
                const tempCanvas = document.createElement('canvas');
                tempCanvas.width = canvas.value.width;
                tempCanvas.height = canvas.value.height;
                const tempCtx = tempCanvas.getContext('2d');
                tempCtx.drawImage(canvas.value, 0, 0);
                canvasDrawings.value = tempCanvas;
            }
            
            const hRatio = canvas.value.width / img.width;
            const vRatio = canvas.value.height / img.height;
            const ratio = Math.min(hRatio, vRatio) * 0.5; // Start at 50% to fit multiple images
            const centerShiftX = (canvas.value.width - img.width * ratio) / 2;
            const centerShiftY = (canvas.value.height - img.height * ratio) / 2;
            
            // Add new image to array
            const newImage = {
                image: img,
                position: { x: centerShiftX + (attachedImages.value.length * 20), y: centerShiftY + (attachedImages.value.length * 20) },
                size: { width: img.width * ratio, height: img.height * ratio },
                scale: 1
            };
            
            attachedImages.value.push(newImage);
            selectedImageIndex.value = attachedImages.value.length - 1;
            
            // Redraw canvas with all images
            redrawCanvas();
            
            saveToHistory();
            showSuccess(`Image ${attachedImages.value.length} attached! Use Hand tool to move/resize.`, 'Image Added');
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
    
    // Reset file input to allow selecting same file again
    e.target.value = '';
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
    if (selectedImageIndex.value < 0 || attachedImages.value.length === 0) return;
    const img = attachedImages.value[selectedImageIndex.value];
    img.scale = Math.min(img.scale + 0.1, 3);
    redrawCanvas();
    saveToHistory();
};

const zoomOut = () => {
    if (selectedImageIndex.value < 0 || attachedImages.value.length === 0) return;
    const img = attachedImages.value[selectedImageIndex.value];
    img.scale = Math.max(img.scale - 0.1, 0.1);
    redrawCanvas();
    saveToHistory();
};

// Crop functionality
const startCrop = () => {
    if (attachedImages.value.length === 0) {
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
        
        attachedImages.value = [];
        selectedImageIndex.value = -1;
        saveToHistory();
    }
    
    isCropping.value = false;
    currentTool.value = 'brush';
};

// Delete selected image
const deleteSelectedImage = () => {
    if (selectedImageIndex.value >= 0 && attachedImages.value.length > 0) {
        attachedImages.value.splice(selectedImageIndex.value, 1);
        selectedImageIndex.value = attachedImages.value.length > 0 ? attachedImages.value.length - 1 : -1;
        redrawCanvas();
        saveToHistory();
        showInfo('Image removed', 'Deleted');
    }
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
                    <button @click="isViewingArchived ? null : clearCanvas" 
                            :disabled="isViewingArchived"
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg transition-all border"
                            :class="isViewingArchived ? 'text-gray-400 bg-gray-100 border-gray-200 cursor-not-allowed' : 'text-indigo-700 hover:bg-indigo-50 border-indigo-200 hover:border-indigo-300'">
                        <i class="pi pi-trash"></i>
                        <span>Clear</span>
                    </button>
                    <button @click="isViewingArchived ? null : saveDrawing" 
                            :disabled="isViewingArchived"
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg transition-all shadow-sm"
                            :class="isViewingArchived ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'bg-indigo-600 text-white hover:bg-indigo-700'">
                        <i class="pi pi-download"></i>
                        <span>Save</span>
                    </button>
                    <button @click="isViewingArchived ? null : openPostToFeedModal"
                            :disabled="isViewingArchived"
                            class="flex-1 sm:flex-none flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg transition-all shadow-sm"
                            :class="isViewingArchived ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'text-white bg-green-600 hover:bg-green-700'">
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
                                @click="isViewingArchived ? null : setTool(tool.id)"
                                :disabled="isViewingArchived"
                                class="p-3 rounded-lg transition-all relative group"
                                :class="[
                                    isViewingArchived ? 'cursor-not-allowed opacity-50' : 'hover:bg-white',
                                    { 'bg-white shadow-sm border border-indigo-200': currentTool === tool.id && !isViewingArchived }
                                ]">
                            <i :class="['pi', tool.icon, 'text-indigo-700', { 'text-indigo-600': currentTool === tool.id }]"></i>
                            
                            <!-- Tooltip - positioned to the right with higher z-index -->
                            <div v-if="!isViewingArchived" class="absolute left-full top-1/2 ml-3 px-3 py-1.5 bg-indigo-700 text-white text-xs rounded-lg 
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
                            <button @click="isViewingArchived ? null : triggerFileInput" 
                                    :disabled="isViewingArchived"
                                    class="px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1"
                                    :class="isViewingArchived ? 'text-gray-400 cursor-not-allowed' : 'text-[#0E1836] hover:bg-[#B8AAFF]/10'">
                                <i class="pi pi-image"></i>
                                <span>Attach Photo</span>
                                <span v-if="attachedImages.length > 0" class="ml-1 px-1.5 py-0.5 bg-indigo-600 text-white text-xs rounded-full">
                                    {{ attachedImages.length }}
                                </span>
                            </button>
                            
                            <!-- Delete Selected Image -->
                            <button v-if="selectedImageIndex >= 0 && attachedImages.length > 0"
                                    @click="deleteSelectedImage" 
                                    class="px-3 py-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors flex items-center gap-1"
                                    title="Delete selected image">
                                <i class="pi pi-trash"></i>
                                <span>Remove Image</span>
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
                    <div class="flex items-center justify-between mb-3">
                        <h4 class="text-md font-semibold text-indigo-900 truncate">Select Sketches</h4>
                        <span v-if="selectedSketchesForPost.length > 0" class="text-sm text-indigo-600 font-medium">
                            {{ selectedSketchesForPost.length }} selected
                        </span>
                    </div>
                    
                    <div v-if="mySketches.length === 0" class="text-center py-8 bg-indigo-50 rounded-lg">
                        <i class="pi pi-inbox text-3xl text-indigo-400 mb-2"></i>
                        <p class="text-indigo-600">No saved sketches. Save a sketch first!</p>
                    </div>
                    
                    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3 max-h-48 overflow-y-auto p-1">
                        <div v-for="sketch in mySketches" 
                             :key="sketch.id"
                             @click="toggleSketchSelection(sketch)"
                             class="relative group cursor-pointer">
                            <img :src="sketch.dataURL" 
                                 class="w-full h-24 object-contain bg-gray-100 rounded-lg border-2 transition-all"
                                 :class="isSketchSelected(sketch) ? 'border-indigo-600 ring-2 ring-indigo-300' : 'border-gray-300 hover:border-indigo-400'">
                            <div v-if="isSketchSelected(sketch)" 
                                 class="absolute top-1 right-1 bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center">
                                <i class="pi pi-check text-xs"></i>
                            </div>
                            <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-[10px] p-1 px-2 rounded-b-lg truncate">
                                {{ sketch.date }}
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Caption Section -->
                <div class="mb-4">
                    <label class="block text-md font-semibold text-indigo-900 mb-2">
                        Add a Caption <span class="text-sm font-normal text-gray-500">(Optional)</span>
                    </label>
                    <textarea v-model="postCaption"
                              placeholder="Write something about your sketch... (optional)"
                              class="w-full px-4 py-3 border border-indigo-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                              rows="3"></textarea>
                </div>
                
                <!-- Preview Section -->
                <div v-if="selectedSketchesForPost.length > 0" class="bg-indigo-50 rounded-lg p-4">
                    <h4 class="text-sm font-semibold text-indigo-900 mb-2">Preview</h4>
                    <div class="bg-white rounded-lg p-3 border border-indigo-200 relative">
                        <!-- Navigation arrows for multiple sketches -->
                        <div v-if="selectedSketchesForPost.length > 1" class="flex items-center justify-center gap-4 mb-2">
                            <button @click="prevPreview" 
                                    :disabled="currentPreviewIndex === 0"
                                    class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center transition-all hover:bg-indigo-200 disabled:opacity-30 disabled:cursor-not-allowed">
                                <i class="pi pi-chevron-left text-indigo-600"></i>
                            </button>
                            <span class="text-sm text-indigo-700 font-medium">
                                {{ currentPreviewIndex + 1 }} / {{ selectedSketchesForPost.length }}
                            </span>
                            <button @click="nextPreview" 
                                    :disabled="currentPreviewIndex >= selectedSketchesForPost.length - 1"
                                    class="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center transition-all hover:bg-indigo-200 disabled:opacity-30 disabled:cursor-not-allowed">
                                <i class="pi pi-chevron-right text-indigo-600"></i>
                            </button>
                        </div>
                        <img :src="selectedSketchesForPost[currentPreviewIndex]?.dataURL" 
                             class="w-full max-h-48 object-contain mb-2 rounded">
                        <p v-if="postCaption.trim()" class="text-sm text-gray-700">{{ postCaption.trim() }}</p>
                    </div>
                </div>
            </div>
            
            <div class="px-6 py-4 border-t border-indigo-100 bg-gray-50 flex justify-end items-center gap-3">
                <button @click="showPostToFeedModal = false" 
                        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
                    Cancel
                </button>
                <button @click="showPostConfirmation"
                        :disabled="selectedSketchesForPost.length === 0 || isPostingToFeed"
                        :class="(selectedSketchesForPost.length === 0 || isPostingToFeed) ? 'opacity-50 cursor-not-allowed' : 'hover:bg-indigo-700'"
                        class="px-6 py-2 bg-indigo-600 text-white rounded-lg transition-colors flex items-center gap-2">
                    <i class="pi" :class="isPostingToFeed ? 'pi-spin pi-spinner' : 'pi-send'"></i>
                    <span>{{ isPostingToFeed ? 'Posting...' : 'Post to Newsfeed' }}</span>
                </button>
            </div>
        </div>
    </div>

    <!-- Post Confirmation Dialog -->
    <Dialog v-model:visible="showPostConfirmDialog" modal header="Confirm Post" :style="{ width: '420px', maxWidth: '90vw' }" :contentStyle="{ padding: '0', overflow: 'visible' }" :dismissableMask="true">
        <div class="p-4">
            <div class="mb-4 text-center">
                <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-3">
                    <i class="pi pi-send text-2xl text-indigo-600"></i>
                </div>
                <h3 class="text-base font-semibold text-gray-900 mb-1">Post to Newsfeed?</h3>
                <p class="text-xs text-gray-600">
                    You are about to submit {{ selectedSketchesForPost.length }} sketch{{ selectedSketchesForPost.length > 1 ? 'es' : '' }} for approval.
                </p>
            </div>

            <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-3">
                <div class="flex items-start gap-2">
                    <i class="pi pi-info-circle text-indigo-600 text-sm mt-0.5"></i>
                    <div class="text-xs text-indigo-800">
                        <p class="font-medium mb-1">What happens next:</p>
                        <ul class="list-disc list-inside space-y-0.5 text-indigo-700">
                            <li>Your sketch will be sent for teacher approval</li>
                            <li>Once approved, it will appear in the newsfeed</li>
                            <li>You will be notified of the result</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <template #footer>
            <div class="flex justify-end gap-2 px-4 py-3 border-t">
                <button @click="showPostConfirmDialog = false" 
                        class="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
                    Cancel
                </button>
                <button @click="postToNewsfeed"
                        :disabled="isPostingToFeed"
                        class="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2">
                    <i class="pi" :class="isPostingToFeed ? 'pi-spin pi-spinner' : 'pi-check'"></i>
                    <span>{{ isPostingToFeed ? 'Posting...' : 'Yes, Post' }}</span>
                </button>
            </div>
        </template>
    </Dialog>

    <!-- Clear Canvas Confirmation Dialog -->
    <Dialog v-model:visible="showClearCanvasDialog" 
            modal 
            header="Clear Canvas" 
            :style="{ width: '90%', maxWidth: '28rem' }">
      <div class="space-y-4">
        <div class="flex items-start gap-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div class="flex-shrink-0">
            <i class="pi pi-exclamation-triangle text-2xl text-yellow-600"></i>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">Clear Canvas?</h3>
            <p class="mt-1 text-gray-600">
              Are you sure you want to clear the canvas? This will erase all your current work. This action cannot be undone.
            </p>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <button @click="showClearCanvasDialog = false"
            class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Cancel
          </button>
          <button @click="confirmClearCanvas"
            class="px-4 py-2 text-white bg-yellow-600 rounded-lg hover:bg-yellow-700 transition-colors flex items-center gap-2">
            <i class="pi pi-trash"></i>
            Clear Canvas
          </button>
        </div>
      </template>
    </Dialog>

    <!-- Delete Sketch Confirmation Dialog -->
    <Dialog v-model:visible="showDeleteConfirmDialog" 
            modal 
            header="Delete Sketch" 
            :style="{ width: '90%', maxWidth: '28rem' }">
      <div class="space-y-4">
        <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex-shrink-0">
            <i class="pi pi-exclamation-triangle text-2xl text-red-600"></i>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">Delete Sketch Permanently?</h3>
            <p class="mt-1 text-gray-600">
              Are you sure you want to delete this sketch? This action cannot be undone.
            </p>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteConfirmDialog = false; sketchToDelete = null;"
            class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Cancel
          </button>
          <button @click="confirmDeleteSketch"
            class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2">
            <i class="pi pi-trash"></i>
            Delete Sketch
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