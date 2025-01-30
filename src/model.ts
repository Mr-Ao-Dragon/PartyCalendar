interface Organization {
	name: string;
	slug: string;
	coverUrl: string;
	globalUrl: string;
	cnUrl: string;
}

export interface PartyData {
	name: string;
	scale: string; // 如果有确定值可以用联合类型，如 "medium" | "small" | "large"
	status: string; // 同上，如 "scheduled" | "ongoing" | "ended"
	slug: string;
	startDate: string; // 或 Date 类型（需处理日期序列化）
	endDate: string; // 或 Date 类型
	address: string;
	city: string;
	coverUrl: string;
	detail: string;
	organization: Organization;
	globalUrl: string;
	cnUrl: string;
}

export default interface DataSourceModel {
	total: number;
	data: PartyData[];
}
