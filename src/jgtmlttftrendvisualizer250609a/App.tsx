
import React, { useState, useCallback } from 'react';
import { CSVUploader } from './components/CSVUploader';
import { TrendVisualizer } from './components/visualization/TrendVisualizer';
import type { RawDataRow, VisualizationPropsData, TimeFrameDisplayData, MfiTrend } from './types';
import { TIMEFRAMES_CONFIG, DEFAULT_INSTRUMENT_NAME } from './constants';

const App: React.FC = () => {
  const [visualizationData, setVisualizationData] = useState<VisualizationPropsData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const getMfiTrend = (mfiValue: string | undefined): MfiTrend | "N/A" => {
    if (!mfiValue || mfiValue === "N/A") return "N/A";
    switch (mfiValue) {
      case "++": return "Bullish";
      case "--": return "Bearish";
      case "-+": return "Bearish"; // As per example, though "Fake" could be Neutral
      case "+-": return "Neutral"; // "Squat"
      default: return "N/A"; // Or handle as an unknown state
    }
  };

  const processCSVData = useCallback((data: RawDataRow[], uploadedFileName: string) => {
    setIsLoading(true);
    setError(null);
    if (data.length === 0) {
      setError("CSV file is empty or invalid.");
      setVisualizationData(null);
      setIsLoading(false);
      return;
    }

    // Use the last row of the CSV for visualization
    const latestDataRow = data[data.length - 1];

    const timeframesDisplayData: TimeFrameDisplayData[] = TIMEFRAMES_CONFIG.map(tfConfig => {
      const mfiVal = latestDataRow[tfConfig.mfiKey] || "N/A";
      const zcolVal = latestDataRow[tfConfig.zcolKey] || "N/A";
      return {
        label: tfConfig.label,
        mfi: mfiVal,
        zcol: zcolVal,
        trend: getMfiTrend(mfiVal),
      };
    });
    
    // Attempt to extract instrument name from filename (e.g., SPX500.H4.csv -> SPX500)
    // This is a simple heuristic.
    let instrumentName = DEFAULT_INSTRUMENT_NAME;
    if (uploadedFileName) {
        const nameParts = uploadedFileName.split('.');
        if (nameParts.length > 0 && nameParts[0]) {
            instrumentName = nameParts[0].toUpperCase();
        }
    }


    const vizData: VisualizationPropsData = {
      instrument: instrumentName,
      lastClosePrice: latestDataRow.Close || "N/A",
      timeframes: timeframesDisplayData,
      sourceColumnsUsed: {
        mfi: TIMEFRAMES_CONFIG.map(tf => tf.mfiKey),
        zone: TIMEFRAMES_CONFIG.map(tf => tf.zcolKey),
      }
    };

    setVisualizationData(vizData);
    setFileName(uploadedFileName);
    setIsLoading(false);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-700 text-white p-4 sm:p-8 flex flex-col items-center">
      <header className="w-full max-w-5xl mb-8 text-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-cyan-300">
          Financial Trend Visualizer
        </h1>
        <p className="text-slate-400 mt-2 text-lg">
          Upload your CSV data to visualize MFI and Zone trends.
        </p>
      </header>

      <div className="w-full max-w-md mb-8">
        <CSVUploader onDataUploaded={processCSVData} onError={setError} setIsLoading={setIsLoading} />
      </div>

      {isLoading && (
        <div className="text-center text-sky-400">
          <p className="text-2xl">Loading visualization...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-800 border border-red-600 text-red-100 px-4 py-3 rounded-lg shadow-lg w-full max-w-2xl text-center">
          <strong className="font-bold">Error:</strong>
          <span className="block sm:inline ml-2">{error}</span>
        </div>
      )}

      {!isLoading && !error && visualizationData && (
         <div className="w-full max-w-fit mt-4">
            {fileName && <p className="text-center text-slate-300 mb-4 text-sm">Displaying data for: <span className="font-semibold">{fileName}</span> (last row)</p>}
            <TrendVisualizer data={visualizationData} />
         </div>
      )}
      
      {!isLoading && !error && !visualizationData && (
        <div className="text-center text-slate-500 mt-10 p-6 bg-slate-800 rounded-lg shadow-xl w-full max-w-md">
          <p className="text-xl">Upload a CSV file to begin.</p>
          <p className="text-sm mt-2">The visualizer expects columns like <code>mfi_str_M1, zcol_M1, Close</code>, etc., as per the Trend specification.</p>
        </div>
      )}
       <footer className="w-full max-w-5xl mt-12 text-center text-slate-500 text-xs">
        <p>Built with React, TypeScript, and Tailwind CSS. MFI + Zone Visualization Pattern.</p>
      </footer>
    </div>
  );
};

export default App;
