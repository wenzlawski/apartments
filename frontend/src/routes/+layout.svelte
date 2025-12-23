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
	<NavbarItem href="/apartments">Apartments</NavbarItem>
	<NavbarItem href="/settings">Settings</NavbarItem>
</Navbar>

{@render children()}
