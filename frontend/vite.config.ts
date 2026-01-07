/// <reference types="vitest/config" />
import { defineConfig } from 'vitest/config';

import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { playwright } from '@vitest/browser-playwright';

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
	server: {
		watch: {
			ignored: ['**./.pnpm-store/**', '**/node_modules/**', '**/node_modules/.pnpm/**']
		}
	},
	test: {
		testTimeout: 2500,
		hookTimeout: 2500,
		expect: {
			requireAssertions: true,
			poll: {
				timeout: 500
			}
		},
		projects: [
			{
				extends: './vite.config.ts',
				test: {
					name: 'client',
					isolate: false,
					browser: {
						enabled: true,
						provider: playwright(),
						instances: [{ browser: 'chromium', headless: true }]
					},
					include: ['tests/**/*.svelte.{test,spec}.{js,ts}']
					// exclude: ['tests/lib/server/**']
				}
			},
			{
				extends: './vite.config.ts',
				test: {
					name: 'server',
					environment: 'node',
					include: ['tests/**/*.{test,spec}.{js,ts}'],
					exclude: ['tests/**/*.svelte.{test,spec}.{js,ts}']
				}
			}
		]
	}
});
