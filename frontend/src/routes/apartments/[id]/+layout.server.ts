import { PUBLIC_BACKEND_API_URL } from '$env/static/public';

import { type LoadEvent, error } from '@sveltejs/kit';

export const load = async ({ params, fetch }: LoadEvent) => {
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
