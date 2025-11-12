<script lang="ts">
	import { page } from '$app/state';
</script>

<h1>{page?.error?.message ?? 'An unexpected error occurred'}</h1>
