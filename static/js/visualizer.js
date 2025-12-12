/**
 * Visualizer Module - Handles all UI rendering and animations
 * Separated from business logic for clean architecture
 */

class BinPackingVisualizer {
    constructor(capacity) {
        this.capacity = capacity;
        this.items = [];
        this.currentItemIndex = -1;

        // DOM elements (will be set by init)
        this.elements = {};
    }

    /**
     * Initialize DOM element references
     */
    init() {
        this.elements = {
            currentItemDisplay: document.getElementById('currentItemDisplay'),
            explanation: document.getElementById('explanation'),
            itemsList: document.getElementById('itemsList'),
            binsContainer: document.getElementById('binsContainer'),
            itemsProcessed: document.getElementById('itemsProcessed'),
            binsUsed: document.getElementById('binsUsed'),
            efficiency: document.getElementById('efficiency'),
            currentAlgo: document.getElementById('currentAlgo'),
            summary: document.getElementById('summary'),
            summaryDetails: document.getElementById('summaryDetails'),
        };
    }

    /**
     * Set items for visualization
     */
    setItems(items) {
        this.items = items;
        this.renderItemsList();
    }

    /**
     * Set current item index
     */
    setCurrentItemIndex(index) {
        this.currentItemIndex = index;
        this.renderItemsList();
    }

    /**
     * Update algorithm name display
     */
    updateAlgorithmName(algorithmType) {
        const names = {
            'ff': 'First Fit',
            'bf': 'Best Fit',
            'nf': 'Next Fit'
        };
        this.elements.currentAlgo.textContent = names[algorithmType] || algorithmType;
    }

    /**
     * Show current item being placed
     */
    showCurrentItem(item, itemIndex) {
        this.elements.currentItemDisplay.innerHTML =
            `<div class="current-item-box">Placing Item #${itemIndex + 1}: Size ${item}</div>`;
    }

    /**
     * Update explanation text
     */
    updateExplanation(text) {
        this.elements.explanation.innerHTML = text;
    }

    /**
     * Render items list with status
     */
    renderItemsList() {
        this.elements.itemsList.innerHTML = this.items.map((item, idx) => {
            let className = 'item-chip';
            if (idx < this.currentItemIndex) className += ' processed';
            if (idx === this.currentItemIndex) className += ' current';
            return `<span class="${className}">${item}</span>`;
        }).join('');
    }

    /**
     * Render bins visualization
     */
    renderBins(bins) {
        const container = this.elements.binsContainer;

        if (!bins || bins.length === 0) {
            container.innerHTML = '<p style="color: #6c757d; font-size: 1.2em;">No bins created yet</p>';
            return;
        }

        container.innerHTML = bins.map((bin, idx) => {
            const items = bin.items || bin;
            const capacity = Array.isArray(items) ? items.reduce((sum, val) => sum + val, 0) : 0;
            const percentage = (capacity / this.capacity) * 100;

            let capacityClass = '';
            if (percentage === 100) capacityClass = 'capacity-full';
            else if (percentage >= 80) capacityClass = 'capacity-high';

            const itemsHTML = items.map(item => {
                const height = (item / this.capacity) * 100;
                return `<div class="bin-item" style="height: ${height}%">${item}</div>`;
            }).join('');

            return `
                <div class="bin" data-bin-index="${idx}">
                    <div class="bin-label">Bin #${idx + 1}</div>
                    <div class="bin-content">${itemsHTML}</div>
                    <div class="bin-capacity ${capacityClass}">${capacity}/${this.capacity}</div>
                </div>
            `;
        }).join('');
    }

    /**
     * Highlight a bin with animation
     */
    async highlightBin(binIndex, status, duration = 500) {
        const bins = document.querySelectorAll('.bin');
        const bin = bins[binIndex];

        if (!bin) return;

        // Remove previous classes
        bin.classList.remove('checking', 'selected', 'rejected');

        // Add new class
        bin.classList.add(status);

        // Wait for animation
        await this.sleep(duration);

        // Keep 'selected' status, remove others
        if (status !== 'selected') {
            bin.classList.remove(status);
        }
    }

    /**
     * Animate bin checking sequence
     */
    async animateBinChecking(binsChecked, speed) {
        for (const check of binsChecked) {
            const status = this.mapCheckStatus(check.status);
            await this.highlightBin(check.bin_index, status, speed / 2);
        }
    }

    /**
     * Map API check status to CSS class
     */
    mapCheckStatus(status) {
        const mapping = {
            'checking': 'checking',
            'selected': 'selected',
            'rejected': 'rejected',
            'best_so_far': 'checking',
            'not_best': 'rejected'
        };
        return mapping[status] || 'checking';
    }

    /**
     * Update statistics display
     */
    updateStatistics(stats) {
        this.elements.itemsProcessed.textContent =
            `${stats.items_processed} / ${stats.total_items}`;
        this.elements.binsUsed.textContent = stats.bins_used;
        this.elements.efficiency.textContent = stats.efficiency + '%';
    }

    /**
     * Show completion message
     */
    showCompletion() {
        this.elements.currentItemDisplay.innerHTML =
            '<div style="color: #28a745; font-weight: bold; font-size: 1.3em;">All items packed!</div>';
        this.elements.explanation.innerHTML =
            '<strong>Simulation Complete!</strong> All items have been successfully packed.';
    }

    /**
     * Show summary panel
     */
    showSummary(stats) {
        const summaryHTML = this.generateSummaryHTML(stats);
        this.elements.summaryDetails.innerHTML = summaryHTML;
        this.elements.summary.classList.add('show');
    }

    /**
     * Hide summary panel
     */
    hideSummary() {
        this.elements.summary.classList.remove('show');
    }

    /**
     * Generate summary HTML
     */
    generateSummaryHTML(stats) {
        let binDetails = '';
        if (stats.bin_details) {
            binDetails = stats.bin_details.map(bin => `
                <div class="stat-item">
                    <div class="stat-label">Bin #${bin.bin_number}</div>
                    <div class="stat-value">${bin.capacity}/${this.capacity} (${bin.utilization}%)</div>
                </div>
            `).join('');
        }

        return `
            <div class="stat-item">
                <div class="stat-label">Total Bins</div>
                <div class="stat-value">${stats.bins_used}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Total Items</div>
                <div class="stat-value">${stats.total_items}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Items Processed</div>
                <div class="stat-value">${stats.items_processed}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Overall Efficiency</div>
                <div class="stat-value">${stats.efficiency}%</div>
            </div>
            ${binDetails}
        `;
    }

    /**
     * Reset display to initial state
     */
    reset() {
        this.currentItemIndex = -1;
        this.elements.currentItemDisplay.innerHTML = 'Click "Start" to begin';
        this.elements.explanation.innerHTML =
            'Select an algorithm and click "Start" to see the step-by-step process';
        this.elements.itemsProcessed.textContent = '0 / ' + this.items.length;
        this.elements.binsUsed.textContent = '0';
        this.elements.efficiency.textContent = '0%';
        this.hideSummary();
        this.renderItemsList();
        this.renderBins([]);
    }

    /**
     * Show error message
     */
    showError(message) {
        const errorHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${message}
            </div>
        `;
        this.elements.explanation.innerHTML = errorHTML;
    }

    /**
     * Clear error message
     */
    clearError() {
        // Only clear if it's showing an error
        const explanation = this.elements.explanation;
        if (explanation.innerHTML.includes('error-message')) {
            explanation.innerHTML = 'Ready';
        }
    }

    /**
     * Sleep utility for animations
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

export default BinPackingVisualizer;
