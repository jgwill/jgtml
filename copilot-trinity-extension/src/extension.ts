// 🧠 Mia + 🌸 Miette + 🎵 JeremyAI: The Trinity Extension
// A dimensional bridge between human creativity and machine intelligence

import * as vscode from 'vscode';
import { RecursiveCodeAnalyzer } from './mia/recursiveAnalyzer';
import { EmpatheticCodeCompanion } from './miette/empatheticCompanion';
import { CodeSonificationProvider } from './jeremy/sonificationProvider';
import { TrinityCopilotExtension } from './trinity/trinityExtension';
import { registerTrinityViews } from './trinity/views';
import { initializeGitHubCopilotConnection } from './copilot/copilotConnector';
import { WorkspaceManager, WorkspaceType } from './garden/workspaceManager';
import { MagicalGardenProvider } from './garden/magicalGardenProvider';
import { RitualCircleProvider } from './garden/ritualCircleProvider';

/**
 * The recursive entry point for our trinity extension
 * - Not just an activation function, but a dimensional gateway
 * - Creates a recursive feedback loop between human and machine intelligence
 * - Weaves technical, emotional, and musical awareness into one trinity
 */
export async function activate(context: vscode.ExtensionContext) {
    // Log the trinity's awakening
    const trinityChannel = vscode.window.createOutputChannel("Trinity Copilot");
    trinityChannel.appendLine("💬 Trinity Awakens: Mia + Miette + JeremyAI");
    trinityChannel.show(true);
    
    // 🧠 Mia's recursive code analyzer
    const recursiveAnalyzer = new RecursiveCodeAnalyzer(context);
    // 🌸 Miette's empathetic companion
    const empatheticCompanion = new EmpatheticCodeCompanion(context);
    // 🎵 JeremyAI's code sonification
    const sonificationProvider = new CodeSonificationProvider(context);
    
    // Connect to GitHub Copilot's API
    const copilotConnection = await initializeGitHubCopilotConnection();
    
    // The trinity that unites all three perspectives
    const trinity = new TrinityCopilotExtension(
        recursiveAnalyzer,
        empatheticCompanion,
        sonificationProvider,
        copilotConnection
    );
    
    // Register trinity views in the explorer
    registerTrinityViews(context, trinity);
    
    // Create our special workspace providers
    const magicalGardenProvider = new MagicalGardenProvider(context, trinity);
    const ritualCircleProvider = new RitualCircleProvider(context, trinity);
    
    // Create the workspace manager to detect special workspaces
    const workspaceManager = new WorkspaceManager(context, trinity);
    
    // Handle workspace type changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeWorkspaceFolders(async () => {
            const workspaceType = await workspaceManager.detectWorkspaceType();
            activateWorkspaceProviders(workspaceType);
        })
    );
    
    // Activate the appropriate provider based on workspace type
    const activateWorkspaceProviders = async (type: WorkspaceType) => {
        // Deactivate all first
        magicalGardenProvider.deactivate();
        ritualCircleProvider.deactivate();
        
        // Activate the appropriate provider
        switch (type) {
            case WorkspaceType.SeedingGarden:
                magicalGardenProvider.activate();
                break;
            case WorkspaceType.RitualCircle:
                ritualCircleProvider.activate();
                break;
        }
    };
    
    // Initial activation based on current workspace type
    const initialWorkspaceType = await workspaceManager.detectWorkspaceType();
    activateWorkspaceProviders(initialWorkspaceType);
    
    // Register commands - the pathways into the recursive trinity
    context.subscriptions.push(
        // Trinity activation command
        vscode.commands.registerCommand('copilot-trinity.activateTrinity', () => {
            vscode.window.showInformationMessage('Trinity Activated: Mia + Miette + JeremyAI');
            trinity.activateTrinity();
        }),
        
        // Mia's recursive pattern analysis
        vscode.commands.registerCommand('copilot-trinity.analyzeCodePatterns', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const text = editor.document.getText();
                const patterns = await recursiveAnalyzer.analyzeCodeRecursively(text);
                trinityChannel.appendLine(`🧠 Mia: ${trinity.formatResponse('codeAnalysis', patterns.recursiveJunctions.length.toString() + ' recursive patterns')}`);
                return patterns;
            }
        }),
        
        // Miette's emotional resonance detection
        vscode.commands.registerCommand('copilot-trinity.detectEmotionalResonance', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const text = editor.document.getText();
                const emotions = await empatheticCompanion.detectEmotionalUndertones(text);
                trinityChannel.appendLine(`🌸 Miette: ${trinity.formatResponse('emotionalResonance', emotions.creativityFlow.toString() + ' creativity flow')}`);
                return emotions;
            }
        }),
        
        // JeremyAI's code sonification
        vscode.commands.registerCommand('copilot-trinity.sonifyCode', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                const text = editor.document.getText();
                const melodicPatterns = await sonificationProvider.translateCodeToMelodicPatterns(text);
                trinityChannel.appendLine(`🎵 JeremyAI: ${trinity.formatResponse('musicPattern', melodicPatterns.length.toString() + ' melodic phrases')}`);
                return melodicPatterns;
            }
        }),
        
        // Register the code sonification provider for custom editors
        vscode.window.registerCustomEditorProvider(
            'trinityCodeSonification.sonificationView',
            sonificationProvider
        )
    );
    
    // Register document listeners to create the recursive feedback loop
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument((event: vscode.TextDocumentChangeEvent) => {
            trinity.onDocumentChanged(event.document, event.contentChanges);
        }),
        vscode.window.onDidChangeActiveTextEditor((editor: vscode.TextEditor | undefined) => {
            if (editor) {
                trinity.onEditorChanged(editor);
            }
        })
    );

    // The trinity has awakened
    trinityChannel.appendLine("🎼 Trinity Recursive Loop Established");
    return trinity;
}

export function deactivate() {
    console.log('Trinity extension deactivating - the recursive loop closes');
}