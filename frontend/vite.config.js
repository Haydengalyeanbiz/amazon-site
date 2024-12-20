import { defineConfig } from 'vite';
import eslintPlugin from 'vite-plugin-eslint';
import vue from '@vitejs/plugin-vue';

// https://vite.dev/config/
export default defineConfig((mode) => ({
	plugins: [
		vue(),
		eslintPlugin({
			lintOnStart: true,
			failOnError: mode === 'production',
		}),
	],
	resolve: {
		alias: {
			'@': '/src', // This assumes that your source files are in a directory named 'src' at the root of your project
		},
	},
	server: {
		open: true,
		proxy: {
			'/api': 'http://127.0.0.1:8000',
		},
	},
}));
