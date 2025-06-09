
export interface TimeframeConfig {
  label: "M1" | "W1" | "D1" | "H4";
  mfiKey: string; // e.g., "mfi_str_M1" or "mfi_str" for H4
  zcolKey: string; // e.g., "zcol_M1" or "zcol" for H4
}

export const TIMEFRAMES_CONFIG: TimeframeConfig[] = [
  { label: "M1", mfiKey: "mfi_str_M1", zcolKey: "zcol_M1" },
  { label: "W1", mfiKey: "mfi_str_W1", zcolKey: "zcol_W1" },
  { label: "D1", mfiKey: "mfi_str_D1", zcolKey: "zcol_D1" },
  { label: "H4", mfiKey: "mfi_str", zcolKey: "zcol" }, // Updated for H4
];

export const DEFAULT_INSTRUMENT_NAME = "SPX500"; // Default instrument name

// MFI Signal Appearance Configuration
export interface MfiSignalAppearance {
  name: string;
  glyph: string;
}

export const MFI_SIGNAL_APPEARANCE_MAP: Readonly<Record<string, MfiSignalAppearance>> = {
  "++": { name: "Green", glyph: "🌿" },
  "--": { name: "Fade", glyph: "🍂" },
  "-+": { name: "Fake", glyph: "🎭" },
  "+-": { name: "Squat", glyph: "🌫" },
  "N/A": { name: "N/A", glyph: "❔" }
};

export const getMfiSignalAppearanceDetails = (mfiValue: string): MfiSignalAppearance => {
  const details = MFI_SIGNAL_APPEARANCE_MAP[mfiValue];
  // Fallback for any unexpected mfiValue, though "N/A" should cover most undefined cases.
  return details || { name: mfiValue, glyph: "◌" }; 
};
