import React, { Component } from 'react';
import { BarChart } from './Chart';
import Toolbar from './Toolbar';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTable, faChartBar, faChartLine } from '@fortawesome/free-solid-svg-icons';

import Select from 'react-select';

import './App.css';

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			graphData: new Array(24).fill(30),
			predictedGraphData: new Array(24).fill(30),
			bgMeanGraphData: new Array(24).fill(30),
			bgQuartileGraphData: new Array(24).fill(30),
		}
	}

	updateGraph = (newData) => {
		let newGraphData = Object.keys(newData).map(key => (newData[key]));
		this.setState({
			graphData: newGraphData
		});
	}

	updatebgGraph = (newData) => {
		let newBGMeanGraphData = Object.keys(newData.mean).map(key => (newData.mean[key]));
		let newBGLowQGraphData = Object.keys(newData.lq).map(key => (newData.lq[key]));
		let newBGUppQGraphData = Object.keys(newData.uq).map(key => (newData.uq[key]));
		let newBGmin = Math.min(...Object.keys(newData.min).map(key => (newData.min[key])));
		let newBGmax = Math.max(...Object.keys(newData.max).map(key => (newData.max[key])));
		let newBGQuartileGraphData = newBGLowQGraphData.map((lq, i) => {
			return [lq, newBGUppQGraphData[i]]
		})
		console.log(Object.keys(newData.min).map(key => (newData.min[key])));
		this.setState({
			predictedGraphData: newBGMeanGraphData, 
			bgMeanGraphData: newBGMeanGraphData, 
			bgQuartileGraphData: newBGQuartileGraphData, 
			bgMin: newBGmin, 
			bgMax: newBGmax, 
		});
	}

	render() {
		const options = [
			{ value: 'All', label: 'All' },
			{ value: 'Holidays', label: 'Holidays' },
			{ value: 'Holidays:Easter', label: 'Holidays: Easter' },
			{ value: 'Holidays:Christmas', label: 'Holidays: Christmas' },
			{ value: 'Weekend', label: 'Weekends' },
			{ value: 'Monday', label: 'Monday' },
			{ value: 'Tuesday', label: 'Tuesday' },
			{ value: 'Wednesday', label: 'Wednesday' },
			{ value: 'Thursday', label: 'Thursday' },
			{ value: 'Friday', label: 'Friday' },
			{ value: '2015', label: '2015' },
			{ value: '2016', label: '2016' }
		]

		return (
			<div id='App'>
				<div id='calendar-bar'>
					<b>Country: Germany</b><br/>
					<small>Set to <u>Europe/Berlin</u> timezone.</small><br/><br/>
					<Toolbar 
						updateGraph={this.updateGraph} 
						updatebgGraph={this.updatebgGraph} 
					/>
				</div>
				<div id='graph'>
					<div id="display">
						<div id='graph-header'>
							<b>Today (16 Apr 2020)</b><br/>
							<b>Bidding zone</b>: DE-AT-LU
							(Read more about bidding zones <a href="https://github.com/sandeshbhatjr/energy-prediction/blob/master/backend/src/empredictor/bidding_zone_info.py">here</a>)
						</div>
						<BarChart 
							data={this.state.graphData} 
							predicted={this.state.predictedGraphData} 
							bgMin={this.state.bgMin}
							bgMax={this.state.bgMax}
							bgMean={this.state.bgMeanGraphData}
							bgQuartiles={this.state.bgQuartileGraphData}
							size={[750,600]} 
							zoomLevel={2}
						/>
						<br/><br/>
						<FontAwesomeIcon className='graph-options' icon={faTable} />
						<FontAwesomeIcon className='graph-options-selected' icon={faChartBar} />
						<FontAwesomeIcon className='graph-options' icon={faChartLine} /><br/><br/>
					</div>
					<div id="additional-info">
						<div id="y-data">
							<div className='options-header'>
								<b>y-Data</b>. <small>Choose an item to plot:</small>
							</div>
							<b><span className="tab-selected">Day-ahead price</span></b>
							<br/><br/>
							<div className='options-header'>
								<b>Background Statistics</b>. <small>Group specific dates and plot their mean and quartiles in the backgrounds for reference.
								Choose one or more of the following criterion:</small>
							</div>
						</div>
						<Select placeholder="No background statistics" className="select-background" isMulti options={options} menuIsOpen />
					</div>
				</div>
				<div id='models'>
					<u>Model prediction summary</u><br/><br/>
					<div className='model-selected'><b>Naive</b> predictions (33.67%)</div>
					<b>AR(k=8)</b> predictions (8.67%)<br/>
					<b>VAR(k=31)</b> predictions (2.67%)<br/>
					<b>ARIMA</b> predictions (5.67%)<br/>
					<b>Simple ETS</b> predictions (2.67%)<br/>
					<b>Holtz Winter</b> predictions (1.67%)<br/>
					<b>Feedforward-NN</b> predictions (1.67%)<br/>
					<b>Simple RNN</b> predictions (1.67%)<br/>
					<b>Simple LSTM</b> predictions (1.07%)<br/><br/>
					Technical details <a href="https://github.com/sandeshbhatjr/energy-prediction">here</a>.
				</div>
			</div>
		);
	}
}

export default App;