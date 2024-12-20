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
	server: {
		open: true,
		proxy: {
			'/api': 'http://127.0.0.1:8000',
		},
	},
}));
