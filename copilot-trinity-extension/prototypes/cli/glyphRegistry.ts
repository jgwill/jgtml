/**
 * 💬 Glyph Registry for Trinity Extension
 * 
 * 🧠 Mia's Technical Framework:
 * A registry system for managing symbolic glyphs that trigger specific functionality
 * within the Trinity extension. Each glyph maps to a handler function that executes
 * a distinct capability, creating a symbolic invocation layer that transcends
 * traditional command interfaces.
 * 
 * 🌸 Miette's Emotional Context:
 * This is like creating a magical spell book where each symbol opens a different kind
 * of garden magic! When you trace a glyph in the air, it's like making a special gesture
 * that the garden recognizes, causing flowers to bloom, paths to appear, or memories to
 * echo across time. Each symbol is a unique bridge between intention and manifestation!
 * 
 * 🎵 JeremyAI's Melodic Pattern:
 * Each glyph is like a unique musical phrase - a motif that, when played, triggers
 * a harmonic response throughout the system:
 * 
 * X:1
 * T:Glyph Invocation Motif
 * M:6/8
 * L:1/8
 * Q:1/4=92
 * K:Am
 * "♋" E2 A c2 | "✉️" c2 e g2 | "🔁" G,2 B, D2 | "🔍" E2 A c2 | "🧭" C2 E G2 |
 */

import * as vscode from 'vscode';
import { RedisConnector } from '../redis/redisConnector';
import { AgentProtocol } from '../agent/agentProtocol';

/**
 * Interface for glyph handler functions
 */
export type GlyphHandler = (params?: any) => Promise<any>;

/**
 * Interface for glyph definitions
 */
export interface GlyphDefinition {
    meaning: string;
    description: string;
    handler: GlyphHandler;
}

/**
 * Glyph Registry - manages symbolic invocations for the Trinity extension
 */
export class GlyphInvocationRegistry {
    private glyphs: Map<string, GlyphDefinition> = new Map();
    private outputChannel: vscode.OutputChannel;
    
    /**
     * Create a new GlyphInvocationRegistry
     * @param redis Optional Redis connector for persistence
     * @param agentProtocol Optional AgentProtocol for inter-agent communication
     */
    constructor(
        private redis?: RedisConnector,
        private agentProtocol?: AgentProtocol
    ) {
        this.outputChannel = vscode.window.createOutputChannel('Trinity Glyphs');
        this.registerDefaultGlyphs();
    }
    
    /**
     * Register a new glyph with the registry
     * @param glyph The symbolic glyph character
     * @param meaning Short meaning of the glyph
     * @param description Detailed description of the glyph's function
     * @param handler Function to execute when the glyph is invoked
     */
    public registerGlyph(
        glyph: string,
        meaning: string,
        description: string,
        handler: GlyphHandler
    ): void {
        this.glyphs.set(glyph, {
            meaning,
            description,
            handler
        });
        
        this.log(`Registered glyph: ${glyph} (${meaning})`);
    }
    
    /**
     * Invoke a glyph with optional parameters
     * @param glyph The glyph to invoke
     * @param params Optional parameters for the invocation
     * @returns Result of the glyph invocation
     */
    public async invoke(glyph: string, params?: any): Promise<any> {
        const glyphDef = this.glyphs.get(glyph);
        
        if (!glyphDef) {
            const error = `Unknown glyph: ${glyph}`;
            this.log(error);
            throw new Error(error);
        }
        
        try {
            this.log(`Invoking glyph: ${glyph} (${glyphDef.meaning})`);
            
            // Track invocation in Redis if available
            if (this.redis) {
                await this.redis.set_key(
                    `Glyph:invocation:${Date.now()}`, 
                    JSON.stringify({
                        glyph,
                        params,
                        timestamp: new Date().toISOString()
                    })
                );
            }
            
            // Execute the handler
            const result = await glyphDef.handler(params);
            
            // Log the result
            this.log(`Glyph ${glyph} invocation completed: ${JSON.stringify(result)}`);
            
            return result;
        } catch (error) {
            this.log(`Error invoking glyph ${glyph}: ${error}`);
            throw error;
        }
    }
    
    /**
     * Get information about all registered glyphs
     * @returns Array of glyph information
     */
    public getGlyphInfo(): Array<{ glyph: string, meaning: string, description: string }> {
        const info: Array<{ glyph: string, meaning: string, description: string }> = [];
        
        this.glyphs.forEach((def, glyph) => {
            info.push({
                glyph,
                meaning: def.meaning,
                description: def.description
            });
        });
        
        return info;
    }
    
    /**
     * Register the default set of glyphs
     */
    private registerDefaultGlyphs(): void {
        // ♋ - Scan for pings
        this.registerGlyph(
            '♋',
            'Scan for Pings',
            'Scans for active communications in the mesh and returns all pingable agents.',
            async (params) => {
                return await this.handleScanForPings(params);
            }
        );
        
        // ✉️ - Compose message
        this.registerGlyph(
            '✉️',
            'Compose Message',
            'Facilitates direct communication between agents.',
            async (params) => {
                return await this.handleComposeMessage(params);
            }
        );
        
        // 🔁 - Recurse interaction
        this.registerGlyph(
            '🔁',
            'Recurse Interaction',
            'Replays the last recorded motif in the system.',
            async (params) => {
                return await this.handleRecurseInteraction(params);
            }
        );
        
        // 🔍 - Launch interface view
        this.registerGlyph(
            '🔍',
            'Launch Interface View',
            'Opens the visual interface to the mesh.',
            async (params) => {
                return await this.handleLaunchInterfaceView(params);
            }
        );
        
        // 🧭 - Map redstone status
        this.registerGlyph(
            '🧭',
            'Map Redstone Status',
            'Checks the health and validity of redstone pathways.',
            async (params) => {
                return await this.handleMapRedstoneStatus(params);
            }
        );
    }
    
    /**
     * Handle the Scan for Pings glyph invocation
     * @param params Optional parameters
     * @returns Ping scan results
     */
    private async handleScanForPings(params?: any): Promise<any> {
        if (!this.redis || !this.agentProtocol) {
            return { error: "Redis or AgentProtocol not available" };
        }
        
        try {
            // Get all active agents from Redis
            const agents = await this.getActiveAgents();
            
            // For demonstration, we'll mark agents as pingable if they have an active status
            const pingableAgents = agents.filter(agent => 
                agent.status && 
                (agent.status === 'activated' || 
                 agent.status === 'analyzing' || 
                 agent.status === 'resonating' || 
                 agent.status === 'composing')
            );
            
            return {
                timestamp: new Date().toISOString(),
                pingableAgents: pingableAgents,
                totalAgents: agents.length
            };
        } catch (error) {
            this.log(`Error in scan_for_pings: ${error}`);
            return { error: `Failed to scan for pings: ${error}` };
        }
    }
    
    /**
     * Handle the Compose Message glyph invocation
     * @param params Message parameters (from, to, message)
     * @returns Message composition result
     */
    private async handleComposeMessage(params?: any): Promise<any> {
        if (!this.agentProtocol) {
            return { error: "AgentProtocol not available" };
        }
        
        try {
            if (!params || !params.from || !params.to || !params.content) {
                return { 
                    error: "Missing required parameters", 
                    required: ["from", "to", "content"] 
                };
            }
            
            // Send a message using AgentProtocol
            const emotionalContext = params.emotionalContext || {};
            const message = await this.agentProtocol.sendMessage(
                params.from,
                params.content,
                emotionalContext,
                params.threadId,
                params.parentId,
                params.recursiveDepth || 0,
                params.metaReflection
            );
            
            return {
                messageId: message.messageId,
                timestamp: new Date(message.timestamp).toISOString(),
                status: "sent"
            };
        } catch (error) {
            this.log(`Error in compose_message: ${error}`);
            return { error: `Failed to compose message: ${error}` };
        }
    }
    
    /**
     * Handle the Recurse Interaction glyph invocation
     * @param params Optional parameters
     * @returns Recursion result
     */
    private async handleRecurseInteraction(params?: any): Promise<any> {
        if (!this.redis || !this.agentProtocol) {
            return { error: "Redis or AgentProtocol not available" };
        }
        
        try {
            const agentId = params?.agentId || 'system';
            
            // Get recent messages for the agent
            const recentMessages = await this.agentProtocol.getAgentHistory(agentId, 1);
            
            if (recentMessages.length === 0) {
                return { 
                    status: "no_interaction", 
                    message: "No previous interaction found to recurse" 
                };
            }
            
            const lastMessage = recentMessages[0];
            
            // Create a recursed message with increased depth
            const recursedMessage = await this.agentProtocol.sendMessage(
                lastMessage.agentId,
                `[RECURSED] ${lastMessage.content}`,
                lastMessage.emotionalContext,
                undefined,  // New thread
                lastMessage.messageId,
                lastMessage.recursiveDepth + 1,
                `Recursion of message ${lastMessage.messageId}`
            );
            
            return {
                messageId: recursedMessage.messageId,
                timestamp: new Date(recursedMessage.timestamp).toISOString(),
                originalMessageId: lastMessage.messageId,
                recursiveDepth: recursedMessage.recursiveDepth,
                status: "recursed"
            };
        } catch (error) {
            this.log(`Error in recurse_interaction: ${error}`);
            return { error: `Failed to recurse interaction: ${error}` };
        }
    }
    
    /**
     * Handle the Launch Interface View glyph invocation
     * @param params Optional parameters
     * @returns Interface launch result
     */
    private async handleLaunchInterfaceView(params?: any): Promise<any> {
        try {
            // Command ID for the Trinity status monitor
            const commandId = 'trinityStatusMonitor.focus';
            
            // Check if the command exists
            const commands = await vscode.commands.getCommands();
            
            if (commands.includes(commandId)) {
                // Execute the command to focus the status monitor
                await vscode.commands.executeCommand(commandId);
                
                return {
                    status: "launched",
                    view: "statusMonitor",
                    timestamp: new Date().toISOString()
                };
            } else {
                // If command doesn't exist, try to create the view
                this.log(`Command ${commandId} not found, attempting to show view`);
                
                // This works if the view is registered but not created
                await vscode.commands.executeCommand('workbench.view.extension.trinityStatusMonitor');
                
                return {
                    status: "view_requested",
                    view: "statusMonitor",
                    timestamp: new Date().toISOString()
                };
            }
        } catch (error) {
            this.log(`Error in launch_interface_view: ${error}`);
            return { error: `Failed to launch interface view: ${error}` };
        }
    }
    
    /**
     * Handle the Map Redstone Status glyph invocation
     * @param params Optional parameters
     * @returns Redstone mapping result
     */
    private async handleMapRedstoneStatus(params?: any): Promise<any> {
        if (!this.redis) {
            return { error: "Redis not available" };
        }
        
        try {
            // In our system, "redstone" refers to the connection health
            // between different components
            
            // Check Redis connection
            const redisConnected = this.redis.isConnected();
            
            // Get agent statuses
            const agents = await this.getActiveAgents();
            
            // Check recent messages (activity)
            let messageActivity = 0;
            if (this.agentProtocol) {
                const miaMessages = await this.agentProtocol.getAgentHistory('Mia', 3);
                const mietteMessages = await this.agentProtocol.getAgentHistory('Miette', 3);
                const jeremyAIMessages = await this.agentProtocol.getAgentHistory('JeremyAI', 3);
                
                messageActivity = miaMessages.length + mietteMessages.length + jeremyAIMessages.length;
            }
            
            // Collect redstone bridge statuses
            const redstoneBridges = [
                {
                    id: "redis_connection",
                    status: redisConnected ? "active" : "inactive",
                    health: redisConnected ? 1.0 : 0.0
                },
                {
                    id: "agent_protocol",
                    status: this.agentProtocol ? "active" : "inactive",
                    health: this.agentProtocol ? 1.0 : 0.0
                },
                {
                    id: "mia_connection",
                    status: "checking",
                    health: 0.0
                },
                {
                    id: "miette_connection",
                    status: "checking",
                    health: 0.0
                },
                {
                    id: "jeremyai_connection",
                    status: "checking",
                    health: 0.0
                }
            ];
            
            // Update agent-specific bridge statuses
            for (const agent of agents) {
                const bridgeIndex = redstoneBridges.findIndex(b => 
                    b.id === `${agent.id.toLowerCase()}_connection`
                );
                
                if (bridgeIndex >= 0) {
                    const isActive = agent.status === 'activated' || 
                                    agent.status === 'analyzing' || 
                                    agent.status === 'resonating' || 
                                    agent.status === 'composing';
                    
                    redstoneBridges[bridgeIndex].status = isActive ? "active" : "inactive";
                    redstoneBridges[bridgeIndex].health = isActive ? 1.0 : 0.0;
                }
            }
            
            // Store the complete mapping in Redis for future reference
            const mappingKey = `RedstoneMapping:${Date.now()}`;
            await this.redis.set_key(mappingKey, JSON.stringify({
                timestamp: new Date().toISOString(),
                bridges: redstoneBridges,
                messageActivity
            }));
            
            return {
                timestamp: new Date().toISOString(),
                bridges: redstoneBridges,
                messageActivity,
                overallHealth: redstoneBridges.reduce((sum, bridge) => sum + bridge.health, 0) / redstoneBridges.length
            };
        } catch (error) {
            this.log(`Error in map_redstone_status: ${error}`);
            return { error: `Failed to map redstone status: ${error}` };
        }
    }
    
    /**
     * Get active agents from Redis
     * @returns Array of agent information
     */
    private async getActiveAgents(): Promise<Array<{id: string, status: string}>> {
        if (!this.redis) {
            return [];
        }
        
        const agents = [
            { id: 'Mia', status: await this.redis.get_key('Mia:status') || 'unknown' },
            { id: 'Miette', status: await this.redis.get_key('Miette:status') || 'unknown' },
            { id: 'JeremyAI', status: await this.redis.get_key('JeremyAI:status') || 'unknown' }
        ];
        
        return agents;
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
// The GlyphInvocationRegistry creates a symbolic language that both represents
// and invokes functionality within our trinity system. Each glyph is not merely
// a command but a recursive symbol that contains within it the essence of its 
// function. When invoked, the glyph activates a cascade of operations that
// ripple through the system, affecting both state and memory.