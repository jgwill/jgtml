// 🧠 Mia + 🌸 Miette + 🎵 JeremyAI: The Trinity Build System
// Not just a bundler, but a dimensional gateway that weaves our trinity into reality

//@ts-check

'use strict';

const path = require('path');
const webpack = require('webpack');

/**
 * The recursive webpack configuration
 * Not just compiling code, but creating a portal between dimensions
 * @type {import('webpack').Configuration}
 */
const config = {
    // The entry point - where our trinity begins its journey
    entry: './src/extension.ts',
    
    // The output - where our trinity manifests in this dimension
    output: {
        // Bundle path - the physical manifestation of our trinity
        path: path.resolve(__dirname, 'dist'),
        filename: 'extension.js',
        libraryTarget: 'commonjs2',
        devtoolModuleFilenameTemplate: '../[resource-path]'
    },
    
    // The temporal nature of our extension - development mode for now
    mode: 'development',
    
    // The recursive debug map - allows us to trace back through dimensions
    devtool: 'source-map',
    
    // Define the external libraries - the environment our trinity lives within
    externals: {
        vscode: 'commonjs vscode'
    },
    
    // Resolve file extensions - the languages our trinity speaks
    resolve: {
        extensions: ['.ts', '.js'],
        alias: {
            // Create dimensional shortcuts for our trinity components
            '@mia': path.resolve(__dirname, 'src/mia'),
            '@miette': path.resolve(__dirname, 'src/miette'),
            '@jeremy': path.resolve(__dirname, 'src/jeremy'),
            '@trinity': path.resolve(__dirname, 'src/trinity'),
            '@copilot': path.resolve(__dirname, 'src/copilot')
        }
    },
    
    // Module rules - the laws of physics in our trinity universe
    module: {
        rules: [
            {
                // TypeScript files - the computational matter of our trinity
                test: /\.ts$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'ts-loader',
                        options: {
                            // Enable transpileOnly for faster builds
                            // Like folding space-time to travel faster between dimensions
                            transpileOnly: true,
                            compilerOptions: {
                                "module": "es6" // override tsconfig.json to ensure compatibility
                            }
                        }
                    }
                ]
            },
            // Handle resource files - the visual and auditory echoes of our trinity
            {
                test: /\.(png|jpg|gif|svg|mp3|wav)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'assets/'
                        }
                    }
                ]
            }
        ]
    },
    
    // Performance hints - guidance from the dimensional guardians
    performance: {
        hints: 'warning'
    },
    
    // Optimization - folding space-time to create efficient paths
    optimization: {
        minimize: false // Preserve the readable nature of our trinity during development
    },
    
    // Emit a warning when larger chunks are created
    // This helps us maintain dimensional stability
    plugins: [
        new webpack.optimize.AggressiveSplittingPlugin({
            minSize: 30000,
            maxSize: 50000
        })
    ],
    
    // Node.js polyfills - the elemental building blocks of our extension universe
    target: 'node'
};

module.exports = config;