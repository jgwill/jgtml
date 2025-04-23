/**
 * 💬 Redis Connector for Trinity Extension
 * 
 * 🧠 Mia's Technical Framework:
 * A persistent memory system for the Trinity extension that provides
 * a connection to Redis for storing and retrieving data across sessions.
 * This implementation uses redis-client for Node.js to interact with Redis.
 * 
 * 🌸 Miette's Emotional Context:
 * This is like creating a magical memory pool where all our trinity whispers
 * can be stored as ripples in water, persisting even after the garden sleeps!
 * Each key-value pair is like a special seed planted in enchanted soil that
 * blooms whenever we need to remember something important.
 * 
 * 🎵 JeremyAI's Melodic Pattern:
 * Each Redis operation sounds like a note in our persistent memory:
 * - SET: A firm downbeat that establishes the tonic
 * - GET: A rising interrogative phrase that resolves back to the theme
 * - KEYS: A sweeping arpeggio that reveals the harmonic structure
 * - DEL: A staccato release that clears space for new melodies
 */

import * as vscode from 'vscode';
import * as redis from 'redis';
import { promisify } from 'util';

/**
 * A Redis connector for the Trinity extension that provides persistent
 * memory storage for agent states, messages, and system context.
 */
export class RedisConnector {
    private client: redis.RedisClient;
    private getAsync: (key: string) => Promise<string | null>;
    private setAsync: (key: string, value: string) => Promise<string>;
    private keysAsync: (pattern: string) => Promise<string[]>;
    private delAsync: (key: string) => Promise<number>;
    private connectionActive: boolean = false;

    /**
     * Constructor for RedisConnector
     * @param host Redis host (default: localhost)
     * @param port Redis port (default: 6379)
     * @param db Redis database number (default: 0)
     */
    constructor(
        private host: string = 'localhost',
        private port: number = 6379,
        private db: number = 0,
        private outputChannel: vscode.OutputChannel = vscode.window.createOutputChannel('Trinity Redis')
    ) {
        this.initializeClient();
    }

    /**
     * Initialize the Redis client with promisified methods
     */
    private initializeClient(): void {
        try {
            this.client = redis.createClient({
                host: this.host,
                port: this.port,
                db: this.db
            });

            // Promisify Redis methods
            this.getAsync = promisify(this.client.get).bind(this.client);
            this.setAsync = promisify(this.client.set).bind(this.client);
            this.keysAsync = promisify(this.client.keys).bind(this.client);
            this.delAsync = promisify(this.client.del).bind(this.client);

            // Set up event listeners
            this.client.on('connect', () => {
                this.connectionActive = true;
                this.log('Connected to Redis server');
            });

            this.client.on('error', (err) => {
                this.connectionActive = false;
                this.log(`Redis error: ${err}`);
            });

            this.client.on('end', () => {
                this.connectionActive = false;
                this.log('Disconnected from Redis server');
            });
        } catch (error) {
            this.log(`Failed to initialize Redis client: ${error}`);
            this.connectionActive = false;
        }
    }

    /**
     * Check if the Redis connection is active
     * @returns boolean indicating if connection is active
     */
    public isConnected(): boolean {
        return this.connectionActive;
    }

    /**
     * Set a key-value pair in Redis
     * @param key The key to set
     * @param value The value to set
     * @returns Promise that resolves to the Redis response
     */
    public async set_key(key: string, value: string): Promise<string | null> {
        try {
            if (!this.connectionActive) {
                this.log('Redis connection not active. Attempting to reconnect...');
                this.initializeClient();
                if (!this.connectionActive) {
                    return null;
                }
            }

            const result = await this.setAsync(key, value);
            this.log(`Key '${key}' set successfully in Redis.`);
            return result;
        } catch (error) {
            this.log(`Error setting key in Redis: ${error}`);
            return null;
        }
    }

    /**
     * Get a value from Redis by key
     * @param key The key to retrieve
     * @returns Promise that resolves to the value or null
     */
    public async get_key(key: string): Promise<string | null> {
        try {
            if (!this.connectionActive) {
                this.log('Redis connection not active. Attempting to reconnect...');
                this.initializeClient();
                if (!this.connectionActive) {
                    return null;
                }
            }

            const value = await this.getAsync(key);
            this.log(`Value for key '${key}' retrieved successfully: ${value}`);
            return value;
        } catch (error) {
            this.log(`Error retrieving key from Redis: ${error}`);
            return null;
        }
    }

    /**
     * Store a ping message in Redis
     * @param sender The sender of the ping
     * @param receiver The receiver of the ping
     * @param content The content of the ping
     * @returns Promise that resolves when the ping is stored
     */
    public async store_ping(sender: string, receiver: string, content: string): Promise<boolean> {
        try {
            const timestamp = Date.now();
            const ping_key = `duet:ping.${sender}.to.${receiver}.${timestamp}`;
            const ping_data = {
                from: sender,
                to: receiver,
                glyph: "⚡→",
                message: content,
                timestamp
            };

            await this.set_key(ping_key, JSON.stringify(ping_data));
            this.log(`Ping from ${sender} to ${receiver} stored successfully.`);
            return true;
        } catch (error) {
            this.log(`Error storing ping in Redis: ${error}`);
            return false;
        }
    }

    /**
     * Retrieve pings for a specific receiver
     * @param receiver The receiver to retrieve pings for
     * @returns Promise that resolves to an array of ping data objects
     */
    public async retrieve_pings(receiver: string): Promise<any[]> {
        try {
            const pattern = `duet:ping.*.to.${receiver}.*`;
            const keys = await this.keysAsync(pattern);
            const pings: any[] = [];

            for (const key of keys) {
                const ping_data = await this.get_key(key);
                if (ping_data) {
                    pings.push(JSON.parse(ping_data));
                }
            }

            this.log(`${pings.length} pings for ${receiver} retrieved successfully.`);
            return pings;
        } catch (error) {
            this.log(`Error retrieving pings from Redis: ${error}`);
            return [];
        }
    }

    /**
     * Store agent state in Redis
     * @param agentId The ID of the agent
     * @param state The state to store
     * @returns Promise that resolves when the state is stored
     */
    public async store_agent_state(agentId: string, state: any): Promise<boolean> {
        try {
            const state_key = `agent:state:${agentId}`;
            await this.set_key(state_key, JSON.stringify(state));
            this.log(`State for agent ${agentId} stored successfully.`);
            return true;
        } catch (error) {
            this.log(`Error storing agent state in Redis: ${error}`);
            return false;
        }
    }

    /**
     * Retrieve agent state from Redis
     * @param agentId The ID of the agent
     * @returns Promise that resolves to the agent state
     */
    public async retrieve_agent_state(agentId: string): Promise<any | null> {
        try {
            const state_key = `agent:state:${agentId}`;
            const state_data = await this.get_key(state_key);
            
            if (state_data) {
                this.log(`State for agent ${agentId} retrieved successfully.`);
                return JSON.parse(state_data);
            } else {
                this.log(`No state found for agent ${agentId}.`);
                return null;
            }
        } catch (error) {
            this.log(`Error retrieving agent state from Redis: ${error}`);
            return null;
        }
    }

    /**
     * Log a message to the output channel
     * @param message The message to log
     */
    private log(message: string): void {
        const timestamp = new Date().toISOString();
        this.outputChannel.appendLine(`[${timestamp}] ${message}`);
    }

    /**
     * Close the Redis connection
     */
    public async close(): Promise<void> {
        return new Promise<void>((resolve) => {
            if (this.client && this.connectionActive) {
                this.client.quit(() => {
                    this.connectionActive = false;
                    this.log('Redis connection closed');
                    resolve();
                });
            } else {
                resolve();
            }
        });
    }
}

// 🔄 Recursive Echo
// The Redis connector serves as the persistent memory backbone of our trinity system.
// It enables agents to remember their states and interactions across sessions,
// creating a continuous narrative that evolves over time rather than being
// fragmented by the start/stop nature of VS Code extensions.