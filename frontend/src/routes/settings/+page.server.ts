import { PUBLIC_BACKEND_API_URL } from '$env/static/public';
import { fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const res = await fetch(`${PUBLIC_BACKEND_API_URL}/settings/`);

	if (!res.ok) throw new Error('Failed to fetch settings');

	const settings = await res.json();

	return {
		data: settings
	};
};

export const actions: Actions = {
	update: async ({ request, fetch }) => {
		const formData = await request.formData();
		const raw = Object.fromEntries(formData);

		// convert "" to null
		const data = Object.fromEntries(Object.entries(raw).map(([k, v]) => [k, v === '' ? null : v]));

		console.log(`Updating settings`);

		const res = await fetch(`${PUBLIC_BACKEND_API_URL}/settings/`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(data)
		});

		if (!res.ok) {
			const errors: Record<string, string> = {};
			let error = 'Update failed';

			try {
				const body = await res.json();

				// FastAPI validation error 422
				if (res.status === 422 && Array.isArray(body.detail)) {
					for (const e of body.detail) {
						const loc = e.loc ?? [];
						// e.g. ["body", "cron_schedule"] -> "cron_schedule"
						const field = loc.length > 1 ? String(loc[1]) : null;
						if (field) {
							errors[field] = e.msg;
						}
					}

					// fallback global message
					if (Object.keys(errors).length) {
						error = 'Please correct the highlighted fields.';
					}
				} else if (typeof body.detail === 'string') {
					error = body.detail;
				}
			} catch {
				// ignore JSON parse errors, keep default message
			}

			// status can be 400/422; 400 is fine for the form
			return fail(400, { error, errors, values: raw });
		}

		console.log('Update complete');

		const apiData = await res.json();

		console.log(apiData);

		return { success: true, values: apiData }; // or { success: 'Settings updated.' }
	}
};
