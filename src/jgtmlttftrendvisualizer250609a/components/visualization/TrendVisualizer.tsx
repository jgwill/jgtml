
import React from 'react';
import { Card } from './shared/Card';
import { ArrowDownIcon } from './shared/IconComponents';
import { UITitleTag, MFIBox, ZoneBox, TrendBox } from './TrendDiagramParts';
import { MetadataSidebar } from './MetadataDisplay';
import type { VisualizationPropsData, TimeFrameDisplayData } from '../../types';

interface VisualizerColumnProps {
  title: string;
  children: React.ReactNode;
}
const VisualizerColumn: React.FC<VisualizerColumnProps> = ({ title, children }) => (
  <Card className="bg-slate-800/70 backdrop-blur-sm text-center p-3 w-32 shadow-lg">
    <UITitleTag title={title} />
    <div className="flex flex-col items-center space-y-3 mt-2">
      {children}
    </div>
  </Card>
);

interface TrendVisualizerProps {
  data: VisualizationPropsData;
}

export const TrendVisualizer: React.FC<TrendVisualizerProps> = ({ data }) => {
  if (!data || data.timeframes.length === 0) {
    return <p className="text-center text-slate-400">No data available for visualization.</p>;
  }

  const { timeframes } = data;

  return (
    <div className="flex flex-col sm:flex-row justify-center p-4 sm:p-6 bg-slate-900/50 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-700/50">
      <MetadataSidebar data={data} />
      <div className="flex flex-row space-x-3 sm:space-x-4 mt-4 sm:mt-0">
        <VisualizerColumn title="MFI Zone Trend">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={`${tf.label}-trend`}>
              <TrendBox label={tf.label} trend={tf.trend} />
              {idx < timeframes.length - 1 && <ArrowDownIcon className="h-5 w-5 text-slate-500" />}
            </React.Fragment>
          ))}
        </VisualizerColumn>
        <VisualizerColumn title="MFI Signal">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={`${tf.label}-mfi`}>
              <MFIBox label={tf.label} mfi={tf.mfi} />
              {idx < timeframes.length - 1 && <ArrowDownIcon className="h-5 w-5 text-slate-500" />}
            </React.Fragment>
          ))}
        </VisualizerColumn>
        <VisualizerColumn title="Zone Color">
          {timeframes.map((tf, idx) => (
            <React.Fragment key={`${tf.label}-zone`}>
              <ZoneBox label={tf.label} zcol={tf.zcol} />
              {idx < timeframes.length - 1 && <ArrowDownIcon className="h-5 w-5 text-slate-500" />}
            </React.Fragment>
          ))}
        </VisualizerColumn>
      </div>
    </div>
  );
};
