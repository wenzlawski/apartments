/** @type {import("prettier").Config} */
const config = {
	useTabs: true,
	singleQuote: true,
	trailingComma: 'none',
	printWidth: 100,
	importOrder: ['^@core/(.*)$', '^@server/(.*)$', '^@ui/(.*)$', '^@(.*)$', '^[./]'],
	importOrderSeparation: true,
	importOrderSortSpecifiers: true,
	plugins: ['prettier-plugin-svelte', '@trivago/prettier-plugin-sort-imports'],
	overrides: [
		{
			files: '*.svelte',
			options: {
				parser: 'svelte'
			}
		}
	]
};

export default config;
