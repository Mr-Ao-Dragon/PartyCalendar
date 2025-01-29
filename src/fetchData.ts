import { Env } from "./index";
import axios from "axios/index";

export async function tesk(env: Env): Promise<any> {
	const data: any = null;
	const apiAddress = await env.MY_KV_NAMESPACE.get("API_ADDRESS");
	if (apiAddress === null) {
		throw new Error("数据源地址未填写");
	}
	axios
		.get(apiAddress)
		.then(function (response) {
			console.log("geted");
		})
		.catch(function (reason) {
			console.error(reason);
			return;
		})
		.finally(function () {
			return;
		});
	return 0;
}
