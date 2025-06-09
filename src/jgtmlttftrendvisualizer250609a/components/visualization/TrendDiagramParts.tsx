
import React from 'react';
import { Card, CardContent } from './shared/Card';

interface TitleTagProps {
  title: string;
}
export const UITitleTag: React.FC<TitleTagProps> = ({ title }) => (
  <div className="text-[10px] text-slate-400 mb-1 font-medium uppercase tracking-wider">
    {title}
  </div>
);

interface MFIBoxProps {
  label: string;
  mfi: string;
}
export const MFIBox: React.FC<MFIBoxProps> = ({ label, mfi }) => {
  const mfiColor =
    mfi === "++" ? "bg-green-700/30 border-green-500/50" :
    mfi === "--" ? "bg-red-700/30 border-red-500/50" : // Changed from yellow to red
    mfi === "-+" ? "bg-red-700/30 border-red-500/50" :
    mfi === "+-" ? "bg-gray-700/30 border-gray-500/50" : 
    "bg-slate-700/30 border-slate-600/50"; // For N/A or unknown

  return (
    <Card className={`${mfiColor} text-center w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base text-slate-100">{label}</div>
        <div className={`text-sm font-medium ${mfi === "N/A" ? 'text-slate-500' : 'text-slate-200'}`}>{mfi}</div>
      </CardContent>
    </Card>
  );
};

interface ZoneBoxProps {
  label: string;
  zcol: string;
}
export const ZoneBox: React.FC<ZoneBoxProps> = ({ label, zcol }) => {
  const zoneColor =
    zcol === "green" ? "bg-green-700/30 border-green-500/50" :
    zcol === "red" ? "bg-red-700/30 border-red-500/50" :
    zcol === "gray" ? "bg-gray-700/30 border-gray-500/50" :
    "bg-slate-700/30 border-slate-600/50"; // For N/A or unknown

    const zcolText = zcol.charAt(0).toUpperCase() + zcol.slice(1);


  return (
    <Card className={`${zoneColor} text-center w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base text-slate-100">{label}</div>
        <div className={`text-sm font-medium ${zcol === "N/A" ? 'text-slate-500' : 'text-slate-300'}`}>{zcolText}</div>
      </CardContent>
    </Card>
  );
};

interface TrendBoxProps {
  label: string;
  trend: "Bullish" | "Bearish" | "Neutral" | "N/A";
}
export const TrendBox: React.FC<TrendBoxProps> = ({ label, trend }) => {
  const trendColor =
    trend === "Bullish" ? "bg-green-700/30 border-green-500/50 text-green-300" :
    trend === "Bearish" ? "bg-red-700/30 border-red-500/50 text-red-300" :
    trend === "Neutral" ? "bg-yellow-700/30 border-yellow-500/50 text-yellow-300" :
    "bg-slate-700/30 border-slate-600/50 text-slate-400"; // For N/A

  return (
    <Card className={`${trendColor} text-center w-24`}>
      <CardContent className="p-2">
        <div className="font-bold text-base text-slate-100">{label}</div>
        <div className="text-sm font-medium">{trend}</div>
      </CardContent>
    </Card>
  );
};
