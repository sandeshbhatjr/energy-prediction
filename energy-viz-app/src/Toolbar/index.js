import React, { Component } from 'react';
import './toolbar.css';
import dateFormat from 'dateformat';

import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

class Toolbar extends Component {
	constructor(props) {
		let today = new Date();
		super(props);
		this.state = {
			startDate: today,
			weekday: 'Loading ...'
		};
		fetch(`http://localhost:8080/daprices/${dateFormat(today, "yyyymmdd")}`)
			.then(res => res.json())
			.then(data => {
				this.setState({ weekday: data.weekday });
			});
	}

	handleChange = date => {
		this.setState({
			startDate: date,
			weekday: 'Loading ...'
		});
		fetch(`http://localhost:8080/daprices/${dateFormat(date, "yyyymmdd")}`)
			.then(res => res.json())
			.then(data => {
				this.setState({ weekday: data.weekday });
			});
	}

	render() {
		return (
			<div id="tool-bar">
				<div id='custom-date-picker' className="custom-date-picker-class">
					<DatePicker selected={this.state.startDate} onChange={this.handleChange} />
				</div>  
				<div id='day-type'>
					{ this.state.weekday }
				</div>
			</div>
		);
	}
}

export default Toolbar;