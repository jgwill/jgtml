
export type RawDataRow = Record<string, string>;

export interface TimeFrameDisplayData {
  label: string; // e.g., "M1", "W1", "D1", "H4"
  trend: "Bullish" | "Bearish" | "Neutral" | "N/A";
  mfi: string;   // e.g., "++", "--", "-+", "+-", or "N/A"
  zcol: string;  // e.g., "green", "red", "gray", or "N/A"
}

export interface VisualizationPropsData {
  instrument: string;
  lastClosePrice: string;
  timeframes: TimeFrameDisplayData[];
  sourceColumnsUsed: { // To display in the SourceBox
    mfi: string[];
    zone: string[];
  };
}

// For MFI string to Trend mapping
export type MfiTrend = "Bullish" | "Bearish" | "Neutral";
