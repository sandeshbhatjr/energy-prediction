import React, { Component } from 'react';
import ReactSlider from 'react-slider';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTable, faChartBar } from '@fortawesome/free-solid-svg-icons';

import Table from './Table';
import BarChart from './BarChart';
import LineChart from './LineChart';

import './index.css';

class Visualisation extends Component {
	constructor(props) {
		super(props);
		this.state = {
			selectedVisualisation: 'Bar',
			zoomLevel: 50,
		}
	}

	changeVisualisation = (newVisualization) => {
		this.setState({
			selectedVisualisation: newVisualization,
		});
	}

	updateZoomLevel = (newZoomLevel) => {
		this.setState({
			zoomLevel: newZoomLevel
		});
	}

	render() {
		const TableVisualisation = (
			<Table 
				data={this.props.data} 
				predicted={this.props.predicted} 
				bgMin={this.props.bgMin}
				bgMax={this.props.bgMax}
				bgMean={this.props.bgMean}
				bgQuartiles={this.props.bgQuartiles}
			/>
		);
		const BarVisualisation = (
			<BarChart 
				data={this.props.data} 
				predicted={this.props.predicted} 
				bgMin={this.props.bgMin}
				bgMax={this.props.bgMax}
				bgMean={this.props.bgMean}
				bgQuartiles={this.props.bgQuartiles}
				size={[750, 550]} 
				zoomLevel={(this.state.zoomLevel / 33) + 0.5}
			/>
		);
		const Loading = (
			<div className="loading-ph"> - Loading data - </div>
		);
		const Visual = (this.state.selectedVisualisation === 'Table')? TableVisualisation : BarVisualisation;
		return (
			<div id="display">
				<div id='graph-header'>
					<b>Hourly visualisation</b><br/>
					<b>Bidding zone</b>: DE-AT-LU
					(Read more about bidding zones <a href="https://github.com/sandeshbhatjr/energy-prediction/blob/master/backend/src/empredictor/bidding_zone_info.py">here</a>)
				</div>
				{ this.props.status? Visual : Loading }
				<br/><br/>
				<span id='visualisation-selector'>
					<FontAwesomeIcon 
						onClick={() => {this.changeVisualisation('Table')}} 
						className={this.state.selectedVisualisation === 'Table'? 'graph-options-selected' : 'graph-options'}
						icon={faTable} 
					/>
					<FontAwesomeIcon 
						onClick={() => {this.changeVisualisation('Bar')}} 
						className={this.state.selectedVisualisation === 'Bar'? 'graph-options-selected' : 'graph-options'}
						icon={faChartBar} 
					/>
				</span>
				<ReactSlider
					className="horizontal-slider"
					thumbClassName="thumb"
					trackClassName="track"
					renderThumb={(props, state) => <div {...props}></div>}
					value={this.state.zoomLevel}
					onChange={this.updateZoomLevel}
				/>
				<br/><br/>
			</div>
		);
	}
}

export default Visualisation;
export { BarChart, LineChart, Table };