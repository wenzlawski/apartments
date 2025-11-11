import { PUBLIC_BACKEND_API_URL } from '$env/static/public';

import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
	const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/${params.id}`);

	if (!res.ok) {
		throw new Error(`Failed to fetch apartment (${res.status})`);
	}

	const apartment = await res.json();

	console.log(apartment);

	return { apartment };
};
