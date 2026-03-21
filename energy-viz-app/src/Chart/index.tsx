import { useState } from 'react'
import ReactSlider from 'react-slider'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTable, faChartBar } from '@fortawesome/free-solid-svg-icons'
import Table from './Table'
import BarChart from './BarChart'
import type { HourlyData, QuartileData } from '../schemas'
import './index.css'

type VisualisationType = 'Bar' | 'Table'

interface VisualisationProps {
  data: HourlyData
  predicted: HourlyData
  bgMin?: number
  bgMax?: number
  bgMean: HourlyData
  bgQuartiles: QuartileData
  status: boolean
  isError?: boolean
  errorMessage?: string
}

export default function Visualisation({
  data,
  predicted,
  bgMin,
  bgMax,
  bgMean,
  bgQuartiles,
  status,
  isError,
  errorMessage,
}: VisualisationProps) {
  const [selectedVis, setSelectedVis] = useState<VisualisationType>('Bar')
  const [zoomLevel, setZoomLevel] = useState(50)

  const chartProps = { data, predicted, bgMin, bgMax, bgMean, bgQuartiles }

  const content = isError ? (
    <div className="loading-ph">Error: {errorMessage ?? 'Failed to load data'}</div>
  ) : !status ? (
    <div className="loading-ph">- Loading data -</div>
  ) : selectedVis === 'Table' ? (
    <Table {...chartProps} />
  ) : (
    <BarChart {...chartProps} size={[750, 550]} zoomLevel={zoomLevel / 33 + 0.5} />
  )

  return (
    <div id="display">
      <div id="graph-header">
        <b>Hourly visualisation</b>
        <br />
        <b>Bidding zone</b>: DE-AT-LU (
        <a href="https://github.com/sandeshbhatjr/energy-prediction/blob/master/backend/src/empredictor/bidding_zone_info.py">
          Read more
        </a>
        )
      </div>

      {content}

      <br />
      <br />
      <span id="visualisation-selector">
        <FontAwesomeIcon
          onClick={() => setSelectedVis('Table')}
          className={selectedVis === 'Table' ? 'graph-options-selected' : 'graph-options'}
          icon={faTable}
        />
        <FontAwesomeIcon
          onClick={() => setSelectedVis('Bar')}
          className={selectedVis === 'Bar' ? 'graph-options-selected' : 'graph-options'}
          icon={faChartBar}
        />
      </span>
      <ReactSlider
        className="horizontal-slider"
        thumbClassName="thumb"
        trackClassName="track"
        renderThumb={(props) => <div {...props} />}
        value={zoomLevel}
        onChange={setZoomLevel}
      />
      <br />
      <br />
    </div>
  )
}
