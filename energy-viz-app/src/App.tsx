import { useState } from 'react'
import Select from 'react-select'
import Visualisation from './Chart'
import Toolbar from './Toolbar'
import { useDayAheadPrices, useSummary } from './hooks'
import type { HourlyData, QuartileData } from './schemas'
import './App.css'

const BG_OPTIONS = [
  { value: 'All', label: 'All' },
  { value: 'Weekend', label: 'Weekends' },
  { value: 'Monday', label: 'Monday' },
  { value: 'Tuesday', label: 'Tuesday' },
  { value: 'Wednesday', label: 'Wednesday' },
  { value: 'Thursday', label: 'Thursday' },
  { value: 'Friday', label: 'Friday' },
] as const

const PLACEHOLDER_DATA: HourlyData = new Array(24).fill(30)
const PLACEHOLDER_QUARTILES: QuartileData = new Array(24).fill([30, 30]) as QuartileData

export default function App() {
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [bgOptions, setBgOptions] = useState<readonly { value: string; label: string }[]>([
    { value: 'All', label: 'All' },
  ])

  const priceQuery = useDayAheadPrices(selectedDate)
  const summaryQuery = useSummary()

  const graphData = priceQuery.data ?? PLACEHOLDER_DATA
  const bgMean = summaryQuery.data?.mean ?? PLACEHOLDER_DATA
  const bgQuartiles = summaryQuery.data?.quartiles ?? PLACEHOLDER_QUARTILES
  const bgMin = summaryQuery.data?.min
  const bgMax = summaryQuery.data?.max
  const isLoaded = priceQuery.isSuccess && summaryQuery.isSuccess

  return (
    <div id="App">
      <div id="calendar-bar">
        <b>Country: Germany</b>
        <br />
        <small>
          Set to <u>Europe/Berlin</u> timezone.
        </small>
        <br />
        <br />
        <Toolbar selectedDate={selectedDate} onDateChange={setSelectedDate} />
      </div>

      <div id="graph">
        <Visualisation
          data={graphData}
          predicted={bgMean}
          bgMin={bgMin}
          bgMax={bgMax}
          bgMean={bgMean}
          bgQuartiles={bgQuartiles}
          status={isLoaded}
          isError={priceQuery.isError}
          errorMessage={priceQuery.error?.message}
        />
        <div id="additional-info">
          <div id="y-data">
            <div className="options-header">
              <b>y-Data</b>. <small>Choose an item to plot:</small>
            </div>
            <b>
              <span className="tab-selected">Day-ahead price</span>
            </b>
            <br />
            <br />
            <div className="options-header">
              <b>Background Statistics</b>.&nbsp;
              <small>
                Group specific dates and plot their mean and quartiles in the
                backgrounds for reference. Choose one or more of the following
                criterion:
              </small>
            </div>
          </div>
          <Select
            placeholder="No background statistics"
            className="select-background"
            isMulti
            options={BG_OPTIONS as unknown as readonly { value: string; label: string }[]}
            value={bgOptions as { value: string; label: string }[]}
            onChange={(val) => setBgOptions(val ?? [])}
          />
        </div>
      </div>

      <div id="models">
        <u>Model prediction summary</u>
        <br />
        <br />
        <div className="model-selected">
          <b>Naive</b> predictions (33.67%)
        </div>
        <br />
        <b>[WIP]</b> Refer to the notebooks for actual predictions for now. One
        will be able to look at them here soon.
        <br />
        <br />
        Technical details{' '}
        <a href="https://github.com/sandeshbhatjr/energy-prediction">here</a>.
      </div>
    </div>
  )
}
