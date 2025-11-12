<script lang="ts">
	import { enhance } from '$app/forms';

	let { data, form } = $props();
	let a = data?.apartment;
</script>

<form method="POST" action="/apartments/{a?.id}?/update" use:enhance>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Address</legend>
		<input type="text" name="address" class="input" value={a?.address ?? ''} />
	</fieldset>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Description</legend>
		<textarea class="textarea" name="description">{a?.description ?? ''}</textarea>
	</fieldset>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Area m<sup>2</sup></legend>
		<input type="number" step="any" name="area_sqm" class="input" value={a?.area_sqm ?? ''} />
	</fieldset>
	<fieldset class="fieldset">
		<legend class="fieldset-legend">Rooms</legend>
		<input type="number" step="0.5" name="num_rooms" class="input" value={a.num_rooms ?? ''} />
	</fieldset>
	<button type="submit" class="btn btn-primary">Save</button>
	<a href="/apartments/{a.id}" class="btn btn-secondary">Cancel</a>
</form>
