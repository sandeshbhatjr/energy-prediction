function* range(start, end, interval) {
	for (let i = start; i <= end; i+=interval) {
		yield i;
	}
}

export { range };