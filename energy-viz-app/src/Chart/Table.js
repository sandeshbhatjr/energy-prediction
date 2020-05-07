import React from 'react';

import './Table.css';

const Table = (props) => {
	const xData = props.data.map((dataPoint, i) => (
		<td>{i}</td>
	));
	const Data = props.data.map((dataPoint) => (
		<td>{dataPoint.toFixed(2)}</td>
	));
	const Predicted = props.predicted.map((dataPoint) => (
		<td>{dataPoint.toFixed(2)}</td>
	));
	const MeanData = props.bgMean.map((dataPoint) => (
		<td>{dataPoint.toFixed(2)}</td>
	));
	const bgLowerQuartilesData = props.bgQuartiles.map((quartile) => (
		<td>{quartile[0].toFixed(2)}</td>
	));
	const bgUpperQuartilesData = props.bgQuartiles.map((quartile) => (
		<td>{quartile[1].toFixed(2)}</td>
	));
	return (
		<div>
			<table>
				<tr>
					<td> <b>Hour</b> </td>
					{ xData }
				</tr>
				<tr>
					<td><b>Actual</b></td>
					{ Data }
				</tr>
				<tr>
					<td><b>Predicted</b></td>
					{ Predicted }
				</tr>
				<tr>
					<td><b>Mean</b></td>
					{ MeanData }
				</tr>
				<tr>
					<td><b>Lower quartile</b></td>
					{ bgLowerQuartilesData }
				</tr>
				<tr>
					<td><b>Upper quartile</b></td>
					{ bgUpperQuartilesData }
				</tr>
			</table>
		</div>
	);
}

export default Table;