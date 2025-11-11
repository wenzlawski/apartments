import { PUBLIC_BACKEND_API_URL } from '$env/static/public';

export async function load() {
	const res = await fetch(`${PUBLIC_BACKEND_API_URL}/apartments/`);

	if (!res.ok) {
		throw new Error('Failed to fetch apartments');
	}

	const apartments = await res.json();

	console.log(apartments);

	return apartments; // of form {data: [...], count: n}
}
