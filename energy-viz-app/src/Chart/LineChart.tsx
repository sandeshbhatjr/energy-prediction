import { useRef, useEffect } from 'react'
import * as d3 from 'd3'
import type { HourlyData } from '../schemas'

interface LineChartProps {
  data: HourlyData
  size: [number, number]
}

export default function LineChart({ data, size }: LineChartProps) {
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    if (!svgRef.current) return

    const [, height] = size
    const node = svgRef.current
    const dataMax = d3.max(data) ?? 0

    const yScale = d3.scaleLinear().domain([0, dataMax]).range([0, height])

    const rects = d3
      .select(node)
      .selectAll<SVGRectElement, number>('rect')
      .data(data)

    rects.exit().remove()

    rects
      .enter()
      .append('rect')
      .merge(rects)
      .style('fill', 'rgb(250,250,150)')
      .attr('x', (_, i) => i * 30)
      .attr('y', (d) => height - yScale(d))
      .attr('height', (d) => yScale(d))
      .attr('width', 20)
      .attr('stroke', 'rgb(150,150,50)')
  }, [data, size])

  return <svg ref={svgRef} width={size[0]} height={size[1]} />
}
