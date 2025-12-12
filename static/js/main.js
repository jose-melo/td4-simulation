/**
 * Main Application Controller
 * Coordinates between API layer and Visualizer layer
 */

import BinPackingAPI from './api.js';
import BinPackingVisualizer from './visualizer.js';

class BinPackingApp {
    constructor() {
        this.api = new BinPackingAPI();
        this.visualizer = null;

        this.config = null;
        this.isRunning = false;
        this.autoPlay = false;
        this.speed = 1000;
        this.currentAlgorithm = 'ff';

        // Custom input state
        this.customCapacity = null;
        this.customItems = null;
        this.isCustomMode = false;

        // DOM elements
        this.elements = {};
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            // Get configuration from backend
            this.config = await this.api.getConfig();

            // Initialize visualizer
            this.visualizer = new BinPackingVisualizer(this.config.capacity);
            this.visualizer.init();
            this.visualizer.setItems(this.config.items);

            // Cache DOM elements
            this.cacheElements();

            // Setup event listeners
            this.setupEventListeners();

            // Display initial info
            this.displayInitialInfo();

            console.log('App initialized successfully', this.config);
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError('Failed to initialize application: ' + error.message);
        }
    }

    /**
     * Cache DOM element references
     */
    cacheElements() {
        this.elements = {
            startBtn: document.getElementById('startBtn'),
            stepBtn: document.getElementById('stepBtn'),
            autoBtn: document.getElementById('autoBtn'),
            resetBtn: document.getElementById('resetBtn'),
            algorithmSelect: document.getElementById('algorithmSelect'),
            speedRange: document.getElementById('speedRange'),
            speedValue: document.getElementById('speedValue'),
            // Custom input elements
            configModeRadios: document.getElementsByName('configMode'),
            customInputs: document.getElementById('customInputs'),
            capacityInput: document.getElementById('capacityInput'),
            itemsInput: document.getElementById('itemsInput'),
            validateBtn: document.getElementById('validateBtn'),
            validationMessage: document.getElementById('validationMessage'),
            itemsListTitle: document.getElementById('itemsListTitle'),
        };
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        this.elements.startBtn.addEventListener('click', () => this.start());
        this.elements.stepBtn.addEventListener('click', () => this.step());
        this.elements.autoBtn.addEventListener('click', () => this.toggleAutoPlay());
        this.elements.resetBtn.addEventListener('click', () => this.reset());

        this.elements.algorithmSelect.addEventListener('change', (e) => {
            this.currentAlgorithm = e.target.value;
            this.visualizer.updateAlgorithmName(e.target.value);
        });

        this.elements.speedRange.addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            this.elements.speedValue.textContent = (this.speed / 1000).toFixed(1) + 's';
        });

        // Config mode radio buttons
        this.elements.configModeRadios.forEach(radio => {
            radio.addEventListener('change', (e) => this.handleConfigModeChange(e));
        });

        // Validate button
        this.elements.validateBtn.addEventListener('click', () => this.validateCustomInput());

        // Allow Enter key in items input
        this.elements.itemsInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.validateCustomInput();
            }
        });
    }

    /**
     * Display initial information
     */
    displayInitialInfo() {
        const capacity = this.isCustomMode ? this.customCapacity : this.config.capacity;
        const items = this.isCustomMode ? this.customItems : this.config.items;
        const totalSize = items.reduce((sum, item) => sum + item, 0);
        const theoreticalMin = Math.ceil(totalSize / capacity);

        const info = `
            <strong>${this.isCustomMode ? 'Custom' : 'Demo'} Configuration:</strong><br>
            Capacity: ${capacity} |
            Items: ${items.length} |
            Total Size: ${totalSize} |
            Theoretical Minimum: ${theoreticalMin} bins
        `;
        this.visualizer.updateExplanation(info);
    }

    /**
     * Handle config mode change (Demo vs Custom)
     */
    handleConfigModeChange(e) {
        const isCustom = e.target.value === 'custom';
        this.elements.customInputs.style.display = isCustom ? 'block' : 'none';

        if (!isCustom) {
            // Reset to demo mode
            this.isCustomMode = false;
            this.customCapacity = null;
            this.customItems = null;
            this.elements.validationMessage.className = '';
            this.elements.validationMessage.style.display = 'none';

            // Update visualizer with demo data
            this.visualizer.setItems(this.config.items);
            this.visualizer.capacity = this.config.capacity;
            this.elements.itemsListTitle.textContent = `Items to Pack (Capacity: ${this.config.capacity})`;
            this.displayInitialInfo();
        }
    }

    /**
     * Validate custom user input
     */
    validateCustomInput() {
        const validationMsg = this.elements.validationMessage;
        validationMsg.className = '';
        validationMsg.style.display = 'none';

        // Get capacity
        const capacity = parseInt(this.elements.capacityInput.value);
        if (!capacity || capacity < 1 || capacity > 100) {
            this.showValidationError('Capacity must be between 1 and 100');
            return;
        }

        // Get items
        const itemsText = this.elements.itemsInput.value.trim();
        if (!itemsText) {
            this.showValidationError('Please enter items');
            return;
        }

        // Parse items (allow comma or space separation)
        const items = itemsText
            .split(/[\s,]+/)
            .map(s => s.trim())
            .filter(s => s.length > 0)
            .map(s => parseInt(s));

        // Validate items
        if (items.length === 0) {
            this.showValidationError('Please enter at least one item');
            return;
        }

        if (items.some(item => isNaN(item) || item < 1)) {
            this.showValidationError('All items must be positive integers');
            return;
        }

        if (items.some(item => item > capacity)) {
            this.showValidationError(`Some items are larger than bin capacity (${capacity})`);
            return;
        }

        // Validation successful!
        this.customCapacity = capacity;
        this.customItems = items;
        this.isCustomMode = true;

        // Update visualizer
        this.visualizer.setItems(items);
        this.visualizer.capacity = capacity;
        this.elements.itemsListTitle.textContent = `Items to Pack (Capacity: ${capacity})`;

        // Show success message
        this.showValidationSuccess(
            `✓ Valid input: ${items.length} items, capacity ${capacity}, ` +
            `total size ${items.reduce((sum, item) => sum + item, 0)}`
        );

        // Update explanation
        this.displayInitialInfo();
    }

    /**
     * Show validation error message
     */
    showValidationError(message) {
        const validationMsg = this.elements.validationMessage;
        validationMsg.textContent = '✗ ' + message;
        validationMsg.className = 'error';
        validationMsg.style.display = 'block';
    }

    /**
     * Show validation success message
     */
    showValidationSuccess(message) {
        const validationMsg = this.elements.validationMessage;
        validationMsg.textContent = message;
        validationMsg.className = 'success';
        validationMsg.style.display = 'block';
    }

    /**
     * Start the simulation
     */
    async start() {
        if (this.isRunning) return;

        // Check if using custom mode without validation
        if (this.isCustomMode && (!this.customCapacity || !this.customItems)) {
            this.showError('Please validate your custom input first');
            return;
        }

        try {
            this.isRunning = true;

            // Disable/enable buttons
            this.elements.startBtn.disabled = true;
            this.elements.stepBtn.disabled = false;
            this.elements.autoBtn.disabled = false;
            this.elements.algorithmSelect.disabled = true;

            // Disable config inputs during simulation
            this.elements.configModeRadios.forEach(radio => radio.disabled = true);
            this.elements.capacityInput.disabled = true;
            this.elements.itemsInput.disabled = true;
            this.elements.validateBtn.disabled = true;

            // Start simulation on backend with appropriate data
            const capacity = this.isCustomMode ? this.customCapacity : null;
            const items = this.isCustomMode ? this.customItems : null;

            const result = await this.api.startSimulation(this.currentAlgorithm, capacity, items);

            console.log('Simulation started:', result);

            const algoNames = {
                'ff': 'First Fit',
                'bf': 'Best Fit',
                'nf': 'Next Fit'
            };
            this.visualizer.updateExplanation(
                `<strong>${algoNames[this.currentAlgorithm]}</strong> algorithm ready. Click "Next Step" to begin!`
            );
            this.visualizer.hideSummary();

        } catch (error) {
            console.error('Start error:', error);
            this.showError('Failed to start simulation: ' + error.message);
            this.isRunning = false;
            this.elements.startBtn.disabled = false;
            this.enableConfigInputs();
        }
    }

    /**
     * Enable config inputs
     */
    enableConfigInputs() {
        this.elements.configModeRadios.forEach(radio => radio.disabled = false);
        this.elements.capacityInput.disabled = false;
        this.elements.itemsInput.disabled = false;
        this.elements.validateBtn.disabled = false;
    }

    /**
     * Execute one step
     */
    async step() {
        if (!this.isRunning) return;

        try {
            // Execute step on backend
            const result = await this.api.executeStep();

            if (result.is_complete) {
                await this.finish();
                return;
            }

            const stepResult = result.step_result;
            const state = result.state;

            // Update visualizer with current item
            this.visualizer.showCurrentItem(stepResult.item, stepResult.item_index);
            this.visualizer.setCurrentItemIndex(stepResult.item_index);

            // Show algorithm explanation
            const algoNames = {
                'ff': 'First Fit',
                'bf': 'Best Fit',
                'nf': 'Next Fit'
            };
            const algoName = algoNames[this.currentAlgorithm];
            this.visualizer.updateExplanation(`<strong>${algoName}:</strong> ${stepResult.explanation}`);

            // Animate bin checking
            if (stepResult.bins_checked && stepResult.bins_checked.length > 0) {
                await this.visualizer.animateBinChecking(stepResult.bins_checked, this.speed);
            }

            // Render bins
            this.visualizer.renderBins(state.bins);

            // Update statistics
            this.visualizer.updateStatistics(state.statistics);

            // Continue auto play if enabled
            if (this.autoPlay) {
                setTimeout(() => this.step(), this.speed);
            }

        } catch (error) {
            console.error('Step error:', error);
            this.showError('Error during step: ' + error.message);
            this.autoPlay = false;
            this.updateAutoPlayButton();
        }
    }

    /**
     * Toggle auto play
     */
    toggleAutoPlay() {
        this.autoPlay = !this.autoPlay;
        this.updateAutoPlayButton();

        if (this.autoPlay) {
            this.elements.stepBtn.disabled = true;
            this.step();
        } else {
            this.elements.stepBtn.disabled = false;
        }
    }

    /**
     * Update auto play button appearance
     */
    updateAutoPlayButton() {
        const btn = this.elements.autoBtn;

        if (this.autoPlay) {
            btn.textContent = 'Pause';
            btn.classList.remove('btn-secondary');
            btn.classList.add('btn-danger');
        } else {
            btn.textContent = 'Auto Play';
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-secondary');
        }
    }

    /**
     * Finish the simulation
     */
    async finish() {
        this.isRunning = false;
        this.autoPlay = false;

        this.elements.stepBtn.disabled = true;
        this.elements.autoBtn.disabled = true;

        this.visualizer.showCompletion();

        // Get final statistics
        try {
            const stats = await this.api.getStatistics();
            this.visualizer.showSummary(stats);
        } catch (error) {
            console.error('Error getting final statistics:', error);
        }

        this.updateAutoPlayButton();
    }

    /**
     * Reset the simulation
     */
    async reset() {
        try {
            // Stop auto play
            this.autoPlay = false;
            this.updateAutoPlayButton();

            // Reset backend
            await this.api.reset();

            // Reset state
            this.isRunning = false;

            // Reset buttons
            this.elements.startBtn.disabled = false;
            this.elements.stepBtn.disabled = true;
            this.elements.autoBtn.disabled = true;
            this.elements.algorithmSelect.disabled = false;

            // Enable config inputs
            this.enableConfigInputs();

            // Reset visualizer
            this.visualizer.reset();
            this.displayInitialInfo();

            console.log('Reset complete');

        } catch (error) {
            console.error('Reset error:', error);
            this.showError('Failed to reset: ' + error.message);
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        this.visualizer.showError(message);
        console.error(message);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const app = new BinPackingApp();
    app.init();

    // Make app available globally for debugging
    window.binPackingApp = app;
});
