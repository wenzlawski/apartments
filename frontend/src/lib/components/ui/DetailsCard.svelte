<script>
	// Props (inputs) in Svelte 5 use the $props() rune
	let { label, value } = $props();
</script>

<div class="stat">
	<p class="stat-title">{@html label}</p>
	<p class="stat-value">{value}</p>
</div>
