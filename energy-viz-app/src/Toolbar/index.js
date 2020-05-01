import React, { Component } from 'react';
import './toolbar.css';
import dateFormat from 'dateformat';

import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

const backendUrl = process.env.NODE_ENV === 'production' ? 'https://energy-predictor.appspot.com/' : 'http://localhost:8080';

class Toolbar extends Component {
	constructor(props) {
		let today = new Date();
		super(props);
		this.state = {
			startDate: today,
			weekday: 'Loading ...'
		};
		fetch(`${backendUrl}/v1/daprices/${dateFormat(today, "yyyymmdd")}`)
			.then(res => res.json())
			.then(data => {
				this.setState({ 
					weekday: data.weekday
				});
				this.props.updateGraph(data['Day Ahead Price']);
			});
		fetch(`${backendUrl}/v1/summary/daily/all`)
			.then(res => res.json())
			.then(data => {
				this.props.updatebgGraph(data);
			});
	}

	handleChange = date => {
		this.setState({
			startDate: date,
			weekday: 'Loading ...'
		});
		fetch(`${backendUrl}/v1/daprices/${dateFormat(date, "yyyymmdd")}`)
			.then(res => res.json())
			.then(data => {
				this.setState({ 
					weekday: data.weekday
				});
				this.props.updateGraph(data['Day Ahead Price']);
			});
	}

	render() {
		return (
			<div id="tool-bar">
				<div id='custom-date-picker' className="custom-date-picker-class">
					<DatePicker selected={this.state.startDate} onChange={this.handleChange} inline />
				</div> 
			</div>
		);
	}
}

export default Toolbar;