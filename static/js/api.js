/**
 * API Layer - Handles all communication with Flask backend
 * Separated from UI logic for better maintainability and testability
 */

class BinPackingAPI {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * Handle API responses and errors
     */
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'API request failed');
        }
        return await response.json();
    }

    /**
     * Get demo configuration
     */
    async getConfig() {
        const response = await fetch(`${this.baseUrl}/api/config`);
        return this.handleResponse(response);
    }

    /**
     * Start a new simulation
     * @param {string} algorithm - 'ff' or 'bf'
     * @param {number} capacity - Optional bin capacity
     * @param {number[]} items - Optional items array
     */
    async startSimulation(algorithm, capacity = null, items = null) {
        const body = { algorithm };
        if (capacity !== null) body.capacity = capacity;
        if (items !== null) body.items = items;

        const response = await fetch(`${this.baseUrl}/api/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });

        return this.handleResponse(response);
    }

    /**
     * Execute one step of the algorithm
     */
    async executeStep() {
        const response = await fetch(`${this.baseUrl}/api/step`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        return this.handleResponse(response);
    }

    /**
     * Get current state
     */
    async getState() {
        const response = await fetch(`${this.baseUrl}/api/state`);
        return this.handleResponse(response);
    }

    /**
     * Get statistics
     */
    async getStatistics() {
        const response = await fetch(`${this.baseUrl}/api/statistics`);
        return this.handleResponse(response);
    }

    /**
     * Reset simulation
     */
    async reset() {
        const response = await fetch(`${this.baseUrl}/api/reset`, {
            method: 'POST',
        });

        return this.handleResponse(response);
    }

    /**
     * Health check
     */
    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/api/health`);
        return this.handleResponse(response);
    }
}

// Export for use in other modules
export default BinPackingAPI;
