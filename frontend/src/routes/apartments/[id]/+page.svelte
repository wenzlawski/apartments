<script>
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import dayjs from 'dayjs';

	// export let data;
	let { data, form } = $props();
	let a = $derived(data?.apartment);
	// let editing = $state(true);
	const timeFormat = 'MMMM D, YYYY, HH:mm';
	const postedAt = $derived(a ? dayjs(a.posted_at).format(timeFormat) : '');
	const scrapedAt = $derived(a ? dayjs(a.scraped_at).format(timeFormat) : '');

	async function deleteApartment() {
		const res = await fetch(`/apartments/${a.id}`, { method: 'DELETE' });
		if (res.ok) {
			// Optionally redirect after delete
			goto('/apartments');
		} else {
			alert('Failed to delete');
		}
	}
</script>

{#if a}
	<h1 class="text-2xl">{a.address}</h1>
	<p class="mt-2">{a.description}</p>
	<p class="mt-2">Posted at: {postedAt}</p>
	<div class="stats">
		<div class="stat">
			<p class="stat-title">Price</p>
			<p class="stat-value">{new Intl.NumberFormat('de-DE', {}).format(Number(a.price))}€</p>
		</div>
		<div class="stat">
			<p class="stat-title">Area m<sup>2</sup></p>
			<p class="stat-value">{a.area_sqm}</p>
		</div>
	</div>
	<p class="mt-2">Rooms: {a.num_rooms}</p>
	<p class="mt-2">Construction year: {a.construction_year}</p>
	<p class="mt-2">Floor: {a.floor}</p>
	<p class="mt-2">Bathrooms: {a.num_bathrooms}</p>
	<p class="mt-2">Maintenance fee: {a.maintenance_fee}</p>
	<p class="mt-2">Commission: {a.has_commission}</p>
	<p class="mt-2">Posting id: {a.posting_id}</p>
	<p class="mt-2">Seller object id: {a.seller_object_id}</p>
	<p class="mt-2">Scraped at: {scrapedAt}</p>
	<p class="mt-2">url: <a class="text-blue-400" href={a.url}>{a.url}</a></p>
	<h1>{a.address}</h1>
	<p>{a.description}</p>
	<button class="btn btn-primary" onclick={deleteApartment}>Delete</button>
	<a class="btn btn-secondary" href="{a.id}/edit">Edit</a>
{:else}
	<p>Apartment not found.</p>
{/if}
