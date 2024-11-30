export default interface ApiResponse {
	code: string;
	source: string;
	data: YearData[];
	rel: string;
}

interface YearData {
	year: number;
	data: MonthData[];
}

interface MonthData {
	month: string;
	list: EventData[];
}

interface EventData {
	title: string;
	name: string;
	image: string;
	state: number;
	groups: string[];
	address: string;
	special: number;
	time_day: number;
	time_start: string;
	time_end: string;
	path: string;
}
