<!-- src/routes/posts/+page.svelte -->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { Grid, html } from 'gridjs';
	import 'gridjs/dist/theme/mermaid.css';
	import { onMount } from 'svelte';

	import { css } from '@emotion/css';
	import { resolve } from '$app/paths';

	export let data;
	let grid;

	onMount(() => {
		grid = new Grid({
			columns: [
				{
					name: 'id',
					hidden: true
				},
				{
					name: 'Address',
					id: 'address'
				},
				{
					name: 'Num of rooms',
					id: 'num_rooms'
				},
				{
					name: 'Price (EUR)',
					id: 'price',
					formatter: (cell) => new Intl.NumberFormat('de-DE', {}).format(Number(cell))
				},
				{
					name: html('Area (m<sup>2</sup>)'),
					id: 'area_sqm'
				}
			],
			sort: true,
			data: data.data,
			autoWidth: true,
			resizable: true,
			className: {
				table: css`
					tr:hover td {
						background-color: rgba(0, 0, 0, 0.15);
					}
				`,
				td: css`
					cursor: pointer;
				`
			}
		});
		grid.on('rowClick', (_, row) => {
			// const itemId = args.
			if (row) {
				console.log(JSON.stringify(row.cells[0].data));
				goto(resolve(`/apartments/${row.cells[0].data}`));
			}
		});
		grid.render(document.getElementById('wrapper')!);
	});
</script>

<div class="flex mb-2 gap-x-2">
	<h1 class="text-xl">Apartments</h1>
	<a href={resolve('/apartments/new')} class="btn btn-primary">New</a>
</div>

{#if data.data && data.count > 0}
	<div id="wrapper"></div>
{:else}
	<p>No posts found.</p>
{/if}
