
import React, { useCallback, useState } from 'react';
import type { RawDataRow } from '../types';

interface CSVUploaderProps {
  onDataUploaded: (data: RawDataRow[], fileName: string) => void;
  onError: (message: string) => void;
  setIsLoading: (isLoading: boolean) => void;
}

export const CSVUploader: React.FC<CSVUploaderProps> = ({ onDataUploaded, onError, setIsLoading }) => {
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    
    setFileName(file.name);
    setIsLoading(true);
    onError(""); // Clear previous errors

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        if (!text) {
          throw new Error("File content is empty.");
        }
        const lines = text.split(/\r\n|\n/).filter(line => line.trim() !== '');
        if (lines.length < 2) {
          throw new Error("CSV must have at least a header and one data row.");
        }

        const header = lines[0].split(',').map(h => h.trim());
        const data: RawDataRow[] = lines.slice(1).map(line => {
          const values = line.split(',');
          const row: RawDataRow = {};
          header.forEach((col, index) => {
            row[col] = values[index]?.trim() || '';
          });
          return row;
        });
        onDataUploaded(data, file.name);
      } catch (err) {
        console.error("CSV Parsing Error:", err);
        let message = "Failed to parse CSV file. Ensure it's a valid CSV.";
        if (err instanceof Error) {
            message = err.message;
        }
        onError(message);
        setFileName(null);
      } finally {
        setIsLoading(false);
        if (event.target) {
            event.target.value = ''; 
        }
      }
    };
    reader.onerror = () => {
        onError("Failed to read file.");
        setIsLoading(false);
        setFileName(null);
        if (event.target) {
            event.target.value = '';
        }
    }
    reader.readAsText(file);
  }, [onDataUploaded, onError, setIsLoading]);

  return (
    <div className="flex items-center space-x-2">
      <label 
        htmlFor="csv-upload" 
        className="sr-only" // Visually hidden but accessible
      >
        Upload CSV File
      </label>
      <input
        id="csv-upload"
        type="file"
        accept=".csv"
        onChange={handleFileUpload}
        className="w-auto text-xs text-slate-300 max-w-[180px] sm:max-w-[200px]
                   file:mr-2 file:py-1.5 file:px-2.5
                   file:rounded-md file:border-0
                   file:text-xs file:font-semibold
                   file:bg-sky-500 file:text-white
                   hover:file:bg-sky-600
                   focus:outline-none focus:ring-1 focus:ring-sky-500 focus:ring-offset-1 focus:ring-offset-slate-700
                   cursor-pointer"
        aria-label="Upload CSV File"
      />
      {fileName && (
        <p 
            className="text-xs text-slate-400 truncate max-w-[70px] sm:max-w-[100px]" 
            title={fileName}
        >
            {fileName}
        </p>
      )}
    </div>
  );
};
