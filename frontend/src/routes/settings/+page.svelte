<script lang="ts">
	import { applyAction, enhance } from '$app/forms';
	import { resolve } from '$app/paths';
	import type { PageProps } from './$types';

	const { data, form }: PageProps = $props();

	let values = $derived({
		...data.data,
		...(form?.values ?? {})
	});
</script>

<h1 class="text-xl">Settings</h1>

<form
	method="POST"
	action="?/update"
	use:enhance={() => {
		return async ({ update }) => {
			update({ reset: false });
		};
	}}
>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Email</legend>
		<input
			type="email"
			name="email"
			class="input validator"
			value={values.email}
			aria-invalid={form?.errors?.email ? 'true' : 'false'}
		/>
	</fieldset>

	<fieldset class="fieldset">
		<legend class="fieldset-legend">Cron Schedule</legend>
		<input
			type="text"
			name="cron_schedule"
			class="input"
			value={values.cron_schedule}
			aria-invalid={form?.errors?.cron_schedule ? 'true' : 'false'}
		/>
		{#if form?.errors?.cron_schedule}
			<p class="text-error">{form.errors.cron_schedule}</p>
		{/if}
	</fieldset>

	{#if form?.error}
		<p class="error">{form.error}</p>
	{:else if form?.success}
		<p class="success">Settings updated.</p>
	{/if}

	<div class="flex flex-wrap mt-2 gap-x-2">
		<button type="submit" class="btn btn-primary">Save</button>
		<a href={resolve('/settings/')} class="btn btn-secondary">Cancel</a>
	</div>
</form>
