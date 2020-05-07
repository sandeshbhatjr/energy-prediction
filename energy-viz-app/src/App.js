import React, { Component } from 'react';
import Visualisation from './Chart';
import Toolbar from './Toolbar';

import Select from 'react-select';

import './App.css';

class App extends Component {
	constructor(props) {
		super(props);
		const tempData = new Array(24).fill(30);
		this.state = {
			graphStatus: false,
			zoomLevel: 50,
			graphData: tempData,
			predictedGraphData: tempData,
			bgMeanGraphData: tempData,
			bgQuartileGraphData: new Array(24).fill([30, 30]),
			bgOptions: { value: 'All', label: 'All' }
		}
	}

	toggleStatus = () => {
		this.setState({
			graphStatus: !this.state.graphStatus
		});
	}

	displayLoadScreen = () => {
		this.loadScreenDisplayTimerId = setTimeout(() => {
			this.toggleStatus();
			console.log('Load screen activated');
		}, 2000);
	}

	updateGraph = (newData) => {
		if (newData) {
			let newGraphData = Object.keys(newData).map(key => (newData[key]));
			if (this.loadScreenDisplayTimerId) {
				clearTimeout(this.loadScreenDisplayTimerId);
			}
			this.setState({
				graphData: newGraphData,
				graphStatus: true,
			});
		}
	}

	updatebgGraph = (newData) => {
		let newBGMeanGraphData = Object.keys(newData.mean).map(key => (newData.mean[key]));
		let newBGLowQGraphData = Object.keys(newData.lq).map(key => (newData.lq[key]));
		let newBGUppQGraphData = Object.keys(newData.uq).map(key => (newData.uq[key]));
		let newBGmin = Math.min(...Object.keys(newData.min).map(key => (newData.min[key])));
		let newBGmax = Math.max(...Object.keys(newData.max).map(key => (newData.max[key])));
		let newBGQuartileGraphData = newBGLowQGraphData.map((lq, i) => {
			return [lq, newBGUppQGraphData[i]]
		});

		if (this.loadScreenDisplayTimerId){
			clearTimeout(this.loadScreenDisplayTimerId);
		}

		this.setState({
			predictedGraphData: newBGMeanGraphData, 
			bgMeanGraphData: newBGMeanGraphData, 
			bgQuartileGraphData: newBGQuartileGraphData, 
			bgMin: newBGmin, 
			bgMax: newBGmax, 
			graphStatus: true,
		});
	}

	render() {
		const options = [
			{ value: 'All', label: 'All' },
			{ value: 'Weekend', label: 'Weekends' },
			{ value: 'Monday', label: 'Monday' },
			{ value: 'Tuesday', label: 'Tuesday' },
			{ value: 'Wednesday', label: 'Wednesday' },
			{ value: 'Thursday', label: 'Thursday' },
			{ value: 'Friday', label: 'Friday' },
		]

		return (
			<div id='App'>
				<div id='calendar-bar'>
					<b>Country: Germany</b><br/>
					<small>Set to <u>Europe/Berlin</u> timezone.</small><br/><br/>
					<Toolbar 
						updateGraph={this.updateGraph} 
						updatebgGraph={this.updatebgGraph} 
						displayLoadScreen={this.displayLoadScreen}
					/>
				</div>
				<div id='graph'>
					<Visualisation 
						data={this.state.graphData} 
						predicted={this.state.predictedGraphData} 
						bgMin={this.state.bgMin}
						bgMax={this.state.bgMax}
						bgMean={this.state.bgMeanGraphData}
						bgQuartiles={this.state.bgQuartileGraphData}
						status={this.state.graphStatus}
					/>
					<div id="additional-info">
						<div id="y-data">
							<div className='options-header'>
								<b>y-Data</b>. <small>Choose an item to plot:</small>
							</div>
							<b><span className="tab-selected">Day-ahead price</span></b>
							<br/><br/>
							<div className='options-header'>
								<b>Background Statistics</b>.&#160;
								<small>
									Group specific dates and plot their mean and 
									quartiles in the backgrounds for reference.
									Choose one or more of the following criterion:
								</small>
							</div>
						</div>
						<Select 
							placeholder="No background statistics" 
							className="select-background" 
							isMulti 
							options={options} 
							width={5}
							autoFocus={false} 
							value={this.state.bgOptions} 
						/>
					</div>
				</div>
				<div id='models'>
					<u>Model prediction summary</u><br/><br/>
					<div className='model-selected'><b>Naive</b> predictions (33.67%)</div><br/>
					<b>[WIP]</b> Refer to the notebooks for actual predictions for now.
					One will be able to look at them here soon. <br/><br/>
					Technical details <a href="https://github.com/sandeshbhatjr/energy-prediction">here</a>.
				</div>
			</div>
		);
	}
}

export default App;