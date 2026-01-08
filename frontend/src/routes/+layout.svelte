<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/layout/Navbar.svelte';
	import NavbarItem from '$lib/components/ui/NavbarItem.svelte';

	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<Navbar>
	<NavbarItem href="/">Home</NavbarItem>
	<NavbarItem href="/apartments">Apartments</NavbarItem>
	<NavbarItem href="/settings">Settings</NavbarItem>
</Navbar>

<div class="max-w-4xl mx-auto px-4 mt-4">
	{@render children()}
</div>
