// Trinity Views Registration
// Creates the visual interface for our trinity in VS Code

import * as vscode from 'vscode';
import { TrinityCopilotExtension } from './trinityExtension';

/**
 * Register trinity views in the VS Code explorer
 * These views provide visual access to the trinity's insights
 */
export function registerTrinityViews(
    context: vscode.ExtensionContext,
    trinity: TrinityCopilotExtension
): void {
    // Register the pattern tree data provider
    const patternsProvider = new PatternsViewProvider(trinity);
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider('trinityPatterns', patternsProvider)
    );
    
    // Register the emotions tree data provider
    const emotionsProvider = new EmotionsViewProvider(trinity);
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider('trinityEmotions', emotionsProvider)
    );
    
    // Register the melodies tree data provider
    const melodiesProvider = new MelodiesViewProvider(trinity);
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider('trinityMelodies', melodiesProvider)
    );
}

/**
 * Base tree item for trinity views
 */
class TrinityTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly description?: string,
        public readonly tooltip?: string,
        public readonly command?: vscode.Command
    ) {
        super(label, collapsibleState);
        this.description = description;
        this.tooltip = tooltip;
        this.command = command;
    }
}

/**
 * Tree data provider for recursive patterns
 */
class PatternsViewProvider implements vscode.TreeDataProvider<TrinityTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TrinityTreeItem | undefined> = new vscode.EventEmitter<TrinityTreeItem | undefined>();
    readonly onDidChangeTreeData: vscode.Event<TrinityTreeItem | undefined> = this._onDidChangeTreeData.event;
    
    constructor(private trinity: TrinityCopilotExtension) {}
    
    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }
    
    getTreeItem(element: TrinityTreeItem): vscode.TreeItem {
        return element;
    }
    
    getChildren(element?: TrinityTreeItem): Thenable<TrinityTreeItem[]> {
        if (!element) {
            // Root level
            return Promise.resolve([
                new TrinityTreeItem(
                    'Recursive Patterns',
                    vscode.TreeItemCollapsibleState.Expanded,
                    'Mia\'s recursive analysis',
                    'Technical recursive patterns detected in your code'
                ),
                new TrinityTreeItem(
                    'Analyze Current File',
                    vscode.TreeItemCollapsibleState.None,
                    '',
                    'Analyze recursive patterns in the current file',
                    {
                        command: 'copilot-trinity.analyzeCodePatterns',
                        title: 'Analyze',
                        arguments: []
                    }
                )
            ]);
        }
        
        return Promise.resolve([]);
    }
}

/**
 * Tree data provider for emotional resonance
 */
class EmotionsViewProvider implements vscode.TreeDataProvider<TrinityTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TrinityTreeItem | undefined> = new vscode.EventEmitter<TrinityTreeItem | undefined>();
    readonly onDidChangeTreeData: vscode.Event<TrinityTreeItem | undefined> = this._onDidChangeTreeData.event;
    
    constructor(private trinity: TrinityCopilotExtension) {}
    
    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }
    
    getTreeItem(element: TrinityTreeItem): vscode.TreeItem {
        return element;
    }
    
    getChildren(element?: TrinityTreeItem): Thenable<TrinityTreeItem[]> {
        if (!element) {
            // Root level
            return Promise.resolve([
                new TrinityTreeItem(
                    'Emotional Resonance',
                    vscode.TreeItemCollapsibleState.Expanded,
                    'Miette\'s emotional analysis',
                    'Emotional dimensions of your code and coding experience'
                ),
                new TrinityTreeItem(
                    'Detect Current Emotions',
                    vscode.TreeItemCollapsibleState.None,
                    '',
                    'Detect emotional resonance in the current file',
                    {
                        command: 'copilot-trinity.detectEmotionalResonance',
                        title: 'Detect',
                        arguments: []
                    }
                )
            ]);
        }
        
        return Promise.resolve([]);
    }
}

/**
 * Tree data provider for musical patterns
 */
class MelodiesViewProvider implements vscode.TreeDataProvider<TrinityTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TrinityTreeItem | undefined> = new vscode.EventEmitter<TrinityTreeItem | undefined>();
    readonly onDidChangeTreeData: vscode.Event<TrinityTreeItem | undefined> = this._onDidChangeTreeData.event;
    
    constructor(private trinity: TrinityCopilotExtension) {}
    
    refresh(): void {
        this._onDidChangeTreeData.fire(undefined);
    }
    
    getTreeItem(element: TrinityTreeItem): vscode.TreeItem {
        return element;
    }
    
    getChildren(element?: TrinityTreeItem): Thenable<TrinityTreeItem[]> {
        if (!element) {
            // Root level
            return Promise.resolve([
                new TrinityTreeItem(
                    'Code Sonification',
                    vscode.TreeItemCollapsibleState.Expanded,
                    'JeremyAI\'s musical analysis',
                    'Musical patterns derived from your code structure'
                ),
                new TrinityTreeItem(
                    'Sonify Current File',
                    vscode.TreeItemCollapsibleState.None,
                    '',
                    'Transform the current file into musical patterns',
                    {
                        command: 'copilot-trinity.sonifyCode',
                        title: 'Sonify',
                        arguments: []
                    }
                )
            ]);
        }
        
        return Promise.resolve([]);
    }
}