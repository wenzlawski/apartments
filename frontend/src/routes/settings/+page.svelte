<script>
	import { enhance } from '$app/forms';

	let { data, form } = $props();
</script>

<h1 class="text-xl">Settings</h1>

<form method="POST" action="?/update" use:enhance>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Email</legend>
		<input
			type="email"
			name="email"
			class="input validator"
			value={form?.values?.email ?? data.email ?? ''}
			aria-invalid={form?.errors?.email ? 'true' : 'false'}
		/>
		{#if form?.errors?.email}
			<p class="text-error">{form.errors.email}</p>
		{/if}
	</fieldset>

	<fieldset class="fieldset">
		<legend class="fieldset-legend">Cron Schedule</legend>
		<input
			type="text"
			name="cron_schedule"
			class="input"
			value={form?.values?.cron_schedule ?? data.cron_schedule ?? ''}
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
		<a href="/settings/" class="btn btn-secondary">Cancel</a>
	</div>
</form>
