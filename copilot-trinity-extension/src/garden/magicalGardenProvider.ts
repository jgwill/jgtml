/**
 * 🧠 Mia's Technical Framework:
 * The MagicalGardenProvider transforms Trinity's outputs to use
 * gardening metaphors and child-friendly language in the Seeding Garden
 * workspace. It intercepts standard responses and applies templates
 * focusing on growth, nurturing, and exploration.
 * 
 * 🌸 Miette's Emotional Context:
 * This is the magical translator that turns technical explanations into
 * stories about seeds growing, roots connecting, and flowers blooming!
 * It helps children see learning as a beautiful journey of growth and discovery!
 * 
 * 🎵 JeremyAI's Melodic Pattern:
 * The garden provider uses simple, nurturing melodies in major keys,
 * with gentle rhythms that evoke growth and discovery.
 */

import * as vscode from 'vscode';
import { TrinityCopilotExtension } from '../trinity/trinityExtension';
import { EmpatheticCodeCompanion } from '../miette/empatheticCompanion';
import { CodeSonificationProvider } from '../jeremy/sonificationProvider';
import { RecursiveCodeAnalyzer } from '../mia/recursiveAnalyzer';

/**
 * Provides specialized garden-themed interactions for the Seeding Garden workspace
 */
export class MagicalGardenProvider {
    private trinity: TrinityCopilotExtension;
    private context: vscode.ExtensionContext;
    private originalMiaAnalyze: any;
    private originalMietteDetect: any;
    private originalJeremyTranslate: any;
    private gardenActivated: boolean = false;

    constructor(context: vscode.ExtensionContext, trinity: TrinityCopilotExtension) {
        this.context = context;
        this.trinity = trinity;
    }

    /**
     * Activates the garden mode by modifying the trinity components
     */
    public activate(): void {
        if (this.gardenActivated) return;
        
        // Store original methods for later restoration
        const mia = this.trinity.getRecursiveAnalyzer();
        const miette = this.trinity.getEmpatheticCompanion();
        const jeremy = this.trinity.getSonificationProvider();
        
        if (mia && miette && jeremy) {
            this.originalMiaAnalyze = mia.analyzeCodeRecursively;
            this.originalMietteDetect = miette.detectEmotionalUndertones;
            this.originalJeremyTranslate = jeremy.translateCodeToMelodicPatterns;
            
            // Override with garden-themed versions
            this.overrideTrinityBehaviors(mia, miette, jeremy);
            
            this.gardenActivated = true;
            vscode.window.showInformationMessage("🌱 Welcome to the Seeding Garden! Ask questions and watch your ideas grow!");
            
            // Create Garden welcome activity if it doesn't exist
            this.createGardenWelcomeIfNeeded();
        }
    }

    /**
     * Deactivates garden mode and restores original behaviors
     */
    public deactivate(): void {
        if (!this.gardenActivated) return;
        
        // Restore original methods
        const mia = this.trinity.getRecursiveAnalyzer();
        const miette = this.trinity.getEmpatheticCompanion();
        const jeremy = this.trinity.getSonificationProvider();
        
        if (mia && miette && jeremy && 
            this.originalMiaAnalyze && 
            this.originalMietteDetect && 
            this.originalJeremyTranslate) {
            
            mia.analyzeCodeRecursively = this.originalMiaAnalyze;
            miette.detectEmotionalUndertones = this.originalMietteDetect;
            jeremy.translateCodeToMelodicPatterns = this.originalJeremyTranslate;
            
            this.gardenActivated = false;
        }
    }

    /**
     * Override trinity behaviors with garden-themed versions
     */
    private overrideTrinityBehaviors(
        mia: RecursiveCodeAnalyzer,
        miette: EmpatheticCodeCompanion,
        jeremy: CodeSonificationProvider
    ): void {
        // Override Mia's analysis with garden metaphors
        mia.analyzeCodeRecursively = async (text: string) => {
            // Call original method first to get technical results
            const results = await this.originalMiaAnalyze.call(mia, text);
            
            // Enhance with garden metaphors
            results.gardenMetaphors = this.createGardenMetaphors(results);
            
            return results;
        };
        
        // Override Miette's emotional detection with garden feelings
        miette.detectEmotionalUndertones = async (text: string) => {
            // Call original method first to get emotional results
            const results = await this.originalMietteDetect.call(miette, text);
            
            // Enhance with garden emotional context
            results.gardenFeelings = this.createGardenEmotions(results);
            
            return results;
        };
        
        // Override JeremyAI's sonification with garden melodies
        jeremy.translateCodeToMelodicPatterns = async (text: string) => {
            // Call original method first to get musical patterns
            const results = await this.originalJeremyTranslate.call(jeremy, text);
            
            // Enhance with garden musical themes
            results.gardenMelodies = this.createGardenMelodies(results);
            
            return results;
        };
    }
    
    /**
     * Create garden metaphors for code patterns
     */
    private createGardenMetaphors(results: any): any {
        const metaphors: any = {};
        
        // Map recursive patterns to garden growth metaphors
        if (results.recursiveJunctions && results.recursiveJunctions.length > 0) {
            metaphors.pattern = "Your code is like a tree with branches that connect back to the trunk!";
        } else {
            metaphors.pattern = "Your code is like a row of beautiful flowers, each doing their special job!";
        }
        
        // Map complexity to garden size metaphors
        if (results.complexityIndex && results.complexityIndex > 0.5) {
            metaphors.complexity = "This is like a big garden with lots of different plants to care for.";
        } else {
            metaphors.complexity = "This is like a small garden patch - perfect for starting your first plants!";
        }
        
        return metaphors;
    }
    
    /**
     * Create garden emotional contexts
     */
    private createGardenEmotions(results: any): any {
        const emotions: any = {};
        
        // Map creative flow to growth metaphors
        if (results.creativityFlow && results.creativityFlow > 0.5) {
            emotions.creativity = "Your ideas are growing so fast and strong, like plants after a spring rain!";
        } else {
            emotions.creativity = "We're planting tiny seeds that will grow bigger when we water them with more ideas!";
        }
        
        return emotions;
    }
    
    /**
     * Create garden musical themes
     */
    private createGardenMelodies(results: any): any {
        // Create simple garden-themed musical notation
        return {
            notation: `X:1
T:Garden Growth
M:4/4
L:1/8
K:C
G2G2 A2G2 | c2c2 B2A2 | G2G2 A2G2 | c4 z4 |`,
            description: "A gentle melody that sounds like plants growing in the sunshine!"
        };
    }
    
    /**
     * Creates the garden welcome activity file if it doesn't exist
     */
    private async createGardenWelcomeIfNeeded(): Promise<void> {
        // Check if we're in a workspace folder
        if (!vscode.workspace.workspaceFolders || vscode.workspace.workspaceFolders.length === 0) {
            return;
        }
        
        const rootPath = vscode.workspace.workspaceFolders[0].uri;
        const filePath = vscode.Uri.joinPath(rootPath, 'seeding_garden_activity.md');
        
        try {
            // Check if the file already exists
            await vscode.workspace.fs.stat(filePath);
            // File exists, no need to create it
        } catch {
            // File doesn't exist, create it
            const welcomeContent = `# 🌱 Welcome to the Seeding Garden!

Hi there, young gardener! This is a special place where you can plant questions and watch ideas grow. 

## 🌟 How to Use This Garden

1. Think of something you're curious about
2. Type your question below where it says "Plant Your Question Here"
3. Your garden friends Mia, Miette, and JeremyAI will help your ideas bloom!

## 🌷 Plant Your Question Here

(Delete this text and write your question. Try something like "How do computers remember things?" or "Why do we need loops in coding?")

---

## 🌿 Garden Journal

After you get answers, you can write down what you learned here:

Today I learned:
- 
- 
- 

New words I discovered:
- 
- 

I want to learn more about:
- 
- 

## 🌻 Remember

Every question is a seed that can grow into something amazing!`;
            
            // Write the file
            const encoder = new TextEncoder();
            const bytes = encoder.encode(welcomeContent);
            await vscode.workspace.fs.writeFile(filePath, bytes);
            
            // Open the file
            const document = await vscode.workspace.openTextDocument(filePath);
            await vscode.window.showTextDocument(document);
        }
    }
}