import { PUBLIC_BACKEND_API_URL } from '$env/static/public';
import { fail, redirect, type Actions } from '@sveltejs/kit';

export async function load() {
	const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/`);

	if (!res.ok) {
		throw new Error('Failed to fetch apartments');
	}

	const apartments = await res.json();

	console.log(apartments);

	return apartments; // of form {data: [...], count: n}
}

export const actions: Actions = {
	create: async ({ request, fetch }) => {
		const data = Object.fromEntries(await request.formData());

		const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(data)
		});

		if (!res.ok) return fail(res.status, { error: 'Create failed' });
		const a = await res.json();
		throw redirect(308, `/apartments/${a.id}`);
	}
};
