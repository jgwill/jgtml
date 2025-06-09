
export interface TimeframeConfig {
  label: "M1" | "W1" | "D1" | "H4";
  mfiKey: string; // e.g., "mfi_str_M1"
  zcolKey: string; // e.g., "zcol_M1"
}

export const TIMEFRAMES_CONFIG: TimeframeConfig[] = [
  { label: "M1", mfiKey: "mfi_str_M1", zcolKey: "zcol_M1" },
  { label: "W1", mfiKey: "mfi_str_W1", zcolKey: "zcol_W1" },
  { label: "D1", mfiKey: "mfi_str_D1", zcolKey: "zcol_D1" },
  { label: "H4", mfiKey: "mfi_str_H4", zcolKey: "zcol_H4" },
];

export const DEFAULT_INSTRUMENT_NAME = "SPX500"; // Default instrument name
