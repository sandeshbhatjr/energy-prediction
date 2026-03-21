import type { HourlyData, QuartileData } from '../schemas'
import './Table.css'

interface TableProps {
  data: HourlyData
  predicted: HourlyData
  bgMean: HourlyData
  bgQuartiles: QuartileData
  bgMin?: number
  bgMax?: number
}

export default function Table({ data, predicted, bgMean, bgQuartiles }: TableProps) {
  return (
    <div>
      <table>
        <tbody>
          <tr>
            <td>
              <b>Hour</b>
            </td>
            {data.map((_, i) => (
              <td key={`hour-${i}`}>{i}</td>
            ))}
          </tr>
          <tr>
            <td>
              <b>Actual</b>
            </td>
            {data.map((d, i) => (
              <td key={`actual-${i}`}>{d.toFixed(2)}</td>
            ))}
          </tr>
          <tr>
            <td>
              <b>Predicted</b>
            </td>
            {predicted.map((d, i) => (
              <td key={`pred-${i}`}>{d.toFixed(2)}</td>
            ))}
          </tr>
          <tr>
            <td>
              <b>Mean</b>
            </td>
            {bgMean.map((d, i) => (
              <td key={`mean-${i}`}>{d.toFixed(2)}</td>
            ))}
          </tr>
          <tr>
            <td>
              <b>Lower quartile</b>
            </td>
            {bgQuartiles.map((q, i) => (
              <td key={`lq-${i}`}>{q[0].toFixed(2)}</td>
            ))}
          </tr>
          <tr>
            <td>
              <b>Upper quartile</b>
            </td>
            {bgQuartiles.map((q, i) => (
              <td key={`uq-${i}`}>{q[1].toFixed(2)}</td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  )
}
