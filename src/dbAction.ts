/*
 * Copyright FCW
 */
import { PartyData } from "./model";
import { Env } from "./index";
import * as schema from "../db/schema";
import { organization, Party } from "../db/schema";
import { drizzle } from "drizzle-orm/d1";

export const buildDbClient = (env: Env) => {
	return drizzle(env.DB, { schema });
};

export async function saveSig(data: PartyData, env: Env): Promise<boolean> {
	// code as here
	const db = buildDbClient(env);
	try {
		await db.transaction(async (tx) => {
			await tx
				.insert(organization)
				.values({
					name: data.organization.name,
					slug: data.organization.slug,
					coverUrl: data.organization.coverUrl,
					globalUrl: data.organization.globalUrl,
					cnUrl: data.organization.cnUrl,
				})
				.onConflictDoNothing()
				.returning()
				.run();
			await tx
				.insert(Party)
				.values([
					{
						name: data.name,
						scale: data.scale,
						status: data.status,
						startDate: data.startDate,
						endDate: data.endDate,
						city: data.city,
						coverUrl: data.coverUrl,
						org: data.organization.name,
						globalUrl: data.globalUrl,
						cnUrl: data.cnUrl,
					},
				])
				.run();
		});
		return true;
	} catch (error) {
		return false;
	}
}
