<template>
	<div>
		<button
			v-if="isAuthenticated"
			@click="handleLogout"
		>
			Logout
		</button>
	</div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
	computed: {
		...mapState(['isAuthenticated']), // Access the Vuex state to check if the user is authenticated
	},
	methods: {
		...mapActions(['logout']),
		async handleLogout() {
			try {
				await this.logout();
			} catch (error) {
				console.error('Logout failed:', error);
			}
		}, // Map Vuex logout action to this component
	},
};
</script>
