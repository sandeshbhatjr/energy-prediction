import { useRef, useEffect } from 'react'
import * as d3 from 'd3'
import type { HourlyData, QuartileData } from '../schemas'

interface BarChartProps {
  data: HourlyData
  predicted: HourlyData
  bgMin?: number
  bgMax?: number
  bgMean: HourlyData
  bgQuartiles: QuartileData
  size: [number, number]
  zoomLevel: number
}

function* range(start: number, end: number, step: number) {
  for (let i = start; i <= end; i += step) {
    yield i
  }
}

export default function BarChart({
  data,
  predicted,
  bgMin = 0,
  bgMax = 100,
  bgMean,
  bgQuartiles,
  size,
  zoomLevel,
}: BarChartProps) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!svgRef.current) return

    const [width, height] = size
    const node = svgRef.current
    const dataMin = bgMin / zoomLevel
    const dataMax = bgMax / zoomLevel

    const yScale = d3
      .scaleLinear()
      .domain([dataMin, dataMax])
      .range([-10, height])

    const yMarkerValues = [
      ...range(Math.floor(dataMin / 10) * 10, Math.floor(dataMax / 10) * 10, 10),
    ]

    const svg = d3.select(node)

    // Y-axis grid lines
    const yMarkers = svg.selectAll<SVGLineElement, number>('line.y-marker').data(yMarkerValues)
    yMarkers.exit().remove()
    yMarkers
      .enter()
      .append('line')
      .attr('class', 'y-marker')
      .merge(yMarkers)
      .attr('x1', 0)
      .attr('y1', (d) => height - yScale(d))
      .attr('x2', width)
      .attr('y2', (d) => height - yScale(d))
      .attr('stroke', 'rgb(200,200,200)')
      .attr('stroke-width', '1px')
      .attr('stroke-dasharray', '2,4')

    // Actual data bars
    const dataBars = svg.selectAll<SVGRectElement, number>('rect.data').data(data)
    dataBars.exit().remove()
    dataBars
      .enter()
      .append('rect')
      .attr('class', 'data')
      .merge(dataBars)
      .style('fill', 'rgb(250,250,150)')
      .style('transition', 'all 1s')
      .attr('x', (_, i) => i * 30)
      .attr('y', (d) => (d > 0 ? height - yScale(d) : height - yScale(0)))
      .attr('height', (d) => Math.abs(yScale(d) - yScale(0)))
      .attr('width', 8)
      .attr('stroke', 'rgb(150,150,50)')
      .attr('opacity', '0.8')

    // Predicted data bars
    const predBars = svg.selectAll<SVGRectElement, number>('rect.predicted').data(predicted)
    predBars.exit().remove()
    predBars
      .enter()
      .append('rect')
      .attr('class', 'predicted')
      .merge(predBars)
      .style('fill', 'rgb(250,150,150)')
      .style('transition', 'all 1s')
      .attr('x', (_, i) => i * 30 + 10)
      .attr('y', (d) => height - yScale(d))
      .attr('height', (d) => yScale(d) - yScale(0))
      .attr('width', 8)
      .attr('stroke', 'rgb(150,50,50)')

    // Background mean circles
    const circles = svg.selectAll<SVGCircleElement, number>('circle.center').data(bgMean)
    circles.exit().remove()
    circles
      .enter()
      .append('circle')
      .attr('class', 'center')
      .merge(circles)
      .attr('cx', (_, i) => i * 30 + 4)
      .attr('cy', (d) => height - yScale(d))
      .attr('r', '3px')

    // Quartile lines
    const bgLines = svg
      .selectAll<SVGLineElement, [number, number]>('line.bg')
      .data(bgQuartiles)
    bgLines.exit().remove()
    bgLines
      .enter()
      .append('line')
      .attr('class', 'bg')
      .merge(bgLines)
      .style('transition', 'all 1s')
      .attr('x1', (_, i) => i * 30 + 4)
      .attr('y1', (d) => height - yScale(d[0]))
      .attr('x2', (_, i) => i * 30 + 4)
      .attr('y2', (d) => height - yScale(d[1]))
      .attr('stroke', 'rgb(100,100,100)')
      .attr('stroke-width', '2px')
      .attr('stroke-dasharray', '2,2')

    // Upper quartile markers
    const uppMarkers = svg
      .selectAll<SVGRectElement, [number, number]>('rect.bgUppQuartileMarker')
      .data(bgQuartiles)
    uppMarkers.exit().remove()
    uppMarkers
      .enter()
      .append('rect')
      .attr('class', 'bgUppQuartileMarker')
      .merge(uppMarkers)
      .attr('x', (_, i) => i * 30)
      .attr('y', (d) => height - yScale(d[1]))
      .attr('height', 1)
      .attr('width', 8)

    // Lower quartile markers
    const lowMarkers = svg
      .selectAll<SVGRectElement, [number, number]>('rect.bgLowQuartileMarker')
      .data(bgQuartiles)
    lowMarkers.exit().remove()
    lowMarkers
      .enter()
      .append('rect')
      .attr('class', 'bgLowQuartileMarker')
      .merge(lowMarkers)
      .attr('x', (_, i) => i * 30)
      .attr('y', (d) => height - yScale(d[0]))
      .attr('height', 1)
      .attr('width', 8)

    // X-axis
    const xAxis = svg.selectAll<SVGLineElement, number>('line.x-axis').data([1])
    xAxis
      .enter()
      .append('line')
      .attr('class', 'x-axis')
      .merge(xAxis)
      .attr('x1', 0)
      .attr('y1', height - yScale(0))
      .attr('x2', width)
      .attr('y2', height - yScale(0))
      .attr('stroke', 'rgb(100,100,100)')
      .attr('stroke-width', '1px')
      .attr('stroke-dasharray', '4,4')
  }, [data, predicted, bgMean, bgQuartiles, bgMin, bgMax, size, zoomLevel])

  return <svg ref={svgRef} width={size[0]} height={size[1]} />
}
