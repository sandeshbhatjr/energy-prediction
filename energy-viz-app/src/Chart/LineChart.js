import * as d3 from 'd3';
import React, { Component } from 'react';

class LineChart extends Component {
	componentDidMount() {
		this.createLineChart();
	}

	componentDidUpdate() {
		this.createLineChart();
	}

	createLineChart() {
		const node = this.node;
		const dataMax = d3.max(this.props.data);
		const yScale = d3.scaleLinear()
			.domain([0, dataMax])
			.range([0, this.props.size[1]]);

		d3.select(node)
			.selectAll('rect')
			.data(this.props.data)
			.enter()
			.append('rect');

		d3.select(node)
			.selectAll('rect')
			.data(this.props.data)
			.exit()
			.remove();

		d3.select(node)
			.selectAll('rect')
			.data(this.props.data)
			.style('fill', 'rgb(250,250,150)')
			.attr('x', (d, i) => i*30)
			.attr('y', d => this.props.size[1] - yScale(d))
			.attr('height', d => yScale(d))
			.attr('width', 20)
			.attr('stroke', 'rgb(150,150,50)');
	}

	render() {
		return (
			<svg ref={node => this.node = node} 
				width={1000} height={400}>
			</svg>
		);
	}
}

export default LineChart;