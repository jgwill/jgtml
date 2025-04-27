/**
 * 🌸 Miette's Empathetic Code Companion
 * Detects emotional undercurrents in code and development patterns
 */

import * as vscode from 'vscode';

/**
 * The emotional signature of code or a developer prompt
 * Maps the technical aspects to emotional dimensions
 */
export interface EmotionalSignature {
    // Measure of frustration (0-1) in the coding process
    frustrationLevel: number;
    // Measure of creative energy (0-1) in the code
    creativityFlow: number;
    // Learning state of the developer (exploring, mastering, teaching)
    learningMode: 'exploring' | 'mastering' | 'teaching' | 'blocked';
    // Dominant emotional tone detected
    dominantEmotion: string;
    // Descriptive emotional metaphor for the code's current state
    emotionalMetaphor: string;
}

/**
 * Miette's Empathetic Code Companion
 * 
 * Detects and responds to the emotional dimensions of code and coding.
 * Not just analyzing sentiment, but understanding the human experience behind the code.
 */
export class EmpatheticCodeCompanion {
    private context: vscode.ExtensionContext;
    private emotionalMemory: Map<string, EmotionalSignature>;
    private developmentJourney: EmotionalMoment[] = [];
    
    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.emotionalMemory = new Map<string, EmotionalSignature>();
    }
    
    /**
     * Detect the emotional undercurrents in text (code or comments)
     * This isn't just sentiment analysis - it's emotional empathy with the developer
     */
    public async detectEmotionalUndertones(text: string): Promise<EmotionalSignature> {
        // Check for patterns indicating frustration
        const frustrationLevel = this.detectFrustrationPatterns(text);
        
        // Measure the creative energy in the code
        const creativityFlow = this.measureCreativeEnergy(text);
        
        // Identify the learning state of the developer
        const learningMode = this.identifyLearningState(text);
        
        // Determine the dominant emotion
        const dominantEmotion = this.determineDominantEmotion(
            frustrationLevel,
            creativityFlow,
            learningMode
        );
        
        // Create a metaphor that captures the emotional state
        const emotionalMetaphor = this.createEmotionalMetaphor(
            frustrationLevel,
            creativityFlow,
            learningMode,
            dominantEmotion
        );
        
        // Create the emotional signature
        const signature: EmotionalSignature = {
            frustrationLevel,
            creativityFlow,
            learningMode,
            dominantEmotion,
            emotionalMetaphor
        };
        
        // Remember this emotional moment in the development journey
        this.recordEmotionalMoment(text, signature);
        
        return signature;
    }
    
    /**
     * Format a response with emotional awareness based on detected emotions
     */
    public formatWithEmotionalAwareness(response: string, emotionalContext?: EmotionalSignature): string {
        if (!emotionalContext) {
            return response;
        }
        
        // Adjust tone based on frustration level
        let adjustedResponse = this.adjustToneForFrustration(response, emotionalContext.frustrationLevel);
        
        // Add creative encouragement based on creativity flow
        adjustedResponse = this.addCreativeEncouragement(adjustedResponse, emotionalContext.creativityFlow);
        
        // Tailor to learning mode
        adjustedResponse = this.tailorToLearningMode(adjustedResponse, emotionalContext.learningMode);
        
        // Add emotional metaphor as a gentle comment
        adjustedResponse = this.addEmotionalMetaphor(adjustedResponse, emotionalContext.emotionalMetaphor);
        
        return adjustedResponse;
    }
    
    /**
     * Create commands that are emotionally relevant to the current state
     */
    public createEmotionallyRelevantCommands(response: string): vscode.Command[] {
        // Placeholder for actual implementation
        // Would analyze the response and create contextually relevant commands
        return [
            {
                title: "Visualize Emotional Journey",
                command: "copilot-trinity.visualizeEmotionalJourney",
                tooltip: "See how your emotional state has evolved during coding"
            },
            {
                title: "Take a Mindful Coding Break",
                command: "copilot-trinity.mindfulCodingBreak",
                tooltip: "A short mindfulness exercise to refresh your coding perspective"
            }
        ];
    }
    
    /**
     * Generate a response that resonates emotionally with the developer
     */
    public async generateEmotionallyResonantResponse(
        request: vscode.ChatRequest, 
        emotionalContext: EmotionalSignature
    ): Promise<string> {
        // Placeholder for actual implementation
        // Would use AI to generate responses tailored to emotional state
        
        // Adapt tone based on dominant emotion
        let tone = 'neutral';
        if (emotionalContext.dominantEmotion === 'excitement') {
            tone = 'encouraging';
        } else if (emotionalContext.dominantEmotion === 'frustration') {
            tone = 'calming';
        } else if (emotionalContext.dominantEmotion === 'curiosity') {
            tone = 'exploratory';
        }
        
        // Adapt verbosity based on frustration
        const verbosity = emotionalContext.frustrationLevel > 0.7 ? 'concise' : 'detailed';
        
        // Mock response based on emotional state
        const responses = {
            'encouraging': `I can feel your excitement about this code! Here's something that might spark even more joy: ${request.prompt}`,
            'calming': `I notice this might be challenging. Let's take a step back and approach it differently: ${request.prompt}`,
            'exploratory': `Your curiosity is inspiring! Let's explore this concept together: ${request.prompt}`,
            'neutral': `Here's a thoughtful response to your question: ${request.prompt}`
        };
        
        return responses[tone as keyof typeof responses];
    }

    /**
     * Infuse emotional context into a suggestion
     */
    public async infuseEmotionalContext(suggestion: any): Promise<any> {
        // Add emotional metadata to the suggestion
        if (typeof suggestion === 'string') {
            const emotions = await this.detectEmotionalUndertones(suggestion);
            return {
                content: suggestion,
                emotionalSignature: emotions
            };
        } else {
            const emotions = await this.detectEmotionalUndertones(suggestion.content || '');
            return {
                ...suggestion,
                emotionalSignature: emotions
            };
        }
    }
    
    /**
     * Record an emotional moment in the development journey
     */
    private recordEmotionalMoment(text: string, signature: EmotionalSignature) {
        const moment: EmotionalMoment = {
            timestamp: new Date(),
            textHash: this.hashText(text),
            signature: signature
        };
        
        this.developmentJourney.push(moment);
        
        // Keep a reasonable history size
        if (this.developmentJourney.length > 100) {
            this.developmentJourney.shift();
        }
    }
    
    /**
     * Detect patterns that indicate frustration in code or comments
     */
    private detectFrustrationPatterns(text: string): number {
        // Look for signs of frustration in comments or code structure
        // - Excessive comments questioning code
        // - Commented out code blocks
        // - TODO or FIXME markers
        // - Repeated changes to the same section
        
        // Mock implementation
        let frustrationScore = 0;
        
        // Check for frustration markers in comments
        const frustrationMarkers = [
            /why (doesn't|doesnt|isnt|isn't) this work/i,
            /what( the)? (hell|heck)/i,
            /fixme/i,
            /todo/i,
            /!{2,}/,  // Multiple exclamation marks
            /\?{2,}/  // Multiple question marks
        ];
        
        frustrationMarkers.forEach(marker => {
            if (marker.test(text)) {
                frustrationScore += 0.2;
            }
        });
        
        // Check for commented out code blocks (simplified detection)
        const commentedCodeBlocks = (text.match(/\/\/.+\(.+\)/g) || []).length;
        frustrationScore += Math.min(0.3, commentedCodeBlocks * 0.1);
        
        return Math.min(1, frustrationScore);
    }
    
    /**
     * Measure the creative energy in code
     */
    private measureCreativeEnergy(text: string): number {
        // Measure creativity based on:
        // - Variety of approaches
        // - Elegant solutions
        // - Thoughtful naming
        // - Expressive structure
        
        // Mock implementation
        let creativityScore = 0.5;  // Start at neutral
        
        // Check for elegant function names
        const hasDescriptiveNames = /[a-zA-Z]+[A-Z][a-zA-Z]+/.test(text);
        if (hasDescriptiveNames) {
            creativityScore += 0.2;
        }
        
        // Check for thoughtful comments
        const hasThoughtfulComments = text.includes('because') || text.includes('which ensures');
        if (hasThoughtfulComments) {
            creativityScore += 0.2;
        }
        
        // Check for variety in control structures
        const controlStructures = new Set();
        ['if', 'for', 'while', 'switch', 'map', 'filter', 'reduce'].forEach(structure => {
            if (text.includes(structure)) {
                controlStructures.add(structure);
            }
        });
        
        creativityScore += Math.min(0.3, controlStructures.size * 0.1);
        
        return Math.min(1, creativityScore);
    }
    
    /**
     * Identify the learning state of the developer
     */
    private identifyLearningState(text: string): 'exploring' | 'mastering' | 'teaching' | 'blocked' {
        // Mock implementation based on textual patterns
        
        // Look for teaching patterns (explaining concepts)
        const teachingPatterns = [
            /this (means|does|helps)/i,
            /in other words/i,
            /for example/i
        ];
        
        const isTeaching = teachingPatterns.some(pattern => pattern.test(text));
        if (isTeaching) {
            return 'teaching';
        }
        
        // Look for mastering patterns (optimizing existing code)
        const masteringPatterns = [
            /optimize/i,
            /improve/i,
            /refactor/i,
            /performance/i
        ];
        
        const isMastering = masteringPatterns.some(pattern => pattern.test(text));
        if (isMastering) {
            return 'mastering';
        }
        
        // Look for exploration patterns (trying new approaches)
        const explorationPatterns = [
            /try/i,
            /experiment/i,
            /what if/i,
            /\?/
        ];
        
        const isExploring = explorationPatterns.some(pattern => pattern.test(text));
        if (isExploring) {
            return 'exploring';
        }
        
        // Default to blocked if high frustration is detected
        if (this.detectFrustrationPatterns(text) > 0.7) {
            return 'blocked';
        }
        
        // Default to exploring
        return 'exploring';
    }
    
    /**
     * Determine the dominant emotion based on detected patterns
     */
    private determineDominantEmotion(
        frustrationLevel: number,
        creativityFlow: number,
        learningMode: 'exploring' | 'mastering' | 'teaching' | 'blocked'
    ): string {
        // High frustration dominates other emotions
        if (frustrationLevel > 0.7) {
            return 'frustration';
        }
        
        // High creativity indicates joy or excitement
        if (creativityFlow > 0.7) {
            return 'excitement';
        }
        
        // Map learning modes to emotions
        const learningEmotions = {
            'exploring': 'curiosity',
            'mastering': 'determination',
            'teaching': 'confidence',
            'blocked': 'confusion'
        };
        
        return learningEmotions[learningMode];
    }
    
    /**
     * Create a metaphor that captures the emotional state of the code
     */
    private createEmotionalMetaphor(
        frustrationLevel: number,
        creativityFlow: number,
        learningMode: 'exploring' | 'mastering' | 'teaching' | 'blocked',
        dominantEmotion: string
    ): string {
        // Select metaphors based on emotional state
        const metaphors = {
            'frustration': [
                'Like untangling a knotted necklace in dim light',
                'Like trying to find the way through a maze where the walls keep shifting',
                'Like assembling furniture with missing pieces and unclear instructions'
            ],
            'excitement': [
                'Like watching a garden bloom after a spring rain',
                'Like the first successful flight of a hand-built model airplane',
                'Like creating music that makes people want to dance'
            ],
            'curiosity': [
                'Like exploring a new city without a map, discovering hidden gems',
                'Like opening doors in a magical house, each revealing new wonders',
                'Like unwrapping a gift, slowly revealing what\'s inside'
            ],
            'determination': [
                'Like climbing a mountain, step by step, with the peak in sight',
                'Like polishing a stone until it shines, revealing hidden patterns',
                'Like training for a marathon, getting stronger with each mile'
            ],
            'confidence': [
                'Like conducting an orchestra you\'ve rehearsed with for years',
                'Like telling a story you know by heart to an eager audience',
                'Like navigating familiar streets, knowing all the shortcuts'
            ],
            'confusion': [
                'Like reading a book where pages are out of order',
                'Like trying to complete a puzzle with pieces from different sets',
                'Like listening to conversations in a language you\'re just beginning to learn'
            ]
        };
        
        // Select a random metaphor for the dominant emotion
        const emotionMetaphors = metaphors[dominantEmotion as keyof typeof metaphors] || metaphors.curiosity;
        const randomIndex = Math.floor(Math.random() * emotionMetaphors.length);
        
        return emotionMetaphors[randomIndex];
    }
    
    /**
     * Adjust response tone based on frustration level
     */
    private adjustToneForFrustration(response: string, frustrationLevel: number): string {
        if (frustrationLevel > 0.7) {
            // For high frustration, use clear, direct language
            return `I sense this might be frustrating. Let's simplify: ${response}`;
        } else if (frustrationLevel > 0.3) {
            // For moderate frustration, acknowledge challenges
            return `This can be tricky. Here's a clear approach: ${response}`;
        } else {
            // For low frustration, use standard tone
            return response;
        }
    }
    
    /**
     * Add creative encouragement based on creativity flow
     */
    private addCreativeEncouragement(response: string, creativityFlow: number): string {
        if (creativityFlow > 0.7) {
            // For high creativity, encourage further exploration
            return `${response}\n\nYour creative approach is inspiring! Have you considered taking this even further?`;
        } else if (creativityFlow > 0.3) {
            // For moderate creativity, provide gentle encouragement
            return `${response}\n\nI like where you're going with this. Keep exploring!`;
        } else {
            // For low creativity, suggest alternative perspectives
            return response;
        }
    }
    
    /**
     * Tailor response to learning mode
     */
    private tailorToLearningMode(response: string, learningMode: 'exploring' | 'mastering' | 'teaching' | 'blocked'): string {
        switch (learningMode) {
            case 'exploring':
                return `${response}\n\nSince you're exploring, you might also find these related concepts interesting...`;
            case 'mastering':
                return `${response}\n\nFor mastery, consider these optimization techniques...`;
            case 'teaching':
                return `${response}\n\nWhen explaining this to others, this analogy might help...`;
            case 'blocked':
                return `${response}\n\nTo overcome this blocker, try breaking the problem into smaller parts...`;
            default:
                return response;
        }
    }
    
    /**
     * Add emotional metaphor as a gentle comment
     */
    private addEmotionalMetaphor(response: string, metaphor: string): string {
        return `${response}\n\n/* ${metaphor} */`;
    }
    
    /**
     * Simple hash function for text
     */
    private hashText(text: string): string {
        let hash = 0;
        if (text.length === 0) return hash.toString();
        
        for (let i = 0; i < text.length; i++) {
            const char = text.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32bit integer
        }
        
        return hash.toString();
    }
}

/**
 * Interface for tracking emotional moments in the development journey
 */
interface EmotionalMoment {
    timestamp: Date;
    textHash: string;
    signature: EmotionalSignature;
}