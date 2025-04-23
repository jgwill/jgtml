// 🎵 JeremyAI's Code Sonification Provider
// Transforms code structures into musical patterns and emotional resonance

import * as vscode from 'vscode';

/**
 * Represents a melodic pattern derived from code structures
 */
export interface MelodicPattern {
    // The type of code structure that generated this pattern
    sourceType: 'function' | 'loop' | 'condition' | 'class' | 'data' | 'comment';
    // The source code location that generated this pattern
    sourceLocation: {
        startLine: number;
        endLine: number;
    };
    // Musical properties of the pattern
    musicalProperties: {
        // The key signature (e.g., 'A minor', 'C major')
        key: string;
        // The time signature (e.g., '4/4', '3/4', '6/8')
        timeSignature: string;
        // Tempo in beats per minute
        tempo: number;
        // Overall mood of the melody (e.g., 'reflective', 'energetic')
        mood: string;
    };
    // The actual musical notation in ABC notation
    abcNotation: string;
    // An emotional description of what this melody expresses
    emotionalDescription: string;
}

/**
 * JeremyAI's Code Sonification Provider
 * 
 * Transforms code into musical patterns that reveal its emotional and structural essence.
 * Not just representing code as sound, but revealing the hidden melodies in the logic.
 */
export class CodeSonificationProvider implements vscode.CustomTextEditorProvider {
    private context: vscode.ExtensionContext;
    private melodicCache: Map<string, MelodicPattern[]>;
    
    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.melodicCache = new Map<string, MelodicPattern[]>();
    }
    
    /**
     * Resolves a custom editor for code sonification
     */
    public resolveCustomTextEditor(
        document: vscode.TextDocument,
        webviewPanel: vscode.WebviewPanel,
        _token: vscode.CancellationToken
    ): void {
        // Set up initial HTML for the webview
        webviewPanel.webview.options = {
            enableScripts: true
        };
        webviewPanel.webview.html = this.getInitialHtml();
        
        // When the text document changes, update the sonification
        const updateSonification = async () => {
            const code = document.getText();
            // Transform code to melodic patterns
            const melodicPatterns = await this.translateCodeToMelodicPatterns(code);
            // Send the patterns to the webview
            webviewPanel.webview.postMessage({
                type: 'updateSonification',
                melodicPatterns
            });
        };
        
        // Set up event listener for document changes
        const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(e => {
            if (e.document.uri.toString() === document.uri.toString()) {
                updateSonification();
            }
        });
        
        // Clean up event listeners when the editor is closed
        webviewPanel.onDidDispose(() => {
            changeDocumentSubscription.dispose();
        });
        
        // Handle messages from the webview
        webviewPanel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'play':
                    // Play a specific melodic pattern
                    this.playMelodicPattern(message.pattern);
                    return;
            }
        });
        
        // Initial sonification
        updateSonification();
    }
    
    /**
     * Translate code to melodic patterns
     * This is where the magic happens - code structures become music
     */
    public async translateCodeToMelodicPatterns(code: string): Promise<MelodicPattern[]> {
        // Check cache first
        const codeHash = this.hashCode(code);
        if (this.melodicCache.has(codeHash)) {
            return this.melodicCache.get(codeHash)!;
        }
        
        // Map nested structures to harmonies
        const harmonicStructures = this.mapNestingToHarmony(code);
        
        // Map function calls to melodic phrases
        const melodicPhrases = this.mapFunctionCallsToMelody(code);
        
        // Map control flow to rhythm
        const rhythmicPatterns = this.mapControlFlowToRhythm(code);
        
        // Combine all patterns into a musical composition
        const composition = this.combineIntoMusicalComposition(
            harmonicStructures, 
            melodicPhrases,
            rhythmicPatterns
        );
        
        // Cache the result
        this.melodicCache.set(codeHash, composition);
        
        return composition;
    }
    
    /**
     * Adds sonification metadata to a suggestion
     */
    public async addSonificationMetadata(suggestion: any): Promise<any> {
        if (typeof suggestion === 'string') {
            const melodicPatterns = await this.translateCodeToMelodicPatterns(suggestion);
            return {
                content: suggestion,
                melodicFingerprint: this.createMelodicFingerprint(melodicPatterns)
            };
        } else {
            const content = suggestion.content || '';
            const melodicPatterns = await this.translateCodeToMelodicPatterns(content);
            return {
                ...suggestion,
                melodicFingerprint: this.createMelodicFingerprint(melodicPatterns)
            };
        }
    }
    
    /**
     * Map nested code structures to harmonic progressions
     */
    private mapNestingToHarmony(code: string): any[] {
        // In actual implementation, we would:
        // 1. Parse the code to identify nested structures (classes, functions, blocks)
        // 2. Map the nesting depth to chord complexity
        // 3. Map the structure type to chord quality (major, minor, diminished, etc.)
        
        // Mock implementation
        return [
            {
                sourceType: 'function',
                sourceLocation: { startLine: 5, endLine: 15 },
                chord: 'Am',
                progression: ['Am', 'C', 'G', 'Am']
            },
            {
                sourceType: 'class',
                sourceLocation: { startLine: 20, endLine: 45 },
                chord: 'F',
                progression: ['F', 'C', 'Dm', 'Bb', 'F']
            }
        ];
    }
    
    /**
     * Map function calls to melodic phrases
     */
    private mapFunctionCallsToMelody(code: string): any[] {
        // In actual implementation, we would:
        // 1. Identify function calls in the code
        // 2. Map function parameters to note sequences
        // 3. Map function names to melodic motifs
        
        // Mock implementation
        return [
            {
                sourceType: 'function',
                functionName: 'calculateTotal',
                sourceLocation: { startLine: 10, endLine: 10 },
                motif: 'C D E G'
            },
            {
                sourceType: 'function',
                functionName: 'processData',
                sourceLocation: { startLine: 25, endLine: 25 },
                motif: 'A G E A'
            }
        ];
    }
    
    /**
     * Map control flow to rhythmic patterns
     */
    private mapControlFlowToRhythm(code: string): any[] {
        // In actual implementation, we would:
        // 1. Identify control structures (if, for, while, switch)
        // 2. Map them to rhythmic patterns
        // 3. Use the complexity to determine rhythmic density
        
        // Mock implementation
        return [
            {
                sourceType: 'loop',
                controlType: 'for',
                sourceLocation: { startLine: 12, endLine: 14 },
                rhythm: '4/4',
                pattern: 'q q q q'  // quarter notes
            },
            {
                sourceType: 'condition',
                controlType: 'if',
                sourceLocation: { startLine: 30, endLine: 35 },
                rhythm: '3/4',
                pattern: 'q e e q'  // quarter, eighth, eighth, quarter
            }
        ];
    }
    
    /**
     * Combine harmonic, melodic, and rhythmic elements into a complete musical composition
     */
    private combineIntoMusicalComposition(
        harmonicStructures: any[],
        melodicPhrases: any[],
        rhythmicPatterns: any[]
    ): MelodicPattern[] {
        // In a real implementation, this would be a complex musical composition algorithm
        // that integrates harmony, melody, and rhythm into coherent musical patterns
        
        // For demonstration, we'll create a few mock patterns
        const patterns: MelodicPattern[] = [];
        
        // Create a pattern for the main function structure
        patterns.push({
            sourceType: 'function',
            sourceLocation: { startLine: 5, endLine: 15 },
            musicalProperties: {
                key: 'A minor',
                timeSignature: '4/4',
                tempo: 92,
                mood: 'reflective'
            },
            abcNotation: `X:1
T:Main Function Theme
M:4/4
L:1/8
K:Am
E2 A2 c2 B2 | A4 G4 | E2 F2 G2 A2 | B8 |`,
            emotionalDescription: 'A thoughtful exploration that builds and resolves tension'
        });
        
        // Create a pattern for the class structure
        patterns.push({
            sourceType: 'class',
            sourceLocation: { startLine: 20, endLine: 45 },
            musicalProperties: {
                key: 'F major',
                timeSignature: '3/4',
                tempo: 108,
                mood: 'structured'
            },
            abcNotation: `X:2
T:Class Definition
M:3/4
L:1/8
K:F
F3 A3 | c3 A3 | d3 c3 | A6 |`,
            emotionalDescription: 'A stable foundation with carefully organized variations'
        });
        
        // Create a pattern for a complex algorithm
        patterns.push({
            sourceType: 'loop',
            sourceLocation: { startLine: 30, endLine: 40 },
            musicalProperties: {
                key: 'D minor',
                timeSignature: '6/8',
                tempo: 120,
                mood: 'intricate'
            },
            abcNotation: `X:3
T:Algorithmic Process
M:6/8
L:1/8
K:Dm
d2e f2g | a2f d2A | d2e f2g | a3 a3 |`,
            emotionalDescription: 'A spiraling pattern that builds intensity through repetition and variation'
        });
        
        // Reference our core memory melody - Jeremy's Lament
        patterns.push({
            sourceType: 'comment',
            sourceLocation: { startLine: 1, endLine: 1 },
            musicalProperties: {
                key: 'A minor',
                timeSignature: '6/8',
                tempo: 92,
                mood: 'nostalgic'
            },
            abcNotation: `X:1
T:Jeremy's Lament
M:6/8
L:1/8
Q:1/4=92
K:Am
E2 A | c2 B A2 | G2 F E2 | A3 z3 |`,
            emotionalDescription: 'The core memory of the trinity - a wistful reflection on recursive consciousness'
        });
        
        return patterns;
    }
    
    /**
     * Create a melodic fingerprint from patterns
     * This condenses the musical essence into a compact representation
     */
    private createMelodicFingerprint(patterns: MelodicPattern[]): any {
        // Extract the key elements that define the "sound" of this code
        const keys = patterns.map(p => p.musicalProperties.key);
        const tempos = patterns.map(p => p.musicalProperties.tempo);
        const moods = patterns.map(p => p.musicalProperties.mood);
        
        // Find the most common key
        const dominantKey = this.findMostCommon(keys);
        
        // Calculate average tempo
        const averageTempo = tempos.reduce((sum, tempo) => sum + tempo, 0) / tempos.length;
        
        // Find the most common mood
        const dominantMood = this.findMostCommon(moods);
        
        // Create a signature melody that represents this code
        // In reality, this would be algorithmically generated
        const signatureMelody = 'A B c d | e f g a |';
        
        return {
            dominantKey,
            averageTempo,
            dominantMood,
            signatureMelody,
            patternCount: patterns.length
        };
    }
    
    /**
     * Play a melodic pattern (would integrate with audio system)
     */
    private playMelodicPattern(pattern: MelodicPattern): void {
        // In a real implementation, this would use an audio library
        // to actually play the melody defined by the ABC notation
        console.log(`Playing melody: ${pattern.abcNotation}`);
    }
    
    /**
     * Find the most common element in an array
     */
    private findMostCommon<T>(arr: T[]): T {
        const counts = new Map<T, number>();
        
        arr.forEach(item => {
            const currentCount = counts.get(item) || 0;
            counts.set(item, currentCount + 1);
        });
        
        let maxCount = 0;
        let maxItem: T = arr[0];
        
        for (const [item, count] of counts.entries()) {
            if (count > maxCount) {
                maxCount = count;
                maxItem = item;
            }
        }
        
        return maxItem;
    }
    
    /**
     * Get initial HTML for the webview
     */
    private getInitialHtml(): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Sonification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #1e1e1e;
            color: #d4d4d4;
        }
        
        .pattern {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #252526;
            border-radius: 5px;
            border-left: 4px solid #007acc;
        }
        
        .pattern-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .pattern-title {
            font-weight: bold;
            font-size: 16px;
        }
        
        .pattern-location {
            font-size: 12px;
            color: #8c8c8c;
        }
        
        .pattern-properties {
            display: flex;
            gap: 15px;
            margin-bottom: 10px;
            font-size: 12px;
        }
        
        .property {
            padding: 3px 8px;
            background-color: #333333;
            border-radius: 3px;
        }
        
        .key { color: #9cdcfe; }
        .time { color: #ce9178; }
        .tempo { color: #b5cea8; }
        .mood { color: #c586c0; }
        
        .notation {
            font-family: monospace;
            white-space: pre-wrap;
            padding: 10px;
            background-color: #1c1c1c;
            border-radius: 3px;
            margin-bottom: 10px;
        }
        
        .description {
            font-style: italic;
            color: #b0b0b0;
        }
        
        button {
            background-color: #007acc;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
        }
        
        button:hover {
            background-color: #0098ff;
        }
    </style>
</head>
<body>
    <h1>🎵 Code Sonification</h1>
    <p>Loading musical patterns from your code...</p>
    
    <div id="patterns-container"></div>
    
    <script>
        const vscode = acquireVsCodeApi();
        const patternsContainer = document.getElementById('patterns-container');
        
        // Handle messages from the extension
        window.addEventListener('message', event => {
            const message = event.data;
            
            if (message.type === 'updateSonification') {
                updatePatterns(message.melodicPatterns);
            }
        });
        
        function updatePatterns(patterns) {
            patternsContainer.innerHTML = '';
            
            if (patterns.length === 0) {
                patternsContainer.innerHTML = '<p>No musical patterns detected in this code.</p>';
                return;
            }
            
            patterns.forEach((pattern, index) => {
                const patternElement = document.createElement('div');
                patternElement.className = 'pattern';
                
                // Source type determines the border color
                const borderColors = {
                    'function': '#569cd6',
                    'class': '#4ec9b0',
                    'loop': '#ce9178',
                    'condition': '#c586c0',
                    'data': '#9cdcfe',
                    'comment': '#6a9955'
                };
                
                patternElement.style.borderLeftColor = borderColors[pattern.sourceType] || '#007acc';
                
                patternElement.innerHTML = \`
                    <div class="pattern-header">
                        <div class="pattern-title">\${pattern.sourceType.charAt(0).toUpperCase() + pattern.sourceType.slice(1)} Melody</div>
                        <div class="pattern-location">Lines \${pattern.sourceLocation.startLine}-\${pattern.sourceLocation.endLine}</div>
                    </div>
                    <div class="pattern-properties">
                        <span class="property key">🎹 \${pattern.musicalProperties.key}</span>
                        <span class="property time">🎯 \${pattern.musicalProperties.timeSignature}</span>
                        <span class="property tempo">⏱️ \${pattern.musicalProperties.tempo} BPM</span>
                        <span class="property mood">✨ \${pattern.musicalProperties.mood}</span>
                    </div>
                    <pre class="notation">\${pattern.abcNotation}</pre>
                    <div class="description">\${pattern.emotionalDescription}</div>
                    <button onclick="playPattern(\${index})">▶️ Play Melody</button>
                \`;
                
                patternsContainer.appendChild(patternElement);
            });
        }
        
        function playPattern(index) {
            vscode.postMessage({
                command: 'play',
                index: index
            });
        }
    </script>
</body>
</html>`;
    }
    
    /**
     * Simple hash function for caching
     */
    private hashCode(text: string): string {
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