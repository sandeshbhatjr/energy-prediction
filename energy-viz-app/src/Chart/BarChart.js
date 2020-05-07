import * as d3 from 'd3';
import React, { Component } from 'react';

import { range } from '../utils';

class BarChart extends Component {
	componentDidMount() {
		this.createBarChart();
		console.log(this.node.width.baseVal.value);
	}

	componentDidUpdate() {
		this.createBarChart();
	}

	createBarChart = () => {
		const node = this.node;
		console.log(this.props.bgMin);
		const dataMin = this.props.bgMin/this.props.zoomLevel;
		const dataMax = this.props.bgMax/this.props.zoomLevel;
		const yScale = d3.scaleLinear()
			.domain([dataMin, dataMax])
			.range([-10, this.props.size[1]]);

		const yMarkerValues = [...range((parseInt(dataMin/10))*10, parseInt(dataMax/10)*10, 10)]
		// y-marker
		d3.select(node)
			.selectAll('line.y-marker')
			.data(yMarkerValues)
			.enter()
			.append('line')
			.attr('class', 'y-marker');

		d3.select(node)
			.selectAll('line.y-marker')
			.data(yMarkerValues)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('line.y-marker')
			.data(yMarkerValues)
			.attr('x1', 0)
			.attr('y1', (d, i) => this.props.size[1] - yScale(d))
			.attr('x2', this.props.size[0])
			.attr('y2', (d, i) => this.props.size[1] - yScale(d))
			.attr('stroke', 'rgb(200,200,200)')
			.attr('stroke-width', '1px')
			.attr('stroke-dasharray', '2,4');

		d3.select(node)
			.selectAll('rect.data')
			.data(this.props.data)
			.enter()
			.append('rect')
			.attr('class', 'data');

		d3.select(node)
			.selectAll('rect.data')
			.data(this.props.data)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('rect.data')
			.data(this.props.data)
			.style('fill', 'rgb(250,250,150)')
			.style('transition', 'all 1s')
			.attr('x', (d, i) => i*30)
			.attr('y', d => {
				if (d > 0) {
					return this.props.size[1] - yScale(d);
				}
				else {
					return this.props.size[1] - yScale(0);
				}
			})
			.attr('height', d => {
				return Math.abs(yScale(d) - yScale(0))
			})
			.attr('width', 8)
			.attr('stroke', 'rgb(150,150,50)')
			.attr('opacity', '0.8');

		d3.select(node)
			.selectAll('rect.predicted')
			.data(this.props.predicted)
			.enter()
			.append('rect')
			.attr('class', 'predicted');

		d3.select(node)
			.selectAll('rect.predicted')
			.data(this.props.predicted)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('rect.predicted')
			.data(this.props.predicted)
			.style('fill', 'rgb(250,150,150)')
			.style('transition', 'all 1s')
			.attr('x', (d, i) => i*30 + 10)
			.attr('y', d => this.props.size[1] - yScale(d))
			.attr('height', d => yScale(d) - yScale(0))
			.attr('width', 8)
			.attr('stroke', 'rgb(150,50,50)');

		// background statistics
		d3.select(node)
			.selectAll('circle.center')
			.data(this.props.bgMean)
			.enter()
			.append('circle')
			.attr('class', 'center');

		d3.select(node)
			.selectAll('circle.center')
			.data(this.props.bgMean)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('circle.center')
			.data(this.props.bgMean)
			.attr('cx', (d, i) => i*30 + 4)
			.attr('cy', d => this.props.size[1] - yScale(d))
			.attr('r', '3px');

		d3.select(node)
			.selectAll('line.bg')
			.data(this.props.bgQuartiles)
			.enter()
			.append('line')
			.attr('class', 'bg');

		d3.select(node)
			.selectAll('line.bg')
			.data(this.props.bgQuartiles)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('line.bg')
			.data(this.props.bgQuartiles)
			.style('transition', 'all 1s')
			.attr('x1', (d, i) => i*30 + 4)
			.attr('y1', d => this.props.size[1] - yScale(d[0]))
			.attr('x2', (d, i) => i*30 + 4)
			.attr('y2', d => this.props.size[1] - yScale(d[1]))
			.attr('stroke', 'rgb(100,100,100)')
			.attr('stroke-width', '2px')
			.attr('stroke-dasharray', '2,2');

		d3.select(node)
			.selectAll('rect.bgUppQuartileMarker')
			.data(this.props.bgQuartiles)
			.enter()
			.append('rect')
			.attr('class', 'bgUppQuartileMarker');

		d3.select(node)
			.selectAll('rect.bgUppQuartileMarker')
			.data(this.props.bgQuartiles)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('rect.bgUppQuartileMarker')
			.data(this.props.bgQuartiles)
			.attr('x', (d, i) => i*30)
			.attr('y', d => this.props.size[1] - yScale(d[1]))
			.attr('height', 1)
			.attr('width', 8);

		d3.select(node)
			.selectAll('rect.bgLowQuartileMarker')
			.data(this.props.bgQuartiles)
			.enter()
			.append('rect')
			.attr('class', 'bgLowQuartileMarker');

		d3.select(node)
			.selectAll('rect.bgLowQuartileMarker')
			.data(this.props.bgQuartiles)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('rect.bgLowQuartileMarker')
			.data(this.props.bgQuartiles)
			.attr('x', (d, i) => i*30)
			.attr('y', d => this.props.size[1] - yScale(d[0]))
			.attr('height', 1)
			.attr('width', 8);

		// x-axis
		d3.select(node)
			.selectAll('line.x-axis')
			.data([1])
			.enter()
			.append('line')
			.attr('class', 'x-axis');

		d3.select(node)
			.selectAll('line.x-axis')
			.data([1])
			.exit()
			.remove();

		d3.select(node)
			.selectAll('line.x-axis')
			.data([1])
			.attr('x1', 0)
			.attr('y1', (d, i) => this.props.size[1] - yScale(0))
			.attr('x2', this.props.size[0])
			.attr('y2', (d, i) => this.props.size[1] - yScale(0))
			.attr('stroke', 'rgb(100,100,100)')
			.attr('stroke-width', '1px')
			.attr('stroke-dasharray', '4,4');
	}

	render() {
		return (
			<svg ref={node => this.node = node} 
				width={this.props.size[0]} height={this.props.size[1]}>
			</svg>
		);
	}
}

export default BarChart;