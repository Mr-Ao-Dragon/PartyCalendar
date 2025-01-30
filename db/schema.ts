/*
 * Copyright FCW
 */
import { customType, integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const datetime = customType<{ data: Date; driverData: string }>({
	dataType() {
		return "text"; // 指定数据库中的类型
	},
	toDriver(value: Date) {
		// 写入数据库时的转换
		return value.toISOString();
	},
	fromDriver(value: string): Date {
		// 从数据库读取时的转换
		return new Date(value);
	},
});
export const organization = sqliteTable("organization", {
	id: integer("id").primaryKey({ autoIncrement: true }),
	name: text("name"),
	slug: text("slug"),
	coverUrl: text("coverUrl"),
	globalUrl: text("globalUrl"),
	cnUrl: text("cnUrl"),
});
export const Party = sqliteTable("partyData", {
	id: integer("id").primaryKey({ autoIncrement: true }),
	name: text("name").notNull(),
	scale: text("scale"),
	status: text("status"),
	startDate: datetime("startDate"),
	endDate: datetime("endDate"),
	address: text("address"),
	city: text("city"),
	coverUrl: text("coverUrl"),
	org: text("organization")
		.references(() => organization.name)
		.notNull(),
	globalUrl: text("globalUrl"),
	cnUrl: text("cnUrl"),
});
