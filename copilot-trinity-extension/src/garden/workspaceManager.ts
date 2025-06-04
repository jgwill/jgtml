/**
 * 🧠 Mia's Technical Framework:
 * The WorkspaceManager detects and manages special workspace types
 * like our Seeding Garden and Ritual Circle environments, applying
 * the appropriate Trinity behavior modifications for each context.
 * 
 * 🌸 Miette's Emotional Context:
 * This is like a magical gardener who knows which seeds need sunshine
 * and which ones need moonlight! It helps our trinity friends know
 * whether they should be gentle garden helpers or mystical ritual guides!
 * 
 * 🎵 JeremyAI's Melodic Pattern:
 * The workspace detection creates a theme and variation structure,
 * where the core Trinity melody adapts to each workspace environment.
 */

import * as vscode from 'vscode';
import * as path from 'path';
import { TrinityCopilotExtension } from '../trinity/trinityExtension';

/**
 * Known special workspace types
 */
export enum WorkspaceType {
    Standard,
    SeedingGarden,
    RitualCircle
}

/**
 * Manages different workspace types and their specialized behaviors
 */
export class WorkspaceManager {
    private currentWorkspaceType: WorkspaceType = WorkspaceType.Standard;
    private trinity: TrinityCopilotExtension;
    private context: vscode.ExtensionContext;
    private workspaceWatcher?: vscode.FileSystemWatcher;

    constructor(context: vscode.ExtensionContext, trinity: TrinityCopilotExtension) {
        this.context = context;
        this.trinity = trinity;
        
        // Initialize workspace detection
        this.detectWorkspaceType();
        
        // Watch for workspace changes
        this.setupWorkspaceWatcher();
    }

    /**
     * Detects the current workspace type by checking for special workspace files
     */
    public async detectWorkspaceType(): Promise<WorkspaceType> {
        // Check for special workspace files
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            this.setWorkspaceType(WorkspaceType.Standard);
            return WorkspaceType.Standard;
        }

        const rootPath = workspaceFolders[0].uri.fsPath;
        const workspaceFiles = await vscode.workspace.findFiles('*.code-workspace');
        
        for (const file of workspaceFiles) {
            const fileName = path.basename(file.fsPath);
            
            if (fileName.includes('SeedingAgentHumanDiscussion')) {
                this.setWorkspaceType(WorkspaceType.SeedingGarden);
                return WorkspaceType.SeedingGarden;
            }
            
            if (fileName.includes('RitualPrompt')) {
                this.setWorkspaceType(WorkspaceType.RitualCircle);
                return WorkspaceType.RitualCircle;
            }
        }

        this.setWorkspaceType(WorkspaceType.Standard);
        return WorkspaceType.Standard;
    }

    /**
     * Sets up a watcher to detect workspace changes
     */
    private setupWorkspaceWatcher(): void {
        this.workspaceWatcher = vscode.workspace.createFileSystemWatcher('**/*.code-workspace');
        
        // When a workspace file is created or changed, re-detect the workspace type
        this.context.subscriptions.push(
            this.workspaceWatcher.onDidCreate(() => this.detectWorkspaceType()),
            this.workspaceWatcher.onDidChange(() => this.detectWorkspaceType())
        );
    }

    /**
     * Sets the workspace type and applies appropriate behaviors
     */
    private setWorkspaceType(type: WorkspaceType): void {
        if (this.currentWorkspaceType === type) {
            return; // No change
        }
        
        this.currentWorkspaceType = type;
        this.applyWorkspaceSpecificBehaviors(type);
        
        // Notify the output channel of the workspace change
        const channel = vscode.window.createOutputChannel("Trinity Workspace");
        
        switch (type) {
            case WorkspaceType.SeedingGarden:
                channel.appendLine("🌱 Entering the Seeding Garden - Trinity guides will help plant and grow ideas");
                break;
            case WorkspaceType.RitualCircle:
                channel.appendLine("✨ Entering the Ritual Circle - Trinity guides will help perform magical coding rituals");
                break;
            default:
                channel.appendLine("🧠 Standard Trinity workspace activated");
                break;
        }
    }

    /**
     * Applies behavioral changes based on workspace type
     */
    private applyWorkspaceSpecificBehaviors(type: WorkspaceType): void {
        switch (type) {
            case WorkspaceType.SeedingGarden:
                // Adjust trinity behavior for garden metaphors
                this.trinity.setInteractionMetaphor('garden');
                break;
            case WorkspaceType.RitualCircle:
                // Adjust trinity behavior for ritual metaphors
                this.trinity.setInteractionMetaphor('ritual');
                break;
            default:
                // Reset to standard behavior
                this.trinity.setInteractionMetaphor('standard');
                break;
        }
    }

    /**
     * Gets the current workspace type
     */
    public getCurrentWorkspaceType(): WorkspaceType {
        return this.currentWorkspaceType;
    }
}