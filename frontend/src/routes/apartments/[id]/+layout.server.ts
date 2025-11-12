import { PUBLIC_BACKEND_API_URL } from '$env/static/public';
import { json } from 'stream/consumers';

import { type Actions, type RequestHandler, error, fail, redirect } from '@sveltejs/kit';

import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
	const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/${params.id}`);

	if (res.status === 422) {
		// 404 is standard, but you can use 422 if your API does
		throw error(404, 'Apartment not found');
	}
	if (!res.ok) {
		throw error(res.status, await res.text());
	}

	const apartment = await res.json();

	console.log(apartment);

	return { apartment };
};
