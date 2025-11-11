<script>
	import dayjs from 'dayjs';

	export let data;
	const a = data?.apartment;
	const timeFormat = 'MMMM D, YYYY, HH:mm';
	const postedAt = a ? dayjs(a.posted_at).format(timeFormat) : '';
	const scrapedAt = a ? dayjs(a.scraped_at).format(timeFormat) : '';
</script>

{#if a}
	<h1 class="text-2xl">{a.address}</h1>
	<p class="mt-2">{a.description}</p>
	<p class="mt-2">Posted at: {postedAt}</p>
	<p class="mt-2">Price: {a.price}</p>
	<p class="mt-2">Rooms: {a.num_rooms}</p>
	<p class="mt-2">Area m<sup>2</sup>: {a.area_sqm}</p>
	<p class="mt-2">Construction year: {a.construction_year}</p>
	<p class="mt-2">Floor: {a.floor}</p>
	<p class="mt-2">Bathrooms: {a.num_bathrooms}</p>
	<p class="mt-2">Maintenance fee: {a.maintenance_fee}</p>
	<p class="mt-2">Commission: {a.has_commission}</p>
	<p class="mt-2">Posting id: {a.posting_id}</p>
	<p class="mt-2">Seller object id: {a.seller_object_id}</p>
	<p class="mt-2">Scraped at: {scrapedAt}</p>
	<p class="mt-2">url: <a class="text-blue-400" href={a.url}>{a.url}</a></p>
{:else}
	<p>Apartment not found.</p>
{/if}
