<script lang="ts">
	// You can add props here if needed, e.g., for styling
	export let className = '';
</script>

<div class={`navbar bg-base-100 shadow-sm ${className}`}>
	<div class="navbar-start">
		<div class="dropdown">
			<div tabindex="0" role="button" class="btn btn-ghost md:hidden">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 6h16M4 12h8m-8 6h16"
					/>
				</svg>
			</div>
			<ul
				tabindex="-1"
				class="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow text-lg"
			>
				<slot />
			</ul>
		</div>
	</div>

	<div class="navbar-center hidden md:flex">
		<ul class="menu menu-horizontal px-1 text-lg">
			<slot />
		</ul>
	</div>
</div>
