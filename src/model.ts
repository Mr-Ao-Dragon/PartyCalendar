export default interface ApiResponse {
	total: 1;
	data: Data[];
}

interface Data {
	name: string;
	scale: string;
	status: string;
	slug: string;
	startDate: string;
	endDate: string;
	address: string;
	city: string;
	coverUrl: string;
	detail: string;
	organization: organization;
	globalUrl: string;
	cnUrl: string;
}

interface organization {
	name: string;
	slug: string;
	coverUrl: string;
	globalUrl: string;
	cnUrl: string;
}
