/**
 * CUBE Protocol - JavaScript Implementation
 * Browser-compatible compression/decompression using pako.js for gzip
 */

class CubeProtocol {
    /**
     * Compress data using CUBE Protocol
     * @param {string} data - Data to compress
     * @param {string} domain - Domain identifier
     * @param {string} sequence - Sequence descriptor
     * @param {string} outcome - Outcome status
     * @returns {CubeObject} Cube object with compressed data
     */
    static compress(data, domain, sequence, outcome) {
        if (typeof data !== 'string') {
            throw new TypeError('Data must be a string');
        }
        if (!domain || !sequence || !outcome) {
            throw new ValueError('domain, sequence, and outcome must be non-empty strings');
        }

        // UTF-8 encode
        const utf8 = new TextEncoder().encode(data);

        // gzip compress (level 9)
        const compressed = pako.gzip(utf8, { level: 9 });

        // Base64 encode
        const base64 = btoa(String.fromCharCode.apply(null, compressed));

        // Calculate optimized dimensions
        const dims = this._optimizeDimensions(base64.length);

        // Slice to cube
        const cubeData = this._sliceToCube(base64, dims);

        // Create descriptor
        const descriptor = `${domain}|${sequence}|${outcome}`;

        return new CubeObject(descriptor, dims, cubeData);
    }

    /**
     * Decompress cube data back to original string
     * @param {string} cubeData - Base64-encoded compressed data
     * @returns {string} Original decompressed string
     */
    static decompress(cubeData) {
        try {
            // Remove cube-fitting padding
            let cleaned = cubeData.replace(/=+$/, '');

            // Re-add proper base64 padding
            const paddingNeeded = (4 - (cleaned.length % 4)) % 4;
            cleaned += '='.repeat(paddingNeeded);

            // Base64 decode
            const binaryString = atob(cleaned);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // gzip decompress
            const decompressed = pako.ungzip(bytes);

            // UTF-8 decode
            const result = new TextDecoder().decode(decompressed);

            return result;
        } catch (err) {
            throw new Error(`Decompression failed: ${err.message}`);
        }
    }

    /**
     * Calculate optimized 3D cube dimensions
     * @private
     */
    static _optimizeDimensions(n) {
        if (n <= 0) return [1, 1, 1];

        // Start with cubic root baseline
        const side = Math.max(1, Math.ceil(Math.pow(n, 1 / 3)));

        let bestDims = [side, side, side];
        let bestWaste = side ** 3 - n;

        // Search nearby dimensions for better fit
        for (let x = Math.max(1, side - 2); x <= side + 2; x++) {
            for (let y = Math.max(1, side - 2); y <= side + 2; y++) {
                const z = Math.max(1, Math.ceil(n / (x * y)));
                const total = x * y * z;
                const waste = total - n;

                if (total >= n && waste >= 0 && waste < bestWaste) {
                    bestDims = [x, y, z];
                    bestWaste = waste;
                }
            }
        }

        return bestDims;
    }

    /**
     * Slice base64 string to fit cube dimensions
     * @private
     */
    static _sliceToCube(encoded, dims) {
        // Return encoded string directly without padding
        // Legacy support: Dimensions are calculated but padding removed for compatibility
        return encoded;
    }

    /**
     * Calculate BLAKE3 hash
     * @private
     */
    static async _blake3(data) {
        // Remove padding and re-add proper base64 padding
        let cleaned = data.replace(/=+$/, '');
        const paddingNeeded = (4 - (cleaned.length % 4)) % 4;
        cleaned += '='.repeat(paddingNeeded);

        // Decode base64
        const binaryString = atob(cleaned);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        // Calculate BLAKE3 using the blake3 library
        const hash = blake3.hash(bytes);
        return hash.toString('hex');
    }
}

/**
 * CubeObject - Encapsulates cube data and metadata
 */
class CubeObject {
    constructor(descriptor, dimensions, data) {
        this.descriptor = descriptor;
        this.dimensions = dimensions;
        this.data = data;
        this._hash = null;
    }

    /**
     * Calculate BLAKE3 hash (async)
     */
    async blake3() {
        if (!this._hash) {
            this._hash = await CubeProtocol._blake3(this.data);
        }
        return this._hash;
    }

    /**
     * Convert to dictionary format (async for hash calculation)
     */
    async asDict() {
        const hash = await this.blake3();

        return {
            protocol_version: 'cube-1.0',
            descriptor: this.descriptor,
            cube: {
                dimensions: this.dimensions,
                encoding: 'base64',
                data: this.data
            },
            hash: {
                algorithm: 'BLAKE3',
                value: hash
            }
        };
    }
}

/**
 * Custom error classes
 */
class ValueError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValueError';
    }
}
