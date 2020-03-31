import React from 'react';
import BarChart from './Chart';
import Toolbar from './Toolbar';

import './App.css';

function App() {
	return (
		<div className='graph'>
			<h1>Day-ahead price</h1>
			<h4>Bidding zone: DE-LU</h4>
			<BarChart data={[
				59160.0,
				56086.0,
				55006.0,
				54418.0,
				55241.0,
				58548.0,
				64522.0,
				70034.0,
				75239.0,
				78418.0,
				80608.0,
				82586.0,
				82762.0,
				81465.0,
				78922.0,
				75878.0,
				72511.0,
				71116.0,
				71651.0,
				73243.0,
				69349.0,
				67064.0,
				64870.0,
				62846.0]} size={[1000,400]} />
			<br/><br/>
			<Toolbar />
			<h3>Background statistics</h3> 
			All . Holiday: Easter . Weekends . Weekdays
		</div>
	);
}

export default App;