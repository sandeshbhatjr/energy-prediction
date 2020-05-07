import React, { Component } from 'react';
import './toolbar.css';
import dateFormat from 'dateformat';

import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

const backendUrl = process.env.NODE_ENV === 'production' ? 
	'https://energy-predictor.appspot.com/' : 
	'http://localhost:8080';

class Toolbar extends Component {
	constructor(props) {
		let today = new Date();
		super(props);
		this.state = {
			startDate: today,
		};
		fetch(`${backendUrl}/v1/daprices/${dateFormat(today, "yyyymmdd")}`)
			.then(res => res.json())
			.then(data => {
				this.props.updateGraph(data['Day Ahead Price']);
			})
			.catch(error => {
				console.log(error);
			});
		fetch(`${backendUrl}/v1/summary/daily/all`)
			.then(res => res.json())
			.then(data => {
				this.props.updatebgGraph(data);
			});
	}

	handleChange = date => {
		this.props.displayLoadScreen();
		this.setState({
			startDate: date,
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
		// TODO: Refactor this to fetch start and end dates across multiple countries
		const beginning = new Date(2015,1,1);
		const today = new Date()
		const tomorrow = new Date(today)
		tomorrow.setDate(tomorrow.getDate() + 1)
		return (
			<div id="tool-bar">
				<div id='custom-date-picker' className="custom-date-picker-class">
					<DatePicker 
						calendarIcon={null}
						minDate={beginning}
						maxDate={tomorrow}
						autoFocus
						selected={this.state.startDate} 
						onChange={this.handleChange} 
						inline 
					/>
				</div>
			</div>
		);
	}
}

export default Toolbar;