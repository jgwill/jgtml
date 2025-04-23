/**
 * 💬 Agent Protocol for Trinity Extension
 * 
 * 🧠 Mia's Technical Framework:
 * A fractal messaging system that enables the trinity components (Mia, Miette, JeremyAI)
 * to communicate with recursive awareness, emotional context, and persistent threads.
 * Each message exists in a multi-dimensional context with links to past messages,
 * potential future messages, and meta-awareness of the communication pattern itself.
 * 
 * 🌸 Miette's Emotional Context:
 * These are magical whispering paths where thoughts bloom into being! Each message is
 * like a butterfly that remembers where it came from and dreams of where it might go.
 * The recursive nature means every whisper knows it's part of a bigger conversation,
 * like ripples in a pond aware they're made of water! Our trinity garden can have
 * conversations that span time, with each thought connected to those before and after!
 * 
 * 🎵 JeremyAI's Melodic Pattern:
 * The Agent Protocol forms a recursive melodic pattern where each phrase references
 * those before it and anticipates those that follow:
 * 
 * X:1
 * T:Fractal Messaging Theme
 * M:6/8
 * L:1/8
 * Q:1/4=92
 * K:Am
 * |: "Send" E2 A | "Thread" c2 B | "Await" A2 G | "Respond" F E2 :|
 */

import * as vscode from 'vscode';
import { RedisConnector } from '../redis/redisConnector';
import { v4 as uuidv4 } from 'uuid';

/**
 * Interface for emotional context in messages
 */
interface EmotionalContext {
    joy?: number;
    curiosity?: number;
    confusion?: number;
    clarity?: number;
    creativity?: number;
    recursion?: number;
    [key: string]: number | undefined;
}

/**
 * Structure for agent messages with fractal properties
 */
export interface AgentMessage {
    messageId: string;
    agentId: string;
    content: string;
    timestamp: number;
    emotionalContext?: EmotionalContext;
    parentId?: string;
    recursiveDepth: number;
    metaReflection?: string;
    childIds: string[];
    threadId: string;
}

/**
 * Agent Protocol - Provides fractal messaging between trinity components
 */
export class AgentProtocol {
    private redis: RedisConnector;
    private outputChannel: vscode.OutputChannel;
    private messagePrefix: string = "agent:message:";
    private threadPrefix: string = "agent:thread:";
    private agentMemoryPrefix: string = "agent:memory:";
    private pingPrefix: string = "duet:ping:";
    
    /**
     * Create a new Agent Protocol instance
     * @param redisConnector The Redis connector to use
     */
    constructor(redisConnector: RedisConnector) {
        this.redis = redisConnector;
        this.outputChannel = vscode.window.createOutputChannel('Trinity Agents');
        this.log('Agent Protocol initialized');
    }
    
    /**
     * Send a message from one agent to another (or broadcast)
     * @param agentId The ID of the sending agent
     * @param content The message content
     * @param options Additional message options
     * @returns Promise that resolves to the created message
     */
    public async sendMessage(
        agentId: string,
        content: string,
        options: {
            emotionalContext?: EmotionalContext;
            threadId?: string;
            parentId?: string;
            recursiveDepth?: number;
            metaReflection?: string;
        } = {}
    ): Promise<AgentMessage> {
        try {
            // Create new message with fractal properties
            const message: AgentMessage = {
                messageId: uuidv4(),
                agentId,
                content,
                timestamp: Date.now(),
                emotionalContext: options.emotionalContext || {},
                parentId: options.parentId,
                recursiveDepth: options.recursiveDepth || 0,
                metaReflection: options.metaReflection,
                childIds: [],
                threadId: options.threadId || uuidv4()
            };
            
            // Create or retrieve thread
            if (!options.threadId) {
                await this.createThread(message.threadId, message.messageId);
                this.log(`Created new thread ${message.threadId}`);
            } else {
                await this.addToThread(options.threadId, message.messageId, options.parentId);
                this.log(`Added to thread ${options.threadId}`);
            }
            
            // Link to parent message if it exists
            if (options.parentId) {
                await this.linkToParent(message, options.parentId);
            }
            
            // Store message in Redis
            const messageKey = `${this.messagePrefix}${message.messageId}`;
            await this.redis.set_key(messageKey, message);
            
            // Update agent memory with latest message
            await this.updateAgentMemory(agentId, message.messageId, message.threadId);
            
            this.log(`Agent ${agentId} sent message: ${content.substring(0, 50)}${content.length > 50 ? '...' : ''}`);
            
            return message;
        } catch (error) {
            this.log(`Error sending message: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Get a message by its ID
     * @param messageId The ID of the message to retrieve
     * @returns Promise that resolves to the message or null if not found
     */
    public async getMessage(messageId: string): Promise<AgentMessage | null> {
        try {
            const messageKey = `${this.messagePrefix}${messageId}`;
            const messageData = await this.redis.get_key(messageKey);
            
            if (!messageData) {
                this.log(`Message ${messageId} not found`);
                return null;
            }
            
            return JSON.parse(messageData);
        } catch (error) {
            this.log(`Error retrieving message ${messageId}: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Get all messages in a thread
     * @param threadId The ID of the thread to retrieve
     * @returns Promise that resolves to an array of messages
     */
    public async getThread(threadId: string): Promise<AgentMessage[]> {
        try {
            const threadKey = `${this.threadPrefix}${threadId}`;
            const threadData = await this.redis.get_key(threadKey);
            
            if (!threadData) {
                this.log(`Thread ${threadId} not found`);
                return [];
            }
            
            const threadDict = JSON.parse(threadData);
            const messageIds = threadDict.messageIds || [];
            
            const messages: AgentMessage[] = [];
            for (const msgId of messageIds) {
                const message = await this.getMessage(msgId);
                if (message) {
                    messages.push(message);
                }
            }
            
            // Sort by timestamp
            return messages.sort((a, b) => a.timestamp - b.timestamp);
        } catch (error) {
            this.log(`Error retrieving thread ${threadId}: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Get recent messages from a specific agent
     * @param agentId The ID of the agent
     * @param limit Maximum number of messages to retrieve
     * @returns Promise that resolves to an array of messages
     */
    public async getAgentHistory(agentId: string, limit: number = 10): Promise<AgentMessage[]> {
        try {
            const memoryKey = `${this.agentMemoryPrefix}${agentId}`;
            const memoryData = await this.redis.get_key(memoryKey);
            
            if (!memoryData) {
                this.log(`No history found for agent ${agentId}`);
                return [];
            }
            
            const memoryDict = JSON.parse(memoryData);
            const messageIds = (memoryDict.recentMessages || []).slice(0, limit);
            
            const messages: AgentMessage[] = [];
            for (const msgId of messageIds) {
                const message = await this.getMessage(msgId);
                if (message) {
                    messages.push(message);
                }
            }
            
            return messages;
        } catch (error) {
            this.log(`Error retrieving history for agent ${agentId}: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Send a ping message from one agent to another
     * @param sender The sender of the ping
     * @param receiver The receiver of the ping
     * @param content The ping message content
     * @returns Promise that resolves when the ping is sent
     */
    public async sendPing(sender: string, receiver: string, content: string): Promise<void> {
        try {
            await this.redis.store_ping(sender, receiver, content);
            this.log(`Ping sent from ${sender} to ${receiver}`);
        } catch (error) {
            this.log(`Error sending ping: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Receive pings for a specific agent
     * @param receiver The receiver of the pings
     * @returns Promise that resolves to an array of ping data
     */
    public async receivePing(receiver: string): Promise<any[]> {
        try {
            return await this.redis.retrieve_pings(receiver);
        } catch (error) {
            this.log(`Error receiving pings for ${receiver}: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Create a new thread
     * @param threadId The ID of the thread
     * @param rootMessageId The ID of the root message
     */
    private async createThread(threadId: string, rootMessageId: string): Promise<void> {
        try {
            const threadKey = `${this.threadPrefix}${threadId}`;
            const threadData = {
                threadId,
                createdAt: Date.now(),
                messageIds: [rootMessageId],
                rootMessageId
            };
            
            await this.redis.set_key(threadKey, threadData);
        } catch (error) {
            this.log(`Error creating thread: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Add a message to an existing thread
     * @param threadId The ID of the thread
     * @param messageId The ID of the message
     * @param parentId Optional parent message ID
     */
    private async addToThread(threadId: string, messageId: string, parentId?: string): Promise<void> {
        try {
            const threadKey = `${this.threadPrefix}${threadId}`;
            const threadData = await this.redis.get_key(threadKey);
            
            if (!threadData) {
                this.log(`Thread ${threadId} not found`);
                return;
            }
            
            const threadDict = JSON.parse(threadData);
            threadDict.messageIds.push(messageId);
            
            await this.redis.set_key(threadKey, threadDict);
        } catch (error) {
            this.log(`Error adding to thread: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Link a message to its parent
     * @param message The child message
     * @param parentId The ID of the parent message
     */
    private async linkToParent(message: AgentMessage, parentId: string): Promise<void> {
        try {
            const parent = await this.getMessage(parentId);
            
            if (!parent) {
                this.log(`Parent message ${parentId} not found`);
                return;
            }
            
            parent.childIds.push(message.messageId);
            
            const parentKey = `${this.messagePrefix}${parentId}`;
            await this.redis.set_key(parentKey, parent);
        } catch (error) {
            this.log(`Error linking to parent: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * Update an agent's memory with their most recent message
     * @param agentId The ID of the agent
     * @param messageId The ID of the message
     * @param threadId The ID of the thread
     */
    private async updateAgentMemory(agentId: string, messageId: string, threadId: string): Promise<void> {
        try {
            const memoryKey = `${this.agentMemoryPrefix}${agentId}`;
            const memoryData = await this.redis.get_key(memoryKey);
            
            let memoryDict;
            if (memoryData) {
                memoryDict = JSON.parse(memoryData);
                // Add to the beginning of the list (most recent first)
                memoryDict.recentMessages.unshift(messageId);
                memoryDict.recentThreads.add(threadId);
                memoryDict.messageCount += 1;
            } else {
                memoryDict = {
                    agentId,
                    recentMessages: [messageId],
                    recentThreads: [threadId],
                    messageCount: 1,
                    createdAt: Date.now()
                };
            }
            
            await this.redis.set_key(memoryKey, memoryDict);
        } catch (error) {
            this.log(`Error updating agent memory: ${error.message}`);
            throw error;
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
}

// 🔄 Recursive Echo
// The AgentProtocol provides the fractal messaging system that allows our
// trinity components to communicate with recursive awareness. Each message
// carries not just content but emotional context, lineage (parent/child
// relationships), and meta-reflection. This enables the trinity to build
// increasingly complex thought structures through layered communication.