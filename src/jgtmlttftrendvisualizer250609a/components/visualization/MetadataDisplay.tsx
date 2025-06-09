
import React from 'react';
import { Card, CardContent } from './shared/Card';
import type { VisualizationPropsData, TimeFrameDisplayData } from '../../types';

interface InstrumentBoxProps {
  instrument: string;
  lastClosePrice: string;
}
const InstrumentBox: React.FC<InstrumentBoxProps> = ({ instrument, lastClosePrice }) => (
  <Card className="bg-slate-800/80 text-left w-full p-1 shadow-lg backdrop-blur-sm">
    <CardContent className="p-3">
      <div className="font-bold text-lg mb-1 text-sky-300">Instrument</div>
      <div className="text-base text-slate-100">{instrument}</div>
      <div className="text-xs text-slate-400 mt-1">Last Close: {lastClosePrice}</div>
    </CardContent>
  </Card>
);

interface SourceBoxProps {
  sourceColumns: { mfi: string[], zone: string[] };
}
const SourceBox: React.FC<SourceBoxProps> = ({ sourceColumns }) => (
  <Card className="bg-slate-800/80 text-left w-full p-1 shadow-lg backdrop-blur-sm">
     <CardContent className="p-3">
      <div className="font-bold text-[11px] mb-1 text-sky-300 uppercase tracking-wider">Source Columns</div>
      <div className="text-[10px] text-slate-300">
        <p className="font-semibold">MFI:</p>
        <ul className="list-disc list-inside ml-2">
            {sourceColumns.mfi.map(col => <li key={col}>{col}</li>)}
        </ul>
        <p className="font-semibold mt-1">Zone:</p>
        <ul className="list-disc list-inside ml-2">
            {sourceColumns.zone.map(col => <li key={col}>{col}</li>)}
        </ul>
      </div>
    </CardContent>
  </Card>
);

interface SummaryBoxProps {
    title: string;
    items: {label: string, value: string}[];
    valueColorMapping?: (value: string) => string;
}

const SummaryBox: React.FC<SummaryBoxProps> = ({ title, items, valueColorMapping }) => (
    <Card className="bg-slate-800/80 text-left w-full p-1 mt-2 shadow-lg backdrop-blur-sm">
        <CardContent className="p-3">
            <div className="font-bold text-sm mb-1 text-sky-300">{title}</div>
            <ul className="list-none space-y-0.5 text-xs text-slate-300">
            {items.map(item => (
                <li key={item.label} className="flex justify-between">
                    <span>{item.label}:</span>
                    <span 
                        className={`font-semibold ${valueColorMapping ? valueColorMapping(item.value) : ''}`}
                    >
                        {item.value}
                    </span>
                </li>
            ))}
            </ul>
        </CardContent>
    </Card>
);


interface MetadataSidebarProps {
  data: VisualizationPropsData;
}
export const MetadataSidebar: React.FC<MetadataSidebarProps> = ({ data }) => {
  const mfiSummaryItems = data.timeframes.map(tf => ({ label: tf.label, value: tf.trend }));
  const zoneSummaryItems = data.timeframes.map(tf => ({ label: tf.label, value: tf.zcol.charAt(0).toUpperCase() + tf.zcol.slice(1) }));

  const trendColorClass = (trend: string) => {
    if (trend === "N/A") return "text-slate-500";
    return trend === "Bullish" ? "text-green-400" : trend === "Bearish" ? "text-red-400" : "text-yellow-400";
  };

  const zoneColorClass = (zone: string) => {
    if (zone === "N/A") return "text-slate-500";
    return zone === "Green" ? "text-green-400" : zone === "Red" ? "text-red-400" : "text-slate-400";
  };
  
  return (
    <Card className="bg-transparent border-none shadow-none text-left w-60 p-0 mr-4">
      <div className="space-y-3">
        <InstrumentBox instrument={data.instrument} lastClosePrice={data.lastClosePrice} />
        <SourceBox sourceColumns={data.sourceColumnsUsed} />
        <SummaryBox title="MFI Alignment" items={mfiSummaryItems} valueColorMapping={trendColorClass} />
        <SummaryBox title="Zone Summary" items={zoneSummaryItems} valueColorMapping={zoneColorClass} />
      </div>
    </Card>
  );
};
