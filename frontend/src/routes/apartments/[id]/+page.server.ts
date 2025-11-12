import { PUBLIC_BACKEND_API_URL } from '$env/static/public';

import { type Actions, error, fail, redirect } from '@sveltejs/kit';

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

	// if (!res.ok) {
	//     throw new Error(`Failed to fetch apartment (${res.status})`);
	// }

	const apartment = await res.json();

	console.log(apartment);

	return { apartment };
};

export const actions: Actions = {
	update: async ({ request, params, fetch }) => {
		const data = Object.fromEntries(await request.formData());

		console.log(`Updating data for ${params.id}`);
		console.log(data);

		const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/${params.id}`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(data)
		});

		console.log('Update complese');

		if (!res.ok) return fail(400, { error: 'Update failed' });
		throw redirect(308, `/apartments/${params.id}`);
	},
	delete: async ({ params, fetch }) => {
		const { id } = params;

		const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/${id}`, {
			method: 'DELETE'
		});

		if (!res.ok) return fail(400, { error: 'Delete failed' });
		throw redirect(303, '/apartments');
	}
};
